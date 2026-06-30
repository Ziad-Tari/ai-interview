from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DbSession
from app.crud.answer import (
    create_answer,
    submit_answer,
    get_answers_by_session,
    evaluate_answer,
)
from app.crud.session import get_session
from app.models.answer import Answer
from app.api.deps import get_db

router = APIRouter(prefix="/answers", tags=["Answers"])


# -----------------------------
# CREATE QUESTION ENTRY
# -----------------------------
@router.post("/create")
async def create_question(
    session_id: int,
    question: str,
    question_stage: str | None = None,
    question_difficulty: str | None = None,
    skill_tag: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    session = await get_session(db, session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    answer = await create_answer(
        db=db,
        session_id=session_id,
        question=question,
        question_stage=question_stage,
        question_difficulty=question_difficulty,
        skill_tag=skill_tag,
    )

    return answer


# -----------------------------
# SUBMIT ANSWER
# -----------------------------
@router.patch("/{answer_id}/submit")
async def submit(
    answer_id: int,
    answer_text: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.get(Answer, answer_id)

    if not result:
        raise HTTPException(status_code=404, detail="Answer not found")

    return await submit_answer(db, result, answer_text)


# -----------------------------
# EVALUATE ANSWER (AI will plug here later)
# -----------------------------
@router.post("/{answer_id}/evaluate")
async def evaluate(
    answer_id: int,
    clarity: float,
    correctness: float,
    depth: float,
    reasoning: float,
    feedback: str,
    db :AsyncSession = Depends(get_db),
):
    answer = await db.get(Answer, answer_id)

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    return await evaluate_answer(
        db=db,
        answer=answer,
        clarity=clarity,
        correctness=correctness,
        depth=depth,
        reasoning=reasoning,
        feedback=feedback,
    )


# -----------------------------
# GET ALL ANSWERS FOR SESSION
# -----------------------------
@router.get("/session/{session_id}")
async def get_session_answers(
    session_id: int,
    db :AsyncSession = Depends(get_db),
):
    return await get_answers_by_session(db, session_id)