from agent_builder import agent, get_registry


@agent("My First Agent", "Custom analysis logic")
def my_agent(ticker, context):
    # Get data
    pe = context.get_fundamental("pe_ratio", 20)
    growth = context.get_fundamental("revenue_growth", 0)

    # Your logic
    score = 0
    if pe < 20:
        score += 1
    if growth > 10:
        score += 1

    # Return signal
    if score >= 2:
        return "bullish", 0.8, f"Strong metrics: PE={pe}, growth={growth}%"
    elif score == 0:
        return "bearish", 0.6, "Weak metrics"

    return "neutral", 0.5, "Mixed signals"


# Register
def register_my_agents():
    registry = get_registry()
    registry.register(my_agent.agent, weight=1.0, tags=["custom"])
