from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.interview import Interview
from app.schemas.interview import InterviewCreate


async def create_interview(db: AsyncSession, data: InterviewCreate) -> Interview:
    interview = Interview(**data.model_dump())
    db.add(interview)
    await db.commit()
    await db.refresh(interview)
    return interview


async def get_interview(db: AsyncSession, interview_id: int):
    result = await db.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    return result.scalar_one_or_none()


async def list_interviews(db: AsyncSession):
    result = await db.execute(select(Interview))
    return result.scalars().all()