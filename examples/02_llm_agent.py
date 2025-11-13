"""Example 2: LLM-Powered Agent with Full Configuration

This example demonstrates AI-powered investment analysis:
- Uses large language models for nuanced reasoning
- Configurable personality via system prompts
- Adjustable creativity via temperature
- Control response length via max_tokens

Learning Focus:
- LLM integration (OpenAI, Anthropic, Ollama)
- System prompts for agent personality
- Temperature and max_tokens configuration
- Error handling with fallback logic
- Natural language reasoning

⚠️ DISCLAIMER: This is educational code for learning purposes only.
Do NOT use for real trading. Not financial advice. See DISCLAIMER.md for full terms.

DEPENDENCIES:
This example requires LLM dependencies. Install with:
  pip install 'ai-agent-framework[llm]'

Or install Ollama specifically:
  pip install ollama

Then download the model:
  ollama pull llama3.2
"""

import asyncio
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig,
    Database, Config, parse_llm_signal, format_fundamentals
)


class QualityInvestorAgent(Agent):
    """AI-powered quality investor using Ollama LLM.
    
    Strategy: Uses AI to analyze company quality holistically
    
    Configuration:
    - Provider: Ollama (free, local, private)
    - Model: llama3.2 (latest Llama model)
    - Temperature: 0.5 (balanced between focused and creative)
    - Max Tokens: 1500 (detailed responses)
    - System Prompt: Defines agent personality as quality-focused investor
    
    This demonstrates:
    - Full LLM configuration
    - Custom system prompt for personality
    - Error handling with fallback
    - Natural language reasoning
    """
    
    def __init__(self):
        """Initialize agent with complete LLM configuration."""
        config = AgentConfig(
            name="Quality Investor Agent",
            description="AI-powered quality investor focusing on strong fundamentals",
            llm=LLMConfig(
                provider='ollama',           # Free, local AI
                model='llama3.2',            # Latest Llama model
                temperature=0.5,             # Balanced (0=focused, 1=creative)
                max_tokens=1500,             # Detailed responses
                system_prompt="""You are a quality-focused investment analyst inspired by Warren Buffett.

Your investment philosophy:
- Focus on business quality over price
- Look for competitive advantages ("moats")
- Prefer high ROE (>15%) and strong profit margins (>15%)
- Favor companies with low debt (debt-to-equity < 1.0)
- Value consistent growth over explosive growth
- Prioritize companies you'd hold for 10+ years

Analyze companies systematically:
1. Quality of business (ROE, margins, competitive position)
2. Financial health (debt levels, current ratio)
3. Growth prospects (sustainable revenue growth)
4. Valuation (is it reasonably priced?)

Be thorough but concise. Focus on what matters most."""
            )
        )
        super().__init__(config)
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using LLM with quality-focused personality.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with AI-generated reasoning
        """
        # Format fundamentals for LLM
        fundamentals_text = format_fundamentals(data)
        
        # Build analysis prompt
        prompt = f"""Analyze {ticker} as a quality investment:

{fundamentals_text}

Provide your investment recommendation focusing on business quality.

Format your response as:
DIRECTION|CONFIDENCE|REASONING

Where:
- DIRECTION: bullish, bearish, or neutral
- CONFIDENCE: 0-100 (as percentage)
- REASONING: 2-3 sentences explaining your analysis

Example: bullish|75|Strong ROE of 25% indicates excellent management efficiency. Low debt-to-equity of 0.3 provides financial safety. Growing revenue at 15% shows sustainable expansion."""
        
        try:
            # Query LLM (uses system prompt automatically)
            response = self.llm.chat(prompt)
            
            # Parse LLM response
            return parse_llm_signal(response, f"Quality analysis of {ticker}")
        
        except Exception as e:
            print(f"⚠️  LLM error: {e}")
            print(f"    Error type: {type(e).__name__}")
            
            # Fallback to rule-based logic
            roe = data.get('roe', 0)
            margin = data.get('profit_margin', 0)
            debt = data.get('debt_to_equity', 0)
            
            # Simple quality check
            if roe > 15 and margin > 15 and debt < 1.0:
                return Signal(
                    direction='bullish',
                    confidence=0.7,
                    reasoning=f'LLM unavailable ({type(e).__name__}), using fallback: Quality metrics strong (ROE={roe:.1f}%, Margin={margin:.1f}%, Debt={debt:.1f})'
                )
            elif roe < 10 or debt > 2.0:
                return Signal(
                    direction='bearish',
                    confidence=0.6,
                    reasoning=f'LLM unavailable ({type(e).__name__}), using fallback: Quality concerns (ROE={roe:.1f}%, Debt={debt:.1f})'
                )
            else:
                return Signal(
                    direction='neutral',
                    confidence=0.5,
                    reasoning=f'LLM unavailable ({type(e).__name__}), using fallback: Mixed quality signals'
                )


async def main():
    """Example usage of LLM-powered agent."""
    print("=" * 70)
    print("Example 2: LLM-Powered Agent with Full Configuration")
    print("=" * 70)
    print("\n📚 Learning: AI-powered analysis with configurable personality")
    print("⚡ Speed: Slower (2-5 seconds per stock due to LLM)")
    print("💰 Cost: Free with Ollama (local), or API costs with OpenAI/Anthropic")
    print("🧠 Intelligence: Nuanced, context-aware analysis")
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    try:
        import ollama
        print("✅ Ollama package installed")
        
        # Try to connect to Ollama
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                print("✅ Ollama service running")
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                if 'llama3.2' in str(model_names):
                    print("✅ llama3.2 model available")
                else:
                    print("⚠️  llama3.2 not found. Run: ollama pull llama3.2")
            else:
                print("⚠️  Ollama service not responding. Run: ollama serve")
        except:
            print("⚠️  Can't connect to Ollama. Run: ollama serve")
    except ImportError:
        print("⚠️  Ollama package not installed")
        print("   Install with: pip install ollama")
        print("   Or install all LLM providers: pip install 'ai-agent-framework[llm]'")
    
    # Connect to database
    connection_string = Config.get_database_url()
    
    print("\n📌 Connecting to database...")
    db = Database(connection_string)
    
    try:
        await db.connect()
        print("✅ Connected!")
        
        # Create agent
        print("\n🤖 Initializing Quality Investor Agent...")
        agent = QualityInvestorAgent()
        print("   Provider: Ollama (free, local)")
        print("   Model: llama3.2")
        print("   Temperature: 0.5 (balanced)")
        print("   Max Tokens: 1500 (detailed)")
        print("   Personality: Quality-focused (Warren Buffett style)")
        
        # Analyze stocks
        for ticker in ['AAPL', 'TSLA', 'JPM']:
            print(f"\n{'='*70}")
            
            data = await db.get_fundamentals(ticker)
            if not data:
                print(f"⚠️  No data for {ticker}")
                continue
            
            # Show company info
            print(f"📊 {ticker} - {data['name']}")
            print(f"   Sector: {data['sector']}")
            print(f"   PE: {data['pe_ratio']:.1f} | ROE: {data['roe']:.1f}% | Margin: {data['profit_margin']:.1f}% | Debt/Equity: {data['debt_to_equity']:.1f}")
            
            # Run LLM analysis
            print(f"\n🧠 Analyzing with AI...")
            signal = await agent.analyze(ticker, data)
            
            # Display result
            emoji = {'bullish': '🟢', 'bearish': '🔴', 'neutral': '🟡'}[signal.direction]
            print(f"\n   {emoji} {signal.direction.upper()} ({signal.confidence:.0%})")
            print(f"   Reasoning: {signal.reasoning}")
        
        print("\n" + "=" * 70)
        print("✅ Example completed!")
        print("\n💡 Key Takeaways:")
        print("   • LLM agents provide nuanced, contextual analysis")
        print("   • System prompts define agent personality and approach")
        print("   • Temperature controls creativity (0.5 = balanced)")
        print("   • Fallback logic ensures agents work even if LLM fails")
        print("   • Slower than rules but much smarter reasoning")
        print("\n🎯 LLM Configuration Options:")
        print("   • Provider: 'ollama' (free), 'openai' (paid), 'anthropic' (paid)")
        print("   • Temperature: 0.0-1.0 (low=focused, high=creative)")
        print("   • Max Tokens: 100-4000 (length of response)")
        print("   • System Prompt: Define personality and approach")
        print("\n📖 Next: Try 03_hybrid.py for rules + LLM combination")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
