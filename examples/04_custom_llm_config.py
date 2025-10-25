"""Example: Customizing LLM temperature and max_tokens per agent.

This example demonstrates how to create agents with different LLM configurations:
- Conservative agent with low temperature (more focused)
- Creative agent with high temperature (more diverse)
- Detailed agent with high max_tokens (longer responses)

Temperature Guide:
  0.0-0.3: Very focused, deterministic, conservative
  0.4-0.7: Balanced, moderate creativity (default range)
  0.8-1.0: Creative, diverse, more random
  1.1-2.0: Highly creative, experimental (use cautiously)

Max Tokens Guide:
  500-1000: Brief, concise responses
  1000-2000: Standard analysis
  2000-4000: Detailed, comprehensive analysis
"""

import asyncio
from agent_framework import Agent, Signal, AgentConfig, LLMConfig, Config
from agent_framework.database import Database


class ConservativeAnalyst(Agent):
    """Conservative analyst with low temperature - very focused, consistent."""
    
    def __init__(self):
        """Initialize with low temperature for focused, deterministic responses."""
        config = AgentConfig(
            name="Conservative Analyst",
            description="Focused, consistent analysis with low temperature",
            llm=LLMConfig(
                provider='ollama',
                temperature=0.2,  # Very focused and deterministic
                max_tokens=800,   # Concise responses
                system_prompt="You are a conservative financial analyst. Be precise and data-driven."
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze with conservative, focused approach."""
        prompt = f"""Analyze {ticker}:
PE: {data.get('pe_ratio', 'N/A')}
Growth: {data.get('revenue_growth', 'N/A')}%
Margin: {data.get('profit_margin', 'N/A')}%

Provide: DIRECTION|CONFIDENCE|REASONING"""
        
        try:
            response = self.llm.chat(prompt)
            parts = response.split('|')
            return Signal(
                direction=parts[0].strip().lower(),
                confidence=float(parts[1].strip().replace('%', '')) / 100,
                reasoning=parts[2].strip()
            )
        except Exception as e:
            return Signal('neutral', 0.5, f'Analysis error: {str(e)[:100]}')


class CreativeStrategist(Agent):
    """Creative strategist with high temperature - diverse, exploratory."""
    
    def __init__(self):
        """Initialize with high temperature for creative, diverse responses."""
        config = AgentConfig(
            name="Creative Strategist",
            description="Exploratory analysis with high temperature",
            llm=LLMConfig(
                provider='ollama',
                temperature=0.9,  # High creativity and diversity
                max_tokens=1500,  # More detailed responses
                system_prompt="You are a creative investment strategist. Think outside the box and consider innovative angles."
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze with creative, exploratory approach."""
        prompt = f"""Creatively analyze {ticker}:
PE: {data.get('pe_ratio', 'N/A')}
Growth: {data.get('revenue_growth', 'N/A')}%
Sector: {data.get('sector', 'N/A')}

Think creatively about opportunities and risks.
Format: DIRECTION|CONFIDENCE|REASONING"""
        
        try:
            response = self.llm.chat(prompt)
            parts = response.split('|')
            return Signal(
                direction=parts[0].strip().lower(),
                confidence=float(parts[1].strip().replace('%', '')) / 100,
                reasoning=parts[2].strip()
            )
        except Exception as e:
            return Signal('neutral', 0.5, f'Analysis error: {str(e)[:100]}')


class DetailedResearcher(Agent):
    """Detailed researcher with high max_tokens - comprehensive analysis."""
    
    def __init__(self):
        """Initialize with high max_tokens for detailed, comprehensive responses."""
        config = AgentConfig(
            name="Detailed Researcher",
            description="Comprehensive analysis with high max_tokens",
            llm=LLMConfig(
                provider='ollama',
                temperature=0.5,  # Balanced
                max_tokens=2500,  # Detailed, comprehensive
                system_prompt="You are a thorough research analyst. Provide detailed, comprehensive analysis with multiple perspectives."
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze with detailed, comprehensive approach."""
        prompt = f"""Provide detailed analysis of {ticker}:

Fundamentals:
- PE Ratio: {data.get('pe_ratio', 'N/A')}
- PB Ratio: {data.get('pb_ratio', 'N/A')}
- ROE: {data.get('roe', 'N/A')}%
- Profit Margin: {data.get('profit_margin', 'N/A')}%
- Revenue Growth: {data.get('revenue_growth', 'N/A')}%
- Debt/Equity: {data.get('debt_to_equity', 'N/A')}
- Dividend Yield: {data.get('dividend_yield', 'N/A')}%

Provide comprehensive analysis considering:
1. Valuation metrics
2. Growth prospects
3. Financial health
4. Risk factors

Format: DIRECTION|CONFIDENCE|DETAILED_REASONING"""
        
        try:
            response = self.llm.chat(prompt)
            parts = response.split('|')
            return Signal(
                direction=parts[0].strip().lower(),
                confidence=float(parts[1].strip().replace('%', '')) / 100,
                reasoning=parts[2].strip() if len(parts) > 2 else parts[1].strip()
            )
        except Exception as e:
            return Signal('neutral', 0.5, f'Analysis error: {str(e)[:100]}')


class CustomizedAgent(Agent):
    """Example of using the helper method for quick customization."""
    
    def __init__(self, temperature: float = 0.7, max_tokens: int = 1000):
        """Initialize with custom temperature and max_tokens.
        
        Args:
            temperature: Response randomness (0.0-2.0)
            max_tokens: Maximum response length
        """
        config = AgentConfig(
            name=f"Custom Agent (T={temperature}, MT={max_tokens})",
            description=f"Agent with temperature={temperature}, max_tokens={max_tokens}",
            llm=LLMConfig.create_custom(
                provider='ollama',
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt="You are a flexible analyst."
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze with custom settings."""
        prompt = f"Analyze {ticker} with PE={data.get('pe_ratio')}. Format: DIRECTION|CONFIDENCE|REASONING"
        
        try:
            response = self.llm.chat(prompt)
            parts = response.split('|')
            return Signal(
                direction=parts[0].strip().lower(),
                confidence=float(parts[1].strip().replace('%', '')) / 100,
                reasoning=parts[2].strip()
            )
        except Exception as e:
            return Signal('neutral', 0.5, f'Error: {str(e)[:100]}')


async def main():
    """Demonstrate different temperature and max_tokens settings."""
    print("=" * 70)
    print("LLM Configuration Per Agent - Temperature & Max Tokens Customization")
    print("=" * 70)
    
    # Connect to database
    connection_string = Config.get_database_url()
    db = Database(connection_string)
    
    try:
        await db.connect()
        print("\n✅ Connected to database")
        
        # Create agents with different configurations
        print("\n🤖 Creating agents with different LLM configurations...")
        
        conservative = ConservativeAnalyst()
        print(f"  ✓ Conservative Analyst (temp=0.2, tokens=800)")
        
        creative = CreativeStrategist()
        print(f"  ✓ Creative Strategist (temp=0.9, tokens=1500)")
        
        detailed = DetailedResearcher()
        print(f"  ✓ Detailed Researcher (temp=0.5, tokens=2500)")
        
        # Custom agents using helper method
        custom_focused = CustomizedAgent(temperature=0.1, max_tokens=500)
        print(f"  ✓ Custom Focused (temp=0.1, tokens=500)")
        
        custom_creative = CustomizedAgent(temperature=1.2, max_tokens=2000)
        print(f"  ✓ Custom Creative (temp=1.2, tokens=2000)")
        
        # Test on one ticker
        ticker = 'AAPL'
        data = await db.get_fundamentals(ticker)
        
        if not data:
            print(f"\n⚠️  No data for {ticker}")
            return
        
        print(f"\n{'='*70}")
        print(f"📊 Analyzing {ticker} - {data['name']}")
        print(f"{'='*70}")
        print(f"PE: {data['pe_ratio']:.1f} | Growth: {data['revenue_growth']:.1f}% | "
              f"Margin: {data['profit_margin']:.1f}%\n")
        
        agents = [
            ("Conservative (T=0.2)", conservative),
            ("Creative (T=0.9)", creative),
            ("Detailed (T=0.5)", detailed),
            ("Custom Focused (T=0.1)", custom_focused),
            ("Custom Creative (T=1.2)", custom_creative)
        ]
        
        for name, agent in agents:
            print(f"\n{name}:")
            print("-" * 70)
            signal = agent.analyze(ticker, data)
            print(f"Direction: {signal.direction.upper()}")
            print(f"Confidence: {signal.confidence:.1%}")
            print(f"Reasoning: {signal.reasoning[:200]}...")  # Truncate for display
        
        print("\n" + "=" * 70)
        print("✅ Example completed!")
        print("\nKey Takeaways:")
        print("  • Low temperature (0.1-0.3) = Focused, consistent responses")
        print("  • High temperature (0.8-1.2) = Creative, diverse responses")
        print("  • Low max_tokens (500-1000) = Concise analysis")
        print("  • High max_tokens (2000-4000) = Detailed analysis")
        print("  • Each agent can have its own configuration!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.disconnect()


if __name__ == "__main__":
    # Note: This example requires Ollama running locally
    # To use OpenAI or Anthropic, change provider in agent configs
    # and set API keys in .env file
    asyncio.run(main())
