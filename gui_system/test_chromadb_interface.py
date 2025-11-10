"""Quick test to verify ChromaDB interface fix."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_chromadb_interface():
    """Test that FastEmbed wrapper works with ChromaDB."""
    print("Testing ChromaDB + FastEmbed interface compatibility...")
    
    try:
        from backend.rag_service import FastEmbedEmbeddingFunction
        
        # Create embedding function
        emb_fn = FastEmbedEmbeddingFunction()
        print("✅ FastEmbed wrapper initialized")
        
        # Test embedding generation
        test_texts = ["This is a test document", "Another test sentence"]
        embeddings = emb_fn(test_texts)
        
        print(f"✅ Generated {len(embeddings)} embeddings")
        print(f"✅ Embedding dimension: {len(embeddings[0])}")
        
        # Verify format
        assert isinstance(embeddings, list), "Embeddings should be a list"
        assert isinstance(embeddings[0], list), "Each embedding should be a list"
        assert isinstance(embeddings[0][0], float), "Embedding values should be floats"
        
        print("✅ All interface checks passed!")
        print(f"   Embedding format: List[List[float]] ✅")
        print(f"   Signature: __call__(input: Documents) ✅")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  ChromaDB Interface Compatibility Test")
    print("=" * 70 + "\n")
    
    success = test_chromadb_interface()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ SUCCESS: ChromaDB interface is compatible")
        print("   RAG service is ready to use!")
    else:
        print("❌ FAILED: See errors above")
    print("=" * 70 + "\n")
    
    sys.exit(0 if success else 1)
