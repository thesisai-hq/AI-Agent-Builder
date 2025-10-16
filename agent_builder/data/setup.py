"""
Database Setup Utilities
"""

import logging
import os

logger = logging.getLogger(__name__)


def load_schema_sql() -> str:
    """Load schema.sql file"""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sql", "schema.sql"
    )

    with open(schema_path, "r") as f:
        return f.read()


def setup_mock_database(db_connection):
    """
    Setup mock database tables and populate with data

    Usage:
        import psycopg2
        from agent_builder.config import Config

        conn = psycopg2.connect(**Config.get_db_params())
        setup_mock_database(conn)
        conn.close()
    """
    from agent_builder.data.generator import MockDataGenerator

    cursor = db_connection.cursor()

    try:
        # Create schema from SQL file
        logger.info("Creating database schema from schema.sql...")
        schema_sql = load_schema_sql()
        cursor.execute(schema_sql)
        db_connection.commit()
        logger.info("✅ Schema created")

        # Generate and insert data
        logger.info("Generating mock data...")
        generator = MockDataGenerator()
        generator.generate_all_data(days=90)

        logger.info("Inserting mock data...")
        success = generator.insert_to_database(db_connection)

        if success:
            logger.info("✅ Mock database setup complete!")

            # Print summary
            cursor.execute("SELECT COUNT(DISTINCT ticker) FROM mock_fundamentals")
            ticker_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM mock_prices")
            price_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM mock_news")
            news_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM mock_technical_indicators")
            tech_count = cursor.fetchone()[0]

            logger.info(
                f"""
📊 Database Summary:
   - Tickers: {ticker_count}
   - Price records: {price_count}
   - News articles: {news_count}
   - Technical indicators: {tech_count}
   - Ready for all agent types!
            """
            )

            return True
        else:
            logger.error("❌ Failed to insert data")
            return False

    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        db_connection.rollback()
        return False

    finally:
        cursor.close()


def verify_mock_data(db_connection):
    """Verify that mock data is properly loaded"""
    cursor = db_connection.cursor()

    try:
        # Check each table
        tables = [
            "mock_fundamentals",
            "mock_prices",
            "mock_news",
            "mock_analyst_ratings",
            "mock_insider_trades",
            "mock_balance_sheet",
            "mock_cash_flow",
            "mock_earnings",
            "mock_sec_filings",
            "mock_technical_indicators",
            "mock_risk_metrics",
            "mock_options_data",
            "mock_macro_indicators",
        ]

        logger.info("Verifying mock data...")

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            logger.info(f"  {table:30s} {count:6d} records")

        # Test sample queries
        logger.info("\n📊 Sample Queries:")

        # Latest prices
        cursor.execute(
            """
            SELECT ticker, price, date 
            FROM mock_latest_prices 
            ORDER BY ticker 
            LIMIT 5
        """
        )
        logger.info("  Latest prices:")
        for row in cursor.fetchall():
            logger.info(f"    {row[0]}: ${row[1]} ({row[2]})")

        # Analyst consensus
        cursor.execute(
            """
            SELECT ticker, buy_count, hold_count, sell_count
            FROM mock_analyst_consensus
            LIMIT 5
        """
        )
        logger.info("\n  Analyst consensus:")
        for row in cursor.fetchall():
            logger.info(f"    {row[0]}: Buy={row[1]} Hold={row[2]} Sell={row[3]}")

        logger.info("\n✅ Mock data verification complete!")
        return True

    except Exception as e:
        logger.error(f"Verification error: {e}")
        return False

    finally:
        cursor.close()


# CLI script for easy setup
if __name__ == "__main__":
    import sys
    import psycopg2
    from agent_builder.config import Config

    logging.basicConfig(level=logging.INFO)

    print("🔧 Mock Database Setup Tool\n")

    # Check config
    if not Config.is_postgres():
        print("❌ PostgreSQL not configured in .env")
        print("   Set DATABASE_URL=postgresql://user:pass@localhost:5432/dbname")
        sys.exit(1)

    try:
        # Connect
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**Config.get_db_params())
        print("✅ Connected\n")

        # Setup
        success = setup_mock_database(conn)

        if success:
            print("\n" + "=" * 60)
            verify_mock_data(conn)
            print("=" * 60)
            print("\n✅ Mock database ready for testing!")
        else:
            print("❌ Setup failed")
            sys.exit(1)

        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
