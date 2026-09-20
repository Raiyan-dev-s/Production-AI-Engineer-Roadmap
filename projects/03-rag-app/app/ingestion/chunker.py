import re
import uuid

from app.schemas.rag import Chunk, Document


class TextChunker:
    """Chunks documents into smaller pieces for embedding and retrieval."""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        strategy: str = "fixed",
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = strategy

    def chunk_text(self, text: str, doc_id: str | None = None) -> list[Chunk]:
        """Split text into chunks using the configured strategy."""
        doc_id = doc_id or str(uuid.uuid4())

        if self.strategy == "fixed":
            return self._fixed_size_chunks(text, doc_id)
        elif self.strategy == "sentence":
            return self._sentence_chunks(text, doc_id)
        elif self.strategy == "semantic":
            return self._semantic_chunks(text, doc_id)
        else:
            raise ValueError(f"Unknown chunking strategy: {self.strategy}")

    def chunk_document(self, document: Document) -> list[Chunk]:
        """Chunk a Document object, preserving metadata."""
        chunks = self.chunk_text(document.content, document.doc_id)
        for chunk in chunks:
            chunk.metadata = {
                **document.metadata,
                **chunk.metadata,
                "chunk_strategy": self.strategy,
            }
        return chunks

    def _fixed_size_chunks(self, text: str, doc_id: str) -> list[Chunk]:
        """Split text into fixed-size chunks with overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    content=chunk_text,
                    doc_id=doc_id,
                    start_index=start,
                    end_index=min(end, len(text)),
                )
            )
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def _sentence_chunks(self, text: str, doc_id: str) -> list[Chunk]:
        """Split text on sentence boundaries, grouping up to chunk_size chars.

        TODO: Improve sentence detection for abbreviations, edge cases.
        """
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current_chunk: list[str] = []
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) > self.chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        content=chunk_text,
                        doc_id=doc_id,
                        start_index=0,  # TODO: track actual positions
                        end_index=len(chunk_text),
                    )
                )
                # Keep overlap sentences
                overlap_sentences: list[str] = []
                overlap_len = 0
                for s in reversed(current_chunk):
                    if overlap_len + len(s) > self.chunk_overlap:
                        break
                    overlap_sentences.insert(0, s)
                    overlap_len += len(s)
                current_chunk = overlap_sentences
                current_length = overlap_len

            current_chunk.append(sentence)
            current_length += len(sentence)

        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    content=chunk_text,
                    doc_id=doc_id,
                    start_index=0,
                    end_index=len(chunk_text),
                )
            )
        return chunks

    def _semantic_chunks(self, text: str, doc_id: str) -> list[Chunk]:
        """Split text based on semantic similarity.

        TODO: Implement real semantic chunking using embeddings to detect
        topic boundaries. This would:
        1. Embed each sentence
        2. Compute cosine similarity between consecutive sentences
        3. Split where similarity drops below a threshold

        For now, falls back to sentence-based chunking.
        """
        # TODO: Replace with real semantic chunking
        # Example approach:
        # from sentence_transformers import SentenceTransformer
        # model = SentenceTransformer('all-MiniLM-L6-v2')
        # embeddings = model.encode(sentences)
        # for i in range(1, len(embeddings)):
        #     sim = cosine_similarity(embeddings[i-1], embeddings[i])
        #     if sim < threshold: split here
        return self._sentence_chunks(text, doc_id)
