from app.core.config import settings
from app.embedding.base import AbstractEmbedder


class OpenAIEmbedder(AbstractEmbedder):
    """Embedding using OpenAI's embedding API.

    TODO: Integrate the openai library:
        pip install openai

    Then implement:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

    API reference: https://platform.openai.com/docs/api-reference/embeddings
    """

    def __init__(self, model: str | None = None, dimension: int | None = None):
        self.model = model or settings.EMBEDDING_MODEL
        self.dimension = dimension or settings.EMBEDDING_DIMENSION
        # TODO: Initialize OpenAI client
        # self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def embed_text(self, text: str) -> list[float]:
        """Embed a single text string.

        TODO: Replace with real OpenAI API call:
            response = client.embeddings.create(
                model=self.model,
                input=[text]
            )
            return response.data[0].embedding
        """
        raise NotImplementedError(
            "OpenAI embedding not implemented. "
            "Install openai and implement the API call."
        )

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts.

        TODO: Replace with real OpenAI API call:
            response = client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]

        Note: OpenAI supports batching — send all texts in one call
        for efficiency (up to 2048 texts per request).
        """
        raise NotImplementedError(
            "OpenAI embedding not implemented. "
            "Install openai and implement the API call."
        )
