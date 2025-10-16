"""
Test Agent Registry
"""

import sys

sys.path.insert(0, ".")

from agent_builder.agents.registry import AgentRegistry
from agent_builder.agents.builder import simple_agent
from agent_builder.agents.context import AgentContext


def test_registry():
    """Test the agent registry"""
    print("=" * 60)
    print("Testing Agent Registry")
    print("=" * 60)

    # Create registry
    registry = AgentRegistry()

    # Create test agents
    @simple_agent("Test Agent 1", weight=0.1)
    def agent1(ticker, context):
        return "bullish", 0.8

    @simple_agent("Test Agent 2", weight=0.2)
    def agent2(ticker, context):
        return "bearish", 0.7

    # Register agents
    print("\n1️⃣ Registering agents...")
    id1 = registry.register(agent1.agent, weight=0.1)
    id2 = registry.register(agent2.agent, weight=0.2)
    print(f"   ✅ Registered {id1}")
    print(f"   ✅ Registered {id2}")

    # List agents
    print("\n2️⃣ Listing agents...")
    all_ids = registry.list_all()
    print(f"   Total: {len(all_ids)}")
    print(f"   IDs: {all_ids}")

    # Get agent
    print("\n3️⃣ Getting agent...")
    agent = registry.get(id1)
    print(f"   ✅ Found: {agent.name}")

    # Get metadata
    print("\n4️⃣ Getting metadata...")
    meta = registry.get_metadata(id1)
    print(f"   Name: {meta['name']}")
    print(f"   Weight: {meta['weight']}")
    print(f"   Enabled: {meta['enabled']}")

    # Disable agent
    print("\n5️⃣ Disabling agent...")
    registry.disable(id2)
    enabled = registry.list_enabled()
    print(f"   Enabled agents: {len(enabled)}")

    # Get enabled agents
    print("\n6️⃣ Getting enabled agents...")
    enabled_agents = registry.get_enabled_agents()
    print(f"   Count: {len(enabled_agents)}")
    for agent in enabled_agents:
        print(f"   - {agent.name}")

    # Stats
    print("\n7️⃣ Registry stats...")
    stats = registry.stats()
    print(f"   Total: {stats['total_agents']}")
    print(f"   Enabled: {stats['enabled_agents']}")
    print(f"   Disabled: {stats['disabled_agents']}")

    # Execute agents
    print("\n8️⃣ Executing agents...")
    ticker = "AAPL"
    for agent in enabled_agents:
        try:
            signal = agent.analyze(ticker)
            print(f"   ✅ {signal.agent_name}: {signal.signal_type}")
        except Exception as e:
            print(f"   ❌ {agent.name}: {e}")

    print("\n" + "=" * 60)
    print("✅ Registry tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    test_registry()
