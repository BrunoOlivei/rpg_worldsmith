from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o"

    @field_validator("openai_model")
    def check_model(cls, v: str) -> str:
        allowed = {"gpt-4", "gpt-4o", "gpt-3.5-turbo"}
        if v not in allowed:
            raise ValueError(f"Modelo inválido: {v}. Use um dos: {", ".join(allowed)}.")
        return v

    class Config:
        env_file = ".env"
