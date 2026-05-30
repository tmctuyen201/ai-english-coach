from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_english_coach.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "change-me-in-production"
    DEBUG: bool = True
    PORT: int = 8089

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
