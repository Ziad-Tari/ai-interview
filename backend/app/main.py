from fastapi import FastAPI
from app.api.routes import interview, sessions

app = FastAPI(title="AI Interviewer")

app.include_router(interview.router, prefix="/interviews", tags=["interviews"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])