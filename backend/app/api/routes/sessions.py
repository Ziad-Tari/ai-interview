from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DbSession
from app.crud.session import (
    create_session,
    get_session,
    get_session_by_room,
    finish_session,
    update_stage,
)
from app.models.session import InterviewStage
from app.api.deps import get_db
from app.services.interview_orchestrator import InterviewOrchestrator


router = APIRouter(prefix="/sessions", tags=["Sessions"])


# -----------------------------
# START SESSION
# -----------------------------
@router.post("/start")
async def start_session(
    room_id: str,
    candidate_id: int,
    interview_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    session = await create_session(
        room_id=room_id,
        candidate_id=candidate_id,
        interview_id = interview_id,
         db=db,
    )

    return session


# -----------------------------
# GET SESSION
# -----------------------------
@router.get("/{session_id}")
async def read_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
):
    session = await get_session(db, session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


# -----------------------------
# GET BY ROOM
# -----------------------------
@router.get("/room/{room_id}")
async def read_session_by_room(
    room_id: str,
    db: AsyncSession = Depends(get_db)):
    session = await get_session_by_room(db, room_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


# -----------------------------
# ADVANCE STAGE
# -----------------------------
@router.patch("/{session_id}/stage")
async def change_stage(
    session_id: int,
    stage: InterviewStage,
    db: AsyncSession = Depends(get_db)
    ):
    session = await get_session(db, session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    updated = await update_stage(db, session, stage)
    return updated


# -----------------------------
# FINISH SESSION
# -----------------------------
@router.post("/{session_id}/finish")
async def finish(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    session = await get_session(db, session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return await finish_session(db, session)

@router.post("/{session_id}/next")
async def next_step(session_id: int, user_answer: str | None = None, db: AsyncSession = Depends(get_db)):
    orchestrator = InterviewOrchestrator()
    return await orchestrator.handle_next(db, session_id, user_answer)