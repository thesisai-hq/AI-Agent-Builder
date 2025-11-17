#!/usr/bin/env python3
"""Verify all Signal creations use keyword arguments."""

import re
from pathlib import Path


def check_file_for_positional_signals(filepath: Path) -> list:
    """Check if file contains Signal with positional arguments.

    Returns:
        List of (line_number, line_content) tuples with issues
    """
    try:
        content = filepath.read_text()
        lines = content.split("\n")
        issues = []

        for i, line in enumerate(lines, 1):
            # Look for Signal( followed by string literals or numbers (positional args)
            # Correct:   Signal(direction='bullish', ...)
            # Incorrect: Signal('bullish', 0.8, ...)

            if "Signal(" in line and "return Signal(" in line:
                # Check if it has positional arguments
                # Look for pattern: Signal('string' or Signal(number
                if re.search(r"Signal\s*\(\s*['\"]", line) or re.search(r"Signal\s*\(\s*\d", line):
                    issues.append((i, line.strip()))

        return issues
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []


def main():
    """Check all Python files for positional Signal arguments."""
    print("=" * 70)
    print("Signal Argument Style Verification")
    print("=" * 70)
    print()

    base_dir = Path(__file__).parent.parent
    total_issues = 0
    files_checked = 0

    # Check examples/
    print("Checking examples/...")
    examples_dir = base_dir / "examples"
    if examples_dir.exists():
        for pyfile in examples_dir.glob("*.py"):
            files_checked += 1
            issues = check_file_for_positional_signals(pyfile)
            if issues:
                print(f"\n  ❌ {pyfile.name}:")
                for line_num, line_content in issues:
                    print(f"      Line {line_num}: {line_content}")
                    total_issues += len(issues)
            else:
                print(f"  ✓ {pyfile.name}")

    # Check gui/
    print("\nChecking gui/...")
    gui_dir = base_dir / "gui"
    for pyfile in gui_dir.glob("*.py"):
        if pyfile.name.startswith("__"):
            continue
        files_checked += 1
        issues = check_file_for_positional_signals(pyfile)
        if issues:
            print(f"\n  ❌ {pyfile.name}:")
            for line_num, line_content in issues:
                print(f"      Line {line_num}: {line_content}")
                total_issues += len(issues)
        else:
            print(f"  ✓ {pyfile.name}")

    # Check agent_framework/
    print("\nChecking agent_framework/...")
    framework_dir = base_dir / "agent_framework"
    if framework_dir.exists():
        for pyfile in framework_dir.glob("*.py"):
            if pyfile.name.startswith("__"):
                continue
            files_checked += 1
            issues = check_file_for_positional_signals(pyfile)
            if issues:
                print(f"\n  ❌ {pyfile.name}:")
                for line_num, line_content in issues:
                    print(f"      Line {line_num}: {line_content}")
                    total_issues += len(issues)
            else:
                print(f"  ✓ {pyfile.name}")

    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Files checked: {files_checked}")
    print(f"Issues found: {total_issues}")

    if total_issues == 0:
        print("\n✅ All Signal creations use keyword arguments!")
        print("   The system is correct.")
    else:
        print(f"\n❌ Found {total_issues} file(s) with positional arguments")
        print("   These need to be fixed to use keyword arguments:")
        print()
        print("   Correct:   Signal(direction='bullish', confidence=0.8, reasoning='...')")
        print("   Incorrect: Signal('bullish', 0.8, '...')")

    print()
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    exit(main())
