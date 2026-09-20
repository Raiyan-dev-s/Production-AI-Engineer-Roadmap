from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    doc_id: str | None = None


class Chunk(BaseModel):
    chunk_id: str
    content: str
    embedding: list[float] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    doc_id: str | None = None
    start_index: int = 0
    end_index: int = 0


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: dict[str, Any] | None = None


class RetrievedChunk(BaseModel):
    chunk: Chunk
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[RetrievedChunk]
    query: str


class IngestRequest(BaseModel):
    content: str | None = None
    file_path: str | None = None
    directory_path: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class IngestResponse(BaseModel):
    doc_id: str
    chunks_created: int
    status: str = "success"
