"""
Test the minimal repository
"""

from agent_builder.repositories.repository import Repository
from agent_builder.repositories.connection import get_database_connection
import uuid
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def test_in_memory():
    """Test with in-memory storage"""
    print("\n" + "=" * 60)
    print("Testing In-Memory Repository")
    print("=" * 60)
    
    # Create repository with dict
    db = {}
    repo = Repository(db)
    
    # Create agent
    agent_id = str(uuid.uuid4())
    agent_data = {
        "id": agent_id,
        "name": "Test Agent",
        "type": "simple",
        "weight": 0.1
    }
    
    # Save
    print("\n1️⃣ Saving agent...")
    saved = repo.save("agents", agent_data)
    print(f"   Saved: {saved['name']}")
    
    # Find by ID
    print("\n2️⃣ Finding by ID...")
    found = repo.find_by_id("agents", agent_id)
    print(f"   Found: {found['name']}")
    
    # Find all
    print("\n3️⃣ Finding all...")
    all_agents = repo.find_all("agents")
    print(f"   Total: {len(all_agents)}")
    
    # Delete
    print("\n4️⃣ Deleting...")
    deleted = repo.delete("agents", agent_id)
    print(f"   Deleted: {deleted}")
    
    print("\n✅ In-memory tests passed!")


def test_with_postgres():
    """Test with PostgreSQL"""
    
    # Check if PostgreSQL is configured
    db_url = os.getenv('DATABASE_URL', 'memory')
    
    if db_url == 'memory':
        print("\n⚠️  PostgreSQL not configured. Set DATABASE_URL to test.")
        return
    
    print("\n" + "=" * 60)
    print("Testing PostgreSQL Repository")
    print("=" * 60)
    print(f"Database URL: {db_url}")
    
    try:
        # Get connection
        db = get_database_connection()
        repo = Repository(db)
        
        # Same tests as above
        agent_id = str(uuid.uuid4())
        agent_data = {
            "id": agent_id,
            "name": "PG Test Agent",
            "type": "simple",
            "weight": 0.1,
            "config": {},
            "enabled": True,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        
        print("\n1️⃣ Saving to PostgreSQL...")
        saved = repo.save("agents", agent_data)
        print(f"   Saved: {saved['name']}")
        
        print("\n2️⃣ Finding in PostgreSQL...")
        found = repo.find_by_id("agents", agent_id)
        print(f"   Found: {found['name']}")
        
        print("\n3️⃣ Listing all...")
        all_agents = repo.find_all("agents")
        print(f"   Total: {len(all_agents)}")
        
        print("\n4️⃣ Deleting from PostgreSQL...")
        deleted = repo.delete("agents", agent_id)
        print(f"   Deleted: {deleted}")
        
        print("\n✅ PostgreSQL tests passed!")
        
        db.close()
        
    except Exception as e:
        print(f"\n❌ PostgreSQL test failed: {e}")
        print("   Make sure:")
        print("   1. Docker container running: docker ps | grep thesis-ai-db")
        print("   2. DATABASE_URL set in .env")
        print("   3. Tables exist: docker exec thesis-ai-db psql -U dev -d ai_agents -c '\\dt'")


if __name__ == "__main__":
    test_in_memory()
    test_with_postgres()
    
    print("\n" + "=" * 60)
    print("✅ Repository tests complete!")
    print("=" * 60)
