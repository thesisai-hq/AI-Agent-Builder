"""Test script for Phase 1 enhanced tools.

Run this to verify all tools are working correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.tools import tool_registry


def test_web_search():
    """Test web search tool."""
    print("=" * 80)
    print("TEST 1: WEB SEARCH")
    print("=" * 80)
    
    result = tool_registry.execute('web_search', ticker='AAPL', max_results=5)
    print(result)
    print("\n")
    
    return "✅ PASSED" if "NEWS FOR AAPL" in result else "❌ FAILED"


def test_financial_data():
    """Test financial data tool."""
    print("=" * 80)
    print("TEST 2: FINANCIAL DATA")
    print("=" * 80)
    
    result = tool_registry.execute('financial_data', ticker='AAPL', include_statements=True)
    print(result)
    print("\n")
    
    return "✅ PASSED" if "COMPREHENSIVE FINANCIAL DATA" in result else "❌ FAILED"


def test_calculator_dcf():
    """Test DCF calculator."""
    print("=" * 80)
    print("TEST 3: CALCULATOR - DCF VALUATION")
    print("=" * 80)
    
    result = tool_registry.execute(
        'calculator',
        ticker='AAPL',
        model='dcf',
        growth_rate=0.10,
        discount_rate=0.10,
        terminal_growth=0.03,
        years=5
    )
    print(result)
    print("\n")
    
    return "✅ PASSED" if "DCF VALUATION" in result else "❌ FAILED"


def test_calculator_graham():
    """Test Graham Number calculator."""
    print("=" * 80)
    print("TEST 4: CALCULATOR - GRAHAM NUMBER")
    print("=" * 80)
    
    result = tool_registry.execute('calculator', ticker='AAPL', model='graham')
    print(result)
    print("\n")
    
    return "✅ PASSED" if "GRAHAM NUMBER" in result else "❌ FAILED"


def test_calculator_altman():
    """Test Altman Z-Score calculator."""
    print("=" * 80)
    print("TEST 5: CALCULATOR - ALTMAN Z-SCORE")
    print("=" * 80)
    
    result = tool_registry.execute('calculator', ticker='AAPL', model='altman')
    print(result)
    print("\n")
    
    return "✅ PASSED" if "ALTMAN Z-SCORE" in result else "❌ FAILED"


def test_calculator_expression():
    """Test math expression calculator."""
    print("=" * 80)
    print("TEST 6: CALCULATOR - MATH EXPRESSION")
    print("=" * 80)
    
    result = tool_registry.execute('calculator', expression='sqrt(144) + log10(100) * 5')
    print(result)
    print("\n")
    
    return "✅ PASSED" if "Calculation:" in result else "❌ FAILED"


def test_document_analysis():
    """Test document analysis (should return placeholder)."""
    print("=" * 80)
    print("TEST 7: DOCUMENT ANALYSIS (Placeholder)")
    print("=" * 80)
    
    result = tool_registry.execute('document_analysis', ticker='AAPL', agent_id='test-agent')
    print(result)
    print("\n")
    
    return "✅ PASSED" if "PLACEHOLDER" in result else "❌ FAILED"


def run_all_tests():
    """Run all tool tests."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "PHASE 1 TOOLS - TEST SUITE" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    results = {}
    
    try:
        results['web_search'] = test_web_search()
    except Exception as e:
        results['web_search'] = f"❌ FAILED: {e}"
    
    try:
        results['financial_data'] = test_financial_data()
    except Exception as e:
        results['financial_data'] = f"❌ FAILED: {e}"
    
    try:
        results['calculator_dcf'] = test_calculator_dcf()
    except Exception as e:
        results['calculator_dcf'] = f"❌ FAILED: {e}"
    
    try:
        results['calculator_graham'] = test_calculator_graham()
    except Exception as e:
        results['calculator_graham'] = f"❌ FAILED: {e}"
    
    try:
        results['calculator_altman'] = test_calculator_altman()
    except Exception as e:
        results['calculator_altman'] = f"❌ FAILED: {e}"
    
    try:
        results['calculator_expression'] = test_calculator_expression()
    except Exception as e:
        results['calculator_expression'] = f"❌ FAILED: {e}"
    
    try:
        results['document_analysis'] = test_document_analysis()
    except Exception as e:
        results['document_analysis'] = f"❌ FAILED: {e}"
    
    # Summary
    print("\n")
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_name, status in results.items():
        print(f"{test_name:.<50} {status}")
    
    print("=" * 80)
    
    # Count results
    passed = sum(1 for s in results.values() if "✅" in s)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Phase 1 tools are fully functional!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
    
    print("\n")


if __name__ == "__main__":
    # Check if we're in the right directory
    if not os.path.exists('backend'):
        print("❌ Error: Run this script from the gui_system directory")
        print("Usage: python test_tools.py")
        sys.exit(1)
    
    run_all_tests()
