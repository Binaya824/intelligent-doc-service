from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.core.config import settings
import logging
from typing import Optional, Set

logger = logging.getLogger(__name__)


class QdrantService:
    _client: Optional[QdrantClient] = None

    def __init__(self):
        if QdrantService._client is None:
            try:
                QdrantService._client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY,
                    check_compatibility=False,  # REQUIRED (you already saw why)
                )
                logger.info("✅ Qdrant client initialized")
            except Exception as e:
                logger.exception("❌ Failed to initialize Qdrant client")
                raise RuntimeError("Qdrant initialization failed") from e

        self.client = QdrantService._client


    def _existing_collections(self) -> Set[str]:
        collections = self.client.get_collections().collections
        return {c.name for c in collections}

    def ensure_collection(self, name: str, vector_size: int = 1024):
        try:
            self._client.get_collection(collection_name=name)
        except:
            self._client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
        logger.info(f"✅ Collection '{name}' created with vector size {vector_size}.")
    
    def get_client(self):
        return self._client