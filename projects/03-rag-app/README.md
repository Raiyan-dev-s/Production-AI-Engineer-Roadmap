# Project 03: RAG Application

A scaffold Retrieval-Augmented Generation (RAG) application showing the complete architecture with placeholder implementations.

## The RAG Pipeline

```
INGEST -> CHUNK -> EMBED -> STORE -> QUERY -> EMBED QUERY -> RETRIEVE -> GENERATE
```

Full cycle:

```
  [User uploads docs]
         |
         v
  +-----------+     +-----------+     +-----------+     +-----------+
  |  INGEST   | --> |   CHUNK   | --> |   EMBED   | --> |   STORE   |
  | load_file |     | fixed     |     | mock or   |     | memory or |
  | load_dir  |     | sentence  |     | openai    |     | chroma    |
  | load_text |     | semantic  |     |           |     |           |
  +-----------+     +-----------+     +-----------+     +-----------+
                                                       |
                                                       v
  +-----------+     +-----------+     +-----------+     +-----------+
  | GENERATE  | <-- | RETRIEVE  | <-- |EMBED QUERY| <-- |   QUERY   |
  | call LLM  |     | semantic  |     | same      |     | user      |
  | build ctx |     | hybrid    |     | embedder  |     | question  |
  | format    |     | search    |     |           |     |           |
  +-----------+     +-----------+     +-----------+     +-----------+
         |
         v
  [Answer with sources]
```

## Architecture

```
app/
  main.py                 # FastAPI application entry point
  core/
    config.py             # Pydantic Settings (env vars, config)
  schemas/
    rag.py                # Document, Chunk, QueryRequest/Response
  ingestion/
    document_loader.py    # Load from file, directory, or text
    chunker.py            # Split docs: fixed-size, sentence, semantic
  embedding/
    base.py               # AbstractEmbedder interface
    mock_embedder.py      # Random vectors for testing
    openai_embedder.py    # OpenAI integration (TODO)
  vectorstore/
    base.py               # AbstractVectorStore interface
    memory_store.py       # In-memory numpy similarity search
    chroma_store.py       # ChromaDB integration (TODO)
  retrieval/
    retriever.py          # Semantic and hybrid search
  generation/
    rag_generator.py      # Build context, call LLM
  api/routes/
    rag.py                # POST /api/ingest, POST /api/query
```

## Setup

```bash
cd projects/03-rag-app
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install fastapi uvicorn pydantic-settings numpy
```

## Environment Variables

```env
# Vector store
VECTOR_STORE_TYPE=memory          # memory | chroma
CHROMA_PERSIST_DIR=./data/chroma

# Embedding
EMBEDDING_TYPE=mock               # mock | openai
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_DIMENSION=1536

# LLM
LLM_PROVIDER=mock                 # mock | openai
LLM_MODEL=gpt-4
OPENAI_API_KEY=sk-...

# Chunking
CHUNK_SIZE=512
CHUNK_OVERLAP=50
CHUNKING_STRATEGY=fixed           # fixed | sentence | semantic

# Retrieval
TOP_K=5
SIMILARITY_THRESHOLD=0.7
```

## Run

```bash
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ingest` | Ingest documents into the vector store |
| POST | `/api/query` | Query the RAG system |
| GET | `/api/stats` | Vector store statistics |
| GET | `/health` | Health check |

## How Each Component Works

### Ingestion
- `DocumentLoader`: Reads files, directories, or raw text into `Document` objects
- Currently supports `.txt` and `.md`; TODO markers for PDF, DOCX, HTML

### Chunking
- **Fixed-size**: Splits every N characters with overlap (fast, simple)
- **Sentence-based**: Splits on sentence boundaries (preserves meaning)
- **Semantic**: TODO - uses embeddings to detect topic boundaries

### Embedding
- `MockEmbedder`: Deterministic random vectors (good for testing)
- `OpenAIEmbedder`: TODO - calls OpenAI embedding API

### Vector Store
- `InMemoryVectorStore`: Working implementation using numpy cosine similarity
- `ChromaStore`: TODO - ChromaDB integration for persistent storage

### Retrieval
- Semantic search: embed query, find top-K similar chunks
- Hybrid search: TODO - combine semantic + keyword (BM25) matching

### Generation
- Builds context string from retrieved chunks
- Calls LLM (mock or real) with context + question
- Returns answer with source attribution

## Integrating Real Services

### OpenAI
```python
# In config.py, set:
OPENAI_API_KEY = "sk-..."
EMBEDDING_TYPE = "openai"
LLM_PROVIDER = "openai"
```

### ChromaDB
```bash
pip install chroma
# In config.py, set:
VECTOR_STORE_TYPE = "chroma"
```

### Custom Embedding Model
Implement `AbstractEmbedder`:
```python
from app.embedding.base import AbstractEmbedder


class MyEmbedder(AbstractEmbedder):
    def embed_text(self, text: str) -> list[float]:
        # Your embedding logic here
        ...

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        # Your batch embedding logic here
        ...
```
