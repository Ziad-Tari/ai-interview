from openai import OpenAI

from app.core.config import settings
from app.services.prompt_builder import PromptBuilder
from app.models.session import InterviewSession
from app.models.answer import Answer


class AIEngine:
    """
    Handles all LLM interactions.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_builder = PromptBuilder()

    # -----------------------------
    # GENERATE QUESTION
    # -----------------------------
    def generate_question(self, session: InterviewSession) -> str:
        prompt = self.prompt_builder.build_question_prompt(session)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt}
            ],
        )

        return response.choices[0].message.content

    # -----------------------------
    # FOLLOW-UP QUESTION
    # -----------------------------
    def generate_followup(self, session: InterviewSession, last_answer: Answer) -> str:
        prompt = self.prompt_builder.build_followup_prompt(session, last_answer)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt}
            ],
        )

        return response.choices[0].message.content