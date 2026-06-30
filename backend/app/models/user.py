from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(Base):
    """
    Core authentication identity.

    This model represents all system users:
    - candidates
    - interviewers
    - admins
    """

    __tablename__ = "users"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id = Column(Integer, primary_key=True, index=True)

    # -----------------------------
    # Authentication
    # -----------------------------
    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password = Column(
        String,
        nullable=False,
    )

    # -----------------------------
    # Role & Access Control
    # -----------------------------
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
        default="candidate",
        index=True,
    )

    # -----------------------------
    # Relationships
    # -----------------------------
    # candidate_profile = relationship(
    #     "Candidate",
    #     back_populates="user",
    #     uselist=False,
    #     cascade="all, delete-orphan",
    # )

    # interviewer_profile = relationship(
    #     "Interviewer",
    #     back_populates="user",
    #     uselist=False,
    #     cascade="all, delete-orphan",
    # )