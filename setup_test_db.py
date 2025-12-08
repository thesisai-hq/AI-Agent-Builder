#!/usr/bin/env python3
"""Setup test database for pytest - works with Docker or local PostgreSQL.

Compatible with thesis-data-fabric schema (thesis_data.*).
"""

import asyncio
import subprocess
import sys


def is_docker_postgres():
    """Check if PostgreSQL is running in Docker."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=agent_framework_db", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
        )
        return "agent_framework_db" in result.stdout
    except Exception:
        return False


def create_test_database():
    """Create test database using available method."""
    print("Creating agent_framework_test database...")

    if is_docker_postgres():
        print("Using Docker PostgreSQL...")
        result = subprocess.run(
            [
                "docker",
                "exec",
                "agent_framework_db",
                "createdb",
                "-U",
                "postgres",
                "agent_framework_test",
            ],
            capture_output=True,
            text=True,
        )
    else:
        print("Using local PostgreSQL...")
        result = subprocess.run(
            ["createdb", "agent_framework_test"],
            capture_output=True,
            text=True,
        )

    if result.returncode != 0 and "already exists" not in result.stderr:
        print(f"Note: {result.stderr}")

    return True


def run_schema():
    """Run schema SQL on test database."""
    print("Running schema...")

    try:
        with open("schema.sql", "r") as f:
            schema = f.read()
    except FileNotFoundError:
        print("❌ schema.sql not found in current directory")
        return False

    if is_docker_postgres():
        result = subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                "agent_framework_db",
                "psql",
                "-U",
                "postgres",
                "agent_framework_test",
            ],
            input=schema,
            capture_output=True,
            text=True,
        )
    else:
        result = subprocess.run(
            ["psql", "agent_framework_test"],
            input=schema,
            capture_output=True,
            text=True,
        )

    if result.returncode != 0:
        print(f"❌ Failed to run schema: {result.stderr}")
        return False

    print("✅ Schema created (thesis_data.*)")
    return True


async def seed_test_database():
    """Seed test database with sample data."""
    print("Seeding test database...")

    from agent_framework import Config
    from agent_framework.database import Database
    from seed_data import (
        seed_filings,
        seed_macro_indicators,
        seed_news,
        seed_prices,
    )

    connection_string = Config.get_test_database_url()
    print(f"Connecting to: {connection_string}")

    db = Database(connection_string)

    try:
        await db.connect()

        # Seed in order (filings first since fundamentals view depends on it)
        await seed_filings(db)
        await seed_prices(db)
        await seed_news(db)
        await seed_macro_indicators(db)

        print("✅ Test database seeded successfully!")
        return True

    except Exception as e:
        print(f"❌ Failed to seed database: {e}")
        return False

    finally:
        await db.disconnect()


def verify_schema():
    """Verify that thesis_data schema exists and has expected tables."""
    print("Verifying schema...")

    verify_sql = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'thesis_data'
    ORDER BY table_name;
    """

    if is_docker_postgres():
        result = subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                "agent_framework_db",
                "psql",
                "-U",
                "postgres",
                "-d",
                "agent_framework_test",
                "-t",
                "-c",
                verify_sql,
            ],
            capture_output=True,
            text=True,
        )
    else:
        result = subprocess.run(
            ["psql", "-d", "agent_framework_test", "-t", "-c", verify_sql],
            capture_output=True,
            text=True,
        )

    if result.returncode == 0:
        tables = [t.strip() for t in result.stdout.strip().split("\n") if t.strip()]
        expected = [
            "edgar_filing_chunks",
            "edgar_filings",
            "macro_indicators",
            "prices",
            "stock_news",
        ]

        print(f"  Found tables: {', '.join(tables)}")

        missing = set(expected) - set(tables)
        if missing:
            print(f"  ⚠️ Missing tables: {', '.join(missing)}")
            return False

        print("✅ All expected tables present")
        return True
    else:
        print(f"❌ Failed to verify schema: {result.stderr}")
        return False


async def main():
    """Main setup function."""
    print("🧪 Setting up test database...")
    print(f"PostgreSQL method: {'Docker' if is_docker_postgres() else 'Local'}")
    print()

    # Step 1: Create database
    if not create_test_database():
        sys.exit(1)

    # Step 2: Run schema
    if not run_schema():
        sys.exit(1)

    # Step 3: Verify schema
    if not verify_schema():
        print("⚠️ Schema verification failed, but continuing...")

    # Step 4: Seed data
    if not await seed_test_database():
        sys.exit(1)

    print()
    print("=" * 60)
    print("✅ Test database ready!")
    print("=" * 60)
    print()
    print("Schema: thesis_data.*")
    print("Tables:")
    print("  - thesis_data.prices")
    print("  - thesis_data.stock_news")
    print("  - thesis_data.edgar_filings")
    print("  - thesis_data.edgar_filing_chunks")
    print("  - thesis_data.macro_indicators")
    print("  - thesis_data.fundamentals (VIEW)")
    print()
    print("Next steps:")
    print("  1. Run tests: pytest tests/ -v")
    print("  2. Run quickstart: python quickstart.py")


if __name__ == "__main__":
    asyncio.run(main())
