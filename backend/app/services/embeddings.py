import logging
from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Model name — multilingual, lightweight, high-quality for FR/EN job descriptions
_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class EmbeddingService:
    """
    Singleton service for generating semantic text embeddings.

    Uses Sentence Transformers with a multilingual model capable of processing
    both French and English job descriptions and resumes.

    Design: Loaded once at app startup to avoid repeated expensive I/O.
    """

    def __init__(self) -> None:
        logger.info(
            "Loading embedding model...",
            extra={"model": _MODEL_NAME},
        )
        self._model = SentenceTransformer(_MODEL_NAME)
        logger.info("Embedding model loaded successfully.", extra={"model": _MODEL_NAME})

    def encode(self, text: str) -> List[float]:
        """
        Generate a dense embedding vector for a given text string.

        Args:
            text: Raw text (job description, resume content, query).

        Returns:
            A list of floats representing the semantic embedding (384 dimensions).
        """
        vector = self._model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts efficiently.

        Args:
            texts: A list of raw text strings.

        Returns:
            A list of embedding vectors.
        """
        vectors = self._model.encode(texts, normalize_embeddings=True, batch_size=32)
        return [v.tolist() for v in vectors]

    @property
    def vector_size(self) -> int:
        """Return the output dimensionality of the embedding model."""
        return self._model.get_sentence_embedding_dimension()


# ---------------------------------------------------------------------------
# Module-level singleton — instantiated once on first import
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """
    Return the shared EmbeddingService singleton.

    Using lru_cache ensures the heavy model is loaded only once,
    even if this function is called from multiple FastAPI dependencies.
    """
    return EmbeddingService()
