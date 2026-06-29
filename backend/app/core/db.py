from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

settings = get_settings()

# Sync engine (IMPORTANT)
engine = create_engine(settings.DATABASE_URL, echo=True)

# Sync session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base for models
Base = declarative_base()