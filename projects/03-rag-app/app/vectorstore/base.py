from abc import ABC, abstractmethod

from app.schemas.rag import Chunk


class AbstractVectorStore(ABC):
    """Base class for vector store implementations."""

    @abstractmethod
    def add_chunks(self, chunks: list[Chunk]) -> list[str]:
        """Add chunks to the store. Returns chunk IDs."""
        ...

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[tuple[Chunk, float]]:
        """Search for similar chunks. Returns (chunk, score) pairs."""
        ...

    @abstractmethod
    def delete(self, chunk_ids: list[str]) -> int:
        """Delete chunks by ID. Returns count deleted."""
        ...

    @abstractmethod
    def count(self) -> int:
        """Return total number of chunks in the store."""
        ...
