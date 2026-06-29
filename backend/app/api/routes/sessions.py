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

router = APIRouter(prefix="/sessions", tags=["Sessions"])


# -----------------------------
# START SESSION
# -----------------------------
@router.post("/start")
async def start_session(
    room_id: str,
    candidate_id: int,
    db: AsyncSession = DbSession,
):
    session = await create_session(
        db=db,
        room_id=room_id,
        candidate_id=candidate_id,
    )

    return session


# -----------------------------
# GET SESSION
# -----------------------------
@router.get("/{session_id}")
async def read_session(
    session_id: int,
    db: AsyncSession = DbSession,
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
    db: AsyncSession = DbSession,
):
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
    db: AsyncSession = DbSession,
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
    db: AsyncSession = DbSession,
):
    session = await get_session(db, session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return await finish_session(db, session)