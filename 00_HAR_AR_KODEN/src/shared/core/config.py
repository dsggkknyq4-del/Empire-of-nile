import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    # General
    ENVIRONMENT: str = "local"
    PROJECT_NAME: str = "Developer_Package_v1"
    
    # Database
    POSTGRES_USER: str = "v1_user"
    POSTGRES_PASSWORD: str = "v1_password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "v1_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Security
    SECRET_KEY: str = "change_this_shared_secret_key_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI / LLM
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-3.5-turbo" # Default MVP model
    
settings = Settings()
