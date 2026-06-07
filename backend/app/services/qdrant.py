import logging
from functools import lru_cache
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from qdrant_client.http.exceptions import UnexpectedResponse

from app.core.config import settings

logger = logging.getLogger(__name__)

# Collection names used across the application
COLLECTION_JOBS = "jobs"
COLLECTION_RESUMES = "resumes"

# Must match the output dim of EmbeddingService (paraphrase-multilingual-MiniLM-L12-v2)
VECTOR_SIZE = 384


class QdrantService:
    """
    Service layer for all interactions with the Qdrant vector database.

    Responsibilities:
    - Create and manage vector collections on startup.
    - Upsert (insert or update) embedding vectors with metadata payloads.
    - Execute hybrid search: dense vector similarity + structured payload filtering.

    Design: Singleton — instantiated once via get_qdrant_service().
    """

    def __init__(self) -> None:
        self._client = QdrantClient(url=settings.QDRANT_URL)
        logger.info("Qdrant client connected.", extra={"url": settings.QDRANT_URL})
        self._init_collections()

    # ------------------------------------------------------------------
    # Collection Management
    # ------------------------------------------------------------------

    def _init_collections(self) -> None:
        """
        Ensure all required collections exist with correct vector configuration.
        Idempotent — safe to call on every app startup.
        """
        for name in [COLLECTION_JOBS, COLLECTION_RESUMES]:
            try:
                self._client.get_collection(name)
                logger.debug("Qdrant collection already exists.", extra={"collection": name})
            except (UnexpectedResponse, Exception):
                self._client.create_collection(
                    collection_name=name,
                    vectors_config=qmodels.VectorParams(
                        size=VECTOR_SIZE,
                        distance=qmodels.Distance.COSINE,
                    ),
                )
                logger.info(
                    "Qdrant collection created.",
                    extra={"collection": name, "vector_size": VECTOR_SIZE},
                )

    # ------------------------------------------------------------------
    # Write Operations
    # ------------------------------------------------------------------

    def upsert(
        self,
        collection: str,
        point_id: str,
        vector: List[float],
        payload: Dict[str, Any],
    ) -> None:
        """
        Insert or update a single vector point in a Qdrant collection.

        Args:
            collection: Target collection name (use COLLECTION_* constants).
            point_id:   Unique string ID for the point (UUID from PostgreSQL).
            vector:     Dense embedding vector (must match VECTOR_SIZE).
            payload:    Structured metadata attached to the point for filtering.
        """
        self._client.upsert(
            collection_name=collection,
            points=[
                qmodels.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )
        logger.debug(
            "Upserted point into Qdrant.",
            extra={"collection": collection, "point_id": point_id},
        )

    # ------------------------------------------------------------------
    # Read / Search Operations
    # ------------------------------------------------------------------

    def search(
        self,
        collection: str,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find the nearest vector neighbours with optional payload filtering.

        Filtering is performed by Qdrant (server-side), never in-memory,
        to maintain O(log n) performance at scale.

        Args:
            collection:   Collection to search.
            query_vector: The query embedding (e.g., resume vector).
            limit:        Maximum number of results to return.
            filters:      Dict of {field: value} pairs for exact-match filtering.
                          Example: {"status": "active", "job_type": "CDI"}

        Returns:
            List of dicts with keys: id, score, payload.
        """
        qdrant_filter: Optional[qmodels.Filter] = None
        if filters:
            conditions = [
                qmodels.FieldCondition(
                    key=key,
                    match=qmodels.MatchValue(value=value),
                )
                for key, value in filters.items()
            ]
            qdrant_filter = qmodels.Filter(must=conditions)

        results = self._client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=limit,
            query_filter=qdrant_filter,
            with_payload=True,
        )

        return [
            {"id": str(r.id), "score": round(r.score, 4), "payload": r.payload}
            for r in results
        ]

    def delete_point(self, collection: str, point_id: str) -> None:
        """Remove a single vector point from a collection."""
        self._client.delete(
            collection_name=collection,
            points_selector=qmodels.PointIdsList(points=[point_id]),
        )
        logger.info(
            "Deleted point from Qdrant.",
            extra={"collection": collection, "point_id": point_id},
        )


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_qdrant_service() -> QdrantService:
    """
    Return the shared QdrantService singleton.
    Thread-safe due to Python's GIL and lru_cache mechanics.
    """
    return QdrantService()
