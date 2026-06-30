from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.session import get_session, update_session
from app.crud.answer import (
    create_answer,
    submit_answer,
    evaluate_answer,
)
from app.services.ai_engine import AIEngine
from app.services.evaluator import Evaluator
from app.services.interview_flow import InterviewFlow
from app.models.session import InterviewStage
from app.api.deps import DbSession

class InterviewOrchestrator:
    """
    Central brain of the AI Interview System.

    This is the ONLY place where:
    - AI is called
    - session state changes
    - evaluation is triggered
    - next question is decided
    """

    def __init__(self):
        self.ai = AIEngine()
        self.evaluator = Evaluator()
        self.flow = InterviewFlow()

    # =========================================================
    # MAIN ENTRY POINT
    # =========================================================
    async def handle_next(self, db= DbSession, session_id: int, user_answer: str | None = None):
        """
        This function drives the entire interview lifecycle.
        """

        # 1. Load session
        session = await get_session(db, session_id)
        if not session:
            raise Exception("Session not found")

        # =====================================================
        # CASE 1: FIRST QUESTION (no answer yet)
        # =====================================================
        if user_answer is None:
            question = self.ai.generate_question(session)

            answer_record = await create_answer(
                db=db,
                session_id=session.id,
                question=question,
                question_stage=session.current_stage,
            )

            return {
                "type": "question",
                "question": question,
                "answer_id": answer_record.id,
                "stage": session.current_stage,
            }

        # =====================================================
        # CASE 2: USER ANSWERED → EVALUATE
        # =====================================================
        # 2. Get last answer record
        answers = await create_answer(
            db=db,
            session_id=session.id,
            question="",
        )

        # NOTE: (simplified - you may replace with proper fetch later)

        # 3. Save answer text
        await submit_answer(
            db=db,
            answer=answers,
            answer_text=user_answer,
        )

        # 4. Evaluate answer (AI)
        evaluation = self.evaluator.evaluate(answers)

        # 5. Save evaluation
        await evaluate_answer(
            db=db,
            answer=answers,
            clarity=evaluation["clarity"],
            correctness=evaluation["correctness"],
            depth=evaluation["depth"],
            reasoning=evaluation["reasoning"],
            feedback=evaluation["feedback"],
        )

        score = (
            evaluation["clarity"]
            + evaluation["correctness"]
            + evaluation["depth"]
            + evaluation["reasoning"]
        ) / 4

        # =====================================================
        # 6. DECIDE NEXT STEP
        # =====================================================
        if self.flow.should_advance_stage(session, score):
            next_stage = self.flow.next_stage(session)
            session.current_stage = next_stage

        session.total_score += score
        session.current_question_index += 1

        await update_session(db, session)

        # =====================================================
        # 7. GENERATE NEXT QUESTION
        # =====================================================
        if session.current_stage == InterviewStage.SUMMARY:
            return {
                "type": "end",
                "final_score": session.total_score,
                "message": "Interview completed",
            }

        next_question = self.ai.generate_question(session)

        next_answer = await create_answer(
            db=db,
            session_id=session.id,
            question=next_question,
            question_stage=session.current_stage,
        )

        return {
            "type": "question",
            "question": next_question,
            "answer_id": next_answer.id,
            "stage": session.current_stage,
        }