from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.interview import InterviewCreate, InterviewResponse
from app.crud.interview import create_interview, list_interviews

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("/", response_model=InterviewResponse)
async def create(data: InterviewCreate, db: AsyncSession = Depends(get_db)):
    return await create_interview(db, data.model_dump())


@router.get("/", response_model=list[InterviewResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await list_interviews(db)