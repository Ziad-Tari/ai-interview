import json

from openai import OpenAI

from app.core.config import settings
from app.services.prompt_builder import PromptBuilder
from app.models.answer import Answer


class Evaluator:
    """
    Evaluates candidate answers using LLM.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_builder = PromptBuilder()

    def evaluate(self, answer: Answer) -> dict:
        prompt = self.prompt_builder.build_evaluation_prompt(answer)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt}
            ],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)