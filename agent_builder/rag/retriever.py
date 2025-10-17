"""Data Retrieval for RAG System"""

from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DataRetriever:
    """Retrieves relevant data from database for RAG context"""

    def __init__(self, db):
        self.db = db

    def get_fundamental_context(self, ticker: str) -> str:
        """Get fundamental analysis context"""
        try:
            data = self.db.execute_one(
                """SELECT ticker, company_name, sector, industry, pe_ratio, roe, 
                   profit_margin, revenue_growth, debt_to_equity, dividend_yield
                   FROM mock_fundamentals WHERE ticker = %s""",
                (ticker,),
            )

            if not data:
                return f"No fundamental data available for {ticker}."

            context = f"""Company: {data['company_name']} ({ticker})
Sector: {data['sector']} | Industry: {data['industry']}

Key Metrics:
- P/E Ratio: {data['pe_ratio']}
- ROE: {data['roe']}%
- Profit Margin: {data['profit_margin']}%
- Revenue Growth: {data['revenue_growth']}%
- Debt/Equity: {data['debt_to_equity']}
- Dividend Yield: {data['dividend_yield']}%"""

            return context
        except Exception as e:
            logger.error(f"Error: {e}")
            return ""

    def get_sec_filing_context(self, ticker: str) -> str:
        """Get SEC filing with full text"""
        try:
            filing = self.db.execute_one(
                """SELECT filing_type, filing_date, revenue, net_income,
                   filing_text, sentiment_score
                   FROM mock_sec_filings WHERE ticker = %s 
                   ORDER BY filing_date DESC LIMIT 1""",
                (ticker,),
            )

            if not filing:
                return f"No SEC filings for {ticker}."

            text = filing.get("filing_text", "")
            excerpt = text[:1000] + "..." if len(text) > 1000 else text

            return f"""SEC Filing ({filing['filing_type']}):
{excerpt}"""
        except Exception as e:
            logger.error(f"Error: {e}")
            return ""

    def get_all_sec_filings(self, ticker: str) -> List[Dict]:
        """Get all SEC filings for vector indexing"""
        try:
            return self.db.execute(
                """SELECT ticker, filing_type, filing_date, filing_text
                   FROM mock_sec_filings WHERE ticker = %s""",
                (ticker,),
            )
        except:
            return []


class ContextBuilder:
    """Builds comprehensive context for LLM prompts"""

    def __init__(self, retriever: DataRetriever):
        self.retriever = retriever

    def build_context(self, ticker: str, include_sec: bool = True) -> str:
        """Build context with fundamental + SEC data"""
        parts = []

        fund = self.retriever.get_fundamental_context(ticker)
        if fund:
            parts.append(fund)

        if include_sec:
            sec = self.retriever.get_sec_filing_context(ticker)
            if sec:
                parts.append(sec)

        return "\\n\\n".join(parts)
