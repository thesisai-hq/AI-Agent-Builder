"""Mock database with realistic financial data for self-contained examples."""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


class MockDatabase:
    """Self-contained mock database with realistic financial data.
    
    Includes:
    - 4 tickers: AAPL, MSFT, TSLA, JPM
    - Fundamentals (PE, ROE, margins, growth)
    - Price history (90 days)
    - News headlines
    - SEC filing excerpts (for RAG testing)
    """
    
    def __init__(self):
        """Initialize with pre-loaded realistic data."""
        self._fundamentals = self._create_fundamentals()
        self._prices = self._create_prices()
        self._news = self._create_news()
        self._filings = self._create_filings()
    
    def _create_fundamentals(self) -> Dict[str, Dict[str, Any]]:
        """Create realistic fundamental data."""
        return {
            'AAPL': {
                'ticker': 'AAPL',
                'name': 'Apple Inc.',
                'sector': 'Technology',
                'market_cap': 2800000000000,  # $2.8T
                'pe_ratio': 28.5,
                'pb_ratio': 45.2,
                'roe': 150.0,  # %
                'profit_margin': 25.3,
                'revenue_growth': 8.5,  # %
                'debt_to_equity': 1.8,
                'current_ratio': 1.0,
                'dividend_yield': 0.5,
            },
            'MSFT': {
                'ticker': 'MSFT',
                'name': 'Microsoft Corporation',
                'sector': 'Technology',
                'market_cap': 2500000000000,
                'pe_ratio': 32.1,
                'pb_ratio': 12.5,
                'roe': 42.5,
                'profit_margin': 36.7,
                'revenue_growth': 12.3,
                'debt_to_equity': 0.5,
                'current_ratio': 1.8,
                'dividend_yield': 0.8,
            },
            'TSLA': {
                'ticker': 'TSLA',
                'name': 'Tesla Inc.',
                'sector': 'Automotive',
                'market_cap': 800000000000,
                'pe_ratio': 52.3,
                'pb_ratio': 15.8,
                'roe': 28.5,
                'profit_margin': 15.5,
                'revenue_growth': 42.0,
                'debt_to_equity': 0.3,
                'current_ratio': 1.5,
                'dividend_yield': 0.0,
            },
            'JPM': {
                'ticker': 'JPM',
                'name': 'JPMorgan Chase & Co.',
                'sector': 'Financials',
                'market_cap': 450000000000,
                'pe_ratio': 11.2,
                'pb_ratio': 1.6,
                'roe': 15.8,
                'profit_margin': 28.5,
                'revenue_growth': 5.2,
                'debt_to_equity': 1.2,
                'current_ratio': 1.1,
                'dividend_yield': 2.5,
            }
        }
    
    def _create_prices(self) -> Dict[str, List[Dict[str, Any]]]:
        """Create 90 days of realistic price data."""
        prices = {}
        base_prices = {'AAPL': 175, 'MSFT': 380, 'TSLA': 240, 'JPM': 155}
        
        for ticker, base_price in base_prices.items():
            ticker_prices = []
            price = base_price
            
            for i in range(90):
                date = datetime.now() - timedelta(days=90-i)
                # Random walk with slight upward bias
                change = random.uniform(-0.03, 0.035)
                price *= (1 + change)
                
                ticker_prices.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(price * 0.99, 2),
                    'high': round(price * 1.02, 2),
                    'low': round(price * 0.98, 2),
                    'close': round(price, 2),
                    'volume': random.randint(50000000, 150000000)
                })
            
            prices[ticker] = ticker_prices
        
        return prices
    
    def _create_news(self) -> Dict[str, List[Dict[str, str]]]:
        """Create realistic news headlines."""
        return {
            'AAPL': [
                {'date': '2025-10-20', 'headline': 'Apple unveils new AI features in iOS 19', 'sentiment': 'positive'},
                {'date': '2025-10-18', 'headline': 'iPhone sales exceed expectations in Q3', 'sentiment': 'positive'},
                {'date': '2025-10-15', 'headline': 'Analysts raise AAPL price target to $200', 'sentiment': 'positive'},
            ],
            'MSFT': [
                {'date': '2025-10-21', 'headline': 'Microsoft Azure revenue grows 30% YoY', 'sentiment': 'positive'},
                {'date': '2025-10-19', 'headline': 'New enterprise AI tools drive adoption', 'sentiment': 'positive'},
                {'date': '2025-10-16', 'headline': 'Microsoft announces stock buyback program', 'sentiment': 'positive'},
            ],
            'TSLA': [
                {'date': '2025-10-22', 'headline': 'Tesla deliveries miss Q3 estimates', 'sentiment': 'negative'},
                {'date': '2025-10-20', 'headline': 'New Gigafactory announced in Mexico', 'sentiment': 'positive'},
                {'date': '2025-10-17', 'headline': 'FSD Beta shows promising improvements', 'sentiment': 'positive'},
            ],
            'JPM': [
                {'date': '2025-10-21', 'headline': 'JPMorgan reports strong Q3 earnings', 'sentiment': 'positive'},
                {'date': '2025-10-18', 'headline': 'Investment banking revenue up 15%', 'sentiment': 'positive'},
                {'date': '2025-10-16', 'headline': 'Dividend increased by 10%', 'sentiment': 'positive'},
            ]
        }
    
    def _create_filings(self) -> Dict[str, str]:
        """Create SEC filing excerpts for RAG testing."""
        return {
            'AAPL': """
Apple Inc. 10-K Annual Report (Fiscal Year 2024)

Business Overview:
Apple designs, manufactures, and markets smartphones, personal computers, tablets, wearables, 
and accessories worldwide. The Company sells and delivers digital content and applications 
through the App Store, Apple Music, Apple TV+, and other services.

Financial Performance:
Total net sales increased 8% year-over-year to $383 billion. iPhone revenue represented 52% 
of total revenue, Services grew to 22% of revenue with strong margin expansion. The Company's 
gross margin improved to 44.1% from 43.3% in the prior year.

Risk Factors:
The Company faces intense competition in global markets. Supply chain disruptions could impact 
product availability. Regulatory changes in key markets may affect business operations. The 
Company depends on third-party developers for the App Store ecosystem.

Innovation:
Significant investments in artificial intelligence and machine learning capabilities. New 
chipsets deliver 40% performance improvements. Expanding healthcare features in wearables.
Research and development expenses increased to $29 billion, representing 7.6% of revenue.
            """,
            'MSFT': """
Microsoft Corporation 10-K Annual Report (Fiscal Year 2024)

Business Segments:
Microsoft operates through three segments: Productivity and Business Processes, Intelligent 
Cloud, and More Personal Computing. Azure cloud services continue to drive growth with 
30% year-over-year revenue increase.

Financial Highlights:
Total revenue increased to $245 billion, up 12% year-over-year. Operating income grew 18% 
to $115 billion. Cloud services now represent 45% of total revenue with expanding margins. 
Commercial bookings increased 23% driven by Azure and Microsoft 365.

Strategic Initiatives:
Major investments in AI infrastructure and capabilities. Integration of AI across all product 
lines including Office, Windows, and Azure. Partnerships with OpenAI driving innovation. 
Gaming segment strengthened with Activision acquisition.

Competitive Position:
Strong position in enterprise cloud computing. Leading productivity software suite. Growing 
presence in cybersecurity. Expanding gaming ecosystem through Xbox and Game Pass.
            """,
            'TSLA': """
Tesla Inc. 10-K Annual Report (Fiscal Year 2024)

Production and Deliveries:
Tesla delivered 1.8 million vehicles in 2024, representing 38% growth year-over-year. Model Y 
remains the best-selling vehicle globally. New Gigafactories in Texas and Berlin ramping production.

Energy Business:
Energy generation and storage revenue grew 54% to $6 billion. Megapack deployment increased 
significantly. Solar installation growth accelerating. Energy storage backlog reaching record levels.

Autonomous Driving:
Full Self-Driving Beta deployed to over 400,000 customers. Neural network improvements showing 
significant progress. Data collection from fleet approaching 10 billion miles. Hardware 4.0 
computers being installed in new vehicles.

Financial Position:
Strong balance sheet with $29 billion in cash. Operating margin improved to 15.5%. Free cash 
flow generation of $8 billion. No debt maturities until 2025. R&D spending increased to support 
autonomous driving and new vehicle programs.
            """,
            'JPM': """
JPMorgan Chase & Co. 10-K Annual Report (Fiscal Year 2024)

Business Overview:
JPMorgan Chase is a leading global financial services firm operating through four segments: 
Consumer & Community Banking, Corporate & Investment Bank, Commercial Banking, and Asset & 
Wealth Management.

Financial Performance:
Total net revenue of $162 billion, up 7% year-over-year. Net income increased to $49 billion. 
Return on tangible common equity of 18%. Investment banking fees increased 15% driven by 
strong M&A activity. Asset management revenue grew with record AUM of $3.2 trillion.

Credit Quality:
Credit reserves remain strong at $23 billion. Net charge-off rate of 0.25%, below historical 
averages. Commercial real estate portfolio performing well. Consumer credit metrics showing 
resilience despite economic headwinds.

Capital Position:
CET1 ratio of 14.2%, well above regulatory requirements. Returned $35 billion to shareholders 
through dividends and buybacks. Strong liquidity position with $1.4 trillion in deposits.
            """
        }
    
    def get_fundamentals(self, ticker: str) -> Dict[str, Any]:
        """Get fundamental data for ticker."""
        return self._fundamentals.get(ticker, {})
    
    def get_prices(self, ticker: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get recent price history."""
        prices = self._prices.get(ticker, [])
        return prices[-days:]
    
    def get_news(self, ticker: str) -> List[Dict[str, str]]:
        """Get recent news for ticker."""
        return self._news.get(ticker, [])
    
    def get_filing(self, ticker: str) -> str:
        """Get SEC filing excerpt."""
        return self._filings.get(ticker, "")
    
    def list_tickers(self) -> List[str]:
        """Get all available tickers."""
        return list(self._fundamentals.keys())