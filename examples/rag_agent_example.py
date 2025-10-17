"""
RAG-Powered Agent Examples
Demonstrates how to use RAG system with LLM agents
"""

from agent_builder import agent, get_registry
from agent_builder.llm import get_llm_provider, PromptTemplates
from agent_builder.rag import DataRetriever, ContextBuilder


# ============================================================================
# RAG-POWERED AGENTS
# ============================================================================


@agent("RAG Comprehensive Agent", "Uses RAG with full context")
def rag_comprehensive_agent(ticker, context):
    """
    RAG-powered comprehensive analysis

    This agent retrieves ALL relevant data and provides it to the LLM
    for comprehensive analysis.
    """
    # Get LLM
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    # Build RAG context
    retriever = DataRetriever(context.db)
    builder = ContextBuilder(retriever)

    rag_context = builder.build_focused_context(
        ticker, focus="comprehensive", max_length=2000
    )

    # Create prompt with context
    prompt = f"""Based on the following comprehensive data, provide a trading signal for {ticker}.

{rag_context}

Provide your analysis in this format:
SIGNAL: [BULLISH/BEARISH/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASONING: [Your analysis in 2-3 sentences]"""

    # Get LLM response
    response = llm.generate(
        prompt=prompt,
        system_prompt=PromptTemplates.ANALYST_SYSTEM,
        temperature=0.3,
        max_tokens=500,
    )

    # Parse response
    parsed = PromptTemplates.parse_llm_response(response.content)

    return (parsed["signal"], parsed["confidence"], parsed["reasoning"])


@agent("RAG SEC Filing Agent", "Analyzes SEC filings with RAG")
def rag_sec_filing_agent(ticker, context):
    """
    RAG-powered SEC filing analysis

    Retrieves and analyzes SEC filing text using LLM
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    # Get SEC filing context
    retriever = DataRetriever(context.db)
    sec_context = retriever.get_sec_filing_context(ticker)

    if not sec_context or "not available" in sec_context.lower():
        return "neutral", 0.3, "No SEC filing available"

    # Create prompt
    prompt = f"""Analyze this SEC filing for {ticker} and identify:
1. Management's tone (optimistic/cautious/concerned)
2. Key risks mentioned
3. Financial outlook
4. Overall sentiment

{sec_context}

Provide SIGNAL, CONFIDENCE, and REASONING."""

    # Get LLM response
    response = llm.generate(
        prompt=prompt,
        system_prompt="You are an SEC filing expert who reads between the lines.",
        temperature=0.4,
        max_tokens=500,
    )

    # Parse
    parsed = PromptTemplates.parse_llm_response(response.content)

    return (parsed["signal"], parsed["confidence"], parsed["reasoning"])


@agent("RAG News Synthesis Agent", "Synthesizes multiple news sources")
def rag_news_synthesis_agent(ticker, context):
    """
    RAG-powered news synthesis

    Retrieves multiple news articles and synthesizes insights
    """
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    # Get news context
    retriever = DataRetriever(context.db)
    news_context = retriever.get_news_context(ticker, limit=10)

    if not news_context or "No recent news" in news_context:
        return "neutral", 0.3, "No news available"

    # Create prompt
    prompt = f"""Analyze these news articles for {ticker} and synthesize:
1. Overall sentiment trend
2. Key themes or concerns
3. Market reaction indicators
4. Trading implications

{news_context}

Provide SIGNAL, CONFIDENCE, and REASONING."""

    # Get LLM response
    response = llm.generate(
        prompt=prompt,
        system_prompt=PromptTemplates.SENTIMENT_ANALYST,
        temperature=0.5,
        max_tokens=500,
    )

    # Parse
    parsed = PromptTemplates.parse_llm_response(response.content)

    return (parsed["signal"], parsed["confidence"], parsed["reasoning"])


# ============================================================================
# REGISTRATION
# ============================================================================


def register_rag_agents():
    """Register RAG-powered agents"""
    registry = get_registry()

    print("\\n" + "=" * 70)
    print("REGISTERING RAG AGENTS")
    print("=" * 70)

    registry.register(
        rag_comprehensive_agent.agent, weight=1.5, tags=["rag", "llm", "comprehensive"]
    )
    print("✅ Registered: RAG Comprehensive Agent")

    registry.register(
        rag_sec_filing_agent.agent, weight=1.3, tags=["rag", "llm", "sec"]
    )
    print("✅ Registered: RAG SEC Filing Agent")

    registry.register(
        rag_news_synthesis_agent.agent, weight=1.2, tags=["rag", "llm", "sentiment"]
    )
    print("✅ Registered: RAG News Synthesis Agent")

    print("=" * 70 + "\\n")


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    """Test RAG agents"""
    from agent_builder.core.config import Config
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.context import AgentContext

    print("\\n🧪 TESTING RAG AGENTS\\n")

    # Check Ollama
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        print("❌ Ollama is not running!")
        print("   Start: ollama serve")
        print("   Pull: ollama pull llama3.2")
        exit(1)

    print("✅ Ollama available\\n")

    # Setup
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)

    # Test ticker
    ticker = "AAPL"
    context = AgentContext(ticker, db)

    # Test RAG context building
    print("Testing RAG Context Builder:\\n")
    retriever = DataRetriever(db)
    builder = ContextBuilder(retriever)

    rag_context = builder.build_focused_context(ticker, "comprehensive")
    print(f"Context length: {len(rag_context)} characters")
    print(f"\\nFirst 500 chars:\\n{rag_context[:500]}...\\n")

    # Test agents
    print("\\nTesting RAG Agents:\\n")

    agents = [
        ("RAG Comprehensive Agent", rag_comprehensive_agent),
        ("RAG SEC Filing Agent", rag_sec_filing_agent),
        ("RAG News Synthesis Agent", rag_news_synthesis_agent),
    ]

    for name, agent_func in agents:
        print(f"\\n{name}:")
        print("-" * 50)
        try:
            signal = agent_func.agent.analyze(ticker, context)
            print(f"Signal: {signal.signal_type}")
            print(f"Confidence: {signal.confidence:.0%}")
            print(f"Reasoning: {signal.reasoning}")
        except Exception as e:
            print(f"❌ ERROR: {e}")

    pool.close()
    print("\\n✅ Test complete\\n")
