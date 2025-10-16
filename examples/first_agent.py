import sys

sys.path.insert(0, ".")

from agent_builder.agents.builder import simple_agent


@simple_agent("Test Agent", weight=0.1)
def test_agent(ticker, context):
    return "bullish", 0.7


@simple_agent("PE Ratio Agent", weight=0.12)
def pe_agent(ticker, context):
    pe_ratio = 18.5
    if pe_ratio < 15:
        return "bullish", 0.8
    elif pe_ratio < 25:
        return "neutral", 0.6
    else:
        return "bearish", 0.4


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Agents")
    print("=" * 60)

    signal1 = test_agent.analyze("AAPL")
    print(f"\n✅ {signal1.agent_name}: {signal1.signal_type} ({signal1.confidence})")

    signal2 = pe_agent.analyze("AAPL")
    print(f"✅ {signal2.agent_name}: {signal2.signal_type} ({signal2.confidence})")

    print("\n" + "=" * 60)
