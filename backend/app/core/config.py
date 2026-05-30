"""
AI English Coach — Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "ai-english-coach"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-n"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://aistudy.io.vn",
    ]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres123@localhost:5432/ai_english_coach"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "english_coach"

    # S3/MinIO
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_AUDIO: str = "audio-recordings"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Anthropic
    ANTHROPIC_API_KEY: str = ""

    # Deepgram
    DEEPGRAM_API_KEY: str = ""

    # FPT.AI
    FPT_API_KEY: str = ""

    # Auth
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    OTP_EXPIRE_MINUTES: int = 5

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_CONVERSATION_PER_DAY: int = 3  # Free tier

    # External URLs
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"
    NEXT_PUBLIC_WS_URL: str = "ws://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
