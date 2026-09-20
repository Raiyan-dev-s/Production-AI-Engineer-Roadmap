from abc import ABC, abstractmethod

from app.schemas.rag import Chunk


class AbstractEmbedder(ABC):
    """Base class for all embedding implementations."""

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Embed a single text string into a vector."""
        ...

    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple text strings into vectors."""
        ...

    def embed_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """Embed a list of Chunk objects, returning new Chunks with embeddings."""
        texts = [c.content for c in chunks]
        embeddings = self.embed_texts(texts)
        embedded = []
        for chunk, embedding in zip(chunks, embeddings, strict=False):
            embedded.append(chunk.model_copy(update={"embedding": embedding}))
        return embedded
