from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    gcp_project_id: str = "your-gcp-project-id"
    default_prompt_secret_id: str = "default-prompt"
    default_gemini_model: str = "gemini-1.5-pro-latest"  # Agent model config

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
