from app.embedding.base import AbstractEmbedder
from app.schemas.rag import RetrievedChunk
from app.vectorstore.base import AbstractVectorStore


class Retriever:
    """Retrieves relevant chunks from the vector store for a given query."""

    def __init__(self, vector_store: AbstractVectorStore, embedder: AbstractEmbedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[RetrievedChunk]:
        """Semantic search: embed query, find similar chunks."""
        query_embedding = self.embedder.embed_text(query)
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters,
        )
        return [RetrievedChunk(chunk=chunk, score=score) for chunk, score in results]

    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
        keyword_weight: float = 0.3,
    ) -> list[RetrievedChunk]:
        """Combine semantic search with keyword matching.

        TODO: Implement proper hybrid search combining:
        1. Semantic similarity (vector search)
        2. Keyword/BM25 matching (text search)
        3. Weighted score combination

        This approach often outperforms pure semantic search for
        queries with specific terms (names, codes, technical jargon).
        """
        # Semantic results
        semantic_results = self.search(query, top_k=top_k * 2, filters=filters)

        # TODO: Implement keyword search
        # - Build inverted index or use BM25
        # - Score documents by keyword overlap
        # keyword_results = self._keyword_search(query, top_k * 2, filters)

        # TODO: Combine scores
        # for result in semantic_results:
        #     keyword_score = keyword_scores.get(result.chunk.chunk_id, 0)
        #     combined = (1 - keyword_weight) * result.score + keyword_weight * keyword_score

        # For now, return pure semantic results
        return semantic_results[:top_k]
