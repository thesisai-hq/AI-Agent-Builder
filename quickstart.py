"""Quick start script to verify framework installation."""

import sys
import asyncio
import os


def check_imports():
    """Check all required imports work."""
    print("🔍 Checking imports...")
    try:
        from agent_framework import (
            Agent, Signal, AgentConfig,
            LLMConfig, RAGConfig,
            Database, get_database
        )
        print("✅ Core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Run: pip install -e .")
        return False


async def test_database():
    """Test database connection."""
    print("\n🗄️  Testing PostgreSQL database...")
    
    # Get connection string from environment
    connection_string = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/agent_framework'
    )
    
    try:
        from agent_framework.database import get_database
        
        db = get_database(connection_string)
        await db.connect()
        
        tickers = await db.list_tickers()
        
        if tickers:
            print(f"✅ Connected to database with {len(tickers)} tickers")
            print(f"   Available: {', '.join(tickers)}")
            
            # Test data retrieval
            data = await db.get_fundamentals(tickers[0])
            print(f"✅ Retrieved data for {tickers[0]}: PE={data.get('pe_ratio', 'N/A')}")
            
            await db.disconnect()
            return True
        else:
            print("⚠️  Database is empty. Run: python seed_data.py")
            await db.disconnect()
            return None  # Database works but needs seeding
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("\n💡 PostgreSQL not running or not seeded. Setup:")
        print("   1. Start PostgreSQL: docker-compose up -d postgres")
        print("   2. Seed database: python seed_data.py")
        return False


async def test_simple_agent():
    """Test simple agent."""
    print("\n🤖 Testing simple agent...")
    
    connection_string = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/agent_framework'
    )
    
    try:
        from agent_framework import Agent, Signal
        from agent_framework.database import get_database
        
        class QuickAgent(Agent):
            def analyze(self, ticker: str, data: dict) -> Signal:
                pe = data.get('pe_ratio', 20)
                return Signal(
                    'bullish' if pe < 20 else 'neutral',
                    0.7,
                    f"PE ratio: {pe:.1f}"
                )
        
        db = get_database(connection_string)
        await db.connect()
        
        tickers = await db.list_tickers()
        if not tickers:
            print("⚠️  No tickers in database. Run: python seed_data.py")
            await db.disconnect()
            return None
        
        agent = QuickAgent()
        data = await db.get_fundamentals(tickers[0])
        signal = agent.analyze(tickers[0], data)
        
        print(f"✅ Agent analysis: {signal.direction.upper()} ({signal.confidence:.0%})")
        print(f"   Reasoning: {signal.reasoning}")
        
        await db.disconnect()
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


async def main():
    """Run all checks."""
    print("=" * 60)
    print("AI Agent Framework - Quick Start Verification")
    print("=" * 60)
    
    checks = [
        ("Imports", check_imports, False),
        ("PostgreSQL Database", test_database, True),
        ("Simple Agent", test_simple_agent, True),
        ("RAG System", test_rag_system, False),
        ("API", test_api, False),
    ]
    
    results = {}
    for name, check_func, is_async in checks:
        try:
            if is_async:
                result = await check_func()
            else:
                result = check_func()
            results[name] = result
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            results[name] = False
    
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
            print(f"⚠️  {name} (optional or needs seeding)")
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
        print("\n⚠️  Some checks failed.")
        print("\n💡 Setup steps:")
        print("  1. Start PostgreSQL: docker-compose up -d postgres")
        print("  2. Seed database: python seed_data.py")
        print("  3. Install dependencies: pip install -e .[all]")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))