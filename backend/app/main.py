from fastapi import FastAPI
from app.api.routes import interview, sessions, users
from app.core.db import Base, engine
from app.models import User
from sqlalchemy.ext.asyncio import AsyncEngine

app = FastAPI(title="AI Interviewer")

app.include_router(interview.router, prefix="/interviews", tags=["interviews"])
app.include_router(sessions.router)
app.include_router(users.router)



async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await init_models()

