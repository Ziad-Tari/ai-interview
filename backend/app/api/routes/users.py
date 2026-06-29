from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import DbSession
from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
async def create_user(
    user: UserCreate,
    db: DbSession
):
    return {"message": "user endpoint ready"}