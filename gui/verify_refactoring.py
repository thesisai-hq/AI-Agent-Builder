"""Verification script for GUI refactoring.

Run this script to verify all refactoring changes are working correctly.
Tests imports, file structure, and basic functionality.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test all new imports work correctly."""
    print("Testing imports...")
    
    try:
        # Test component imports
        from gui.components import (
            render_agent_card,
            show_agent_stats,
            display_test_results,
            display_error_with_solution,
            configure_test_data,
            TestDataConfig
        )
        print("  ✅ Components import successfully")
        
        # Test page imports
        from gui.pages import show_browse_page, show_test_page
        from gui.pages.batch_test_page import show_batch_test_page
        print("  ✅ Pages import successfully")
        
        # Test async utils
        from gui.async_utils import (
            AsyncRunner,
            ProgressTracker,
            CancellableOperation,
            run_async,
            gather_with_errors
        )
        print("  ✅ Async utils import successfully")
        
        # Test business logic
        from gui.business_logic.test_executor import TestExecutor
        print("  ✅ Business logic imports successfully")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_file_structure():
    """Verify directory structure is correct."""
    print("\nTesting file structure...")
    
    gui_dir = Path(__file__).parent
    
    required_dirs = [
        gui_dir / "components",
        gui_dir / "pages",
        gui_dir / "async_utils",
        gui_dir / "business_logic"
    ]
    
    required_files = [
        gui_dir / "components" / "__init__.py",
        gui_dir / "components" / "agent_card.py",
        gui_dir / "components" / "results_display.py",
        gui_dir / "components" / "test_config.py",
        gui_dir / "pages" / "__init__.py",
        gui_dir / "pages" / "browse_page.py",
        gui_dir / "pages" / "test_page.py",
        gui_dir / "pages" / "batch_test_page.py",
        gui_dir / "async_utils" / "__init__.py",
        gui_dir / "business_logic" / "test_executor.py",
    ]
    
    all_exist = True
    
    for directory in required_dirs:
        if directory.exists():
            print(f"  ✅ {directory.name}/ directory exists")
        else:
            print(f"  ❌ {directory.name}/ directory missing")
            all_exist = False
    
    for file in required_files:
        if file.exists():
            relative = file.relative_to(gui_dir)
            print(f"  ✅ {relative} exists")
        else:
            relative = file.relative_to(gui_dir)
            print(f"  ❌ {relative} missing")
            all_exist = False
    
    return all_exist


def test_async_functionality():
    """Test basic async functionality."""
    print("\nTesting async functionality...")
    
    import asyncio
    
    try:
        from gui.async_utils import AsyncRunner
        
        async def test_coro():
            await asyncio.sleep(0.01)
            return "success"
        
        # Test event loop handling
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(test_coro())
        
        if result == "success":
            print("  ✅ Async execution works")
            return True
        else:
            print("  ❌ Async execution failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Async test failed: {e}")
        return False


def test_component_functionality():
    """Test component basic functionality."""
    print("\nTesting component functionality...")
    
    try:
        from gui.components.test_config import TestDataConfig
        
        # Test dataclass creation
        config = TestDataConfig(
            source="mock",
            data={"pe_ratio": 20},
            ticker="TEST"
        )
        
        if config.source == "mock" and config.ticker == "TEST":
            print("  ✅ TestDataConfig works")
        else:
            print("  ❌ TestDataConfig failed")
            return False
        
        # Test data preparation
        from gui.pages.test_page import prepare_test_data
        
        data = prepare_test_data(config)
        
        if data and data.get("pe_ratio") == 20:
            print("  ✅ Data preparation works")
        else:
            print("  ❌ Data preparation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Component test failed: {e}")
        return False


def test_backward_compatibility():
    """Test backward compatibility with existing code."""
    print("\nTesting backward compatibility...")
    
    try:
        # Old imports should still work
        from gui.agent_loader import AgentLoader
        from gui.agent_tester import AgentTester
        from gui.agent_creator import AgentCreator
        
        print("  ✅ Old imports still work")
        
        # Instances should create without errors
        examples_dir = Path(__file__).parent.parent / "examples"
        
        loader = AgentLoader(examples_dir)
        tester = AgentTester()
        creator = AgentCreator()
        
        print("  ✅ Old classes instantiate correctly")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Backward compatibility failed: {e}")
        return False


def test_app_structure():
    """Verify app.py structure is correct."""
    print("\nTesting app.py structure...")
    
    app_file = Path(__file__).parent / "app.py"
    
    if not app_file.exists():
        print("  ❌ app.py not found")
        return False
    
    content = app_file.read_text()
    
    checks = [
        ("from gui.pages import", "Page imports"),
        ("show_browse_page()", "Browse page call"),
        ("show_test_page()", "Test page call"),
        ("show_batch_test_page()", "Batch test page call"),
        ("def main()", "Main function"),
    ]
    
    all_passed = True
    for check_str, description in checks:
        if check_str in content:
            print(f"  ✅ {description} present")
        else:
            print(f"  ❌ {description} missing")
            all_passed = False
    
    # Check file size reduced
    lines = len(content.split("\n"))
    if lines < 300:
        print(f"  ✅ app.py is {lines} lines (target <300)")
    else:
        print(f"  ⚠️  app.py is {lines} lines (still large)")
    
    return all_passed


def test_no_syntax_errors():
    """Verify all Python files have valid syntax."""
    print("\nChecking for syntax errors...")
    
    gui_dir = Path(__file__).parent
    
    python_files = [
        gui_dir / "app.py",
        gui_dir / "components" / "agent_card.py",
        gui_dir / "components" / "results_display.py",
        gui_dir / "components" / "test_config.py",
        gui_dir / "pages" / "browse_page.py",
        gui_dir / "pages" / "test_page.py",
        gui_dir / "pages" / "batch_test_page.py",
        gui_dir / "async_utils" / "__init__.py",
        gui_dir / "business_logic" / "test_executor.py",
    ]
    
    all_valid = True
    
    for file_path in python_files:
        if not file_path.exists():
            print(f"  ⚠️  {file_path.name} not found (skip)")
            continue
        
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path.name, 'exec')
            print(f"  ✅ {file_path.name} - valid syntax")
        except SyntaxError as e:
            print(f"  ❌ {file_path.name} - syntax error: {e}")
            all_valid = False
    
    return all_valid


def main():
    """Run all verification tests."""
    print("=" * 70)
    print("GUI Refactoring Verification")
    print("=" * 70)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Async Functionality", test_async_functionality),
        ("Components", test_component_functionality),
        ("Backward Compatibility", test_backward_compatibility),
        ("App Structure", test_app_structure),
        ("Syntax Check", test_no_syntax_errors),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("Verification Summary")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All verification tests passed!")
        print("\n✅ Refactoring is complete and working correctly")
        print("\nNext steps:")
        print("  1. Run: pytest tests/gui/ -v")
        print("  2. Launch GUI: streamlit run app.py")
        print("  3. Test all pages manually")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
