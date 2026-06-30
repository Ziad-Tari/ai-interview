from pydantic import BaseModel
from typing import Optional


class InterviewCreate(BaseModel):
    title: str
    role: str
    description: Optional[str] = None
    difficulty: str = "intermediate"
    total_questions: int = 10
    time_limit_minutes: Optional[int] = None
    passing_score: float = 70.0


class InterviewResponse(BaseModel):
    id: int
    title: str
    role: str
    description: Optional[str]
    difficulty: str
    total_questions: int
    time_limit_minutes: Optional[int]
    passing_score: float

    class Config:
        from_attributes = True