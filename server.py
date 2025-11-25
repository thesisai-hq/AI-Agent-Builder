"""Example API Server - Deploy agents as REST API.

This is an EXAMPLE file showing how to deploy agents via HTTP API.
The framework provides API infrastructure in agent_framework/api.py

You create this file to:
1. Register your agents
2. Start the API server
3. Expose agents via HTTP endpoints

For multi-agent orchestration, see: docs/MULTI_AGENT_SYSTEMS.md
"""

from agent_framework import api_app, register_agent_instance
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_and_register_agents():
    """Create agents and register them with the API.
    
    Replace this with your actual agents!
    """
    from agent_framework import Agent, Signal
    
    # Example: Simple value agent
    class ExampleValueAgent(Agent):
        """Example value investing agent."""
        
        async def analyze(self, ticker: str, data: dict) -> Signal:
            pe = data.get('pe_ratio', 0)
            
            if pe < 15:
                return Signal(
                    direction='bullish',
                    confidence=0.8,
                    reasoning=f'Undervalued: PE={pe:.1f}'
                )
            elif pe > 30:
                return Signal(
                    direction='bearish',
                    confidence=0.7,
                    reasoning=f'Overvalued: PE={pe:.1f}'
                )
            else:
                return Signal(
                    direction='neutral',
                    confidence=0.6,
                    reasoning=f'Fair value: PE={pe:.1f}'
                )
    
    # Register agents (makes them available via API)
    agents = {
        'value': ExampleValueAgent(),
        # Add more agents here:
        # 'growth': GrowthAgent(),
        # 'quality': QualityAgent(),
    }
    
    for name, agent in agents.items():
        register_agent_instance(name, agent)
        logger.info(f"✅ Registered agent: {name}")
    
    return agents


def main():
    """Start the API server."""
    
    print("=" * 60)
    print("AI Agent API Server")
    print("=" * 60)
    print()
    
    # Register agents
    agents = create_and_register_agents()
    
    print()
    print(f"✅ {len(agents)} agent(s) registered")
    print()
    print("=" * 60)
    print("Starting API Server")
    print("=" * 60)
    print()
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check:      http://localhost:8000/health")
    print("📋 List Agents:       http://localhost:8000/agents")
    print()
    print("Example API call:")
    print('  curl -X POST http://localhost:8000/analyze \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"agent_name":"value","ticker":"AAPL"}\'')
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Start server with auto-reload
    uvicorn.run(
        api_app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )


if __name__ == "__main__":
    main()
