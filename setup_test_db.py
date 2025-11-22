#!/usr/bin/env python3
"""Setup test database for pytest - works with Docker or local PostgreSQL."""

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
    except:
        return False


def create_test_database():
    """Create test database using available method."""
    print("Creating agent_framework_test database...")

    if is_docker_postgres():
        print("Using Docker PostgreSQL...")
        # Docker method
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
        # Local method
        result = subprocess.run(
            ["createdb", "agent_framework_test"], capture_output=True, text=True
        )

    if result.returncode != 0 and "already exists" not in result.stderr:
        print(f"Note: {result.stderr}")

    return True


def run_schema():
    """Run schema SQL on test database."""
    print("Running schema...")

    with open("schema.sql", "r") as f:
        schema = f.read()

    if is_docker_postgres():
        # Docker method
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
        # Local method
        result = subprocess.run(
            ["psql", "agent_framework_test"], input=schema, capture_output=True, text=True
        )

    if result.returncode != 0:
        print(f"❌ Failed to run schema: {result.stderr}")
        return False

    return True


async def seed_test_database():
    """Seed test database with sample data."""
    print("Seeding test database...")

    from agent_framework import Config
    from agent_framework.database import Database
    from seed_data import seed_filings, seed_fundamentals, seed_news, seed_prices

    # Use test database URL
    connection_string = Config.get_test_database_url()
    print(f"Connecting to: {connection_string}")

    db = Database(connection_string)

    try:
        await db.connect()
        await seed_fundamentals(db)
        await seed_prices(db)
        await seed_news(db)
        await seed_filings(db)
        print("✅ Test database seeded successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to seed database: {e}")
        return False
    finally:
        await db.disconnect()


async def main():
    """Main setup function."""
    print("🧪 Setting up test database...")
    print(f"PostgreSQL method: {'Docker' if is_docker_postgres() else 'Local'}")
    print()

    # Create database
    if not create_test_database():
        sys.exit(1)

    # Run schema
    if not run_schema():
        sys.exit(1)

    # Seed data
    if not await seed_test_database():
        sys.exit(1)

    print()
    print("=" * 60)
    print("✅ Test database ready!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Run tests: pytest tests/ -v")
    print("  2. Run quickstart: python quickstart.py")


if __name__ == "__main__":
    asyncio.run(main())
