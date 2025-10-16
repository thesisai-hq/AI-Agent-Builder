#!/usr/bin/env python3
"""
Setup Test Database - One-command setup for public users
Run: python setup_test_database.py
"""

import os
import sys
import time

# Add instructions at the top
INSTRUCTIONS = """
╔════════════════════════════════════════════════════════════════╗
║       AI INVESTMENT ADVISOR - TEST DATABASE SETUP              ║
╚════════════════════════════════════════════════════════════════╝

This script creates a comprehensive mock financial database for testing.

📋 WHAT IT DOES:
   1. Creates 13 database tables (fundamentals, prices, news, etc.)
   2. Generates realistic test data for 8 major stocks
   3. Populates 90 days of price history
   4. Creates technical indicators, risk metrics, and macro data
   5. Adds news articles, analyst ratings, and insider trades

⚡ REQUIREMENTS:
   - PostgreSQL running (locally or Docker)
   - .env file with DATABASE_URL configured

🐳 QUICK START WITH DOCKER:
   docker run -d \\
     --name agent-test-db \\
     -e POSTGRES_PASSWORD=agent_password \\
     -e POSTGRES_USER=agent_user \\
     -e POSTGRES_DB=agent_test \\
     -p 5432:5432 \\
     postgres:15

   Then add to .env:
   DATABASE_URL=postgresql://agent_user:agent_password@localhost:5432/agent_test

"""


def print_header():
    """Print setup header"""
    print(INSTRUCTIONS)


def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...\n")

    issues = []

    # Check if .env exists
    if not os.path.exists(".env"):
        issues.append("❌ .env file not found")
        issues.append("   Create .env with: DATABASE_URL=postgresql://...")

    # Check if DATABASE_URL is set
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        issues.append("❌ python-dotenv not installed")
        issues.append("   Run: pip install python-dotenv")
        return False, issues

    db_url = os.getenv("DATABASE_URL")
    if not db_url or db_url == "memory":
        issues.append("❌ DATABASE_URL not configured in .env")
        issues.append("   Set: DATABASE_URL=postgresql://user:pass@host:port/dbname")
    elif not db_url.startswith("postgresql"):
        issues.append("❌ DATABASE_URL must be PostgreSQL")
        issues.append(f"   Current: {db_url}")

    # Try to import required packages
    try:
        import psycopg2
    except ImportError:
        issues.append("❌ psycopg2 not installed")
        issues.append("   Run: pip install psycopg2-binary")

    # Try to connect to database
    if not issues:
        try:
            import psycopg2
            from urllib.parse import urlparse

            parsed = urlparse(db_url)
            conn_params = {
                "host": parsed.hostname or "localhost",
                "port": parsed.port or 5432,
                "database": parsed.path.lstrip("/"),
                "user": parsed.username,
                "password": parsed.password,
            }

            print(
                f"Connecting to: {parsed.hostname}:{parsed.port}/{parsed.path.lstrip('/')}"
            )
            conn = psycopg2.connect(**conn_params, connect_timeout=5)
            conn.close()
            print("✅ Database connection successful\n")

        except ImportError:
            pass  # Already handled above
        except Exception as e:
            issues.append(f"❌ Cannot connect to database: {e}")
            issues.append("   Make sure PostgreSQL is running")
            issues.append("   Check DATABASE_URL settings")

    if issues:
        print("\n".join(issues))
        return False, issues

    return True, []


def run_setup():
    """Run the database setup"""
    from dotenv import load_dotenv
    import psycopg2
    from urllib.parse import urlparse

    load_dotenv()

    # Parse DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    parsed = urlparse(db_url)

    conn_params = {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "database": parsed.path.lstrip("/"),
        "user": parsed.username,
        "password": parsed.password,
    }

    print("=" * 70)
    print("🔨 CREATING DATABASE SCHEMA")
    print("=" * 70)

    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Load and execute schema
        print("\n📋 Loading schema from sql/schema.sql...")
        schema_path = os.path.join("sql", "schema.sql")

        if not os.path.exists(schema_path):
            print(f"❌ Schema file not found: {schema_path}")
            print("   Make sure you're running this from the project root directory")
            return False

        with open(schema_path, "r") as f:
            schema_sql = f.read()

        print("📋 Executing schema...")
        cursor.execute(schema_sql)
        conn.commit()

        print("✅ Schema created successfully")
        print("\n   Tables created:")
        print("   - mock_fundamentals")
        print("   - mock_balance_sheet")
        print("   - mock_cash_flow")
        print("   - mock_earnings")
        print("   - mock_sec_filings")
        print("   - mock_prices")
        print("   - mock_technical_indicators")
        print("   - mock_news")
        print("   - mock_analyst_ratings")
        print("   - mock_insider_trades")
        print("   - mock_risk_metrics")
        print("   - mock_options_data")
        print("   - mock_macro_indicators")

        cursor.close()

        # Generate data
        print("\n" + "=" * 70)
        print("📊 GENERATING TEST DATA")
        print("=" * 70)

        from agent_builder.data.generator import MockDataGenerator

        generator = MockDataGenerator()

        # List tickers
        tickers = list(generator.TICKER_PROFILES.keys())
        print(f"\n🎯 Generating data for {len(tickers)} stocks:")
        for ticker in tickers:
            profile = generator.TICKER_PROFILES[ticker]
            print(f"   {ticker:6s} - {profile['name']:30s} ({profile['sector']})")

        print("\n⏳ Generating 90 days of comprehensive data...")
        print("   This may take 15-30 seconds...\n")

        start_time = time.time()
        data = generator.generate_all_data(days=90)
        generation_time = time.time() - start_time

        print(f"\n✅ Data generated in {generation_time:.1f} seconds")

        # Insert data
        print("\n📥 Inserting into database...")
        print("   This may take 10-20 seconds...\n")

        start_time = time.time()
        success = generator.insert_to_database(conn)
        insert_time = time.time() - start_time

        if not success:
            raise Exception("Data insertion failed")

        print(f"\n✅ Data inserted in {insert_time:.1f} seconds")

        # Verify
        print("\n" + "=" * 70)
        print("✅ VERIFICATION")
        print("=" * 70)

        cursor = conn.cursor()

        # Count records
        tables = [
            ("mock_fundamentals", "Companies"),
            ("mock_prices", "Price records"),
            ("mock_technical_indicators", "Technical indicators"),
            ("mock_risk_metrics", "Risk metrics"),
            ("mock_balance_sheet", "Balance sheets"),
            ("mock_cash_flow", "Cash flow statements"),
            ("mock_earnings", "Earnings reports"),
            ("mock_sec_filings", "SEC filings"),
            ("mock_news", "News articles"),
            ("mock_analyst_ratings", "Analyst ratings"),
            ("mock_insider_trades", "Insider trades"),
            ("mock_options_data", "Options data"),
            ("mock_macro_indicators", "Macro indicators"),
        ]

        print("\n📊 Record counts:")
        total_records = 0
        for table, description in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"   {description:30s} {count:6,} records")

        print(f"\n   {'TOTAL':30s} {total_records:6,} records")

        # Sample queries
        print("\n💰 Sample latest prices:")
        cursor.execute(
            """
            SELECT ticker, price, date 
            FROM mock_latest_prices 
            ORDER BY ticker 
            LIMIT 5
        """
        )
        for row in cursor.fetchall():
            print(f"   {row[0]:6s} ${row[1]:7.2f}  ({row[2]})")

        print("\n📰 Sample news sentiment:")
        cursor.execute(
            """
            SELECT ticker, sentiment, COUNT(*) as count
            FROM mock_news
            GROUP BY ticker, sentiment
            ORDER BY ticker, sentiment
            LIMIT 10
        """
        )
        for row in cursor.fetchall():
            print(f"   {row[0]:6s} {row[1]:8s} {row[2]:3d} articles")

        print("\n📈 Technical indicators coverage:")
        cursor.execute(
            """
            SELECT ticker, COUNT(*) as days
            FROM mock_technical_indicators
            GROUP BY ticker
            ORDER BY ticker
        """
        )
        for row in cursor.fetchall():
            print(f"   {row[0]:6s} {row[1]:3d} days of technical data")

        print("\n💹 Risk metrics coverage:")
        cursor.execute(
            """
            SELECT ticker, COUNT(*) as days
            FROM mock_risk_metrics
            GROUP BY ticker
            ORDER BY ticker
        """
        )
        for row in cursor.fetchall():
            print(f"   {row[0]:6s} {row[1]:3d} days of risk data")

        print("\n🌍 Macro indicators:")
        cursor.execute(
            """
            SELECT COUNT(*) as data_points,
                   MIN(date) as earliest,
                   MAX(date) as latest
            FROM mock_macro_indicators
        """
        )
        row = cursor.fetchone()
        print(f"   {row[0]} data points from {row[1]} to {row[2]}")

        cursor.close()
        conn.close()

        print("\n" + "=" * 70)
        print("🎉 SUCCESS! Test database is ready!")
        print("=" * 70)

        print("\n✅ You can now:")
        print("\n1️⃣  Start the API server:")
        print("   python -m agent_builder.api.main")

        print("\n2️⃣  Test an analysis:")
        print("   curl -X POST http://localhost:8000/analyze \\")
        print("        -H 'Content-Type: application/json' \\")
        print('        -d \'{"ticker": "AAPL"}\'')

        print("\n3️⃣  View API docs:")
        print("   http://localhost:8000/docs")

        print("\n4️⃣  Connect to database:")
        print(f"   psql {db_url}")

        print("\n5️⃣  Create custom agents:")
        print("   See examples/ directory for agent templates")

        print("\n📚 Supported Agent Types:")
        print("   ✅ Fundamental Agents (P/E, ROE, cash flow, earnings)")
        print("   ✅ Macro Agents (Fed rates, GDP, inflation, VIX)")
        print("   ✅ Technical Agents (RSI, MACD, Bollinger Bands)")
        print("   ✅ Sentiment Agents (news, analysts, insiders)")
        print("   ✅ Risk Agents (volatility, VaR, Sharpe ratio)")

        print("\n" + "=" * 70)
        print()

        return True

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you're running this script from the project root directory.")
        print("The directory structure should be:")
        print("  ├── sql/")
        print("  │   └── schema.sql")
        print("  ├── agent_builder/")
        print("  │   └── data/")
        print("  │       └── generator.py")
        print("  └── setup_test_database.py (you are here)")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        print("\nFull error:")
        traceback.print_exc()
        return False


def show_docker_help():
    """Show Docker setup instructions"""
    print("\n" + "=" * 70)
    print("🐳 DOCKER SETUP GUIDE")
    print("=" * 70)

    print("\n1️⃣  Start PostgreSQL with Docker:")
    print("\n   docker run -d \\")
    print("     --name agent-test-db \\")
    print("     -e POSTGRES_PASSWORD=agent_password \\")
    print("     -e POSTGRES_USER=agent_user \\")
    print("     -e POSTGRES_DB=agent_test \\")
    print("     -p 5432:5432 \\")
    print("     postgres:15")

    print("\n2️⃣  Wait for database to start (10 seconds):")
    print("\n   docker logs -f agent-test-db")
    print("   # Look for: 'database system is ready to accept connections'")

    print("\n3️⃣  Create .env file:")
    print(
        "\n   echo 'DATABASE_URL=postgresql://agent_user:agent_password@localhost:5432/agent_test' > .env"
    )

    print("\n4️⃣  Run this script again:")
    print("\n   python setup_test_database.py")

    print("\n" + "=" * 70)

    print("\n📖 Alternative: Use docker-compose")
    print("\n   docker compose -f docker-compose.test.yml up -d")
    print("   # Then run: python setup_test_database.py")

    print("\n" + "=" * 70)


def main():
    """Main entry point"""
    print_header()

    # Check requirements
    requirements_ok, issues = check_requirements()

    if not requirements_ok:
        print("\n" + "=" * 70)
        print("❌ Requirements not met. Please fix the issues above.")
        print("=" * 70)

        # Check if it's a database connection issue
        if any("Cannot connect" in issue for issue in issues):
            response = input(
                "\n💡 Would you like to see Docker setup instructions? [Y/n]: "
            )
            if response.lower() != "n":
                show_docker_help()

        sys.exit(1)

    # Confirm with user
    print("=" * 70)
    print("Ready to setup test database")
    print("=" * 70)

    print("\n⚠️  This will:")
    print("   - DROP existing mock_* tables (if any)")
    print("   - CREATE 13 new tables")
    print("   - INSERT ~5,000 records")
    print("   - Take approximately 30-60 seconds")

    response = input("\nContinue? [Y/n]: ")
    if response.lower() == "n":
        print("\nSetup cancelled.")
        sys.exit(0)

    print()

    # Run setup
    success = run_setup()

    if success:
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("❌ Setup failed. Please check the errors above.")
        print("=" * 70)

        print("\n💡 Common issues:")
        print("   1. PostgreSQL not running → Start with Docker")
        print("   2. Wrong DATABASE_URL → Check .env file")
        print("   3. Permission denied → Check database user permissions")
        print("   4. Missing files → Run from project root directory")

        print("\n📖 Need help?")
        print("   - Read: QUICKSTART.md")
        print("   - Read: TEST_DATABASE.md")
        print("   - Check: docker-compose.test.yml")

        sys.exit(1)


if __name__ == "__main__":
    main()
