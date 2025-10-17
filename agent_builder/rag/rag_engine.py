"""RAG Engine - Orchestrates retrieval and generation"""

from typing import Optional, List, Dict
import logging

from agent_builder.rag.embeddings import get_embedding_model
from agent_builder.rag.vectorstores import get_vector_store
from agent_builder.rag.retriever import DataRetriever

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    RAG Engine - Flexible retrieval-augmented generation

    Allows agents to choose embedding model and vector store at runtime

    Usage:
        # Simple setup
        rag = RAGEngine(db, embedding="simple", vectorstore="memory")

        # Advanced setup
        rag = RAGEngine(
            db,
            embedding="sentence-transformers",
            embedding_model="all-MiniLM-L6-v2",
            vectorstore="chroma",
            collection_name="my_analysis"
        )

        # Use in agent
        context = rag.get_relevant_context("AAPL", query="earnings growth")
    """

    def __init__(
        self,
        db,
        embedding: str = "sentence-transformers",
        embedding_model: Optional[str] = None,
        vectorstore: str = "memory",
        **vectorstore_kwargs,
    ):
        """
        Initialize RAG engine

        Args:
            db: Database instance
            embedding: "simple", "sentence-transformers", "ollama"
            embedding_model: Model name (optional)
            vectorstore: "memory", "chroma", "faiss"
            **vectorstore_kwargs: Additional args for vector store
        """
        self.db = db
        self.retriever = DataRetriever(db)

        # Initialize embedding model
        logger.info(
            f"Initializing RAG with {embedding} embeddings and {vectorstore} store"
        )

        self.embedding_model = get_embedding_model(
            provider=embedding, model=embedding_model
        )

        # Initialize vector store
        if vectorstore == "faiss":
            vectorstore_kwargs["dimensions"] = self.embedding_model.dimensions

        self.vector_store = get_vector_store(
            store_type=vectorstore,
            embedding_model=self.embedding_model,
            **vectorstore_kwargs,
        )

        logger.info("✅ RAG engine initialized")

    def index_sec_filings(self, ticker: str):
        """
        Index SEC filings for semantic search

        This allows you to search through SEC filing text
        """
        # Get all filings
        filings = self.retriever.get_all_sec_filings(ticker)

        if not filings:
            logger.warning(f"No SEC filings to index for {ticker}")
            return

        # Prepare documents
        documents = []
        metadata = []
        ids = []

        for filing in filings:
            text = filing.get("filing_text", "")
            if text:
                documents.append(text)
                metadata.append(
                    {
                        "ticker": filing["ticker"],
                        "filing_type": filing["filing_type"],
                        "filing_date": str(filing["filing_date"]),
                    }
                )
                ids.append(
                    f"{filing['ticker']}_{filing['filing_type']}_{filing['filing_date']}"
                )

        if not documents:
            logger.warning(f"No filing text to index for {ticker}")
            return

        # Generate embeddings
        logger.info(f"Generating embeddings for {len(documents)} filings...")
        embeddings = self.embedding_model.embed_batch(documents)

        # Add to vector store
        self.vector_store.add_documents(
            documents=documents, embeddings=embeddings, metadata=metadata, ids=ids
        )

        logger.info(f"✅ Indexed {len(documents)} SEC filings for {ticker}")

    def search_sec_filings(
        self, query: str, ticker: Optional[str] = None, top_k: int = 3
    ) -> List[Dict]:
        """
        Semantic search through SEC filings

        Args:
            query: Search query (e.g., "revenue growth strategy")
            ticker: Filter by ticker (optional)
            top_k: Number of results

        Returns:
            List of relevant filing excerpts with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.embed_text(query)

        # Search
        filter_dict = {"ticker": ticker} if ticker else None
        results = self.vector_store.search(
            query_embedding=query_embedding, top_k=top_k, filter_dict=filter_dict
        )

        # Format results
        formatted = []
        for doc, meta, score in results:
            formatted.append(
                {
                    "text": doc[:500] + "..." if len(doc) > 500 else doc,
                    "full_text": doc,
                    "metadata": meta,
                    "similarity": score,
                }
            )

        return formatted

    def get_relevant_context(
        self, ticker: str, query: str, use_vector_search: bool = True
    ) -> str:
        """
        Get relevant context for a specific query

        Args:
            ticker: Stock ticker
            query: What you're looking for
            use_vector_search: Use semantic search on SEC filings

        Returns:
            Relevant context string
        """
        context_parts = []

        # Always include fundamentals
        fund = self.retriever.get_fundamental_context(ticker)
        if fund:
            context_parts.append(fund)

        # Use vector search for SEC filings if enabled
        if use_vector_search:
            relevant_filings = self.search_sec_filings(query, ticker, top_k=2)
            if relevant_filings:
                context_parts.append("\\nRelevant SEC Filing Excerpts:")
                for i, filing in enumerate(relevant_filings, 1):
                    context_parts.append(f"\\n[Excerpt {i}] {filing['text']}")

        return "\\n\\n".join(context_parts)
