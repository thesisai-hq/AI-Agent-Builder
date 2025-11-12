#!/usr/bin/env python3
"""Generate example strategy agents from templates."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from gui.agent_creator import AgentCreator
from gui.templates import StrategyTemplates


def generate_example_strategies():
    """Generate example strategy agents in examples/ directory."""
    
    print("=" * 60)
    print("Generating Example Strategy Agents")
    print("=" * 60)
    print()
    
    creator = AgentCreator()
    templates = StrategyTemplates.get_all_templates()
    examples_dir = Path(__file__).parent.parent / "examples"
    
    for strategy_name, template in templates.items():
        print(f"Generating: {strategy_name}...")
        
        # Generate agent code
        code = creator.generate_agent_code(
            agent_name=template['agent_name'],
            description=template['description'],
            agent_type=template['agent_type'],
            rules=template.get('rules')
        )
        
        # Create filename
        filename = f"05_{template['agent_name'].lower()}.py"
        filepath = examples_dir / filename
        
        # Save file
        try:
            filepath.write_text(code, encoding='utf-8')
            print(f"  ✓ Saved: {filename}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print()
    print("=" * 60)
    print("✓ Example strategies generated!")
    print("=" * 60)
    print()
    print("Students can now:")
    print("  1. Browse examples/")
    print("  2. View strategy code")
    print("  3. Duplicate to create variations")
    print("  4. Test with different data")
    print()


if __name__ == "__main__":
    generate_example_strategies()
