from app.core.config import settings
from app.schemas.rag import QueryResponse, RetrievedChunk


class RAGGenerator:
    """Generates answers using retrieved context via an LLM.

    The pipeline: query → retrieve → build context → call LLM → return answer
    """

    def __init__(self, llm_provider: str | None = None):
        self.llm_provider = llm_provider or settings.LLM_PROVIDER

    def generate(
        self,
        query: str,
        retrieved_chunks: list[RetrievedChunk],
    ) -> QueryResponse:
        """Generate a response given the query and retrieved context."""
        context = self._build_context(retrieved_chunks)
        prompt = self._build_prompt(query, context)
        answer = self._call_llm(prompt)
        return QueryResponse(
            answer=answer,
            sources=retrieved_chunks,
            query=query,
        )

    def _build_context(self, chunks: list[RetrievedChunk]) -> str:
        """Build a context string from retrieved chunks."""
        parts = []
        for i, rc in enumerate(chunks, 1):
            source = rc.chunk.metadata.get("source", "unknown")
            parts.append(f"[Source {i}: {source}]\n{rc.chunk.content}")
        return "\n\n".join(parts)

    def _build_prompt(self, query: str, context: str) -> str:
        """Build the full prompt with context and query.

        TODO: Experiment with different prompt templates:
        - Few-shot examples
        - Chain-of-thought instructions
        - Domain-specific instructions
        """
        return (
            "You are a helpful assistant. Answer the question based on the "
            "following context. If the context doesn't contain enough information "
            "to answer, say so clearly.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            "Answer:"
        )

    def _call_llm(self, prompt: str) -> str:
        """Call the LLM to generate a response.

        TODO: Integrate real LLM providers:

        OpenAI:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
            )
            return response.choices[0].message.content

        Anthropic:
            import anthropic
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=settings.LLM_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        """
        # Mock response for testing
        return (
            f"[MOCK LLM] This is a placeholder response. "
            f"Integrate a real LLM provider (OpenAI, Anthropic, etc.) "
            f"to generate actual answers. Prompt length: {len(prompt)} chars."
        )
