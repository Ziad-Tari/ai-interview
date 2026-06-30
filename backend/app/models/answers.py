from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.db import Base


class Answer(Base):
    """
    Represents a single interview turn:

    - question asked by AI
    - candidate answer
    - AI evaluation (score + feedback)

    This is the atomic unit of an interview session.
    """

    __tablename__ = "answers"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id = Column(Integer, primary_key=True, index=True)

    # -----------------------------
    # Relationships
    # -----------------------------
    session_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False,
        index=True,
    )

    # -----------------------------
    # Question Data
    # -----------------------------
    question = Column(
        Text,
        nullable=False,
    )

    question_stage = Column(
        String,
        nullable=True,  # warmup / technical / etc.
    )

    question_difficulty = Column(
        String,
        nullable=True,  # easy / medium / hard
    )

    # Optional skill tagging (e.g., "system design", "python", etc.)
    skill_tag = Column(
        String,
        nullable=True,
    )

    # -----------------------------
    # Candidate Response
    # -----------------------------
    answer = Column(
        Text,
        nullable=True,
    )

    # -----------------------------
    # AI Evaluation
    # -----------------------------
    clarity_score = Column(Float, nullable=True)
    correctness_score = Column(Float, nullable=True)
    depth_score = Column(Float, nullable=True)
    reasoning_score = Column(Float, nullable=True)

    total_score = Column(Float, nullable=True)

    feedback = Column(Text, nullable=True)

    # -----------------------------
    # Metadata
    # -----------------------------
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    answered_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    evaluated_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # -----------------------------
    # ORM Relationships
    # -----------------------------
    session = relationship(
        "InterviewSession",
        back_populates="answers",
    )



async def get_last_answer(db: AsyncSession, session_id: int) -> Answer | None:
    result = await db.execute(
        select(Answer)
        .where(Answer.session_id == session_id)
        .order_by(Answer.id.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()