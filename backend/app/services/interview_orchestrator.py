from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.session import get_session, update_session
from app.crud.answers import (
    create_answer,
    submit_answer,
    evaluate_answer,
    get_last_answer,
)

from app.services.ai_engine import AIEngine
from app.services.evaluator import Evaluator
from app.services.interview_flow import InterviewFlow

from app.models.session import InterviewStage


class InterviewOrchestrator:
    """
    Central brain of the AI Interview System.
    """

    def __init__(self):
        self.ai = AIEngine()
        self.evaluator = Evaluator()
        self.flow = InterviewFlow()

    async def handle_next(
        self,
        db: AsyncSession,
        session_id: int,
        user_answer: str | None = None,
    ):
        # -----------------------------
        # 1. LOAD SESSION
        # -----------------------------
        session = await get_session(session_id ,db)
        if not session:
            raise Exception("Session not found")

        # =====================================================
        # CASE 1: FIRST QUESTION
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
        # CASE 2: USER ANSWERED PREVIOUS QUESTION
        # =====================================================

        # 2. GET LAST ACTIVE QUESTION
        answer = await get_last_answer(db, session.id)

        if not answer:
            raise Exception("No active question found for session")

        # 3. SAVE USER ANSWER
        await submit_answer(
            db=db,
            answer=answer,
            answer_text=user_answer,
        )

        # 4. AI EVALUATION
        evaluation = self.evaluator.evaluate(answer)

        # 5. SAVE EVALUATION
        await evaluate_answer(
            db=db,
            answer=answer,
            clarity=evaluation["clarity"],
            correctness=evaluation["correctness"],
            depth=evaluation["depth"],
            reasoning=evaluation["reasoning"],
            feedback=evaluation["feedback"],
        )

        # 6. SCORE CALCULATION
        score = (
            evaluation["clarity"]
            + evaluation["correctness"]
            + evaluation["depth"]
            + evaluation["reasoning"]
        ) / 4

        # =====================================================
        # 7. UPDATE SESSION STATE
        # =====================================================

        if self.flow.should_advance_stage(session, score):
            session.current_stage = self.flow.next_stage(session)

        session.total_score += score
        session.current_question_index += 1

        await update_session(db, session)

        # =====================================================
        # 8. END CONDITION
        # =====================================================

        if session.current_stage == InterviewStage.SUMMARY:
            return {
                "type": "end",
                "final_score": session.total_score,
                "message": "Interview completed",
            }

        # =====================================================
        # 9. GENERATE NEXT QUESTION
        # =====================================================

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