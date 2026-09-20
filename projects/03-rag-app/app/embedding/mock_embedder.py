import random

from app.embedding.base import AbstractEmbedder


class MockEmbedder(AbstractEmbedder):
    """Returns random vectors for testing without API keys.

    Useful for:
    - Unit testing the RAG pipeline
    - Development without API costs
    - CI/CD environments
    """

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        random.seed(42)  # Deterministic for reproducible tests

    def embed_text(self, text: str) -> list[float]:
        random.seed(hash(text) % (2**32))
        return [random.gauss(0, 1) for _ in range(self.dimension)]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(t) for t in texts]
