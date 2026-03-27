from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    APP_NAME: str = "FutureSeat API"
    APP_ENV:  str = "development"

    DATABASE_URL: str

    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    ADMIN_USERNAME:       str = "admin"
    ADMIN_PASSWORD:       str = "9100"
    ADMIN_SESSION_SECRET: str = "AIzaSyDJ9nqv4VaV48Wi8v-HGyQjZbjZq7k2Q58"

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
    )


settings = Settings()