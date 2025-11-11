#!/usr/bin/env python3
"""Test script to verify GUI setup and file saving."""

from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gui.agent_loader import AgentLoader
from gui.agent_creator import AgentCreator


def test_setup():
    """Test basic setup and file saving."""
    print("=" * 60)
    print("Agent Builder GUI - Setup Test")
    print("=" * 60)
    print()
    
    # Test 1: Find examples directory
    print("Test 1: Locating examples directory...")
    examples_dir = Path(__file__).parent.parent / "examples"
    examples_dir = examples_dir.resolve()
    print(f"  Examples dir: {examples_dir}")
    print(f"  Exists: {examples_dir.exists()}")
    
    if not examples_dir.exists():
        print("  Creating directory...")
        examples_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {examples_dir.exists()}")
    
    print("  ✓ Pass")
    print()
    
    # Test 2: Initialize loader
    print("Test 2: Initialize AgentLoader...")
    loader = AgentLoader(examples_dir)
    print(f"  Loader created")
    print(f"  Examples dir: {loader.examples_dir}")
    print("  ✓ Pass")
    print()
    
    # Test 3: List existing agents
    print("Test 3: List existing agents...")
    agents = loader.list_agents()
    print(f"  Found {len(agents)} agents")
    for agent in agents[:3]:  # Show first 3
        print(f"    - {agent['name']} ({agent['filename']})")
    if len(agents) > 3:
        print(f"    ... and {len(agents) - 3} more")
    print("  ✓ Pass")
    print()
    
    # Test 4: Generate test agent code
    print("Test 4: Generate test agent code...")
    creator = AgentCreator()
    code = creator.generate_agent_code(
        agent_name="TestAgent",
        description="Test agent for setup verification",
        agent_type="Rule-Based",
        rules=[{
            "metric": "pe_ratio",
            "operator": "<",
            "threshold": 15,
            "direction": "bullish",
            "confidence": 0.8
        }]
    )
    print(f"  Generated {len(code)} characters of code")
    print("  ✓ Pass")
    print()
    
    # Test 5: Save test agent
    print("Test 5: Save test agent...")
    test_filename = "test_setup_agent.py"
    
    # Remove if exists
    test_path = examples_dir / test_filename
    if test_path.exists():
        print(f"  Removing existing: {test_path}")
        test_path.unlink()
    
    success, message = loader.save_agent(test_filename, code)
    print(f"  Save result: {success}")
    print(f"  Message: {message}")
    
    if success:
        print(f"  File exists: {test_path.exists()}")
        if test_path.exists():
            print(f"  File size: {test_path.stat().st_size} bytes")
            print("  ✓ Pass")
            print()
            
            # Clean up
            print("Cleaning up test file...")
            test_path.unlink()
            print("  ✓ Removed")
        else:
            print("  ✗ FAIL: File not found after save")
    else:
        print("  ✗ FAIL: Save operation failed")
    
    print()
    print("=" * 60)
    print("Setup test complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_setup()
