from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text, Float

from app.core.db import Base


class Interview(Base):
    """
    Interview template definition.

    This is NOT a live interview session.

    It defines:
    - interview type
    - role target
    - difficulty baseline
    - description / context
    """

    __tablename__ = "interviews"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id = Column(Integer, primary_key=True, index=True)

    # -----------------------------
    # Metadata
    # -----------------------------
    title = Column(
        String,
        nullable=False,
        index=True,
    )

    role = Column(
        String,
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    difficulty = Column(
        String,
        nullable=False,
        default="intermediate",
    )

    # -----------------------------
    # Configuration
    # -----------------------------
    total_questions = Column(
        Integer,
        nullable=False,
        default=10,
    )

    time_limit_minutes = Column(
        Integer,
        nullable=True,
    )

    # Optional weighting for scoring system
    passing_score = Column(
        Float,
        nullable=False,
        default=70.0,
    )

    # -----------------------------
    # Audit fields
    # -----------------------------
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )