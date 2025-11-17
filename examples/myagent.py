"""Auto-generated LLM-powered agent: MyAgent



DEPENDENCIES:
This agent requires LLM dependencies. Install with:
  pip install 'ai-agent-framework[llm]'

Or install specific provider:
  pip install ollama

To check which providers are installed:
  python3 gui/check_llm_deps.py
"""

import asyncio

from agent_framework import (
    Agent,
    AgentConfig,
    Config,
    Database,
    LLMConfig,
    Signal,
    format_fundamentals,
    parse_llm_signal,
)


class MyAgent(Agent):
    """"""

    def __init__(self):
        """Initialize agent with LLM configuration."""
        config = AgentConfig(
            name="MyAgent",
            description="",
            llm=LLMConfig(
                provider="ollama",
                model="llama3.2",
                temperature=0.5,
                max_tokens=1000,
                system_prompt="""You are a financial analyst.""",
            ),
        )
        super().__init__(config)

    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using LLM with configured personality.

        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary

        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Format fundamentals for LLM
        fundamentals_text = format_fundamentals(data)

        # Build prompt
        prompt = f"""Analyze {ticker} with the following data:

{fundamentals_text}

Provide your investment recommendation.
Format: DIRECTION|CONFIDENCE|REASONING
Example: bullish|75|Strong growth with healthy margins"""

        try:
            # Query LLM
            response = self.llm.chat(prompt)
            return parse_llm_signal(response, f"Analysis of {ticker}")

        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            # LLM agents should NOT use rule-based fallback
            # That defeats the purpose of using AI
            return Signal(
                direction="neutral",
                confidence=0.2,
                reasoning=f"LLM service unavailable ({type(e).__name__}). Cannot provide AI-powered analysis without LLM. Error: {str(e)[:100]}",
            )


async def main():
    """Example usage of the LLM-powered agent."""
    print(f"{'-' * 60}")
    print("MyAgent - LLM-Powered Analysis")
    print(f"{'-' * 60}\n")

    # Connect to database
    db = Database(Config.get_database_url())
    await db.connect()

    try:
        # Create agent
        agent = MyAgent()

        # Analyze tickers
        for ticker in ["AAPL", "TSLA"]:
            data = await db.get_fundamentals(ticker)

            if not data:
                print(f"⚠️  No data for {ticker}")
                continue

            print(f"📊 Analyzing {ticker}...")
            signal = agent.analyze(ticker, data)

            print(f"{signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"{signal.reasoning}\n")

    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
