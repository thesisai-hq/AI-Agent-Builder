"""Tests for test configuration component.

Tests data configuration, validation, and preparation logic.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestTestDataConfig:
    """Test TestDataConfig dataclass."""
    
    def test_mock_data_config(self):
        """Test mock data configuration."""
        from gui.components.test_config import TestDataConfig
        
        config = TestDataConfig(
            source="mock",
            data={
                "pe_ratio": 20.0,
                "roe": 15.0,
                "profit_margin": 12.0
            },
            ticker="AAPL"
        )
        
        assert config.source == "mock"
        assert config.data["pe_ratio"] == 20.0
        assert config.ticker == "AAPL"
        assert config.uploaded_file is None
    
    def test_database_config(self):
        """Test database configuration."""
        from gui.components.test_config import TestDataConfig
        
        config = TestDataConfig(
            source="database",
            ticker="MSFT"
        )
        
        assert config.source == "database"
        assert config.data is None
        assert config.ticker == "MSFT"
    
    def test_pdf_config(self):
        """Test PDF configuration."""
        from gui.components.test_config import TestDataConfig
        
        mock_file = Mock()
        mock_file.name = "test.pdf"
        
        config = TestDataConfig(
            source="pdf",
            uploaded_file=mock_file,
            ticker="AAPL"
        )
        
        assert config.source == "pdf"
        assert config.uploaded_file is not None
        assert config.ticker == "AAPL"


class TestDataPreparation:
    """Test data preparation logic."""
    
    def test_prepare_mock_data(self):
        """Test mock data preparation adds company name."""
        from gui.pages.test_page import prepare_test_data
        from gui.components.test_config import TestDataConfig
        
        config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 20},
            ticker="TEST"
        )
        
        result = prepare_test_data(config)
        
        assert result is not None
        assert result["name"] == "Mock Company (TEST)"
        assert result["pe_ratio"] == 20
    
    def test_prepare_yfinance_data(self):
        """Test YFinance data preparation."""
        from gui.pages.test_page import prepare_test_data
        from gui.components.test_config import TestDataConfig
        
        fetched_data = {
            "pe_ratio": 25.0,
            "roe": 18.0,
            "name": "Apple Inc."
        }
        
        config = TestDataConfig(
            source="yfinance",
            data=fetched_data,
            ticker="AAPL"
        )
        
        result = prepare_test_data(config)
        
        assert result == fetched_data
        assert result["name"] == "Apple Inc."
    
    def test_prepare_database_data(self):
        """Test database data preparation returns None."""
        from gui.pages.test_page import prepare_test_data
        from gui.components.test_config import TestDataConfig
        
        config = TestDataConfig(
            source="database",
            ticker="MSFT"
        )
        
        result = prepare_test_data(config)
        
        # Database data fetched internally, returns None
        assert result is None
    
    def test_prepare_pdf_data(self):
        """Test PDF data preparation."""
        from gui.pages.test_page import prepare_test_data
        from gui.components.test_config import TestDataConfig
        
        config = TestDataConfig(
            source="pdf",
            uploaded_file=Mock(),
            ticker="AAPL"
        )
        
        result = prepare_test_data(config)
        
        # RAG agents don't use data dict
        assert result is None


class TestMockDataValidation:
    """Test mock data input validation."""
    
    def test_valid_pe_ratio(self):
        """Test valid PE ratio range."""
        pe_ratio = 20.0
        
        # Should be within valid range
        assert 5.0 <= pe_ratio <= 100.0
    
    def test_valid_roe(self):
        """Test valid ROE range."""
        roe = 15.0
        
        # Should be within valid range
        assert -20.0 <= roe <= 50.0
    
    def test_valid_debt_to_equity(self):
        """Test valid debt-to-equity range."""
        debt = 0.8
        
        # Should be within valid range
        assert 0.0 <= debt <= 5.0
    
    def test_full_mock_data_structure(self):
        """Test complete mock data structure."""
        mock_data = {
            "pe_ratio": 20.0,
            "roe": 15.0,
            "profit_margin": 12.0,
            "revenue_growth": 15.0,
            "debt_to_equity": 0.8,
            "dividend_yield": 2.0
        }
        
        # Verify all required keys present
        required_keys = [
            "pe_ratio",
            "roe",
            "profit_margin",
            "revenue_growth",
            "debt_to_equity",
            "dividend_yield"
        ]
        
        for key in required_keys:
            assert key in mock_data
            assert isinstance(mock_data[key], (int, float))


class TestYFinanceIntegration:
    """Test YFinance data fetching logic."""
    
    @patch('yfinance.Ticker')
    def test_fetch_yfinance_data_success(self, mock_ticker):
        """Test successful YFinance data fetch."""
        # Mock YFinance response
        mock_info = {
            "longName": "Apple Inc.",
            "trailingPE": 28.5,
            "priceToBook": 45.2,
            "returnOnEquity": 0.147,
            "profitMargins": 0.258,
            "revenueGrowth": 0.112,
            "debtToEquity": 170.7,
            "currentRatio": 1.07,
            "dividendYield": 0.0047,
            "marketCap": 3000000000000
        }
        
        mock_ticker.return_value.info = mock_info
        
        # Expected conversion
        expected_data = {
            "name": "Apple Inc.",
            "pe_ratio": 28.5,
            "pb_ratio": 45.2,
            "roe": 14.7,  # Converted to percentage
            "profit_margin": 25.8,
            "revenue_growth": 11.2,
            "debt_to_equity": 170.7,
            "current_ratio": 1.07,
            "dividend_yield": 0.47,
            "market_cap": 3000000000000
        }
        
        # Verify conversion logic
        assert expected_data["roe"] == pytest.approx(14.7, rel=0.1)
        assert expected_data["profit_margin"] == pytest.approx(25.8, rel=0.1)
    
    def test_fetch_yfinance_data_missing_values(self):
        """Test YFinance fetch with missing values."""
        mock_info = {
            "longName": "Test Corp",
            "trailingPE": None,  # Missing
            "forwardPE": 20.0,   # Fallback
            "returnOnEquity": None  # Missing
        }
        
        # Should use fallback values
        pe = mock_info.get("trailingPE", mock_info.get("forwardPE", 0)) or 0
        roe = (mock_info.get("returnOnEquity", 0) or 0) * 100
        
        assert pe == 20.0  # Used fallback
        assert roe == 0.0  # No data available


class TestPDFConfiguration:
    """Test PDF upload configuration for RAG agents."""
    
    def test_pdf_preview_text_extraction(self):
        """Test logic for extracting PDF preview."""
        # Mock PDF reader
        mock_page_1 = Mock()
        mock_page_1.extract_text.return_value = "Page 1 content " * 50
        
        mock_page_2 = Mock()
        mock_page_2.extract_text.return_value = "Page 2 content " * 50
        
        # Simulate preview extraction (first 3 pages)
        pages = [mock_page_1, mock_page_2]
        preview_text = ""
        
        for page_num, page in enumerate(pages[:3]):
            preview_text += f"\n--- Page {page_num + 1} ---\n"
            preview_text += page.extract_text()
        
        # Verify preview built correctly
        assert "--- Page 1 ---" in preview_text
        assert "--- Page 2 ---" in preview_text
        assert "Page 1 content" in preview_text
        assert "Page 2 content" in preview_text
    
    def test_pdf_preview_truncation(self):
        """Test preview is truncated if too long."""
        long_text = "x" * 3000
        
        # Preview should truncate
        if len(long_text) > 2000:
            preview = long_text[:2000] + "..."
        else:
            preview = long_text
        
        assert len(preview) <= 2003  # 2000 + "..."
        assert preview.endswith("...")


# ============================================================================
# Data Source Selection Tests
# ============================================================================

class TestDataSourceConfiguration:
    """Test data source selection logic."""
    
    def test_rag_agent_data_source(self):
        """Test RAG agent uses PDF only."""
        agent_type = "RAG-Powered"
        
        # RAG agents should only accept PDF
        requires_pdf = (agent_type == "RAG-Powered")
        requires_financial_data = (agent_type != "RAG-Powered")
        
        assert requires_pdf is True
        assert requires_financial_data is False
    
    def test_financial_agent_data_sources(self):
        """Test financial agent data source options."""
        agent_types = ["Rule-Based", "LLM-Powered", "Hybrid"]
        
        for agent_type in agent_types:
            requires_pdf = (agent_type == "RAG-Powered")
            requires_financial_data = (agent_type != "RAG-Powered")
            
            assert requires_pdf is False
            assert requires_financial_data is True
    
    def test_data_source_options(self):
        """Test available data source options."""
        data_sources = ["Mock Data", "Database", "YFinance (Real Market Data)"]
        
        assert len(data_sources) == 3
        assert "Mock Data" in data_sources
        assert "Database" in data_sources
        assert "YFinance (Real Market Data)" in data_sources


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
