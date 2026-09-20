from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VERSION: str = "0.1.0"

    # Vector store configuration
    VECTOR_STORE_TYPE: str = "memory"  # "memory" | "chroma" | "pinecone" | "weaviate"
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    PINECONE_API_KEY: str = ""
    PINECONE_INDEX_NAME: str = "rag-index"

    # Embedding configuration
    EMBEDDING_TYPE: str = "mock"  # "mock" | "openai"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_DIMENSION: int = 1536

    # LLM configuration
    LLM_PROVIDER: str = "mock"  # "mock" | "openai"
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 1024

    # Chunking configuration
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    CHUNKING_STRATEGY: str = "fixed"  # "fixed" | "sentence" | "semantic"

    # Retrieval configuration
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.7

    # API keys
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
