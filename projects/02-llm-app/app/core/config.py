from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = Field(default="development", description="Application environment")
    DEBUG: bool = Field(default=True, description="Enable debug mode")

    OPENAI_API_KEY: str | None = Field(default=None, description="OpenAI API key")
    ANTHROPIC_API_KEY: str | None = Field(default=None, description="Anthropic API key")

    LLM_PROVIDER: str = Field(
        default="mock",
        description="LLM provider: mock, openai, or anthropic",
    )
    MODEL_NAME: str = Field(
        default="gpt-3.5-turbo",
        description="Model name to use for generation",
    )
    MAX_TOKENS: int = Field(default=1024, description="Maximum tokens for generation")
    TEMPERATURE: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Sampling temperature"
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
