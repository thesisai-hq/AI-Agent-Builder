"""Comprehensive test suite for AI Agent Framework with PostgreSQL."""

import pytest
import asyncio
import os
from datetime import datetime
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig, RAGConfig,
    Database, get_database
)


# Test configuration
TEST_DB_URL = os.getenv(
    'TEST_DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/agent_framework'
)


class TestModels:
    """Test data models."""
    
    def test_signal_creation(self):
        """Test Signal dataclass."""
        signal = Signal(
            direction='bullish',
            confidence=0.8,
            reasoning='Test reasoning'
        )
        assert signal.direction == 'bullish'
        assert signal.confidence == 0.8
        assert signal.reasoning == 'Test reasoning'
        assert isinstance(signal.timestamp, datetime)
    
    def test_signal_validation(self):
        """Test Signal validation."""
        with pytest.raises(ValueError):
            Signal('invalid', 0.5, 'test')  # Invalid direction
        
        with pytest.raises(ValueError):
            Signal('bullish', 1.5, 'test')  # Invalid confidence
    
    def test_signal_immutability(self):
        """Test Signal is immutable (frozen)."""
        signal = Signal('bullish', 0.8, 'test')
        with pytest.raises(AttributeError):
            signal.confidence = 0.9
    
    def test_llm_config(self):
        """Test LLM configuration."""
        config = LLMConfig(
            provider='openai',
            model='gpt-4',
            system_prompt='Test prompt'
        )
        assert config.provider == 'openai'
        assert config.system_prompt == 'Test prompt'
    
    def test_agent_config(self):
        """Test Agent configuration."""
        config = AgentConfig(
            name='TestAgent',
            description='Test',
            llm=LLMConfig(provider='ollama', model='llama3')
        )
        assert config.name == 'TestAgent'
        assert config.llm.provider == 'ollama'


class TestDatabase:
    """Test PostgreSQL database."""
    
    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Test database connects successfully."""
        db = get_database(TEST_DB_URL)
        await db.connect()
        assert db._pool is not None
        await db.disconnect()
    
    @pytest.mark.asyncio
    async def test_list_tickers(self):
        """Test listing tickers."""
        db = get_database(TEST_DB_URL)
        await db.connect()
        
        tickers = await db.list_tickers()
        assert isinstance(tickers, list)
        assert len(tickers) > 0
        
        await db.disconnect()
    
    @pytest.mark.asyncio
    async def test_get_fundamentals(self):
        """Test fundamental data retrieval."""
        db = get_database(TEST_DB_URL)
        await db.connect()
        
        tickers = await db.list_tickers()
        if tickers:
            data = await db.get_fundamentals(tickers[0])
            assert 'ticker' in data
            assert 'pe_ratio' in data
            assert 'market_cap' in data
        
        await db.disconnect()
    
    @pytest.mark.asyncio
    async def test_get_prices(self):
        """Test price history retrieval."""
        db = get_database(TEST_DB_URL)
        await db.connect()
        
        tickers = await db.list_tickers()
        if tickers:
            prices = await db.get_prices(tickers[0], days=30)
            assert isinstance(prices, list)
            if prices:
                assert 'close' in prices[0]
                assert 'volume' in prices[0]
        
        await db.disconnect()
    
    @pytest.mark.asyncio
    async def test_get_news(self):
        """Test news retrieval."""
        db = get_database(TEST_DB_URL)
        await db.connect()
        
        tickers = await db.list_tickers()
        if tickers:
            news = await db.get_news(tickers[0])
            assert isinstance(news, list)
            if news:
                assert 'headline' in news[0]
        
        await db.disconnect()
    
    @pytest.mark.asyncio
    async def test_get_filing(self):
        """Test SEC filing retrieval."""
        db = get_database(TEST_DB_URL)
        await db.connect()
        
        tickers = await db.list_tickers()
        if tickers:
            filing = await db.get_filing(tickers[0])
            assert isinstance(filing, str)
        
        await db.disconnect()


class SimpleTestAgent(Agent):
    """Simple agent for testing."""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 20)
        if pe < 15:
            return Signal('bullish', 0.8, 'Low PE')
        return Signal('neutral', 0.5, 'Fair PE')


class TestAgent:
    """Test Agent base class."""
    
    def test_agent_creation(self):
        """Test basic agent creation."""
        agent = SimpleTestAgent()
        assert agent.config.name == 'SimpleTestAgent'
    
    def test_agent_with_config(self):
        """Test agent with custom config."""
        config = AgentConfig(
            name='CustomAgent',
            description='Test agent'
        )
        agent = SimpleTestAgent(config)
        assert agent.config.name == 'CustomAgent'
    
    @pytest.mark.asyncio
    async def test_agent_analyze(self):
        """Test agent analysis."""
        db = get_database(TEST_DB_URL)
        await db.connect()
        
        agent = SimpleTestAgent()
        tickers = await db.list_tickers()
        
        if tickers:
            data = await db.get_fundamentals(tickers[0])
            signal = agent.analyze(tickers[0], data)
            assert isinstance(signal, Signal)
            assert signal.direction in ('bullish', 'bearish', 'neutral')
            assert 0 <= signal.confidence <= 1
        
        await db.disconnect()
    
    def test_lazy_llm_initialization(self):
        """Test LLM is not initialized without config."""
        agent = SimpleTestAgent()
        assert agent._llm is None
    
    def test_lazy_rag_initialization(self):
        """Test RAG is not initialized without config."""
        agent = SimpleTestAgent()
        assert agent._rag is None


class TestRAGSystem:
    """Test RAG system."""
    
    def test_rag_creation(self):
        """Test RAG system creation."""
        from agent_framework import RAGSystem
        config = RAGConfig(chunk_size=100, top_k=2)
        rag = RAGSystem(config)
        assert rag.config.chunk_size == 100
        assert rag.config.top_k == 2
    
    def test_chunk_text(self):
        """Test text chunking."""
        from agent_framework import RAGSystem
        config = RAGConfig(chunk_size=10, chunk_overlap=2)
        rag = RAGSystem(config)
        
        text = "word " * 50  # 50 words
        chunks = rag.chunk_text(text)
        assert len(chunks) > 1
        assert all(len(chunk.split()) <= 10 for chunk in chunks)
    
    def test_add_document(self):
        """Test adding documents."""
        from agent_framework import RAGSystem
        config = RAGConfig()
        rag = RAGSystem(config)
        
        text = "This is a test document with some content."
        rag.add_document(text)
        assert len(rag.documents) > 0
    
    def test_query(self):
        """Test querying documents."""
        from agent_framework import RAGSystem
        config = RAGConfig(top_k=2)
        rag = RAGSystem(config)
        
        # Add documents
        rag.add_document("Apple is a technology company that makes iPhones.")
        rag.add_document("Microsoft develops software and cloud services.")
        
        # Query
        result = rag.query("Tell me about Apple")
        assert len(result) > 0
        assert 'apple' in result.lower() or 'iphone' in result.lower()
    
    def test_clear(self):
        """Test clearing RAG system."""
        from agent_framework import RAGSystem
        config = RAGConfig()
        rag = RAGSystem(config)
        
        rag.add_document("Test document")
        assert len(rag.documents) > 0
        
        rag.clear()
        assert len(rag.documents) == 0


class TestIntegration:
    """Integration tests."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_simple_agent(self):
        """Test complete flow with simple agent."""
        # Setup
        db = get_database(TEST_DB_URL)
        await db.connect()
        
        agent = SimpleTestAgent()
        
        # Analyze all tickers
        tickers = await db.list_tickers()
        for ticker in tickers[:2]:  # Test first 2 tickers
            data = await db.get_fundamentals(ticker)
            signal = agent.analyze(ticker, data)
            
            # Verify signal
            assert signal.direction in ('bullish', 'bearish', 'neutral')
            assert 0 <= signal.confidence <= 1
            assert len(signal.reasoning) > 0
            assert isinstance(signal.timestamp, datetime)
        
        await db.disconnect()
    
    @pytest.mark.asyncio
    async def test_rag_with_sec_filing(self):
        """Test RAG with actual SEC filing."""
        from agent_framework import RAGSystem
        
        db = get_database(TEST_DB_URL)
        await db.connect()
        
        tickers = await db.list_tickers()
        if tickers:
            filing = await db.get_filing(tickers[0])
            
            if filing:
                config = RAGConfig(chunk_size=300, top_k=3)
                rag = RAGSystem(config)
                rag.add_document(filing)
                
                # Query filing
                result = rag.query("What are the financial performance metrics?")
                assert len(result) > 0
        
        await db.disconnect()


def test_imports():
    """Test all imports work."""
    from agent_framework import (
        Agent, Signal, AgentConfig,
        LLMConfig, RAGConfig,
        LLMClient, RAGSystem,
        Database, get_database,
        api_app, register_agent_instance
    )
    assert Agent is not None
    assert Signal is not None
    assert Database is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--asyncio-mode=auto'])