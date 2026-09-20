from app.schemas.rag import Chunk
from app.vectorstore.base import AbstractVectorStore


class ChromaStore(AbstractVectorStore):
    """ChromaDB vector store integration.

    TODO: Implement using the chromadb library:
        pip install chromadb

        import chromadb
        client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        collection = client.get_or_create_collection("rag-docs")

    ChromaDB handles embedding storage, indexing, and querying internally.
    Consider wrapping or delegating to ChromaDB's built-in embedding function.
    """

    def __init__(self, collection_name: str = "rag-docs"):
        self.collection_name = collection_name
        # TODO: Initialize ChromaDB client
        # import chromadb
        # self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        # self.collection = self.client.get_or_create_collection(collection_name)

    def add_chunks(self, chunks: list[Chunk]) -> list[str]:
        """Add chunks to ChromaDB.

        TODO: Implement:
            self.collection.add(
                documents=[c.content for c in chunks],
                embeddings=[c.embedding for c in chunks],
                ids=[c.chunk_id for c in chunks],
                metadatas=[c.metadata for c in chunks],
            )
        """
        raise NotImplementedError("ChromaDB store not yet integrated")

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[tuple[Chunk, float]]:
        """Query ChromaDB for similar chunks.

        TODO: Implement:
            where_filter = filters if filters else None
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where_filter,
            )
            # Map results back to Chunk objects with scores
        """
        raise NotImplementedError("ChromaDB store not yet integrated")

    def delete(self, chunk_ids: list[str]) -> int:
        """Delete chunks from ChromaDB.

        TODO: Implement:
            self.collection.delete(ids=chunk_ids)
            return len(chunk_ids)
        """
        raise NotImplementedError("ChromaDB store not yet integrated")

    def count(self) -> int:
        """Return total chunk count.

        TODO: Implement:
            return self.collection.count()
        """
        raise NotImplementedError("ChromaDB store not yet integrated")
