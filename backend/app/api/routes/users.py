# app/api/routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud import user as user_crud


router = APIRouter(prefix="/users", tags=["Users"])


# -------------------------
# CREATE USER
# -------------------------
@router.post("/", response_model=UserCreate)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    # ⚠️ DO NOT store raw passwords in real apps
    user = await user_crud.create_user(
        db=db,
        email=payload.email,
        hashed_password=payload.password,
    )
    
    return {
        "email": user.email,
        "password":  user.hashed_password}


# -------------------------
# GET ALL USERS
# -------------------------
@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_users(db)


# -------------------------
# GET USER BY ID
# -------------------------
@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -------------------------
# DELETE USER
# -------------------------
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_crud.delete_user(db, user)
    return {"message": "User deleted"}