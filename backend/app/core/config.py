from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    APP_NAME: str = "FutureSeat API"
    APP_ENV:  str = "development"

    DATABASE_URL: str
    
    # Add these back! Pydantic needs to know to look for them in the .env file.
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_SESSION_SECRET: str

    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [o.strip() for o in value.split(",") if o.strip()]
        return []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # Adding this prevents crashes if you have extra unused variables in your .env
        extra="ignore" 
    )

settings = Settings()