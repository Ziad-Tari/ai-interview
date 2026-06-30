# app/crud/user.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


async def create_user(db: AsyncSession, email: str, hashed_password: str):
    user = User(email=email, hashed_password=hashed_password)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def delete_user(db: AsyncSession, user):
    await db.delete(user)
    await db.commit()