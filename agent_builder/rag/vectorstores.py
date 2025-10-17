"""Vector Store Implementations - All Free Options"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BaseVectorStore(ABC):
    """Base class for all vector stores"""

    @abstractmethod
    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadata: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
    ):
        """Add documents with embeddings"""
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict] = None,
    ) -> List[Tuple[str, Dict, float]]:
        """Search for similar documents"""
        pass

    @abstractmethod
    def clear(self):
        """Clear all documents"""
        pass


# ============================================================================
# OPTION 1: In-Memory (No Dependencies)
# ============================================================================


class InMemoryVectorStore(BaseVectorStore):
    """
    In-memory vector store - No external dependencies

    Pros:
    - ✅ Zero setup
    - ✅ Fast for small datasets
    - ✅ No dependencies

    Cons:
    - ⚠️ Lost on restart
    - ⚠️ Slow for >10K documents
    - ⚠️ No persistence

    Use for: Quick tests, temporary storage, small datasets
    """

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.documents = []
        self.embeddings = []
        self.metadata = []
        self.ids = []
        logger.info("Initialized InMemoryVectorStore")

    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadata: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
    ):
        if metadata is None:
            metadata = [{} for _ in documents]
        if ids is None:
            ids = [
                f"doc_{i}"
                for i in range(
                    len(self.documents), len(self.documents) + len(documents)
                )
            ]

        self.documents.extend(documents)
        self.embeddings.extend(embeddings)
        self.metadata.extend(metadata)
        self.ids.extend(ids)

        logger.info(f"Added {len(documents)} documents (total: {len(self.documents)})")

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict] = None,
    ) -> List[Tuple[str, Dict, float]]:
        if not self.embeddings:
            return []

        # Calculate similarities
        similarities = []
        for i, emb in enumerate(self.embeddings):
            # Apply filter if provided
            if filter_dict:
                match = all(
                    self.metadata[i].get(k) == v for k, v in filter_dict.items()
                )
                if not match:
                    continue

            sim = self.embedding_model.cosine_similarity(query_embedding, emb)
            similarities.append((i, sim))

        # Sort and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in similarities[:top_k]:
            results.append((self.documents[idx], self.metadata[idx], score))

        return results

    def clear(self):
        self.documents = []
        self.embeddings = []
        self.metadata = []
        self.ids = []
        logger.info("Vector store cleared")


# ============================================================================
# OPTION 2: ChromaDB (Persistent, Easy to Use)
# ============================================================================


class ChromaDBVectorStore(BaseVectorStore):
    """
    ChromaDB vector store - Persistent storage

    Pros:
    - ✅ Free and open source
    - ✅ Persistent (survives restarts)
    - ✅ Built-in embedding support
    - ✅ Easy to use
    - ✅ Good for <1M documents

    Cons:
    - ⚠️ Requires chromadb package
    - ⚠️ Not optimized for massive scale

    Install: pip install chromadb
    """

    def __init__(
        self,
        collection_name: str = "stock_analysis",
        persist_directory: str = "./chroma_db",
        embedding_model=None,
    ):
        try:
            import chromadb

            self.embedding_model = embedding_model
            self.client = chromadb.PersistentClient(path=persist_directory)

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Stock analysis documents"},
            )

            logger.info(f"✅ ChromaDB initialized: {collection_name}")
            logger.info(f"   Existing documents: {self.collection.count()}")

        except ImportError:
            logger.error("chromadb not installed")
            logger.error("Install: pip install chromadb")
            raise

    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadata: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
    ):
        if metadata is None:
            metadata = [{} for _ in documents]
        if ids is None:
            import uuid

            ids = [str(uuid.uuid4()) for _ in documents]

        self.collection.add(
            documents=documents, embeddings=embeddings, metadatas=metadata, ids=ids
        )

        logger.info(f"Added {len(documents)} documents to ChromaDB")

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict] = None,
    ) -> List[Tuple[str, Dict, float]]:

        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k, where=filter_dict
        )

        # Format results
        output = []
        if results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                output.append(
                    (
                        results["documents"][0][i],
                        results["metadatas"][0][i],
                        results["distances"][0][i],
                    )
                )

        return output

    def clear(self):
        """Clear collection"""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(self.collection.name)
        logger.info("ChromaDB collection cleared")


# ============================================================================
# OPTION 3: FAISS (High Performance)
# ============================================================================


class FAISSVectorStore(BaseVectorStore):
    """
    FAISS vector store - High performance

    Pros:
    - ✅ Very fast (Meta/Facebook built)
    - ✅ Free and open source
    - ✅ Handles millions of vectors
    - ✅ GPU support available

    Cons:
    - ⚠️ Requires numpy + faiss
    - ⚠️ No built-in persistence (need to save/load manually)
    - ⚠️ More complex API

    Install: pip install faiss-cpu numpy
    """

    def __init__(self, embedding_model, dimensions: int):
        try:
            import faiss
            import numpy as np

            self.embedding_model = embedding_model
            self.dimensions = dimensions

            # Create FAISS index (Flat L2 distance)
            self.index = faiss.IndexFlatL2(dimensions)

            # Storage for metadata
            self.documents = []
            self.metadata = []
            self.ids = []

            logger.info(f"✅ FAISS initialized ({dimensions} dims)")

        except ImportError:
            logger.error("faiss-cpu not installed")
            logger.error("Install: pip install faiss-cpu numpy")
            raise

    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadata: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None,
    ):
        import numpy as np

        if metadata is None:
            metadata = [{} for _ in documents]
        if ids is None:
            ids = [
                f"doc_{i}"
                for i in range(
                    len(self.documents), len(self.documents) + len(documents)
                )
            ]

        # Convert to numpy array
        vectors = np.array(embeddings).astype("float32")

        # Add to FAISS index
        self.index.add(vectors)

        # Store metadata
        self.documents.extend(documents)
        self.metadata.extend(metadata)
        self.ids.extend(ids)

        logger.info(
            f"Added {len(documents)} documents to FAISS (total: {self.index.ntotal})"
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict] = None,
    ) -> List[Tuple[str, Dict, float]]:
        import numpy as np

        if self.index.ntotal == 0:
            return []

        # Convert query to numpy
        query_vector = np.array([query_embedding]).astype("float32")

        # Search
        distances, indices = self.index.search(query_vector, top_k)

        # Format results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                # Apply filter if provided
                if filter_dict:
                    match = all(
                        self.metadata[idx].get(k) == v for k, v in filter_dict.items()
                    )
                    if not match:
                        continue

                # Convert distance to similarity (lower distance = higher similarity)
                similarity = 1.0 / (1.0 + distances[0][i])

                results.append((self.documents[idx], self.metadata[idx], similarity))

        return results

    def clear(self):
        import faiss

        self.index = faiss.IndexFlatL2(self.dimensions)
        self.documents = []
        self.metadata = []
        self.ids = []
        logger.info("FAISS index cleared")

    def save(self, filepath: str):
        """Save FAISS index to disk"""
        import faiss

        faiss.write_index(self.index, filepath)
        logger.info(f"Saved FAISS index to {filepath}")

    def load(self, filepath: str):
        """Load FAISS index from disk"""
        import faiss

        self.index = faiss.read_index(filepath)
        logger.info(f"Loaded FAISS index from {filepath}")


# ============================================================================
# FACTORY FUNCTION
# ============================================================================


def get_vector_store(
    store_type: str = "memory", embedding_model=None, **kwargs
) -> BaseVectorStore:
    """
    Factory to get vector store

    Args:
        store_type: "memory", "chroma", "faiss"
        embedding_model: Embedding model instance (required for some stores)
        **kwargs: Store-specific arguments

    Returns:
        Vector store instance

    Usage:
        # In-memory (simple)
        store = get_vector_store("memory", embedding_model=emb)

        # ChromaDB (persistent)
        store = get_vector_store("chroma", collection_name="my_collection")

        # FAISS (fast)
        store = get_vector_store("faiss", embedding_model=emb, dimensions=384)
    """
    store_type = store_type.lower()

    if store_type == "memory":
        if not embedding_model:
            raise ValueError("embedding_model required for InMemoryVectorStore")
        return InMemoryVectorStore(embedding_model)

    elif store_type == "chroma" or store_type == "chromadb":
        collection_name = kwargs.get("collection_name", "stock_analysis")
        persist_directory = kwargs.get("persist_directory", "./chroma_db")
        return ChromaDBVectorStore(
            collection_name=collection_name,
            persist_directory=persist_directory,
            embedding_model=embedding_model,
        )

    elif store_type == "faiss":
        if not embedding_model:
            raise ValueError("embedding_model required for FAISSVectorStore")
        dimensions = kwargs.get("dimensions", embedding_model.dimensions)
        return FAISSVectorStore(embedding_model, dimensions)

    else:
        logger.warning(f"Unknown store type {store_type}, using memory")
        return InMemoryVectorStore(embedding_model)
