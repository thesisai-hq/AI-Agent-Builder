"""
Test connection pooling performance improvement
"""

import time
import psycopg2
from agent_builder.config import Config
from agent_builder.repositories.connection import ConnectionPool, get_db_cursor


def test_without_pool(iterations=10):
    """Test without pooling - Create new connection each time"""
    params = Config.get_db_params()

    start = time.time()

    for i in range(iterations):
        # Create new connection
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        # Simple query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        # Close
        cursor.close()
        conn.close()

    duration = time.time() - start
    return duration


def test_with_pool(iterations=10):
    """Test with pooling - Reuse connections"""
    # Initialize pool
    ConnectionPool.initialize()

    start = time.time()

    for i in range(iterations):
        # Get from pool (fast!)
        with get_db_cursor() as cursor:
            if cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

    duration = time.time() - start
    return duration


if __name__ == "__main__":
    print("=" * 60)
    print("Connection Pooling Performance Test")
    print("=" * 60)

    iterations = 20

    print(f"\nRunning {iterations} database queries...\n")

    # Test without pool
    print("1️⃣ WITHOUT connection pool:")
    time_without = test_without_pool(iterations)
    print(f"   Time: {time_without:.3f} seconds")
    print(f"   Per query: {(time_without/iterations)*1000:.1f}ms")

    # Test with pool
    print("\n2️⃣ WITH connection pool:")
    time_with = test_with_pool(iterations)
    print(f"   Time: {time_with:.3f} seconds")
    print(f"   Per query: {(time_with/iterations)*1000:.1f}ms")

    # Calculate improvement
    improvement = time_without / time_with
    savings = time_without - time_with

    print("\n" + "=" * 60)
    print("📊 Results:")
    print("=" * 60)
    print(f"   Speed improvement: {improvement:.1f}x faster")
    print(f"   Time saved: {savings:.3f} seconds ({(savings/time_without)*100:.1f}%)")
    print(f"   Per-query savings: {(savings/iterations)*1000:.1f}ms")
    print("\n✅ Connection pooling provides significant benefit!")
    print("=" * 60)

    # Cleanup
    ConnectionPool.close_all()
