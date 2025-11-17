"""Benjamin Graham Value Strategy

Classic value investing principles with margin of safety.

Strategy:
- Low PE (< 15): +2 points
- Low PB (< 1.5): +1 point
- Conservative debt (< 1.0): +1 point
- Strong liquidity (Current Ratio > 2.0): +1 point
- Dividend income (> 2%): +1 point

Score >= 3: Strong value candidate
Score <= 0: Avoid (overvalued or risky)
"""

import asyncio

from agent_framework import Agent, Config, Database, Signal


class GrahamValueAgent(Agent):
    """Benjamin Graham value investing: Low PE, low PB, margin of safety"""

    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using score-based strategy.

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
        pe_ratio = data.get("pe_ratio", 0)
        pb_ratio = data.get("pb_ratio", 0)
        debt_to_equity = data.get("debt_to_equity", 0)
        current_ratio = data.get("current_ratio", 0)
        dividend_yield = data.get("dividend_yield", 0)

        # Calculate score
        # PE < 15 = +2 points
        if pe_ratio < 15:
            score += 2
            reasons.append(f"Pe Ratio {pe_ratio:.1f} < 15 (+2 pts)")

        # PB < 1.5 = +1 point
        if pb_ratio < 1.5:
            score += 1
            reasons.append(f"Pb Ratio {pb_ratio:.1f} < 1.5 (+1 pts)")

        # Debt < 1.0 = +1 point
        if debt_to_equity < 1.0:
            score += 1
            reasons.append(f"Debt To Equity {debt_to_equity:.1f} < 1.0 (+1 pts)")

        # Current Ratio > 2.0 = +1 point
        if current_ratio > 2.0:
            score += 1
            reasons.append(f"Current Ratio {current_ratio:.1f} > 2.0 (+1 pts)")

        # Dividend > 2% = +1 point
        if dividend_yield > 2.0:
            score += 1
            reasons.append(f"Dividend Yield {dividend_yield:.1f}% > 2.0 (+1 pts)")

        # Determine signal based on score
        if score >= 3:
            return Signal(
                direction="bullish",
                confidence=0.8,
                reasoning=f"Value Score: {score} (bullish threshold: 3). " + "; ".join(reasons),
            )
        elif score <= 0:
            return Signal(
                direction="bearish",
                confidence=0.6,
                reasoning=f"Value Score: {score} (bearish threshold: 0). " + "; ".join(reasons)
                if reasons
                else "No value criteria met",
            )
        else:
            return Signal(
                direction="neutral",
                confidence=0.5,
                reasoning=f"Value Score: {score} (between 0 and 3). " + "; ".join(reasons)
                if reasons
                else "Neutral score",
            )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print("GrahamValueAgent - Score-Based Strategy")
    print(f"{'-' * 60}\n")

    db = Database(Config.get_database_url())
    await db.connect()

    try:
        agent = GrahamValueAgent()

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
