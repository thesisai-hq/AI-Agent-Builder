#!/usr/bin/env python3
"""Test Signal creation to verify fix."""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_framework import Signal


def test_signal_creation():
    """Test that Signal can be created with keyword arguments."""
    print("Testing Signal creation...")
    print()

    # Test 1: Basic Signal creation (correct way)
    print("Test 1: Creating Signal with keyword arguments")
    try:
        signal = Signal(direction="bullish", confidence=0.8, reasoning="Test reasoning")
        print(f"  ✓ Success: {signal.direction} ({signal.confidence:.0%})")
        print(f"    Reasoning: {signal.reasoning}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

    print()

    # Test 2: Try positional arguments (should fail)
    print("Test 2: Creating Signal with positional arguments (should fail)")
    try:
        signal = Signal("bullish", 0.8, "Test reasoning")
        print(f"  ✗ Unexpected success: {signal}")
    except TypeError as e:
        print(f"  ✓ Expected error: {e}")

    print()

    # Test 3: All Signal directions
    print("Test 3: Testing all signal directions")
    for direction in ["bullish", "bearish", "neutral"]:
        try:
            signal = Signal(
                direction=direction, confidence=0.7, reasoning=f"Test {direction} signal"
            )
            print(f"  ✓ {direction}: {signal.confidence:.0%}")
        except Exception as e:
            print(f"  ✗ {direction} failed: {e}")

    print()
    print("=" * 60)
    print("Signal creation test complete!")
    print()
    print("The correct way to create a Signal:")
    print(
        """
    signal = Signal(
        direction='bullish',  # or 'bearish', 'neutral'
        confidence=0.8,       # 0.0 to 1.0
        reasoning='Your reasoning here'
    )
    """
    )


if __name__ == "__main__":
    test_signal_creation()
