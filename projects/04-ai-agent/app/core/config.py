from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VERSION: str = "0.1.0"

    # LLM configuration for agent reasoning
    LLM_PROVIDER: str = "mock"  # "mock" | "openai"
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 2048

    # Agent configuration
    MAX_ITERATIONS: int = 10  # Max reasoning loops before forced answer
    MAX_TOOL_CALLS: int = 5  # Max tool calls per run

    # API keys
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
