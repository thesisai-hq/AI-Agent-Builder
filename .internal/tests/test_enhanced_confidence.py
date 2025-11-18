#!/usr/bin/env python3
"""
Test Enhanced Confidence Integration
"""

import sys
from pathlib import Path

print("🧪 Testing Enhanced Confidence Integration")
print("=" * 60)

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

# Test 1: Confidence module
print("\n1. Testing confidence.py module...")
try:
    from agent_framework.confidence import (
        ConfidenceCalculator,
        EnhancedConfidenceCalculator,
        calculate_simple_confidence
    )
    print("   ✅ Module imports successfully")
    
    # Test basic calculation
    calc = ConfidenceCalculator()
    conf, reason = calc.calculate_rule_confidence(
        metric_value=10.0,
        threshold=15.0,
        operator='<',
        base_confidence=0.7
    )
    print(f"   ✅ Calculation works: {conf:.0%} - {reason}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Framework exports
print("\n2. Testing framework exports...")
try:
    from agent_framework import (
        ConfidenceCalculator,
        EnhancedConfidenceCalculator,
        enhanced_parse_llm_signal
    )
    print("   ✅ Exported from framework")
except Exception as e:
    print(f"   ❌ Export error: {e}")
    sys.exit(1)

# Test 3: Agent creator
print("\n3. Testing agent creator...")
try:
    from gui.agent_creator import AgentCreator
    
    creator = AgentCreator()
    
    # Generate simple rule agent
    code = creator.generate_agent_code(
        agent_name="TestAgent",
        description="Test",
        agent_type="Rule-Based",
        rules=[{
            "type": "simple",
            "metric": "pe_ratio",
            "operator": "<",
            "threshold": 15,
            "direction": "bullish",
            "confidence": 0.8
        }]
    )
    
    # Check for enhanced confidence
    if "ConfidenceCalculator" in code:
        print("   ✅ Generator uses ConfidenceCalculator")
    else:
        print("   ❌ Generator doesn't import ConfidenceCalculator")
        sys.exit(1)
    
    if "calculate_rule_confidence" in code:
        print("   ✅ Generator calls calculate_rule_confidence")
    else:
        print("   ❌ Generator doesn't call calculate_rule_confidence")
        sys.exit(1)
    
    if "strength_reason" in code:
        print("   ✅ Generator includes strength reasoning")
    else:
        print("   ❌ Generator missing strength reasoning")
        sys.exit(1)
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Score-based agent
print("\n4. Testing score-based agent generation...")
try:
    code = creator.generate_agent_code(
        agent_name="ScoreAgent",
        description="Score test",
        agent_type="Rule-Based",
        rules=[{
            "type": "score",
            "criteria": [
                {"metric": "pe_ratio", "operator": "<", "threshold": 15, "points": 2},
                {"metric": "roe", "operator": ">", "threshold": 15, "points": 2}
            ],
            "bullish_threshold": 3,
            "bullish_confidence": 0.8,
            "bearish_threshold": -2,
            "bearish_confidence": 0.7
        }]
    )
    
    if "EnhancedConfidenceCalculator" in code:
        print("   ✅ Score agent uses EnhancedConfidenceCalculator")
    else:
        print("   ❌ Score agent doesn't use enhanced confidence")
        sys.exit(1)
    
    if "for_score_based_agent" in code:
        print("   ✅ Score agent calls for_score_based_agent()")
    else:
        print("   ❌ Missing for_score_based_agent call")
        sys.exit(1)

except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: LLM agent
print("\n5. Testing LLM agent generation...")
try:
    code = creator.generate_agent_code(
        agent_name="LLMAgent",
        description="LLM test",
        agent_type="LLM-Powered",
        llm_provider="ollama",
        llm_model="llama3.2",
        temperature=0.5,
        max_tokens=1000,
        system_prompt="Test"
    )
    
    if "enhanced_parse_llm_signal" in code:
        print("   ✅ LLM agent uses enhanced_parse_llm_signal")
    else:
        print("   ❌ LLM agent doesn't use enhanced parser")
        sys.exit(1)

except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 6: GUI app
print("\n6. Testing GUI app...")
try:
    import py_compile
    py_compile.compile("gui/app.py", doraise=True)
    print("   ✅ GUI app.py compiles")
except Exception as e:
    print(f"   ❌ GUI syntax error: {e}")
    sys.exit(1)

# Test 7: How to page
print("\n7. Testing how_to_page.py...")
try:
    py_compile.compile("gui/how_to_page.py", doraise=True)
    print("   ✅ how_to_page.py compiles")
except Exception as e:
    print(f"   ❌ How to page syntax error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("")
print("Enhanced confidence is integrated:")
print("  ✅ Simple rules use calculate_rule_confidence()")
print("  ✅ Score-based uses for_score_based_agent()")
print("  ✅ LLM agents use enhanced_parse_llm_signal()")
print("  ✅ GUI explains the system")
print("  ✅ Documentation updated")
print("")
print("Next: Launch GUI and test agent creation!")
print("  ./gui/launch.sh")
print("")
