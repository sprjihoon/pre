from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://prepacking:prepacking1234@localhost:5432/prepacking"
    SYNC_DATABASE_URL: str = "postgresql://prepacking:prepacking1234@localhost:5432/prepacking"
    UPLOAD_DIR: str = "uploads"
    MODEL_STORE_DIR: str = "../model_store"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()
