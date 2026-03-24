from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./prepacking.db"
    SYNC_DATABASE_URL: str = "sqlite:///./prepacking.db"
    UPLOAD_DIR: str = "uploads"
    MODEL_STORE_DIR: str = "../model_store"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()
