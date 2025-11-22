"""RAG (Retrieval-Augmented Generation) system for document analysis.

WARNING: This implementation loads all documents into memory. For production:
- Use a vector database (pgvector, Pinecone, Weaviate)
- Implement pagination for large documents
- Add document metadata tracking
- Consider streaming for processing large files
"""

import logging
from typing import List

import numpy as np

from .models import RAGConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGError(Exception):
    """Base exception for RAG errors."""

    pass


class RAGSystem:
    """Simple RAG system for analyzing documents (e.g., SEC filings).

    Features:
    - Chunk documents into manageable pieces
    - Use sentence-transformers for embeddings (no API needed)
    - Retrieve top-k relevant chunks for queries

    Limitations:
    - All documents stored in memory (not scalable beyond a few documents)
    - No persistence between sessions
    - Sequential processing only

    For production use with many documents, consider:
    - PostgreSQL with pgvector extension
    - Dedicated vector databases (Pinecone, Weaviate, Qdrant)
    - Document streaming and batch processing

    Example:
        config = RAGConfig(chunk_size=300, top_k=3)
        rag = RAGSystem(config)
        rag.add_document(sec_filing_text)
        context = rag.query("What are the risk factors?")
    """

    def __init__(self, config: RAGConfig):
        """Initialize RAG system.

        Args:
            config: RAG configuration
        """
        self.config = config
        self._model = None
        self.documents: List[str] = []
        self.embeddings: np.ndarray = None

        # Warn if configuration might cause memory issues
        if config.chunk_size > 1000:
            logger.warning(
                f"Large chunk_size ({config.chunk_size}) may impact performance. "
                "Consider using 300-500 for better results."
            )

    def _get_model(self):
        """Lazy load embedding model.

        Returns:
            SentenceTransformer model

        Raises:
            RAGError: If model loading fails
        """
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer

                logger.info(f"Loading embedding model: {self.config.embedding_model}")
                self._model = SentenceTransformer(self.config.embedding_model)
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise RAGError(
                    "Could not load embedding model. Install: pip install sentence-transformers"
                ) from e
        return self._model

    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks.

        Args:
            text: Document text

        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []

        chunk_size = self.config.chunk_size
        overlap = self.config.chunk_overlap

        if len(words) < chunk_size:
            # Document smaller than chunk size
            return [text] if text.strip() else []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i : i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)

        logger.debug(f"Split text into {len(chunks)} chunks")
        return chunks

    def add_document(self, text: str) -> int:
        """Add document to RAG system.

        Args:
            text: Document text (e.g., SEC filing)

        Returns:
            Number of chunks added

        Raises:
            RAGError: If embedding generation fails
        """
        if not text or not text.strip():
            logger.warning("Attempted to add empty document")
            return 0

        # Warn if storing many documents
        if len(self.documents) > 100:
            logger.warning(
                f"RAG system has {len(self.documents)} chunks. "
                "Consider using a vector database for better performance."
            )

        try:
            chunks = self.chunk_text(text)
            if not chunks:
                return 0

            self.documents.extend(chunks)

            # Generate embeddings
            model = self._get_model()
            new_embeddings = model.encode(chunks, show_progress_bar=False)

            if self.embeddings is None:
                self.embeddings = new_embeddings
            else:
                self.embeddings = np.vstack([self.embeddings, new_embeddings])

            logger.info(f"Added document with {len(chunks)} chunks")
            return len(chunks)

        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            raise RAGError("Could not process document") from e

    def query(self, question: str, return_scores: bool = False) -> str:
        """Query documents and return relevant context.

        Args:
            question: Query text
            return_scores: If True, include similarity scores in output

        Returns:
            Concatenated top-k relevant chunks

        Raises:
            RAGError: If query processing fails
        """
        if not self.documents:
            logger.warning("Query on empty RAG system")
            return ""

        try:
            # Encode question
            model = self._get_model()
            query_embedding = model.encode([question], show_progress_bar=False)[0]

            # Calculate cosine similarity
            similarities = np.dot(self.embeddings, query_embedding) / (
                np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
            )

            # Get top-k indices
            top_k = min(self.config.top_k, len(self.documents))
            top_indices = np.argsort(similarities)[-top_k:][::-1]

            # Return concatenated chunks
            context_chunks = []
            for idx in top_indices:
                chunk = self.documents[idx]
                if return_scores:
                    score = similarities[idx]
                    context_chunks.append(f"[Score: {score:.3f}] {chunk}")
                else:
                    context_chunks.append(chunk)

            result = "\n\n".join(context_chunks)
            logger.debug(f"Query returned {len(context_chunks)} chunks")
            return result

        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise RAGError("Could not process query") from e

    def clear(self):
        """Clear all documents and embeddings."""
        self.documents = []
        self.embeddings = None
        logger.info("Cleared RAG system")

    def get_stats(self) -> dict:
        """Get RAG system statistics.

        Returns:
            Dictionary with system stats
        """
        return {
            "num_chunks": len(self.documents),
            "embedding_shape": self.embeddings.shape if self.embeddings is not None else None,
            "chunk_size": self.config.chunk_size,
            "top_k": self.config.top_k,
        }
