"""Setup mock database with test data"""

import psycopg2
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


def setup_mock_database():
    """Setup mock database with test data"""

    db_url = os.getenv("DATABASE_URL")

    if not db_url or db_url == "memory":
        print("⚠️  No PostgreSQL DATABASE_URL found in .env")
        print("Please set DATABASE_URL in .env file")
        print("Example: DATABASE_URL=postgresql://user:pass@localhost:5432/dbname")
        return

    parsed = urlparse(db_url)

    print("=" * 70)
    print("MOCK DATABASE SETUP")
    print("=" * 70)
    print(f"🔗 Connecting to database...")
    print(f"   Host: {parsed.hostname}")
    print(f"   Database: {parsed.path.lstrip('/')}")

    try:
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path.lstrip("/"),
            user=parsed.username,
            password=parsed.password,
        )

        print("✅ Connected to database")

        sql_file = os.path.join(os.path.dirname(__file__), "mock_data.sql")

        if not os.path.exists(sql_file):
            print(f"❌ SQL file not found: {sql_file}")
            return

        with open(sql_file, "r") as f:
            sql = f.read()

        print("📄 Executing SQL script...")

        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        print("✅ Mock database setup complete!")
        print("📊 Database contains:")

        cursor.execute(
            """
            SELECT 'mock_fundamentals' as table_name, COUNT(*) as records 
            FROM mock_fundamentals
            UNION ALL SELECT 'mock_prices', COUNT(*) FROM mock_prices
            UNION ALL SELECT 'mock_news', COUNT(*) FROM mock_news
            UNION ALL SELECT 'mock_analyst_ratings', COUNT(*) FROM mock_analyst_ratings
            UNION ALL SELECT 'mock_insider_trades', COUNT(*) FROM mock_insider_trades
            UNION ALL SELECT 'mock_sec_filings', COUNT(*) FROM mock_sec_filings
            UNION ALL SELECT 'mock_macro_indicators', COUNT(*) FROM mock_macro_indicators
            UNION ALL SELECT 'mock_options', COUNT(*) FROM mock_options
        """
        )

        for row in cursor.fetchall():
            print(f"   ✓ {row[0]}: {row[1]} records")

        cursor.close()
        conn.close()

        print("" + "=" * 70)
        print("🎉 Ready to test! Available tickers: AAPL, TSLA, MSFT, GOOGL, NVDA")
        print("=" * 70)
        print("📝 Next: python main.py")

    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    setup_mock_database()
