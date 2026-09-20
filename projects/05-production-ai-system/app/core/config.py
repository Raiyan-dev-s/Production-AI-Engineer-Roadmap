from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"  # development | staging | production

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    CORS_ORIGINS: list[str] = ["*"]

    # AI Model
    MODEL_NAME: str = "gpt-4"
    MODEL_VERSION: str = "1.0"
    MODEL_PATH: str = ""  # For local models
    MAX_BATCH_SIZE: int = 32
    INFERENCE_TIMEOUT: float = 30.0

    # Fallback
    FALLBACK_MODEL: str = "gpt-3.5-turbo"
    ENABLE_FALLBACK: bool = True
    MAX_RETRIES: int = 3

    # Monitoring
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    # Data validation
    MAX_INPUT_LENGTH: int = 10000
    ALLOWED_INPUT_TYPES: list[str] = ["text", "json"]

    # API keys
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
