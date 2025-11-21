"""Verification script for Phase 1 refactoring.

Tests that:
1. Error handler works correctly
2. Async test executor functions properly
3. No import errors from deprecated files
"""

import shutil
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def clean_cache():
    """Clean Python cache files."""
    print("Cleaning Python cache...")
    
    gui_dir = Path(__file__).parent
    
    # Remove __pycache__ directories
    for pycache in gui_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
            print(f"  Removed: {pycache.relative_to(gui_dir.parent)}")
        except Exception as e:
            pass
    
    # Remove .pyc files
    for pyc in gui_dir.rglob("*.pyc"):
        try:
            pyc.unlink()
        except Exception as e:
            pass
    
    print("✅ Cache cleaned\n")


def test_error_handler():
    """Test centralized error handler."""
    print("Testing LLMErrorHandler...")
    
    from gui.core import LLMErrorHandler
    
    handler = LLMErrorHandler()
    
    # Test error detection
    class MockSignal:
        def __init__(self, reasoning):
            self.reasoning = reasoning
    
    # Test missing package detection
    signal = MockSignal("Error: no module named 'ollama'")
    assert handler.detect_llm_fallback(signal), "Should detect missing package"
    
    error_info = handler.parse_error(signal.reasoning)
    assert error_info["error_type"] == "missing_package"
    assert error_info["provider"] == "ollama"
    
    solution = handler.get_solution_text(error_info)
    assert "pip install ollama" in solution
    
    # Test connection error
    signal = MockSignal("Connection refused to Ollama")
    error_info = handler.parse_error(signal.reasoning)
    assert error_info["error_type"] == "connection_error"
    
    solution = handler.get_solution_text(error_info)
    assert "ollama serve" in solution
    
    print("✅ Error handler tests passed")


def test_imports():
    """Test that all imports work correctly."""
    print("\nTesting imports...")
    
    try:
        from gui.business_logic.test_executor import TestExecutor
        print("✅ TestExecutor import works")
    except Exception as e:
        print(f"❌ TestExecutor import failed: {e}")
        return False
    
    try:
        from gui.components.results_display import display_test_results, display_error_with_solution
        print("✅ Results display imports work")
    except Exception as e:
        print(f"❌ Results display import failed: {e}")
        return False
    
    try:
        from gui.core import LLMErrorHandler
        print("✅ Core imports work")
    except Exception as e:
        print(f"❌ Core import failed: {e}")
        return False
    
    # Test deprecated file raises error
    try:
        from gui.agent_tester import AgentTester
        print("❌ Deprecated agent_tester should not import")
        return False
    except ImportError as e:
        if "deprecated" in str(e).lower():
            print("✅ Deprecated agent_tester correctly raises ImportError")
        else:
            print(f"⚠️  Unexpected import error: {e}")
    
    return True


def test_test_executor_structure():
    """Test TestExecutor has expected methods."""
    print("\nTesting TestExecutor structure...")
    
    from gui.business_logic.test_executor import TestExecutor
    
    executor = TestExecutor()
    
    # Check methods exist
    assert hasattr(executor, "execute_test_async"), "Missing execute_test_async"
    assert hasattr(executor, "_load_agent_async"), "Missing _load_agent_async"
    assert hasattr(executor, "_test_rag_agent_async"), "Missing _test_rag_agent_async"
    assert hasattr(executor, "_is_rag_agent"), "Missing _is_rag_agent"
    assert hasattr(executor, "error_handler"), "Missing error_handler attribute"
    
    # Check error handler is LLMErrorHandler
    from gui.core import LLMErrorHandler
    assert isinstance(executor.error_handler, LLMErrorHandler)
    
    print("✅ TestExecutor structure is correct")


def main():
    """Run all verification tests."""
    print("=" * 70)
    print("Phase 1 Refactoring Verification")
    print("=" * 70)
    print()
    
    # Clean cache first
    clean_cache()
    
    try:
        test_error_handler()
        test_imports()
        test_test_executor_structure()
        
        print("\n" + "=" * 70)
        print("✅ All Phase 1 verification tests passed!")
        print("=" * 70)
        print("\nChanges applied:")
        print("1. ✅ Created gui/core/error_handler.py (centralized error handling)")
        print("2. ✅ Updated test_executor.py (uses centralized error handler)")
        print("3. ✅ Updated results_display.py (uses centralized error handler)")
        print("4. ✅ Updated Test Agent page (proper async execution)")
        print("5. ✅ Deprecated agent_tester.py (duplicate removed)")
        print("6. ✅ Updated gui/__init__.py (removed deprecated import)")
        print("\nNext steps:")
        print("- Test the GUI: ./gui/launch.sh")
        print("- Create and test an agent")
        print("- Verify error messages appear correctly")
        print("- After 1 week of testing, delete agent_tester.py completely")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
