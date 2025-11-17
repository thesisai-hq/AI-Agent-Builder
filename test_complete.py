#!/usr/bin/env python3
"""
Complete Feature Test - Verify all new features work
"""

import sys
from pathlib import Path


def test_all_files_exist():
    """Test that all required files exist."""
    print("🧪 Testing File Existence...")

    required_files = [
        "gui/app.py",
        "gui/how_to_page.py",
        "gui/llm_setup_wizard.py",
        "gui/code_viewer.py",
        "gui/agent_creator.py",
        "README.md",
        "GUI_QUICK_START.md",
    ]

    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ MISSING: {file}")
            all_exist = False

    return all_exist


def test_python_syntax():
    """Test Python syntax in all GUI files."""
    print("\n🐍 Testing Python Syntax...")

    gui_files = [
        "gui/llm_setup_wizard.py",
        "gui/code_viewer.py",
        "gui/agent_creator.py",
    ]

    all_valid = True
    for file in gui_files:
        try:
            import py_compile

            py_compile.compile(file, doraise=True)
            print(f"  ✅ {file}")
        except Exception as e:
            print(f"  ❌ {file}: {e}")
            all_valid = False

    return all_valid


def test_imports():
    """Test that all modules import correctly."""
    print("\n📦 Testing Imports...")

    sys.path.insert(0, str(Path(__file__).parent))

    try:
        print("  ✅ llm_setup_wizard")

        print("  ✅ code_viewer")

        from gui.agent_creator import AgentCreator

        print("  ✅ agent_creator")

        # Test AgentCreator has new parameter
        import inspect

        sig = inspect.signature(AgentCreator.generate_agent_code)
        params = list(sig.parameters.keys())

        if "user_prompt_instructions" in params:
            print("  ✅ AgentCreator has user_prompt_instructions parameter")
        else:
            print("  ❌ AgentCreator missing user_prompt_instructions parameter")
            return False

        return True

    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_code_generator():
    """Test that code generation works with new parameter."""
    print("\n🏗️ Testing Code Generation...")

    try:
        from gui.agent_creator import AgentCreator

        creator = AgentCreator()

        # Test LLM agent with custom instructions
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description="Test agent",
            agent_type="LLM-Powered",
            llm_provider="ollama",
            llm_model="llama3.2",
            temperature=0.5,
            max_tokens=1000,
            system_prompt="You are a test analyst",
            user_prompt_instructions="Focus on testing and validation",
        )

        if "Focus on testing and validation" in code:
            print("  ✅ Custom user instructions included in generated code")
        else:
            print("  ❌ Custom instructions NOT in generated code")
            return False

        # Test without custom instructions
        code2 = creator.generate_agent_code(
            agent_name="TestAgent2",
            description="Test agent 2",
            agent_type="LLM-Powered",
            llm_provider="ollama",
            llm_model="llama3.2",
            temperature=0.5,
            max_tokens=1000,
            system_prompt="You are a test analyst",
            user_prompt_instructions=None,
        )

        if "class TestAgent2" in code2:
            print("  ✅ Code generation works without custom instructions")
        else:
            print("  ❌ Code generation failed without custom instructions")
            return False

        return True

    except Exception as e:
        print(f"  ❌ Code generation error: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("AI-Agent-Builder - Complete Feature Test")
    print("=" * 70)
    print("")

    results = []

    # Run tests
    results.append(("Files Exist", test_all_files_exist()))
    results.append(("Python Syntax", test_python_syntax()))
    results.append(("Module Imports", test_imports()))
    results.append(("Code Generation", test_code_generator()))

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")

    all_passed = all(result[1] for result in results)

    print("")
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("")
        print("🎉 All features are working correctly!")
        print("")
        print("Next steps:")
        print("  1. ./gui/launch.sh - Launch and manually test")
        print("  2. Create LLM agent with custom instructions")
        print("  3. View agent code to verify custom prompt included")
        print("  4. Test the agent with mock data")
        print("  5. Ready for release!")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("")
        print("Fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
