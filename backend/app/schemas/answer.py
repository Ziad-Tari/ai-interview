from pydantic import BaseModel
from typing import Optional


# -----------------------------
# CREATE QUESTION
# -----------------------------
class AnswerCreate(BaseModel):
    session_id: int
    question: str
    question_stage: Optional[str] = None
    question_difficulty: Optional[str] = None
    skill_tag: Optional[str] = None


# -----------------------------
# SUBMIT ANSWER
# -----------------------------
class AnswerSubmit(BaseModel):
    answer_text: str


# -----------------------------
# EVALUATION OUTPUT
# -----------------------------
class AnswerEvaluation(BaseModel):
    clarity: float
    correctness: float
    depth: float
    reasoning: float
    feedback: str


# -----------------------------
# READ
# -----------------------------
class AnswerOut(BaseModel):
    id: int
    session_id: int
    question: str
    answer: Optional[str]

    clarity_score: Optional[float]
    correctness_score: Optional[float]
    depth_score: Optional[float]
    reasoning_score: Optional[float]

    total_score: Optional[float]
    feedback: Optional[str]

    model_config = {
        "from_attributes": True
    }