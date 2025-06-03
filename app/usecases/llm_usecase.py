import logging
import os
from typing import List

import instructor
from anthropic import AnthropicBedrock
from instructor.utils import disable_pydantic_error_url
from pydantic import BaseModel
from structlog import get_logger

from app.models.wellness_profile import WellnessProfileResponse


class LLMUsecase:
    def __init__(self):
        self.aws_region = os.environ.get('BEDROCK_REGION')
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
        self, user_response: str, question: str, response_history: List[str]
    ) -> WellnessProfileResponse:
        prompt = f"""
        ROLE: Wellness profile data extractor and conversation analyzer

        INPUT DATA:
        - Current user response: "{user_response}"
        - Current question asked: "{question}"
        - Complete conversation history: {response_history}

        TASK 1 - COMPREHENSIVE DATA EXTRACTION:
        Analyze the ENTIRE conversation history (including current response) to extract information for:
        • age (integer) • gender (male/female/other) • activityLevel (sedentary/moderate/active)
        • dietaryPreference (vegetarian/vegan/keto/paleo/omnivore/no_preference)
        • sleepQuality (good/average/poor) • stressLevel (low/medium/high) • healthGoals (free text)

        Extract information from ANY point in the conversation, not just the current response.
        Set unmentioned/unclear fields to null.

        TASK 2 - HISTORICAL COMPLETENESS EVALUATION:
        Review the complete conversation history and assess:
        1. Which wellness profile fields have been adequately covered across ALL previous exchanges
        2. Which fields still need clarification or have never been addressed
        3. Whether the user has provided sufficient detail for a complete wellness profile

        TASK 3 - INTELLIGENT FOLLOW-UP DECISION:
        Based on the complete conversation analysis:
        1. Score each field: HIGH (clearly established), MEDIUM (partially covered), LOW (missing/unclear)
        2. Consider conversation flow and user engagement level
        3. If critical fields are still missing OR user responses suggest more context is needed:
           → Generate ONE thoughtful follow-up question that addresses the most important gaps
        4. If the wellness profile is sufficiently complete based on conversation history:
           → Set follow-up question to null

        FOLLOW-UP QUESTION GUIDELINES:
        - Prioritize missing high-impact fields (age, health goals, activity level)
        - Reference previous conversation context when appropriate
        - Ask in a natural, conversational way
        - Combine multiple missing fields into one coherent question when possible

        OUTPUT: Complete extracted profile + confidence scores + strategic follow-up question (if needed)
        """
        return self.__generate_questions_from_llm(
            prompt=prompt, response_model=WellnessProfileResponse, powerful_model=True
        )
