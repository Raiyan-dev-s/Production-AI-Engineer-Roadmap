from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.embedding.mock_embedder import MockEmbedder
from app.generation.rag_generator import RAGGenerator
from app.ingestion.chunker import TextChunker
from app.ingestion.document_loader import DocumentLoader
from app.retrieval.retriever import Retriever
from app.schemas.rag import (
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)
from app.vectorstore.memory_store import InMemoryVectorStore

router = APIRouter()

# --- Shared components (in production, use dependency injection) ---

_vector_store = InMemoryVectorStore()
_embedder = MockEmbedder(dimension=settings.EMBEDDING_DIMENSION)
_loader = DocumentLoader()
_chunker = TextChunker(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
    strategy=settings.CHUNKING_STRATEGY,
)
_retriever = Retriever(vector_store=_vector_store, embedder=_embedder)
_generator = RAGGenerator()


@router.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    """Ingest a document into the RAG pipeline.

    Flow: Load → Chunk → Embed → Store
    """
    try:
        # Step 1: Load documents
        if request.content:
            docs = [_loader.load_text(request.content, request.metadata)]
        elif request.file_path:
            docs = [_loader.load_file(request.file_path, request.metadata)]
        elif request.directory_path:
            docs = _loader.load_directory(request.directory_path, request.metadata)
        else:
            raise HTTPException(
                status_code=400,
                detail="Provide content, file_path, or directory_path",
            )

        if not docs:
            raise HTTPException(status_code=404, detail="No documents found")

        chunks_created = 0
        for doc in docs:
            # Step 2: Chunk
            chunks = _chunker.chunk_document(doc)

            # Step 3: Embed
            embedded_chunks = _embedder.embed_chunks(chunks)

            # Step 4: Store
            _vector_store.add_chunks(embedded_chunks)
            chunks_created += len(embedded_chunks)

        return IngestResponse(
            doc_id=docs[0].doc_id or "",
            chunks_created=chunks_created,
            status="success",
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the RAG system.

    Flow: Embed query → Retrieve context → Generate answer
    """
    try:
        # Step 1: Retrieve relevant chunks
        retrieved = _retriever.search(
            query=request.query,
            top_k=request.top_k,
            filters=request.filters,
        )

        if not retrieved:
            return QueryResponse(
                answer="No relevant documents found. Try ingesting some documents first.",
                sources=[],
                query=request.query,
            )

        # Step 2: Generate answer
        response = _generator.generate(request.query, retrieved)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e!s}") from e


@router.get("/stats")
async def stats():
    """Return vector store statistics."""
    return {
        "total_chunks": _vector_store.count(),
        "embedding_model": settings.EMBEDDING_MODEL,
        "chunk_size": settings.CHUNK_SIZE,
        "chunk_strategy": settings.CHUNKING_STRATEGY,
    }
