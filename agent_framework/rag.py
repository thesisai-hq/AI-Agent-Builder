"""RAG (Retrieval-Augmented Generation) system for document analysis."""

from typing import List, Tuple
import numpy as np
from .models import RAGConfig


class RAGSystem:
    """Simple RAG system for analyzing documents (e.g., SEC filings).
    
    Design:
    - Chunk documents into manageable pieces
    - Use sentence-transformers for embeddings (no API needed)
    - Retrieve top-k relevant chunks for queries
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
    
    def _get_model(self):
        """Lazy load embedding model."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.config.embedding_model)
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
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def add_document(self, text: str):
        """Add document to RAG system.
        
        Args:
            text: Document text (e.g., SEC filing)
        """
        chunks = self.chunk_text(text)
        self.documents.extend(chunks)
        
        # Generate embeddings
        model = self._get_model()
        new_embeddings = model.encode(chunks)
        
        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
    
    def query(self, question: str) -> str:
        """Query documents and return relevant context.
        
        Args:
            question: Query text
            
        Returns:
            Concatenated top-k relevant chunks
        """
        if not self.documents:
            return ""
        
        # Encode question
        model = self._get_model()
        query_embedding = model.encode([question])[0]
        
        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-self.config.top_k:][::-1]
        
        # Return concatenated chunks
        context_chunks = [self.documents[i] for i in top_indices]
        return "\n\n".join(context_chunks)
    
    def clear(self):
        """Clear all documents and embeddings."""
        self.documents = []
        self.embeddings = None