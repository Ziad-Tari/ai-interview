from app.models.session import InterviewSession, InterviewStage
from app.models.answer import Answer


class PromptBuilder:
    """
    Builds structured prompts for the LLM.
    No API calls here. Only text construction.
    """

    def build_question_prompt(self, session: InterviewSession) -> str:
        return f"""
You are a professional technical interviewer.

Context:
- Stage: {session.current_stage}
- Candidate ID: {session.candidate_id}
- Question index: {session.current_question_index}

Rules:
- Ask ONE clear question
- Match difficulty to stage
- Do not explain answers
- Be concise and realistic

Generate the next interview question.
        """.strip()

    def build_followup_prompt(
        self,
        session: InterviewSession,
        last_answer: Answer,
    ) -> str:
        return f"""
You are a strict but fair technical interviewer.

Current stage: {session.current_stage}

Previous question:
{last_answer.question}

Candidate answer:
{last_answer.answer}

Task:
- Evaluate understanding
- Ask a deeper follow-up if needed
- Or move to next concept

Be realistic like a real interviewer.
        """.strip()

    def build_evaluation_prompt(self, answer: Answer) -> str:
        return f"""
You are an expert interview evaluator.

Question:
{answer.question}

Candidate Answer:
{answer.answer}

Return STRICT JSON:
{{
  "clarity": 1-5,
  "correctness": 1-5,
  "depth": 1-5,
  "reasoning": 1-5,
  "feedback": "short feedback"
}}
        """.strip()