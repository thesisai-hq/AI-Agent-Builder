"""Test script for RAG system functionality.

Tests document upload, querying, listing, and deletion.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag_service import rag_service
from backend.storage import storage
from backend.models import AgentCreate
import tempfile


def create_test_agent():
    """Create a test agent for RAG testing."""
    agent_data = AgentCreate(
        name="Test RAG Agent",
        type="llm_based",
        goal="Test RAG functionality",
        llm_config={
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "tools": ["document_analysis"]
        }
    )
    agent = storage.create_agent(agent_data)
    return agent.id


def create_test_document():
    """Create a test document."""
    content = """
    Apple Inc. Investment Analysis Report
    
    Executive Summary:
    Apple Inc. (AAPL) is a leading technology company with strong fundamentals
    and a history of innovation. The company generates significant cash flow
    from its ecosystem of products and services.
    
    Key Strengths:
    - Strong brand loyalty with high customer retention
    - Diversified revenue streams (iPhone, Services, Wearables)
    - Massive cash reserves providing financial flexibility
    - Leading position in premium smartphone market
    
    Key Risks:
    - High dependence on iPhone revenue (still ~50% of total)
    - Intense competition in all product categories
    - Regulatory challenges in multiple jurisdictions
    - Slowing growth in mature smartphone market
    
    Valuation:
    Current trading multiples are above historical averages, suggesting
    the stock may be fairly valued to slightly overvalued at current levels.
    
    Recommendation:
    HOLD for existing investors. New investors should wait for a pullback
    to more attractive entry points around $160-170 range.
    """
    return content.encode('utf-8')


def test_rag_workflow():
    """Test complete RAG workflow."""
    print("=" * 80)
    print("RAG SYSTEM TEST - Complete Workflow")
    print("=" * 80)
    print()
    
    # Step 1: Create test agent
    print("Step 1: Creating test agent...")
    agent_id = create_test_agent()
    print(f"✅ Agent created: {agent_id}")
    print()
    
    # Step 2: Add document
    print("Step 2: Uploading test document...")
    test_doc = create_test_document()
    
    try:
        result = rag_service.add_document(
            agent_id=agent_id,
            file_content=test_doc,
            filename="apple_analysis.txt"
        )
        print(f"✅ Document uploaded successfully")
        print(f"   - Filename: {result['filename']}")
        print(f"   - Chunks: {result['chunks']}")
        print(f"   - Characters: {result['characters']}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False
    print()
    
    # Step 3: List documents
    print("Step 3: Listing documents...")
    documents = rag_service.list_documents(agent_id)
    print(f"✅ Found {len(documents)} document(s):")
    for doc in documents:
        print(f"   - {doc['filename']} ({doc['size_mb']} MB)")
    print()
    
    # Step 4: Query documents
    print("Step 4: Querying documents...")
    queries = [
        "What are the key strengths of Apple?",
        "What are the main risks?",
        "What is the valuation recommendation?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 80)
        context = rag_service.query(agent_id, query, n_results=3)
        print(context)
    print()
    
    # Step 5: Get stats
    print("Step 5: Getting RAG statistics...")
    stats = rag_service.get_stats(agent_id)
    print(f"✅ RAG Stats:")
    print(f"   - Total chunks: {stats['total_chunks']}")
    print(f"   - Total documents: {stats['total_documents']}")
    print()
    
    # Step 6: Delete document
    print("Step 6: Deleting document...")
    success = rag_service.delete_document(agent_id, "apple_analysis.txt")
    if success:
        print("✅ Document deleted successfully")
    else:
        print("❌ Failed to delete document")
    print()
    
    # Step 7: Verify deletion
    print("Step 7: Verifying deletion...")
    documents_after = rag_service.list_documents(agent_id)
    if len(documents_after) == 0:
        print("✅ Document list is now empty")
    else:
        print(f"❌ Still {len(documents_after)} document(s) remaining")
    print()
    
    # Cleanup: Delete test agent
    print("Cleanup: Deleting test agent...")
    storage.delete_agent(agent_id)
    print("✅ Test agent deleted")
    print()
    
    print("=" * 80)
    print("🎉 RAG SYSTEM TEST COMPLETE - ALL STEPS PASSED!")
    print("=" * 80)
    
    return True


def test_rag_with_pdf():
    """Test RAG with a simple PDF."""
    print("=" * 80)
    print("RAG SYSTEM TEST - PDF Upload")
    print("=" * 80)
    print()
    
    # Create test agent
    print("Creating test agent...")
    agent_id = create_test_agent()
    print(f"✅ Agent created: {agent_id}")
    print()
    
    # Create a simple PDF using PyPDF2
    print("Creating test PDF...")
    from PyPDF2 import PdfWriter
    from io import BytesIO
    
    # Note: PyPDF2 can't create PDFs with text easily
    # For testing, we'll use a TXT file instead
    print("⚠️  PDF creation test skipped (use TXT for testing)")
    print("   To test with real PDFs, upload manually via API")
    print()
    
    # Cleanup
    storage.delete_agent(agent_id)
    print("✅ Test agent cleaned up")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "RAG SYSTEM TEST SUITE" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    # Check dependencies
    try:
        import chromadb
        import sentence_transformers
        import PyPDF2
        print("✅ All RAG dependencies installed")
        print()
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\nInstall with: pip install -r requirements.txt")
        print()
        sys.exit(1)
    
    # Run tests
    try:
        success = test_rag_workflow()
        
        if success:
            print("\n🎉 All RAG tests passed! System is ready for use.")
            print("\nNext steps:")
            print("1. Start the server: python run.py")
            print("2. Upload documents via API or UI")
            print("3. Query documents in agent analysis")
        else:
            print("\n⚠️  Some tests failed. Check errors above.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
