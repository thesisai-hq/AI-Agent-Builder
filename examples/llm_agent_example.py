"""
LLM-Powered Agent Example
Demonstrates how to use LLM framework in agents
"""

from agent_builder import agent, get_registry
from agent_builder.llm import get_llm_provider, PromptTemplates


# ============================================================================
# LLM-POWERED AGENTS
# ============================================================================


@agent("LLM Fundamental Agent", "Uses LLM to analyze fundamentals")
def llm_fundamental_agent(ticker, context):
    """
    LLM-powered fundamental analysis

    This agent uses an LLM to analyze fundamental metrics
    """
    # Get LLM provider (Ollama by default)
    llm = get_llm_provider("ollama", model="llama3.2")

    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    # Get fundamental data
    fundamentals = context.get_fundamentals()

    if not fundamentals:
        return "neutral", 0.3, "No fundamental data"

    # Create prompt
    prompt = PromptTemplates.fundamental_analysis(ticker, fundamentals)
    system = PromptTemplates.FUNDAMENTAL_ANALYST

    # Get LLM response
    response = llm.generate(
        prompt=prompt,
        system_prompt=system,
        temperature=0.3,  # Lower = more deterministic
        max_tokens=500,
    )

    # Parse response
    parsed = PromptTemplates.parse_llm_response(response.content)

    return (parsed["signal"], parsed["confidence"], parsed["reasoning"])


@agent("LLM News Agent", "Uses LLM to analyze news sentiment")
def llm_news_agent(ticker, context):
    """
    LLM-powered news sentiment analysis
    """
    llm = get_llm_provider("ollama")

    if not llm or not llm.is_available():
        return "neutral", 0.3, "LLM not available"

    # Get news
    news = context.get_news(limit=5)

    if not news:
        return "neutral", 0.3, "No news available"

    # Create prompt
    prompt = PromptTemplates.news_analysis(ticker, news)
    system = PromptTemplates.SENTIMENT_ANALYST

    # Get LLM response
    response = llm.generate(
        prompt=prompt, system_prompt=system, temperature=0.5, max_tokens=500
    )

    # Parse response
    parsed = PromptTemplates.parse_llm_response(response.content)

    return (parsed["signal"], parsed["confidence"], parsed["reasoning"])


# ============================================================================
# REGISTRATION
# ============================================================================


def register_llm_agents():
    """Register LLM-powered agents"""
    registry = get_registry()

    print("\\n" + "=" * 70)
    print("REGISTERING LLM AGENTS")
    print("=" * 70)

    registry.register(
        llm_fundamental_agent.agent, weight=1.2, tags=["llm", "fundamental"]
    )
    print("✅ Registered: LLM Fundamental Agent")

    registry.register(llm_news_agent.agent, weight=1.0, tags=["llm", "sentiment"])
    print("✅ Registered: LLM News Agent")

    print("=" * 70 + "\\n")


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    """Test LLM agents directly"""
    from agent_builder.core.config import Config
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.context import AgentContext

    print("\\n🧪 TESTING LLM AGENTS\\n")

    # Check Ollama
    llm = get_llm_provider("ollama")
    if not llm or not llm.is_available():
        print("❌ Ollama is not running!")
        print("   Start it with: ollama serve")
        print("   Pull model: ollama pull llama3.2")
        exit(1)

    print("✅ Ollama is available\\n")

    # Setup database
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)

    # Test ticker
    ticker = "AAPL"
    context = AgentContext(ticker, db)

    # Test agents
    print(f"Testing LLM agents for {ticker}:\\n")

    agents = [
        ("LLM Fundamental Agent", llm_fundamental_agent),
        ("LLM News Agent", llm_news_agent),
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
