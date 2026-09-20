import numpy as np

from app.schemas.rag import Chunk
from app.vectorstore.base import AbstractVectorStore


class InMemoryVectorStore(AbstractVectorStore):
    """In-memory vector store using numpy for cosine similarity search.

    Suitable for:
    - Prototyping and development
    - Small datasets (< 100k chunks)
    - Testing without external dependencies
    """

    def __init__(self):
        self._chunks: dict[str, Chunk] = {}
        self._embeddings: dict[str, np.ndarray] = {}

    def add_chunks(self, chunks: list[Chunk]) -> list[str]:
        """Add chunks with embeddings to the store."""
        chunk_ids = []
        for chunk in chunks:
            if chunk.embedding is None:
                raise ValueError(f"Chunk {chunk.chunk_id} has no embedding")
            self._chunks[chunk.chunk_id] = chunk
            self._embeddings[chunk.chunk_id] = np.array(
                chunk.embedding, dtype=np.float32
            )
            chunk_ids.append(chunk.chunk_id)
        return chunk_ids

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[tuple[Chunk, float]]:
        """Find most similar chunks using cosine similarity."""
        if not self._embeddings:
            return []

        query_vec = np.array(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return []

        results = []
        for chunk_id, emb in self._embeddings.items():
            chunk = self._chunks[chunk_id]

            # Apply metadata filters
            if filters and not all(
                chunk.metadata.get(k) == v for k, v in filters.items()
            ):
                continue

            # Cosine similarity
            emb_norm = np.linalg.norm(emb)
            if emb_norm == 0:
                continue
            score = float(np.dot(query_vec, emb) / (query_norm * emb_norm))
            results.append((chunk, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def delete(self, chunk_ids: list[str]) -> int:
        """Delete chunks by ID."""
        count = 0
        for cid in chunk_ids:
            if cid in self._chunks:
                del self._chunks[cid]
                del self._embeddings[cid]
                count += 1
        return count

    def count(self) -> int:
        return len(self._chunks)
