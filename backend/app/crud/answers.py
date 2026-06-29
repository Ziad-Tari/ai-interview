from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from datetime import datetime, timezone

from app.models.answer import Answer


# -----------------------------
# CREATE ANSWER
# -----------------------------
async def create_answer(
    db: AsyncSession,
    session_id: int,
    question: str,
    question_stage: str | None = None,
    question_difficulty: str | None = None,
    skill_tag: str | None = None,
) -> Answer:
    answer = Answer(
        session_id=session_id,
        question=question,
        question_stage=question_stage,
        question_difficulty=question_difficulty,
        skill_tag=skill_tag,
        created_at=datetime.now(timezone.utc),
    )

    db.add(answer)
    await db.commit()
    await db.refresh(answer)
    return answer


# -----------------------------
# GET ANSWERS BY SESSION
# -----------------------------
async def get_answers_by_session(
    db: AsyncSession,
    session_id: int,
) -> list[Answer]:
    result = await db.execute(
        select(Answer).where(Answer.session_id == session_id)
    )
    return result.scalars().all()


# -----------------------------
# UPDATE ANSWER (user reply)
# -----------------------------
async def submit_answer(
    db: AsyncSession,
    answer: Answer,
    answer_text: str,
) -> Answer:
    answer.answer = answer_text
    answer.answered_at = datetime.now(timezone.utc)

    db.add(answer)
    await db.commit()
    await db.refresh(answer)
    return answer


# -----------------------------
# UPDATE EVALUATION
# -----------------------------
async def evaluate_answer(
    db: AsyncSession,
    answer: Answer,
    clarity: float,
    correctness: float,
    depth: float,
    reasoning: float,
    feedback: str,
) -> Answer:
    answer.clarity_score = clarity
    answer.correctness_score = correctness
    answer.depth_score = depth
    answer.reasoning_score = reasoning

    answer.total_score = (clarity + correctness + depth + reasoning) / 4
    answer.feedback = feedback
    answer.evaluated_at = datetime.now(timezone.utc)

    db.add(answer)
    await db.commit()
    await db.refresh(answer)
    return answer