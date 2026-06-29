from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship

from app.core.db import Base


class InterviewStatus(str, Enum):
    """
    Overall status of an interview session.
    """

    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InterviewStage(str, Enum):
    """
    Current phase of the interview.
    """

    WARMUP = "warmup"
    TECHNICAL = "technical"
    DEEP_DIVE = "deep_dive"
    BEHAVIORAL = "behavioral"
    SUMMARY = "summary"


class InterviewSession(Base):
    """
    Represents one complete interview session.

    This model stores ONLY the interview state.
    Questions, answers, and AI evaluations are stored
    in separate tables.
    """

    __tablename__ = "interview_sessions"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # -----------------------------
    # Relationships
    # -----------------------------
    room_id = Column(
        ForeignKey("interview_rooms.room_id"),
        nullable=False,
        index=True,
    )

    candidate_id = Column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # -----------------------------
    # Interview State
    # -----------------------------
    status = Column(
        SqlEnum(InterviewStatus),
        nullable=False,
        default=InterviewStatus.CREATED,
    )

    current_stage = Column(
        SqlEnum(InterviewStage),
        nullable=False,
        default=InterviewStage.WARMUP,
    )

    current_question_index = Column(
        Integer,
        nullable=False,
        default=0,
    )

    # Running score throughout interview
    total_score = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    # -----------------------------
    # Timestamps
    # -----------------------------
    started_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # -----------------------------
    # ORM Relationships
    # -----------------------------
    answers = relationship(
        "Answer",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    room = relationship(
        "InterviewRoom",
    )

    candidate = relationship(
        "User",
    )