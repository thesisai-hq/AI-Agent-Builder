"""
Test Script for Advanced Macro Analyst
Comprehensive testing of macroeconomic analysis capabilities
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

# Import the advanced macro analyst
from advanced_macro_analyst import (
    advanced_macro_analyst,
    generate_macro_report,
    register_advanced_macro_analyst,
    analyze_economic_indicators,
    detect_market_regime,
    analyze_sector_impact,
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


def test_economic_indicators(context):
    """Test Stage 1: Economic indicator analysis"""
    print_header("STAGE 1: ECONOMIC INDICATORS TEST")

    result = analyze_economic_indicators(context)

    print("📊 Economic Scores:")
    for indicator, score in result["detailed_scores"].items():
        print(f"   • {indicator.replace('_', ' ').title()}: {score:.2f}/2.0")

    print(f"\n📈 Overall Economic Score: {result['score']:.1f}/10")
    print(f"💼 Economic Stance: {result['stance'].upper()}")

    print("\n✅ Bullish Factors:")
    for factor in result["bullish_factors"]:
        print(f"   • {factor}")

    print("\n⚠️  Bearish Factors:")
    for factor in result["bearish_factors"]:
        print(f"   • {factor}")

    return result


def test_market_regime(context):
    """Test Stage 2: Market regime detection"""
    print_header("STAGE 2: MARKET REGIME TEST")

    result = detect_market_regime(context)

    print(f"🎯 Detected Regime: {result['regime']}")
    print(f"📊 Confidence: {result['confidence']:.0%}")

    print("\n📋 Regime Characteristics:")
    for char in result["characteristics"]:
        print(f"   • {char}")

    print("\n💡 Recommendations for This Regime:")
    for rec in result["recommendations"]:
        print(f"   → {rec}")

    print("\n📊 Regime Scores:")
    for regime, score in result["regime_scores"].items():
        print(f"   • {regime.upper()}: {score} points")

    return result


def test_sector_impact(ticker, context):
    """Test Stage 3: Sector impact analysis"""
    print_header(f"STAGE 3: SECTOR IMPACT TEST - {ticker}")

    fundamentals = context.get_fundamentals()
    sector = fundamentals.get("sector", "Unknown") if fundamentals else "Unknown"

    econ_result = analyze_economic_indicators(context)
    regime_result = detect_market_regime(context)
    sector_result = analyze_sector_impact(sector, econ_result, regime_result)

    print(f"🏭 Sector: {sector_result['sector']}")
    print(f"📊 Sector Type: {sector_result['sector_type'].replace('_', ' ').title()}")
    print(f"🎯 Macro Favorability: {sector_result['favorability']}")
    print(f"📈 Favorability Score: {sector_result['favorability_score']}")

    print(f"\n💡 Reasoning:\n   {sector_result['reasoning']}")

    print("\n📋 Recommendations:")
    for rec in sector_result["recommendations"]:
        print(f"   → {rec}")

    return sector_result


def test_single_stock(ticker, db):
    """Test complete macro analysis on single stock"""
    print_header(f"COMPLETE MACRO ANALYSIS: {ticker}")

    context = AgentContext(ticker, db)

    try:
        # Run the advanced analysis
        signal, confidence, reasoning = advanced_macro_analyst(ticker, context)

        # Print results
        print_section("QUICK SUMMARY")
        print(f"📊 Macro Signal: {signal.upper()}")
        print(f"🎯 Confidence: {confidence:.0%}")
        print(f"💡 Reasoning:\n   {reasoning}\n")

        # Generate detailed report
        print_section("DETAILED MACRO REPORT")
        report = generate_macro_report(ticker, context)
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


def test_sector_comparison(db):
    """Compare macro impact across different sectors"""
    print_header("SECTOR COMPARISON - MACRO IMPACT")

    # Different sectors to test
    test_stocks = {
        "AAPL": "Technology",
        "MSFT": "Technology",
        "GOOGL": "Technology",
        "TSLA": "Automotive",
    }

    context_any = AgentContext("AAPL", db)
    econ_result = analyze_economic_indicators(context_any)
    regime_result = detect_market_regime(context_any)

    print(f"📊 Current Macro Environment:")
    print(f"   Economic Score: {econ_result['score']:.1f}/10 ({econ_result['stance']})")
    print(f"   Market Regime: {regime_result['regime']}\n")

    print_section("SECTOR-BY-SECTOR IMPACT")

    results = []
    sectors_tested = set()

    for ticker, expected_sector in test_stocks.items():
        context = AgentContext(ticker, db)
        fundamentals = context.get_fundamentals()
        sector = (
            fundamentals.get("sector", expected_sector)
            if fundamentals
            else expected_sector
        )

        if sector in sectors_tested:
            continue
        sectors_tested.add(sector)

        sector_result = analyze_sector_impact(sector, econ_result, regime_result)

        results.append(
            {
                "sector": sector,
                "favorability": sector_result["favorability"],
                "score": sector_result["favorability_score"],
                "reasoning": sector_result["reasoning"],
            }
        )

    # Sort by favorability
    results.sort(key=lambda x: x["score"], reverse=True)

    # Print comparison table
    print(f"{'Sector':<25} {'Favorability':<15} {'Score':<8} {'Summary'}")
    print("-" * 80)

    for r in results:
        emoji = (
            "✅"
            if r["favorability"] == "POSITIVE"
            else "⚠️" if r["favorability"] == "NEUTRAL" else "❌"
        )
        print(
            f"{r['sector']:<25} {emoji} {r['favorability']:<14} {r['score']:>6} {r['reasoning'][:30]}..."
        )

    print_section("SECTOR ROTATION RECOMMENDATIONS")

    positive = [r for r in results if r["favorability"] == "POSITIVE"]
    negative = [r for r in results if r["favorability"] == "NEGATIVE"]

    if positive:
        print("✅ OVERWEIGHT (Macro tailwinds):")
        for r in positive:
            print(f"   • {r['sector']}: {r['reasoning']}")

    if negative:
        print("\n❌ UNDERWEIGHT (Macro headwinds):")
        for r in negative:
            print(f"   • {r['sector']}: {r['reasoning']}")

    return results


def test_regime_scenarios(db):
    """Test how different regimes affect recommendations"""
    print_header("REGIME SCENARIO ANALYSIS")

    context = AgentContext("AAPL", db)

    print("🎭 Current Market Regime Assessment:\n")

    regime_result = detect_market_regime(context)

    print(f"Detected Regime: {regime_result['regime']}")
    print(f"Confidence: {regime_result['confidence']:.0%}\n")

    print("📊 What This Regime Means:\n")

    regime_implications = {
        "BULL_MARKET": {
            "description": "Rising market with low volatility",
            "favor": ["Growth stocks", "Cyclicals", "Small-caps"],
            "avoid": ["Defensives", "High dividend stocks"],
            "strategy": "Aggressive growth positioning",
        },
        "BEAR_MARKET": {
            "description": "Falling market with high volatility",
            "favor": ["Defensives", "Quality", "Large-caps"],
            "avoid": ["Cyclicals", "High beta", "Leverage"],
            "strategy": "Capital preservation, defensive positioning",
        },
        "RISK_ON": {
            "description": "Growth-focused, risk-seeking environment",
            "favor": ["Emerging markets", "Small-caps", "High beta"],
            "avoid": ["Bonds", "Utilities", "Low volatility"],
            "strategy": "Embrace risk for higher returns",
        },
        "RISK_OFF": {
            "description": "Safety-focused, risk-averse environment",
            "favor": ["Treasuries", "Gold", "Staples", "Healthcare"],
            "avoid": ["Cyclicals", "Emerging markets"],
            "strategy": "Preserve capital, reduce risk",
        },
    }

    current_regime = regime_result["regime"]
    if current_regime in regime_implications:
        impl = regime_implications[current_regime]

        print(f"Description: {impl['description']}\n")

        print("Favor:")
        for item in impl["favor"]:
            print(f"   ✅ {item}")

        print("\nAvoid:")
        for item in impl["avoid"]:
            print(f"   ❌ {item}")

        print(f"\nRecommended Strategy: {impl['strategy']}")


def test_combined_analysis(ticker, db):
    """Test combining macro and fundamental analysis"""
    print_header(f"COMBINED ANALYSIS: MACRO + FUNDAMENTAL - {ticker}")

    context = AgentContext(ticker, db)

    # Run macro analysis
    print("Running macro analysis...")
    macro_signal, macro_conf, macro_reasoning = advanced_macro_analyst(ticker, context)

    print("\n📊 Macro Analysis Result:")
    print(f"   Signal: {macro_signal}")
    print(f"   Confidence: {macro_conf:.0%}")
    print(f"   Reasoning: {macro_reasoning[:100]}...\n")

    # Try to run fundamental analysis if available
    try:
        from advanced_fundamental_analyst import advanced_fundamental_analyst

        print("Running fundamental analysis...")
        fund_signal, fund_conf, fund_reasoning = advanced_fundamental_analyst(
            ticker, context
        )

        print("\n📊 Fundamental Analysis Result:")
        print(f"   Signal: {fund_signal}")
        print(f"   Confidence: {fund_conf:.0%}")
        print(f"   Reasoning: {fund_reasoning[:100]}...\n")

        # Combine signals
        print_section("COMBINED RECOMMENDATION")

        signal_scores = {"bullish": 1.0, "neutral": 0.5, "bearish": 0.0}

        macro_score = signal_scores[macro_signal] * macro_conf
        fund_score = signal_scores[fund_signal] * fund_conf

        # Equal weight for this example
        combined_score = (macro_score + fund_score) / 2

        if combined_score >= 0.65:
            combined_signal = "STRONG BUY"
        elif combined_score >= 0.55:
            combined_signal = "BUY"
        elif combined_score >= 0.45:
            combined_signal = "HOLD"
        elif combined_score >= 0.35:
            combined_signal = "SELL"
        else:
            combined_signal = "STRONG SELL"

        avg_conf = (macro_conf + fund_conf) / 2

        print(f"🎯 Combined Signal: {combined_signal}")
        print(f"📊 Combined Confidence: {avg_conf:.0%}")

        print("\n📋 Analysis Summary:")
        print(f"   Macro: {macro_signal} ({macro_conf:.0%})")
        print(f"   Fundamental: {fund_signal} ({fund_conf:.0%})")

        if macro_signal == fund_signal:
            print(f"\n   ✅ Both analyses agree → High conviction")
        else:
            print(f"\n   ⚠️  Analyses disagree → Lower conviction, need more research")

    except ImportError:
        print("ℹ️  Fundamental analyst not available (optional)")
        print("   Macro analysis standalone is sufficient for macro-focused strategy")


def main():
    """Main test runner"""
    print("\n" + "=" * 80)
    print(" ADVANCED MACRO ANALYST - TEST SUITE")
    print(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)

    # Setup
    print("\n⚙️  Setting up...")
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)

    print(f"✅ Connected to database")
    print(f"✅ Testing macro analysis capabilities\n")

    # Run tests based on command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "--indicators":
            # Test economic indicators
            context = AgentContext("AAPL", db)
            test_economic_indicators(context)

        elif mode == "--regime":
            # Test regime detection
            context = AgentContext("AAPL", db)
            test_regime_scenarios(db)

        elif mode == "--sectors":
            # Test sector comparison
            test_sector_comparison(db)

        elif mode == "--single":
            # Test single stock
            ticker = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
            test_single_stock(ticker, db)

        elif mode == "--combined":
            # Test macro + fundamental
            ticker = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
            test_combined_analysis(ticker, db)

        elif mode == "--all":
            # Run comprehensive tests
            print_header("RUNNING COMPREHENSIVE MACRO TESTS")

            context = AgentContext("AAPL", db)

            # Test each stage
            test_economic_indicators(context)
            test_market_regime(context)
            test_sector_impact("AAPL", context)

            # Full analysis
            test_single_stock("AAPL", db)

            # Sector comparison
            test_sector_comparison(db)

            # Combined analysis
            test_combined_analysis("AAPL", db)

        else:
            print(f"❌ Unknown mode: {mode}")
            print_usage()

    else:
        # Default: single stock analysis
        print("ℹ️  Running default test (single stock macro analysis)")
        print("   Use --help for more options\n")
        test_single_stock("AAPL", db)

    # Cleanup
    pool.close()

    print("\n" + "=" * 80)
    print(" MACRO TEST SUITE COMPLETE")
    print("=" * 80 + "\n")


def print_usage():
    """Print usage instructions"""
    print("\n" + "=" * 80)
    print(" USAGE")
    print("=" * 80)
    print(
        """
Available test modes:

  python test_macro_analyst.py --indicators
      Test economic indicator analysis (Stage 1)

  python test_macro_analyst.py --regime
      Test market regime detection (Stage 2)

  python test_macro_analyst.py --sectors
      Compare macro impact across sectors (Stage 3)

  python test_macro_analyst.py --single [TICKER]
      Complete macro analysis for one stock
      Example: python test_macro_analyst.py --single AAPL

  python test_macro_analyst.py --combined [TICKER]
      Combine macro + fundamental analysis
      Example: python test_macro_analyst.py --combined TSLA

  python test_macro_analyst.py --all
      Run all test modes (comprehensive)

  python test_macro_analyst.py --help
      Show this help message

Available tickers: AAPL, TSLA, MSFT, GOOGL, NVDA

Examples:
  # Quick test
  python test_macro_analyst.py --single AAPL

  # Sector rotation analysis
  python test_macro_analyst.py --sectors

  # Full test suite
  python test_macro_analyst.py --all
"""
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_usage()
    else:
        main()
