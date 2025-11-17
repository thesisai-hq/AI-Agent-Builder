"""Warren Buffett Quality Strategy

Focus on high-quality businesses with strong fundamentals.

Strategy:
- High ROE (> 15%): +2 points
- Strong margins (> 15%): +2 points
- Low debt (< 0.5): +1 point
- Consistent growth (> 10%): +1 point
- Financial stability (Current Ratio > 1.5): +1 point

Score >= 4: Bullish (high quality company)
Score <= 1: Bearish (low quality)

⚠️ DISCLAIMER: This is educational code demonstrating investment concepts.
Inspired by Warren Buffett's philosophy but NOT endorsed by him or Berkshire Hathaway.
Do NOT use for real trading. Not financial advice. See DISCLAIMER.md for full terms.
"""

import asyncio

from agent_framework import Agent, Config, Database, Signal


class BuffettQualityAgent(Agent):
    """Warren Buffett-style quality investing: High ROE, strong margins, low debt"""

    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using score-based quality metrics.

        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary

        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Initialize score and reasons
        score = 0
        reasons = []

        # Extract metrics
        roe = data.get("roe", 0)
        profit_margin = data.get("profit_margin", 0)
        debt_to_equity = data.get("debt_to_equity", 0)
        revenue_growth = data.get("revenue_growth", 0)
        current_ratio = data.get("current_ratio", 0)

        # Calculate score
        # ROE > 15% = +2 points
        if roe > 15:
            score += 2
            reasons.append(f"Roe {roe:.1f}% > 15 (+2 pts)")

        # Profit Margin > 15% = +2 points
        if profit_margin > 15:
            score += 2
            reasons.append(f"Profit Margin {profit_margin:.1f}% > 15 (+2 pts)")

        # Debt < 0.5 = +1 point
        if debt_to_equity < 0.5:
            score += 1
            reasons.append(f"Debt To Equity {debt_to_equity:.1f} < 0.5 (+1 pts)")

        # Growth > 10% = +1 point
        if revenue_growth > 10:
            score += 1
            reasons.append(f"Revenue Growth {revenue_growth:.1f}% > 10 (+1 pts)")

        # Current Ratio > 1.5 = +1 point
        if current_ratio > 1.5:
            score += 1
            reasons.append(f"Current Ratio {current_ratio:.1f} > 1.5 (+1 pts)")

        # Determine signal based on score
        if score >= 4:
            return Signal(
                direction="bullish",
                confidence=0.85,
                reasoning=f"Quality Score: {score} (bullish threshold: 4). " + "; ".join(reasons),
            )
        elif score <= 1:
            return Signal(
                direction="bearish",
                confidence=0.6,
                reasoning=f"Quality Score: {score} (bearish threshold: 1). " + "; ".join(reasons),
            )
        else:
            return Signal(
                direction="neutral",
                confidence=0.5,
                reasoning=f"Quality Score: {score} (between 1 and 4). " + "; ".join(reasons)
                if reasons
                else "Neutral score",
            )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print("BuffettQualityAgent - Score-Based Strategy")
    print(f"{'-' * 60}\n")

    db = Database(Config.get_database_url())
    await db.connect()

    try:
        agent = BuffettQualityAgent()

        for ticker in ["AAPL", "MSFT", "GOOGL"]:
            data = await db.get_fundamentals(ticker)

            if not data:
                print(f"⚠️  No data for {ticker}")
                continue

            signal = await agent.analyze(ticker, data)
            print(f"📊 {ticker}: {signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"   {signal.reasoning}\n")

    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
