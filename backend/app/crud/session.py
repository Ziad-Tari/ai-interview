from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.session import InterviewSession, InterviewStatus, InterviewStage
from app.api.deps import DbSession

# -----------------------------
# CREATE SESSION
# -----------------------------
async def create_session(
    room_id: str,
    candidate_id: int,
    interview_id: int,
    db: AsyncSession,
) -> InterviewSession:
    session = InterviewSession(
        room_id=room_id,
        candidate_id=candidate_id,
        status=InterviewStatus.CREATED,
        current_stage=InterviewStage.WARMUP,
        current_question_index=0,
        total_score=0.0,
        interview_id = interview_id
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


# -----------------------------
# GET SESSION BY ID
# -----------------------------
async def get_session(
    session_id: int,
    db: AsyncSession,
) -> InterviewSession | None:
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == session_id)
    )
    return result.scalar_one_or_none()


# -----------------------------
# GET SESSION BY ROOM
# -----------------------------
async def get_session_by_room(
    room_id: str,
    db: AsyncSession,
) -> InterviewSession | None:
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.room_id == room_id)
    )
    return result.scalar_one_or_none()


# -----------------------------
# UPDATE SESSION
# -----------------------------
async def update_session(session: InterviewSession, db: AsyncSession,) -> InterviewSession:
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


# -----------------------------
# UPDATE STAGE
# -----------------------------
async def update_stage(
    session: InterviewSession,
    stage: InterviewStage,
    db: AsyncSession,
) -> InterviewSession:
    session.current_stage = stage
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


# -----------------------------
# FINISH SESSION
# -----------------------------
async def finish_session(
    session: InterviewSession,
    db: AsyncSession,
) -> InterviewSession:
    session.status = InterviewStatus.COMPLETED
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session