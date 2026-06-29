from pydantic import BaseModel
from typing import Optional

from app.models.session import InterviewStage, InterviewStatus


# -----------------------------
# CREATE
# -----------------------------
class SessionCreate(BaseModel):
    room_id: str
    candidate_id: int


# -----------------------------
# READ
# -----------------------------
class SessionOut(BaseModel):
    id: int
    room_id: str
    candidate_id: int
    status: InterviewStatus
    current_stage: InterviewStage
    current_question_index: int
    total_score: float

    model_config = {
        "from_attributes": True
    }


# -----------------------------
# UPDATE STAGE
# -----------------------------
class SessionStageUpdate(BaseModel):
    stage: InterviewStage