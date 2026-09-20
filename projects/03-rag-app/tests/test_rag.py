"""Tests for the RAG application."""

from app.core.config import settings


def test_settings_loads():
    """Verify settings load with defaults."""
    assert settings.VERSION is not None


def test_mock_embedder_dimensions():
    """Mock embedder returns correct dimension vectors."""
    from app.embedding.mock_embedder import MockEmbedder

    embedder = MockEmbedder()
    vectors = embedder.embed_texts(["hello world"])
    assert len(vectors) == 1
    assert len(vectors[0]) == settings.EMBEDDING_DIMENSION


def test_memory_vector_store_add_and_search():
    """In-memory vector store can add and search."""
    from app.schemas.rag import Chunk
    from app.vectorstore.memory_store import InMemoryVectorStore

    store = InMemoryVectorStore()
    chunk = Chunk(
        chunk_id="1",
        doc_id="doc1",
        content="test content",
        metadata={"source": "test"},
        start_index=0,
        end_index=12,
        embedding=[0.1, 0.2, 0.3],
    )
    store.add_chunks([chunk])
    results = store.search([0.1, 0.2, 0.3], top_k=1)
    assert len(results) >= 1
