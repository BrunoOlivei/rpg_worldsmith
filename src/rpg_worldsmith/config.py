from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    TITLE: str = "RPG Worldsmith"
    DESCRIPTION: str = "Gerador de mundos de RPG com IA"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "America/Sao_Paulo"
    OPEN_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"
    DATA_PATH: Path = Path("data")
    PYTHONPATH: str = "src"

    @field_validator("OPENAI_MODEL")
    def check_model(cls, v: str) -> str:
        allowed = {"gpt-4", "gpt-4o", "gpt-3.5-turbo"}
        if v not in allowed:
            raise ValueError(f"Modelo inválido: {v}. Use um dos: {", ".join(allowed)}.")
        return v

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
