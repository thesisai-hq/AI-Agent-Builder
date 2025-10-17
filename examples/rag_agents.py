"""
RAG-Powered Agents with Flexible Configuration
Demonstrates different embedding/vector store combinations
"""

from agent_builder import agent, get_registry
from agent_builder.llm import get_llm_provider, PromptTemplates
from agent_builder.rag import RAGEngine


# ============================================================================
# AGENT 1: Simple RAG (No Dependencies)
# ============================================================================


@agent("Simple RAG Agent", "Uses hash embeddings + in-memory store")
def simple_rag_agent(ticker, context):
    """
    Simplest RAG setup - zero external dependencies
    Good for: Quick testing, minimal setup
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    # Create RAG with simple embeddings + in-memory store
    rag = RAGEngine(db=context.db, embedding="simple", vectorstore="memory")

    # Index SEC filings
    rag.index_sec_filings(ticker)

    # Get relevant context
    rag_context = rag.get_relevant_context(
        ticker=ticker, query="financial performance and outlook"
    )

    # Generate analysis
    prompt = f"""{rag_context}

Analyze {ticker} and provide trading signal.

Provide: SIGNAL, CONFIDENCE, REASONING"""

    response = llm.generate(prompt, temperature=0.3, max_tokens=300)
    parsed = PromptTemplates.parse_llm_response(response.content)

    return parsed["signal"], parsed["confidence"], parsed["reasoning"]


# ============================================================================
# AGENT 2: Sentence Transformers RAG (Recommended)
# ============================================================================


@agent("ST-Chroma RAG Agent", "Uses sentence-transformers + ChromaDB")
def st_chroma_rag_agent(ticker, context):
    """
    Production-quality RAG with semantic search
    Good for: Real analysis, persistent storage

    Requires: pip install sentence-transformers chromadb
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    try:
        # Create RAG with sentence transformers + ChromaDB
        rag = RAGEngine(
            db=context.db,
            embedding="sentence-transformers",
            embedding_model="all-MiniLM-L6-v2",
            vectorstore="chroma",
            collection_name="stock_sec_filings",
            persist_directory="./chroma_db",
        )

        # Index SEC filings (only first time, then cached)
        rag.index_sec_filings(ticker)

        # Search for relevant content
        rag_context = rag.get_relevant_context(
            ticker=ticker, query="revenue growth, profitability, and risk factors"
        )

        # Generate analysis
        prompt = f"""{rag_context}

Based on the above data, analyze {ticker} focusing on:
1. Growth potential
2. Financial health
3. Key risks

Provide: SIGNAL, CONFIDENCE, REASONING"""

        response = llm.generate(
            prompt=prompt,
            system_prompt=PromptTemplates.ANALYST_SYSTEM,
            temperature=0.3,
            max_tokens=400,
        )

        parsed = PromptTemplates.parse_llm_response(response.content)
        return parsed["signal"], parsed["confidence"], parsed["reasoning"]

    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return "neutral", 0.3, "RAG dependencies not installed"


# ============================================================================
# AGENT 3: FAISS RAG (High Performance)
# ============================================================================


@agent("FAISS RAG Agent", "Uses sentence-transformers + FAISS")
def faiss_rag_agent(ticker, context):
    """
    High-performance RAG with FAISS
    Good for: Large datasets, fast search

    Requires: pip install sentence-transformers faiss-cpu numpy
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    try:
        # Create RAG with sentence transformers + FAISS
        rag = RAGEngine(
            db=context.db,
            embedding="sentence-transformers",
            embedding_model="all-MiniLM-L6-v2",
            vectorstore="faiss",
            dimensions=384,
        )

        # Index SEC filings
        rag.index_sec_filings(ticker)

        # Get relevant context
        rag_context = rag.get_relevant_context(
            ticker=ticker, query="management outlook and competitive position"
        )

        # Generate
        prompt = f"""{rag_context}

Analyze {ticker} based on this data.

Provide: SIGNAL, CONFIDENCE, REASONING"""

        response = llm.generate(prompt, temperature=0.3, max_tokens=300)
        parsed = PromptTemplates.parse_llm_response(response.content)

        return parsed["signal"], parsed["confidence"], parsed["reasoning"]

    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return "neutral", 0.3, "RAG dependencies not installed"


# ============================================================================
# AGENT 4: Ollama Embeddings RAG (All Local)
# ============================================================================


@agent("Ollama RAG Agent", "Uses Ollama embeddings + ChromaDB")
def ollama_rag_agent(ticker, context):
    """
    Fully local RAG - no external APIs
    Good for: Privacy, offline use

    Requires:
        - pip install chromadb
        - ollama pull nomic-embed-text
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    try:
        # Create RAG with Ollama embeddings + ChromaDB
        rag = RAGEngine(
            db=context.db,
            embedding="ollama",
            embedding_model="nomic-embed-text",
            vectorstore="chroma",
            collection_name="ollama_sec_filings",
        )

        # Index and search
        rag.index_sec_filings(ticker)
        rag_context = rag.get_relevant_context(ticker, query="financial outlook")

        # Generate
        prompt = f"""{rag_context}

Analyze {ticker}.

Provide: SIGNAL, CONFIDENCE, REASONING"""

        response = llm.generate(prompt, temperature=0.3, max_tokens=300)
        parsed = PromptTemplates.parse_llm_response(response.content)

        return parsed["signal"], parsed["confidence"], parsed["reasoning"]

    except Exception as e:
        logger.error(f"Ollama RAG error: {e}")
        return "neutral", 0.3, str(e)


# ============================================================================
# REGISTRATION
# ============================================================================


def register_rag_agents():
    """
    Register RAG agents

    Choose which agents to enable based on available dependencies
    """
    registry = get_registry()

    print("\\n" + "=" * 70)
    print("REGISTERING RAG AGENTS")
    print("=" * 70)

    # Always register simple (no dependencies)
    registry.register(simple_rag_agent.agent, weight=1.0, tags=["rag", "simple"])
    print("✅ Simple RAG Agent (no dependencies)")

    # Try to register sentence-transformers agents
    try:
        import sentence_transformers

        registry.register(
            st_chroma_rag_agent.agent,
            weight=1.5,
            tags=["rag", "semantic", "persistent"],
        )
        print("✅ ST-Chroma RAG Agent (sentence-transformers + ChromaDB)")

        try:
            import faiss

            registry.register(
                faiss_rag_agent.agent, weight=1.4, tags=["rag", "semantic", "fast"]
            )
            print("✅ FAISS RAG Agent (sentence-transformers + FAISS)")
        except ImportError:
            print("⚠️  FAISS not available (pip install faiss-cpu)")

    except ImportError:
        print("⚠️  sentence-transformers not available")
        print("   Install: pip install sentence-transformers chromadb")

    # Try to register Ollama embedding agent
    try:
        from agent_builder.rag.embeddings import OllamaEmbedding

        test = OllamaEmbedding()  # Test if Ollama is available

        registry.register(
            ollama_rag_agent.agent, weight=1.3, tags=["rag", "local", "ollama"]
        )
        print("✅ Ollama RAG Agent (Ollama embeddings + ChromaDB)")

    except Exception as e:
        print(f"⚠️  Ollama embeddings not available: {e}")
        print("   Pull: ollama pull nomic-embed-text")

    stats = registry.stats()
    print(f"\\n📊 Total RAG agents: {stats['total']}")
    print("=" * 70 + "\\n")


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    """Test different RAG configurations"""
    from agent_builder.core.config import Config
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.context import AgentContext

    print("\\n" + "=" * 70)
    print("TESTING RAG CONFIGURATIONS")
    print("=" * 70)

    # Setup
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)
    ticker = "AAPL"

    # ========================================================================
    # TEST 1: Simple RAG (No dependencies)
    # ========================================================================
    print("\\n1️⃣  Testing Simple RAG (hash + memory)...")
    try:
        rag_simple = RAGEngine(db=db, embedding="simple", vectorstore="memory")
        rag_simple.index_sec_filings(ticker)
        results = rag_simple.search_sec_filings("revenue growth", ticker=ticker)
        print(f"   ✅ Found {len(results)} results")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # ========================================================================
    # TEST 2: Sentence Transformers + ChromaDB
    # ========================================================================
    print("\\n2️⃣  Testing Sentence Transformers + ChromaDB...")
    try:
        rag_st = RAGEngine(
            db=db,
            embedding="sentence-transformers",
            embedding_model="all-MiniLM-L6-v2",
            vectorstore="chroma",
            collection_name="test_collection",
            persist_directory="./test_chroma",
        )
        rag_st.index_sec_filings(ticker)
        results = rag_st.search_sec_filings("earnings performance", ticker=ticker)
        print(f"   ✅ Found {len(results)} results")
        if results:
            print(f"   Top result similarity: {results[0]['similarity']:.3f}")
    except ImportError:
        print("   ⚠️  sentence-transformers not installed")
        print("      pip install sentence-transformers chromadb")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # ========================================================================
    # TEST 3: Sentence Transformers + FAISS
    # ========================================================================
    print("\\n3️⃣  Testing Sentence Transformers + FAISS...")
    try:
        rag_faiss = RAGEngine(
            db=db, embedding="sentence-transformers", vectorstore="faiss"
        )
        rag_faiss.index_sec_filings(ticker)
        results = rag_faiss.search_sec_filings("risk factors", ticker=ticker)
        print(f"   ✅ Found {len(results)} results")
    except ImportError as e:
        print(f"   ⚠️  Missing: {e}")
        print("      pip install faiss-cpu numpy")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # ========================================================================
    # TEST 4: Ollama Embeddings + ChromaDB
    # ========================================================================
    print("\\n4️⃣  Testing Ollama Embeddings + ChromaDB...")
    try:
        rag_ollama = RAGEngine(
            db=db,
            embedding="ollama",
            embedding_model="nomic-embed-text",
            vectorstore="chroma",
            collection_name="ollama_collection",
        )
        rag_ollama.index_sec_filings(ticker)
        results = rag_ollama.search_sec_filings("competitive advantages", ticker=ticker)
        print(f"   ✅ Found {len(results)} results")
    except Exception as e:
        print(f"   ⚠️  {e}")
        print("      Pull: ollama pull nomic-embed-text")

    pool.close()

    print("\\n" + "=" * 70)
    print("✅ RAG TESTING COMPLETE")
    print("=" * 70)
    print("\\nRecommended setup:")
    print("  pip install sentence-transformers chromadb")
    print("\\n")
