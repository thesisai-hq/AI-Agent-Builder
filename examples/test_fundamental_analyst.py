"""
Test Script for Advanced Fundamental Analyst
Run this to see the complete analysis in action
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent_builder.core.config import Config
from agent_builder.core.database import DatabasePool, Database
from agent_builder.agents.context import AgentContext
from agent_builder.agents.registry import get_registry

# Import the advanced fundamental analyst
from advanced_fundamental_analyst import (
    advanced_fundamental_analyst,
    generate_detailed_report,
    register_advanced_fundamental_analyst,
)


def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*80}")
    print(f" {text}")
    print(f"{'='*80}\n")


def print_section(text):
    """Print formatted section"""
    print(f"\n{'-'*80}")
    print(f" {text}")
    print(f"{'-'*80}\n")


def test_single_stock(ticker, db):
    """Test analysis on a single stock"""
    print_header(f"ANALYZING: {ticker}")

    context = AgentContext(ticker, db)

    try:
        # Run the advanced analysis
        signal, confidence, reasoning = advanced_fundamental_analyst(ticker, context)

        # Print results
        print_section("QUICK SUMMARY")
        print(f"📊 Signal: {signal.upper()}")
        print(f"🎯 Confidence: {confidence:.0%}")
        print(f"💡 Reasoning: {reasoning}\n")

        # Generate detailed report
        print_section("DETAILED REPORT")
        report = generate_detailed_report(ticker, context)
        print(report)

        return {
            "ticker": ticker,
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning,
            "success": True,
        }

    except Exception as e:
        print(f"❌ Error analyzing {ticker}: {e}")
        import traceback

        traceback.print_exc()
        return {"ticker": ticker, "success": False, "error": str(e)}


def test_multiple_stocks(tickers, db):
    """Test analysis on multiple stocks"""
    print_header("MULTI-STOCK COMPARISON")

    results = []

    for ticker in tickers:
        context = AgentContext(ticker, db)

        try:
            signal, confidence, reasoning = advanced_fundamental_analyst(
                ticker, context
            )
            results.append(
                {
                    "ticker": ticker,
                    "signal": signal,
                    "confidence": confidence,
                    "reasoning": reasoning[:100] + "...",
                }
            )
        except Exception as e:
            print(f"❌ {ticker}: {e}")
            results.append(
                {
                    "ticker": ticker,
                    "signal": "error",
                    "confidence": 0,
                    "reasoning": str(e),
                }
            )

    # Print comparison table
    print_section("COMPARISON TABLE")
    print(f"{'Ticker':<8} {'Signal':<10} {'Confidence':<12} {'Summary'}")
    print("-" * 80)

    for r in results:
        print(
            f"{r['ticker']:<8} {r['signal']:<10} {r['confidence']:<12.0%} {r['reasoning'][:50]}"
        )

    # Print recommendations
    print_section("RECOMMENDATIONS")

    bullish = [r for r in results if r["signal"] == "bullish"]
    bearish = [r for r in results if r["signal"] == "bearish"]
    neutral = [r for r in results if r["signal"] == "neutral"]

    if bullish:
        print("✅ BULLISH (Consider buying):")
        for r in sorted(bullish, key=lambda x: x["confidence"], reverse=True):
            print(f"   • {r['ticker']}: {r['confidence']:.0%} confidence")

    if bearish:
        print("\n❌ BEARISH (Consider avoiding):")
        for r in sorted(bearish, key=lambda x: x["confidence"], reverse=True):
            print(f"   • {r['ticker']}: {r['confidence']:.0%} confidence")

    if neutral:
        print("\n⚠️  NEUTRAL (Wait and see):")
        for r in neutral:
            print(f"   • {r['ticker']}: {r['confidence']:.0%} confidence")

    return results


def test_via_api(ticker, db):
    """Test using the agent registry (as API would)"""
    print_header(f"TESTING VIA REGISTRY: {ticker}")

    # Register the agent
    register_advanced_fundamental_analyst()

    # Get from registry
    registry = get_registry()
    agent = registry.get("advanced_fundamental_analyst")

    if not agent:
        print("❌ Agent not found in registry")
        return

    # Run analysis
    context = AgentContext(ticker, db)
    signal = agent.analyze(ticker, context)

    print_section("REGISTRY RESULT")
    print(f"Agent: {signal.agent_name}")
    print(f"Signal: {signal.signal_type}")
    print(f"Confidence: {signal.confidence:.0%}")
    print(f"Reasoning: {signal.reasoning}")
    print(f"Timestamp: {signal.timestamp}")


def performance_test(ticker, db, iterations=3):
    """Test performance"""
    print_header(f"PERFORMANCE TEST: {ticker} ({iterations} iterations)")

    import time

    context = AgentContext(ticker, db)
    times = []

    for i in range(iterations):
        start = time.time()

        try:
            signal, confidence, reasoning = advanced_fundamental_analyst(
                ticker, context
            )
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  Iteration {i+1}: {elapsed:.2f}s - {signal} ({confidence:.0%})")
        except Exception as e:
            print(f"  Iteration {i+1}: Failed - {e}")

    if times:
        print(f"\n📊 Performance Summary:")
        print(f"  Average: {sum(times)/len(times):.2f}s")
        print(f"  Min: {min(times):.2f}s")
        print(f"  Max: {max(times):.2f}s")


def main():
    """Main test runner"""
    print("\n" + "=" * 80)
    print(" ADVANCED FUNDAMENTAL ANALYST - TEST SUITE")
    print(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)

    # Setup
    print("\n⚙️  Setting up...")
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)

    # Available test tickers
    available_tickers = ["AAPL", "TSLA", "MSFT", "GOOGL", "NVDA"]

    print(f"✅ Connected to database")
    print(f"✅ Available tickers: {', '.join(available_tickers)}\n")

    # Run tests based on command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "--single":
            # Test single stock
            ticker = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
            test_single_stock(ticker, db)

        elif mode == "--compare":
            # Compare multiple stocks
            tickers = sys.argv[2:] if len(sys.argv) > 2 else available_tickers[:3]
            test_multiple_stocks(tickers, db)

        elif mode == "--registry":
            # Test via registry
            ticker = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
            test_via_api(ticker, db)

        elif mode == "--performance":
            # Performance test
            ticker = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
            iterations = int(sys.argv[3]) if len(sys.argv) > 3 else 3
            performance_test(ticker, db, iterations)

        elif mode == "--all":
            # Run all tests
            print_header("RUNNING ALL TESTS")

            # Single stock
            test_single_stock("AAPL", db)

            # Multiple stocks
            test_multiple_stocks(["AAPL", "TSLA", "MSFT"], db)

            # Via registry
            test_via_api("AAPL", db)

            # Performance
            performance_test("AAPL", db, 2)

        else:
            print(f"❌ Unknown mode: {mode}")
            print_usage()

    else:
        # Default: single stock analysis
        print("ℹ️  Running default test (single stock analysis)")
        print("   Use --help for more options\n")
        test_single_stock("AAPL", db)

    # Cleanup
    pool.close()

    print("\n" + "=" * 80)
    print(" TEST SUITE COMPLETE")
    print("=" * 80 + "\n")


def print_usage():
    """Print usage instructions"""
    print("\n" + "=" * 80)
    print(" USAGE")
    print("=" * 80)
    print(
        """
Available modes:

  python test_fundamental_analyst.py --single [TICKER]
      Analyze a single stock in detail
      Example: python test_fundamental_analyst.py --single AAPL

  python test_fundamental_analyst.py --compare [TICKER1] [TICKER2] ...
      Compare multiple stocks
      Example: python test_fundamental_analyst.py --compare AAPL TSLA MSFT

  python test_fundamental_analyst.py --registry [TICKER]
      Test via agent registry (simulates API usage)
      Example: python test_fundamental_analyst.py --registry AAPL

  python test_fundamental_analyst.py --performance [TICKER] [ITERATIONS]
      Run performance test
      Example: python test_fundamental_analyst.py --performance AAPL 5

  python test_fundamental_analyst.py --all
      Run all test modes

  python test_fundamental_analyst.py --help
      Show this help message

Available tickers: AAPL, TSLA, MSFT, GOOGL, NVDA
"""
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_usage()
    else:
        main()
