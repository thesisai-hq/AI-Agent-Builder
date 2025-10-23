"""Quick start script to verify framework installation."""

import sys


def check_imports():
    """Check all required imports work."""
    print("🔍 Checking imports...")
    try:
        from agent_framework import (
            Agent, Signal, AgentConfig,
            LLMConfig, RAGConfig,
            MockDatabase
        )
        print("✅ Core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_mock_database():
    """Test mock database."""
    print("\n🗄️  Testing mock database...")
    try:
        from agent_framework import MockDatabase
        
        db = MockDatabase()
        tickers = db.list_tickers()
        print(f"✅ Loaded {len(tickers)} tickers: {', '.join(tickers)}")
        
        # Test data retrieval
        data = db.get_fundamentals('AAPL')
        print(f"✅ AAPL PE Ratio: {data['pe_ratio']:.1f}")
        
        prices = db.get_prices('AAPL', days=5)
        print(f"✅ Retrieved {len(prices)} days of price data")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def test_simple_agent():
    """Test simple agent."""
    print("\n🤖 Testing simple agent...")
    try:
        from agent_framework import Agent, Signal, MockDatabase
        
        class QuickAgent(Agent):
            def analyze(self, ticker: str, data: dict) -> Signal:
                pe = data.get('pe_ratio', 20)
                return Signal(
                    'bullish' if pe < 20 else 'neutral',
                    0.7,
                    f"PE ratio: {pe:.1f}"
                )
        
        db = MockDatabase()
        agent = QuickAgent()
        signal = agent.analyze('AAPL', db.get_fundamentals('AAPL'))
        
        print(f"✅ Agent analysis: {signal.direction.upper()} ({signal.confidence:.0%})")
        print(f"   Reasoning: {signal.reasoning}")
        
        return True
    except Exception as e:
        print(f"❌ Agent error: {e}")
        return False


def test_rag_system():
    """Test RAG system."""
    print("\n📚 Testing RAG system...")
    try:
        from agent_framework import RAGSystem, RAGConfig
        
        config = RAGConfig(chunk_size=100, top_k=2)
        rag = RAGSystem(config)
        
        # Add document
        doc = "Apple Inc. is a technology company. They make iPhones and computers."
        rag.add_document(doc)
        
        # Query
        result = rag.query("What does Apple make?")
        print(f"✅ RAG query successful")
        print(f"   Result preview: {result[:100]}...")
        
        return True
    except ImportError:
        print("⚠️  RAG requires: pip install sentence-transformers")
        return None  # Optional dependency
    except Exception as e:
        print(f"❌ RAG error: {e}")
        return False


def test_api():
    """Test API setup."""
    print("\n🌐 Testing API...")
    try:
        from agent_framework import api_app
        print(f"✅ FastAPI app loaded: {api_app.title}")
        return True
    except Exception as e:
        print(f"❌ API error: {e}")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("AI Agent Framework - Quick Start")
    print("=" * 60)
    
    checks = [
        ("Imports", check_imports),
        ("Mock Database", test_mock_database),
        ("Simple Agent", test_simple_agent),
        ("RAG System", test_rag_system),
        ("API", test_api),
    ]
    
    results = {}
    for name, check in checks:
        result = check()
        results[name] = result
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r is True)
    optional = sum(1 for r in results.values() if r is None)
    failed = sum(1 for r in results.values() if r is False)
    
    for name, result in results.items():
        if result is True:
            print(f"✅ {name}")
        elif result is None:
            print(f"⚠️  {name} (optional)")
        else:
            print(f"❌ {name}")
    
    print(f"\nPassed: {passed}/{len(checks) - optional}")
    
    if failed == 0:
        print("\n🎉 Framework is ready to use!")
        print("\nNext steps:")
        print("  1. Run examples: python examples/01_basic.py")
        print("  2. Start API: uvicorn agent_framework.api:app --reload")
        print("  3. Run tests: pytest tests/")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please install missing dependencies:")
        print("  pip install -e .[all]")
        return 1


if __name__ == "__main__":
    sys.exit(main())