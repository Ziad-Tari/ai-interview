from fastapi import FastAPI
from app.api.routes import interview, sessions, users
from app.core.db import Base, engine
from app.models import User

app = FastAPI(title="AI Interviewer")

app.include_router(interview.router, prefix="/interviews", tags=["interviews"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
app.include_router(users.router)

Base.metadata.create_all(bind=engine)
    