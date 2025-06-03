import logging
import os

import instructor
from anthropic import AnthropicBedrock
from instructor.utils import disable_pydantic_error_url
from pydantic import BaseModel
from structlog import get_logger

from app.models.wellness_profile import WellnessProfileResponse


class LLMUsecase:
    def __init__(self):
        self.aws_region = os.environ.get('AWS_DEFAULT_REGION')
        self.sonnet_model_id = os.getenv('SONNET_MODEL_ID')
        self.haiku_model_id = os.getenv('HAIKU_MODEL_ID')
        self.max_tokens = os.getenv('MAX_TOKENS') or 4096

        self.is_local = os.getenv('IS_LOCAL')  # set to True if testing locally
        self.logging_level = logging.DEBUG if self.is_local else logging.INFO
        logging.basicConfig(level=self.logging_level)
        self.logger = get_logger()

    def __generate_questions_from_llm(
        self, prompt: str, response_model: BaseModel, powerful_model: bool
    ):
        """
        Generate response from the LLM.

        :param str prompt: The prompt for the response generator.
        :param BaseModel response_model: The response model to validate the output.
        :return BaseModel: The validated output from the LLM.
        """
        disable_pydantic_error_url()  # instructor not include error url in response to save on tokens

        model_id = self.sonnet_model_id if powerful_model else self.haiku_model_id

        self.logger.info(
            f'Generating questions from LLM with prompt: {prompt}',
            model=model_id,
            max_tokens=self.max_tokens,
        )

        model = AnthropicBedrock(aws_region=self.aws_region)
        client = instructor.from_anthropic(model, mode=instructor.Mode.ANTHROPIC_TOOLS)
        resp, _ = client.chat.completions.create_with_completion(
            model=model_id,
            max_tokens=self.max_tokens,
            messages=[
                {'role': 'user', 'content': prompt},
            ],
            response_model=response_model,
            max_retries=2,
        )
        return resp

    def get_output_model_from_user_response(
        self, user_response: str, question: str
    ) -> WellnessProfileResponse:
        prompt = f"""
        You are a wellness assistant. Extract wellness profile fields ONLY from information explicitly mentioned in the user's reply. Do NOT infer or guess missing information.

        Guidelines for extraction:
        - age: integer (only if explicitly stated)
        - gender: male, female, or other (only if explicitly stated)
        - activityLevel: sedentary, moderate, or active (only if explicitly stated)
        - dietaryPreference: vegetarian, vegan, keto, paleo, omnivore, or no_preference (only if explicitly stated)
        - sleepQuality: good, average, or poor (only if explicitly stated)
        - stressLevel: low, medium, or high (only if explicitly stated)
        - healthGoals: brief free text (only if explicitly stated)

        IMPORTANT: Set fields to null/None if they are NOT explicitly mentioned in the user's response.
        
        CONFIDENCE SCORING AND FOLLOW-UP QUESTIONS:
        1. For every field that IS extracted, assign a confidence score (high, medium, low):
           - HIGH: Information is explicitly and clearly stated
           - MEDIUM: Information is mentioned but somewhat ambiguous or unclear
           - LOW: Information is vague, implied, or uncertain
        
        2. MANDATORY: If ANY extracted field has medium or low confidence, you MUST generate a follow-up question that addresses ALL such fields. The follow-up question should:
           - Specifically ask for clarification on EVERY field with medium/low confidence
           - Be concise but comprehensive
           - Use natural language to ask about multiple fields in a single, coherent question
           - Prioritize the most important unclear information first
        
        3. Example follow-up question format when multiple fields need clarification:
           "I'd like to clarify a few details: [specific question about field 1], and [specific question about field 2]. Also, [question about field 3]?"
        
        User response: "{user_response}"
        Current question: "{question}"

        Remember: Extract only explicitly mentioned fields, set others to null, and ensure ALL medium/low confidence fields are addressed in your follow-up question.
        """
        return self.__generate_questions_from_llm(
            prompt=prompt, response_model=WellnessProfileResponse, powerful_model=True
        )
