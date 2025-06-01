import logging
import os

import instructor
from pydantic import BaseModel
from anthropic import AnthropicBedrock
from instructor.utils import disable_pydantic_error_url


class LLMUsecase:
    def __init__(self):
        self.aws_region = os.environ.get('AWS_DEFAULT_REGION')
        self.is_local = os.getenv('IS_LOCAL')  # set to True if testing locally
        self.logging_level = logging.DEBUG if self.is_local else logging.INFO
        self.model_id = os.getenv('ANTHROPIC_MODEL_ID')
        self.max_tokens = os.getenv('MAX_TOKENS') or 4096

        logging.basicConfig(level=self.logging_level)

    async def generate_questions_from_llm(
        self,
        prompt: str,
        response_model: BaseModel
    ):
        """
        Generate response from the LLM.

        :param str prompt: The prompt for the response generator.
        :param BaseModel response_model: The response model to validate the output.
        :return BaseModel: The validated output from the LLM.
        """
        disable_pydantic_error_url()  # instructor not include error url in response to save on tokens

        model = AnthropicBedrock(aws_region=self.aws_region)
        client = instructor.from_anthropic(model, mode=instructor.Mode.ANTHROPIC_TOOLS)
        resp, _ = await client.chat.completions.create_with_completion(
            model=self.model_id,
            max_tokens=self.max_tokens,
            messages=[
                {'role': 'user', 'content': prompt},
            ],
            response_model=response_model,
            max_retries=2,
        )
        return resp
