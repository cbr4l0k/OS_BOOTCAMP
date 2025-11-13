from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """
    Application configuration settings.

    This configuration loads from environment variables or .env file.
    Priority: environment variables > .env file > default values
    """

    # OpenAI API Configuration
    openai_api_key: str = Field(
        ...,
        description="API key for the OpenAI-compatible service"
    )

    openai_api_base: str = Field(
        default="https://foundation-models.api.cloud.ru/v1",
        description="Base URL for the OpenAI-compatible API"
    )

    model_name: str = Field(
        default="GigaChat/GigaChat-2-Max",
        description="Name of the model to use"
    )

    # Application Settings
    streaming: bool = Field(
        default=True,
        description="Enable streaming responses"
    )

    # Chainlit Configuration
    chainlit_port: int = Field(
        default=8000,
        description="Port for Chainlit server"
    )

    chainlit_host: str = Field(
        default="0.0.0.0",
        description="Host for Chainlit server"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Create a singleton instance
config = AppConfig()