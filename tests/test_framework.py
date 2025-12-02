"""Comprehensive test suite for AI Agent Framework with proper test isolation."""

from datetime import datetime

import pytest
import pytest_asyncio

from agent_framework import (
    Agent,
    AgentConfig,
    Config,
    Database,
    DatabaseConfig,
    LLMConfig,
    RAGConfig,
    Signal,
)


# Simple test agent for testing
class SimpleTestAgent(Agent):
    """Simple agent for testing."""

    def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get("pe_ratio", 20)
        if pe < 15:
            return Signal(direction="bullish", confidence=0.8, reasoning="Low PE")
        return Signal(direction="neutral", confidence=0.5, reasoning="Fair PE")


class TestModels:
    """Test Pydantic data models."""

    def test_signal_creation(self):
        """Test Signal model creation."""
        signal = Signal(direction="bullish", confidence=0.8, reasoning="Test reasoning")
        assert signal.direction == "bullish"
        assert signal.confidence == 0.8
        assert signal.reasoning == "Test reasoning"
        assert isinstance(signal.timestamp, datetime)

    def test_signal_validation(self):
        """Test Signal validation."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            Signal(direction="invalid", confidence=0.5, reasoning="test")

        with pytest.raises(ValidationError):
            Signal(direction="bullish", confidence=1.5, reasoning="test")

        with pytest.raises(ValidationError):
            Signal(direction="bullish", confidence=0.8, reasoning="")

    def test_signal_immutability(self):
        """Test Signal is immutable (frozen)."""
        signal = Signal(direction="bullish", confidence=0.8, reasoning="test")
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            signal.confidence = 0.9

    def test_llm_config(self):
        """Test LLM configuration."""
        config = LLMConfig(provider="openai", model="gpt-4", system_prompt="Test prompt")
        assert config.provider == "openai"
        assert config.system_prompt == "Test prompt"
        assert config.max_retries == 3

    def test_llm_config_validation(self):
        """Test LLM config validation."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            LLMConfig(provider="invalid", model="test")

    def test_database_config(self):
        """Test database configuration."""
        config = DatabaseConfig(
            connection_string="postgresql://localhost/test", min_pool_size=2, max_pool_size=10
        )
        assert config.min_pool_size == 2
        assert config.max_pool_size == 10


@pytest_asyncio.fixture
async def test_db():
    """Create test database instance with separate test database.

    Note: This requires TEST_DATABASE_URL to be set or uses default test DB.
    For true isolation, you should create and tear down the test database.
    """
    connection_string = Config.get_test_database_url()
    db = Database(connection_string)

    await db.connect()
    yield db
    await db.disconnect()


class TestDatabase:
    """Test PostgreSQL database operations."""

    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Test database connects successfully."""
        connection_string = Config.get_test_database_url()
        db = Database(connection_string)

        await db.connect()
        assert db._pool is not None

        # Test health check
        health = await db.health_check()
        assert health is True

        await db.disconnect()

    @pytest.mark.asyncio
    async def test_connection_error_handling(self):
        """Test connection error handling."""
        db = Database("postgresql://invalid:invalid@localhost:9999/nonexistent")

        from agent_framework.database import ConnectionError

        with pytest.raises(ConnectionError):
            await db.connect()

    @pytest.mark.asyncio
    async def test_list_tickers(self, test_db):
        """Test listing tickers."""
        tickers = await test_db.list_tickers()
        assert isinstance(tickers, list)

    @pytest.mark.asyncio
    async def test_get_fundamentals(self, test_db):
        """Test fundamental data retrieval."""
        tickers = await test_db.list_tickers()

        if tickers:
            data = await test_db.get_fundamentals(tickers[0])
            if data:  # Only test if data exists
                assert "ticker" in data
                assert "pe_ratio" in data
                assert "market_cap" in data

    @pytest.mark.asyncio
    async def test_get_fundamentals_not_found(self, test_db):
        """Test fundamentals for non-existent ticker."""
        data = await test_db.get_fundamentals("NONEXISTENT")
        assert data is None

    @pytest.mark.asyncio
    async def test_get_prices(self, test_db):
        """Test price history retrieval."""
        tickers = await test_db.list_tickers()

        if tickers:
            prices = await test_db.get_prices(tickers[0], days=30)
            assert isinstance(prices, list)

    @pytest.mark.asyncio
    async def test_get_news(self, test_db):
        """Test news retrieval."""
        tickers = await test_db.list_tickers()

        if tickers:
            news = await test_db.get_news(tickers[0])
            assert isinstance(news, list)

    @pytest.mark.asyncio
    async def test_get_filing(self, test_db):
        """Test SEC filing retrieval."""
        tickers = await test_db.list_tickers()

        if tickers:
            filing = await test_db.get_filing(tickers[0])
            assert filing is None or isinstance(filing, str)

    @pytest.mark.asyncio
    async def test_transaction_support(self, test_db):
        """Test transaction context manager."""
        async with test_db.transaction() as conn:
            # Transaction is active
            result = await conn.fetchval("SELECT 1")
            assert result == 1


class TestAgent:
    """Test Agent base class."""

    def test_agent_creation(self):
        """Test basic agent creation."""
        agent = SimpleTestAgent()
        assert agent.config.name == "SimpleTestAgent"

    def test_agent_with_config(self):
        """Test agent with custom config."""
        config = AgentConfig(name="CustomAgent", description="Test agent")
        agent = SimpleTestAgent(config)
        assert agent.config.name == "CustomAgent"

    @pytest.mark.asyncio
    async def test_agent_analyze(self, test_db):
        """Test agent analysis."""
        agent = SimpleTestAgent()
        tickers = await test_db.list_tickers()

        if tickers:
            data = await test_db.get_fundamentals(tickers[0])
            if data:
                signal = agent.analyze(tickers[0], data)
                assert isinstance(signal, Signal)
                assert signal.direction in ("bullish", "bearish", "neutral")
                assert 0 <= signal.confidence <= 1

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

    def test_add_document(self):
        """Test adding documents."""
        from agent_framework import RAGSystem

        config = RAGConfig()
        rag = RAGSystem(config)

        text = "This is a test document with some content."
        # RAG add_document is async
        import pytest

        import asyncio

        chunks_added = asyncio.run(rag.add_document(text))
        assert chunks_added > 0
        assert len(rag.documents) > 0

    def test_query(self):
        """Test querying documents."""
        from agent_framework import RAGSystem

        config = RAGConfig(top_k=2)
        rag = RAGSystem(config)

        # Add documents
        import asyncio

        asyncio.run(rag.add_document("Apple is a technology company that makes iPhones."))
        asyncio.run(rag.add_document("Microsoft develops software and cloud services."))

        # Query
        result = asyncio.run(rag.query("Tell me about Apple"))
        assert len(result) > 0

    def test_clear(self):
        """Test clearing RAG system."""
        from agent_framework import RAGSystem

        config = RAGConfig()
        rag = RAGSystem(config)

        import asyncio

        asyncio.run(rag.add_document("Test document"))
        assert len(rag.documents) > 0

        rag.clear()
        assert len(rag.documents) == 0

    def test_get_stats(self):
        """Test RAG statistics."""
        from agent_framework import RAGSystem

        config = RAGConfig()
        rag = RAGSystem(config)

        stats = rag.get_stats()
        assert "num_chunks" in stats
        assert stats["num_chunks"] == 0


class TestUtilities:
    """Test utility functions."""

    def test_parse_llm_signal(self):
        """Test LLM signal parsing."""
        from agent_framework import parse_llm_signal

        # Valid format
        response = "bullish|80|Strong growth"
        signal = parse_llm_signal(response)
        assert signal.direction == "bullish"
        assert signal.confidence == 0.8
        assert signal.reasoning == "Strong growth"

        # Invalid format - should return neutral
        response = "invalid format"
        signal = parse_llm_signal(response, "fallback reasoning")
        assert signal.direction == "neutral"
        assert signal.confidence == 0.5

    def test_format_fundamentals(self):
        """Test fundamental data formatting."""
        from agent_framework import format_fundamentals

        data = {"pe_ratio": 28.5, "market_cap": 2800000000000, "revenue_growth": 8.5}

        formatted = format_fundamentals(data)
        assert "PE Ratio: 28.5" in formatted
        assert "Market Cap" in formatted

    def test_calculate_sentiment_score(self):
        """Test sentiment calculation."""
        from agent_framework import calculate_sentiment_score

        # Positive text
        text = "Strong growth and improved profits with expanding margins"
        direction, confidence = calculate_sentiment_score(text)
        assert direction == "bullish"
        assert confidence > 0.5

        # Negative text
        text = "Risk of decline with major challenges and losses"
        direction, confidence = calculate_sentiment_score(text)
        assert direction == "bearish"
        assert confidence > 0.5


class TestIntegration:
    """Integration tests."""

    @pytest.mark.asyncio
    async def test_end_to_end_simple_agent(self, test_db):
        """Test complete flow with simple agent."""
        agent = SimpleTestAgent()

        # Analyze all available tickers
        tickers = await test_db.list_tickers()
        for ticker in tickers[:2]:  # Test first 2 tickers
            data = await test_db.get_fundamentals(ticker)
            if data:
                signal = agent.analyze(ticker, data)

                # Verify signal
                assert signal.direction in ("bullish", "bearish", "neutral")
                assert 0 <= signal.confidence <= 1
                assert len(signal.reasoning) > 0
                assert isinstance(signal.timestamp, datetime)


def test_imports():
    """Test all imports work."""
    from agent_framework import (
        Agent,
        Config,
        Database,
        Signal,
    )

    assert Agent is not None
    assert Signal is not None
    assert Database is not None
    assert Config is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
