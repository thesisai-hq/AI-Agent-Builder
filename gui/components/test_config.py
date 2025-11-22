"""Test configuration component.

Handles test data configuration for different agent types (RAG, financial).
Returns standardized TestDataConfig object.
"""

from dataclasses import dataclass
from typing import Optional, Any

import streamlit as st


@dataclass
class TestDataConfig:
    """Standardized test data configuration."""
    source: str  # "mock", "database", "yfinance", "pdf"
    data: Optional[dict] = None  # Financial data for non-RAG agents
    uploaded_file: Optional[Any] = None  # PDF for RAG agents
    ticker: str = "AAPL"  # Ticker symbol


def configure_test_data(agent_type: str, ticker: str) -> Optional[TestDataConfig]:
    """Configure test data based on agent type.
    
    Args:
        agent_type: Type of agent ("RAG-Powered", "Rule-Based", etc.)
        ticker: Ticker symbol
    
    Returns:
        TestDataConfig or None if configuration incomplete
    """
    if agent_type == "RAG-Powered":
        return _configure_rag_test_data(ticker)
    else:
        return _configure_financial_test_data(ticker)


def _configure_rag_test_data(ticker: str) -> Optional[TestDataConfig]:
    """Configure PDF upload for RAG agents.
    
    Args:
        ticker: Ticker symbol
    
    Returns:
        TestDataConfig with uploaded file or None
    """
    st.subheader("📄 Document Upload")
    st.markdown("RAG agents analyze documents. Upload a PDF to test:")
    
    uploaded_file = st.file_uploader(
        "Drag and drop PDF here",
        type=["pdf"],
        help="Upload SEC filing, earnings report, or any financial document",
    )
    
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        _show_pdf_preview(uploaded_file)
        
        return TestDataConfig(
            source="pdf",
            uploaded_file=uploaded_file,
            ticker=ticker
        )
    
    return None


def _show_pdf_preview(uploaded_file) -> None:
    """Show preview of uploaded PDF.
    
    Args:
        uploaded_file: Streamlit uploaded file object
    """
    with st.expander("Preview Document Text"):
        try:
            from PyPDF2 import PdfReader
            
            pdf_reader = PdfReader(uploaded_file)
            preview_text = ""
            
            for page_num, page in enumerate(pdf_reader.pages[:3]):
                preview_text += f"\n--- Page {page_num + 1} ---\n"
                preview_text += page.extract_text()
            
            st.text_area(
                "Document Preview (first 3 pages)",
                preview_text[:2000] + "..." if len(preview_text) > 2000 else preview_text,
                height=200,
            )
            st.caption(f"Total pages: {len(pdf_reader.pages)}")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")


def _configure_financial_test_data(ticker: str) -> TestDataConfig:
    """Configure financial data (mock, database, or YFinance).
    
    Args:
        ticker: Ticker symbol
    
    Returns:
        TestDataConfig with appropriate data
    """
    st.subheader("Test Data")
    
    data_source = st.radio(
        "Data Source",
        ["Mock Data", "Database", "YFinance (Real Market Data)"],
        help="Mock: Fictional data for testing | Database: Sample data | YFinance: Real current market data",
    )
    
    if data_source == "Mock Data":
        data = _configure_mock_data()
        return TestDataConfig(source="mock", data=data, ticker=ticker)
    
    elif data_source == "YFinance (Real Market Data)":
        data = _fetch_yfinance_data(ticker)
        if data:
            return TestDataConfig(source="yfinance", data=data, ticker=ticker)
        else:
            return TestDataConfig(source="yfinance", data=None, ticker=ticker)
    
    else:  # Database
        return TestDataConfig(source="database", ticker=ticker)


def _configure_mock_data() -> dict:
    """Configure mock financial data through input form.
    
    Returns:
        Dictionary of mock financial metrics
    """
    st.subheader("Mock Financial Data")
    
    # Import metrics here to avoid circular dependency
    from gui.metrics import MetricDefinitions
    metrics = MetricDefinitions.get_all_metrics()
    
    mock_data = {}
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        pe_def = metrics["pe_ratio"]
        mock_data["pe_ratio"] = st.number_input(
            "PE Ratio", 5.0, 100.0, 20.0, help=pe_def["tooltip"]
        )
        
        growth_def = metrics["revenue_growth"]
        mock_data["revenue_growth"] = st.number_input(
            "Revenue Growth (%)", -20.0, 100.0, 15.0, help=growth_def["tooltip"]
        )
    
    with col_b:
        margin_def = metrics["profit_margin"]
        mock_data["profit_margin"] = st.number_input(
            "Profit Margin (%)", -10.0, 50.0, 12.0, help=margin_def["tooltip"]
        )
        
        roe_def = metrics["roe"]
        mock_data["roe"] = st.number_input(
            "ROE (%)", -20.0, 50.0, 15.0, help=roe_def["tooltip"]
        )
    
    with col_c:
        debt_def = metrics["debt_to_equity"]
        mock_data["debt_to_equity"] = st.number_input(
            "Debt/Equity", 0.0, 5.0, 0.8, help=debt_def["tooltip"]
        )
        
        div_def = metrics["dividend_yield"]
        mock_data["dividend_yield"] = st.number_input(
            "Dividend Yield (%)", 0.0, 10.0, 2.0, help=div_def["tooltip"]
        )
    
    return mock_data


def _fetch_yfinance_data(ticker: str) -> Optional[dict]:
    """Fetch real market data from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Dictionary of financial metrics or None if fetch fails
    """
    st.info("🌐 **Real Market Data:** Will fetch current data from Yahoo Finance")
    st.caption(f"Data for: **{ticker}**")
    
    with st.spinner(f"Fetching real data for {ticker}..."):
        try:
            import yfinance as yf
            
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract relevant fundamentals
            mock_data = {
                "name": info.get("longName", ticker),
                "pe_ratio": info.get("trailingPE", info.get("forwardPE", 0)) or 0,
                "pb_ratio": info.get("priceToBook", 0) or 0,
                "roe": (info.get("returnOnEquity", 0) or 0) * 100,
                "profit_margin": (info.get("profitMargins", 0) or 0) * 100,
                "revenue_growth": (info.get("revenueGrowth", 0) or 0) * 100,
                "debt_to_equity": info.get("debtToEquity", 0) or 0,
                "current_ratio": info.get("currentRatio", 0) or 0,
                "dividend_yield": (info.get("dividendYield", 0) or 0) * 100,
                "market_cap": info.get("marketCap", 0) or 0,
            }
            
            st.success("✅ Real data fetched successfully!")
            
            # Display fetched data
            _show_fetched_data(mock_data)
            
            return mock_data
            
        except ImportError:
            st.error("❌ yfinance not installed. Run: pip install yfinance")
            st.info("💡 Or run ./gui/setup.sh to install all dependencies")
            return None
            
        except Exception as e:
            st.error(f"❌ Error fetching data for {ticker}: {str(e)}")
            st.info(
                "💡 **Tips:**\n"
                "- Check ticker symbol is correct (e.g., AAPL not Apple)\n"
                "- Check internet connection\n"
                "- Try a different ticker"
            )
            return None


def _show_fetched_data(data: dict) -> None:
    """Display fetched financial data.
    
    Args:
        data: Dictionary of financial metrics
    """
    with st.expander("📊 View Fetched Data"):
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("PE Ratio", f"{data['pe_ratio']:.1f}")
            st.metric("Revenue Growth", f"{data['revenue_growth']:.1f}%")
        
        with col_b:
            st.metric("Profit Margin", f"{data['profit_margin']:.1f}%")
            st.metric("ROE", f"{data['roe']:.1f}%")
        
        with col_c:
            st.metric("Debt/Equity", f"{data['debt_to_equity']:.1f}")
            st.metric("Dividend Yield", f"{data['dividend_yield']:.1f}%")
