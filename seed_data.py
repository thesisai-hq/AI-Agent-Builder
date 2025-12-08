"""Seed PostgreSQL database with sample financial data.

Compatible with thesis-data-fabric production database schema.

⚠️ DATA DISCLAIMER:
ALL DATA IN THIS FILE IS SYNTHETIC/FICTIONAL FOR EDUCATIONAL PURPOSES ONLY.
Should NEVER be used for real investment decisions.
See DISCLAIMER.md for complete legal terms.
"""

import asyncio
import json
import random
import uuid
from datetime import datetime, timedelta

from agent_framework import Config
from agent_framework.database import Database

# =============================================================================
# CHUNK SIZE for filing text (matches thesis-data-fabric)
# =============================================================================
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks for LLM processing."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


# =============================================================================
# SEED FILINGS (replaces seed_fundamentals)
# =============================================================================
async def seed_filings(db: Database):
    """Insert sample SEC filings with financial_data JSON."""
    print("📄 Seeding SEC filings...")

    filings_data = [
        {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "cik": "0000320193",
            "financial_data": {
                "sector": "Technology",
                "market_cap": 2800000000000,
                "pe_ratio": 28.5,
                "pb_ratio": 45.2,
                "roe": 150.0,
                "profit_margin": 25.3,
                "revenue_growth": 8.5,
                "debt_to_equity": 1.8,
                "current_ratio": 1.0,
                "dividend_yield": 0.5,
            },
            "content": """Apple Inc. 10-K Annual Report (Fiscal Year 2024)

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
Research and development expenses increased to $29 billion, representing 7.6% of revenue.""",
        },
        {
            "ticker": "MSFT",
            "company_name": "Microsoft Corporation",
            "cik": "0000789019",
            "financial_data": {
                "sector": "Technology",
                "market_cap": 2500000000000,
                "pe_ratio": 32.1,
                "pb_ratio": 12.5,
                "roe": 42.5,
                "profit_margin": 36.7,
                "revenue_growth": 12.3,
                "debt_to_equity": 0.5,
                "current_ratio": 1.8,
                "dividend_yield": 0.8,
            },
            "content": """Microsoft Corporation 10-K Annual Report (Fiscal Year 2024)

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
presence in cybersecurity. Expanding gaming ecosystem through Xbox and Game Pass.""",
        },
        {
            "ticker": "TSLA",
            "company_name": "Tesla Inc.",
            "cik": "0001318605",
            "financial_data": {
                "sector": "Automotive",
                "market_cap": 800000000000,
                "pe_ratio": 52.3,
                "pb_ratio": 15.8,
                "roe": 28.5,
                "profit_margin": 15.5,
                "revenue_growth": 42.0,
                "debt_to_equity": 0.3,
                "current_ratio": 1.5,
                "dividend_yield": 0.0,
            },
            "content": """Tesla Inc. 10-K Annual Report (Fiscal Year 2024)

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
autonomous driving and new vehicle programs.""",
        },
        {
            "ticker": "JPM",
            "company_name": "JPMorgan Chase & Co.",
            "cik": "0000019617",
            "financial_data": {
                "sector": "Financials",
                "market_cap": 450000000000,
                "pe_ratio": 11.2,
                "pb_ratio": 1.6,
                "roe": 15.8,
                "profit_margin": 28.5,
                "revenue_growth": 5.2,
                "debt_to_equity": 1.2,
                "current_ratio": 1.1,
                "dividend_yield": 2.5,
            },
            "content": """JPMorgan Chase & Co. 10-K Annual Report (Fiscal Year 2024)

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
through dividends and buybacks. Strong liquidity position with $1.4 trillion in deposits.""",
        },
    ]

    for data in filings_data:
        filing_id = f"{data['ticker']}-10K-2024-{uuid.uuid4().hex[:8]}"

        # Insert filing metadata
        await db.add_filing(
            {
                "filing_id": filing_id,
                "ticker": data["ticker"],
                "cik": data["cik"],
                "company_name": data["company_name"],
                "filing_type": "10-K",
                "filing_date": datetime.now().date(),
                "filing_url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={data['cik']}",
                "is_xbrl": True,
                "sections": json.dumps(["Business", "Risk Factors", "Financial Data"]),
                "financial_data": json.dumps(data["financial_data"]),
            }
        )

        # Insert chunked content
        chunks = chunk_text(data["content"])
        for idx, chunk in enumerate(chunks):
            await db.add_filing_chunk(filing_id, idx, chunk)

        print(f"  ✓ Added 10-K for {data['ticker']} ({len(chunks)} chunks)")


# =============================================================================
# SEED PRICES
# =============================================================================
async def seed_prices(db: Database):
    """Insert sample price data into thesis_data.prices."""
    print("\n💹 Seeding price history...")

    base_prices = {"AAPL": 175, "MSFT": 380, "TSLA": 240, "JPM": 155}

    for ticker, base_price in base_prices.items():
        price = base_price
        count = 0

        for i in range(90):
            date = datetime.now() - timedelta(days=90 - i)
            change = random.uniform(-0.03, 0.035)
            price *= 1 + change

            await db.add_price(
                ticker,
                {
                    "date": date.date(),
                    "open": round(price * 0.99, 2),
                    "high": round(price * 1.02, 2),
                    "low": round(price * 0.98, 2),
                    "close": round(price, 2),
                    "volume": random.randint(50000000, 150000000),
                    "source": "mock",
                },
            )
            count += 1

        print(f"  ✓ Added {count} price records for {ticker}")


# =============================================================================
# SEED NEWS
# =============================================================================
async def seed_news(db: Database):
    """Insert sample news into thesis_data.stock_news."""
    print("\n📰 Seeding news...")

    news_data = {
        "AAPL": [
            {
                "headline": "Apple unveils new AI features in iOS 19",
                "sentiment_label": "positive",
                "sentiment_score": 0.75,
            },
            {
                "headline": "iPhone sales exceed expectations in Q3",
                "sentiment_label": "positive",
                "sentiment_score": 0.82,
            },
            {
                "headline": "Analysts raise AAPL price target to $200",
                "sentiment_label": "positive",
                "sentiment_score": 0.68,
            },
        ],
        "MSFT": [
            {
                "headline": "Microsoft Azure revenue grows 30% YoY",
                "sentiment_label": "positive",
                "sentiment_score": 0.85,
            },
            {
                "headline": "New enterprise AI tools drive adoption",
                "sentiment_label": "positive",
                "sentiment_score": 0.72,
            },
            {
                "headline": "Microsoft announces stock buyback program",
                "sentiment_label": "positive",
                "sentiment_score": 0.65,
            },
        ],
        "TSLA": [
            {
                "headline": "Tesla deliveries miss Q3 estimates",
                "sentiment_label": "negative",
                "sentiment_score": -0.45,
            },
            {
                "headline": "New Gigafactory announced in Mexico",
                "sentiment_label": "positive",
                "sentiment_score": 0.58,
            },
            {
                "headline": "FSD Beta shows promising improvements",
                "sentiment_label": "positive",
                "sentiment_score": 0.62,
            },
        ],
        "JPM": [
            {
                "headline": "JPMorgan reports strong Q3 earnings",
                "sentiment_label": "positive",
                "sentiment_score": 0.78,
            },
            {
                "headline": "Investment banking revenue up 15%",
                "sentiment_label": "positive",
                "sentiment_score": 0.65,
            },
            {
                "headline": "Dividend increased by 10%",
                "sentiment_label": "positive",
                "sentiment_score": 0.55,
            },
        ],
    }

    base_date = datetime.now()
    for ticker, articles in news_data.items():
        for i, article in enumerate(articles):
            article_id = f"{ticker}-{base_date.strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
            published_at = base_date - timedelta(days=i * 2, hours=random.randint(0, 12))

            await db.add_news(
                ticker,
                {
                    "article_id": article_id,
                    "headline": article["headline"],
                    "summary": f"Summary of: {article['headline']}",
                    "url": f"https://example.com/news/{article_id}",
                    "published_at": published_at,
                    "source": "Mock News",
                    "sentiment_score": article["sentiment_score"],
                    "sentiment_label": article["sentiment_label"],
                    "has_earnings_keyword": "earnings" in article["headline"].lower()
                    or "revenue" in article["headline"].lower(),
                    "has_acquisition_keyword": "acquisition" in article["headline"].lower()
                    or "buyback" in article["headline"].lower(),
                    "has_regulatory_keyword": False,
                },
            )

        print(f"  ✓ Added {len(articles)} news items for {ticker}")


# =============================================================================
# SEED MACRO INDICATORS
# =============================================================================
async def seed_macro_indicators(db: Database):
    """Insert sample macro indicators into thesis_data.macro_indicators."""
    print("\n📊 Seeding macro indicators...")

    indicators = [
        {
            "name": "cpi",
            "series_id": "CPIAUCSL",
            "units": "Index 1982-1984=100",
            "base": 310,
            "volatility": 0.002,
        },
        {
            "name": "unemployment",
            "series_id": "UNRATE",
            "units": "Percent",
            "base": 3.8,
            "volatility": 0.05,
        },
        {
            "name": "fed_funds",
            "series_id": "DFF",
            "units": "Percent",
            "base": 5.25,
            "volatility": 0.01,
        },
        {
            "name": "10y_yield",
            "series_id": "DGS10",
            "units": "Percent",
            "base": 4.2,
            "volatility": 0.03,
        },
        {
            "name": "gdp",
            "series_id": "GDP",
            "units": "Billions of Dollars",
            "base": 27500,
            "volatility": 0.005,
        },
        {
            "name": "inflation",
            "series_id": "T10YIE",
            "units": "Percent",
            "base": 2.3,
            "volatility": 0.02,
        },
    ]

    for ind in indicators:
        value = ind["base"]
        count = 0

        # Generate 12 months of data (monthly for most, could be daily for rates)
        for i in range(365):
            date = datetime.now() - timedelta(days=365 - i)

            # Only add monthly data for CPI/unemployment/GDP, daily for rates
            if ind["name"] in ["cpi", "unemployment", "gdp"]:
                if date.day != 1:
                    continue

            change = random.uniform(-ind["volatility"], ind["volatility"])
            value *= 1 + change

            await db.add_macro_indicator(
                {
                    "indicator_name": ind["name"],
                    "series_id": ind["series_id"],
                    "date": date.date(),
                    "value": round(value, 4),
                    "units": ind["units"],
                    "year": date.year,
                    "month": date.month,
                    "quarter": (date.month - 1) // 3 + 1,
                }
            )
            count += 1

        print(f"  ✓ Added {count} records for {ind['name']}")


# =============================================================================
# MAIN
# =============================================================================
async def main():
    """Run all seed functions."""
    print("=" * 60)
    print("AI Agent Framework - Database Seeding")
    print("Compatible with thesis-data-fabric schema")
    print("=" * 60)
    print()
    print("⚠️  DISCLAIMER: Sample data for educational use only")
    print("   NOT real market data. See DISCLAIMER.md for full terms.")
    print("=" * 60)

    connection_string = Config.get_database_url()
    print(f"\n📌 Connecting to database...")
    print(f"   URL: {connection_string}")

    db = Database(connection_string)

    try:
        await db.connect()
        print("✅ Connected!")

        await seed_filings(db)
        await seed_prices(db)
        await seed_news(db)
        await seed_macro_indicators(db)

        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)

        # Verify data
        tickers = await db.list_tickers()
        print(f"\n📋 Available tickers: {', '.join(tickers)}")

        indicators = await db.list_macro_indicators()
        print(f"📊 Available indicators: {', '.join(indicators)}")

        # Show sample data
        for ticker in tickers:
            data = await db.get_fundamentals(ticker)
            if data:
                print(
                    f"\n{ticker}: PE={data['pe_ratio']:.1f}, Growth={data['revenue_growth']:.1f}%"
                )

    except Exception as e:
        print(f"\n❌ Seeding failed: {e}")
        raise

    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
