from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Loads all configuration from environment variables (.env file or system env).
    """

    # ======================
    # API
    # ======================
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Interviewer"

    # ======================
    # SECURITY
    # ======================
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # default fallback
    ALGORITHM: str = "HS256"

    # ======================
    # DATABASE
    # ======================
    DATABASE_URL: str

    # ======================
    # AI / LLM
    # ======================
    OPENAI_API_KEY: str | None = None

    # ======================
    # INITIAL ADMIN
    # ======================
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    # ======================
    # ENVIRONMENT
    # ======================
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()