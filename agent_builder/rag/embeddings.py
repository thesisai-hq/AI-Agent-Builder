"""Embedding Model Implementations - All Free Options"""

from abc import ABC, abstractmethod
from typing import List, Optional
import logging
import hashlib

logger = logging.getLogger(__name__)


class BaseEmbedding(ABC):
    """Base class for all embedding models"""

    def __init__(self, dimensions: int):
        self.dimensions = dimensions

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Convert text to embedding vector"""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Convert multiple texts to embeddings"""
        pass

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between vectors"""
        dot = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = sum(a * a for a in vec1) ** 0.5
        mag2 = sum(b * b for b in vec2) ** 0.5
        return dot / (mag1 * mag2) if mag1 and mag2 else 0.0


# ============================================================================
# OPTION 1: Simple Hash-Based (No Dependencies)
# ============================================================================


class SimpleHashEmbedding(BaseEmbedding):
    """
    Simple hash-based embedding - No external dependencies

    Pros:
    - ✅ Zero dependencies
    - ✅ Instant setup
    - ✅ Deterministic

    Cons:
    - ⚠️ Not semantic (similar texts don't have similar vectors)
    - ⚠️ Only good for exact/near-exact matching

    Use for: Testing, placeholder, simple keyword matching
    """

    def __init__(self, dimensions: int = 128):
        super().__init__(dimensions)
        logger.info(f"Initialized SimpleHashEmbedding ({dimensions} dims)")

    def embed_text(self, text: str) -> List[float]:
        # Hash text to bytes
        hash_obj = hashlib.sha256(text.lower().strip().encode())
        hash_bytes = hash_obj.digest()

        # Convert to floats [0, 1]
        vector = []
        for i in range(0, min(len(hash_bytes), self.dimensions), 2):
            val = (hash_bytes[i] + hash_bytes[i + 1]) / 512.0
            vector.append(val)

        # Pad if needed
        while len(vector) < self.dimensions:
            vector.append(0.0)

        return vector[: self.dimensions]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(text) for text in texts]


# ============================================================================
# OPTION 2: Sentence Transformers (Recommended)
# ============================================================================


class SentenceTransformerEmbedding(BaseEmbedding):
    """
    Sentence Transformers - Semantic embeddings

    Pros:
    - ✅ Free and open source
    - ✅ Runs locally
    - ✅ Semantic understanding
    - ✅ Fast (50-100ms per text)
    - ✅ Many pre-trained models

    Cons:
    - ⚠️ Requires ~500MB download first time
    - ⚠️ Needs some RAM

    Models:
    - all-MiniLM-L6-v2: Fast, 384 dims (recommended)
    - all-mpnet-base-v2: Accurate, 768 dims
    - multi-qa-mpnet-base-dot-v1: Q&A optimized

    Install: pip install sentence-transformers
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading SentenceTransformer: {model_name}...")
            self.model = SentenceTransformer(model_name)
            dimensions = self.model.get_sentence_embedding_dimension()
            super().__init__(dimensions)
            logger.info(f"✅ Loaded {model_name} ({dimensions} dims)")

        except ImportError:
            logger.error("sentence-transformers not installed")
            logger.error("Install: pip install sentence-transformers")
            raise

    def embed_text(self, text: str) -> List[float]:
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()


# ============================================================================
# OPTION 3: Ollama Embeddings (Local LLM)
# ============================================================================


class OllamaEmbedding(BaseEmbedding):
    """
    Ollama embeddings - Uses local Ollama server

    Pros:
    - ✅ Free and local
    - ✅ Private (no API calls)
    - ✅ Works with existing Ollama setup

    Cons:
    - ⚠️ Requires Ollama running
    - ⚠️ Slower than sentence-transformers
    - ⚠️ Quality depends on model

    Models:
    - nomic-embed-text: 768 dims (recommended)
    - mxbai-embed-large: 1024 dims

    Setup:
        ollama pull nomic-embed-text
    """

    def __init__(
        self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"
    ):
        try:
            import requests

            self.model = model
            self.base_url = base_url.rstrip("/")

            # Get dimensions by doing a test embedding
            test_embedding = self._embed_single("test")
            dimensions = len(test_embedding)

            super().__init__(dimensions)
            logger.info(f"✅ Ollama embedding ready: {model} ({dimensions} dims)")

        except Exception as e:
            logger.error(f"Ollama embedding initialization failed: {e}")
            raise

    def _embed_single(self, text: str) -> List[float]:
        import requests

        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": self.model, "prompt": text},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def embed_text(self, text: str) -> List[float]:
        return self._embed_single(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(text) for text in texts]


# ============================================================================
# FACTORY FUNCTION
# ============================================================================


def get_embedding_model(
    provider: str = "sentence-transformers", model: Optional[str] = None, **kwargs
) -> BaseEmbedding:
    """
    Factory to get embedding model

    Args:
        provider: "simple", "sentence-transformers", "ollama"
        model: Model name (uses default if None)
        **kwargs: Provider-specific args

    Returns:
        Embedding model instance

    Usage:
        # Simple (no dependencies)
        emb = get_embedding_model("simple")

        # Sentence Transformers (recommended)
        emb = get_embedding_model("sentence-transformers")
        emb = get_embedding_model("sentence-transformers", model="all-mpnet-base-v2")

        # Ollama (if you have it)
        emb = get_embedding_model("ollama", model="nomic-embed-text")
    """
    provider = provider.lower()

    if provider == "simple":
        dimensions = kwargs.get("dimensions", 128)
        return SimpleHashEmbedding(dimensions=dimensions)

    elif provider == "sentence-transformers" or provider == "st":
        model = model or "all-MiniLM-L6-v2"
        return SentenceTransformerEmbedding(model_name=model)

    elif provider == "ollama":
        model = model or "nomic-embed-text"
        base_url = kwargs.get("base_url", "http://localhost:11434")
        return OllamaEmbedding(model=model, base_url=base_url)

    else:
        logger.warning(f"Unknown provider {provider}, using simple")
        return SimpleHashEmbedding()
