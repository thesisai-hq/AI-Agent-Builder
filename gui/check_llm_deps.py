#!/usr/bin/env python3
"""Check which LLM providers are available on this machine."""

import sys


def check_provider(provider_name: str, package_name: str, install_cmd: str):
    """Check if a provider package is installed.
    
    Args:
        provider_name: Display name (e.g., "OpenAI")
        package_name: Python package name (e.g., "openai")
        install_cmd: Installation command
    """
    try:
        __import__(package_name)
        print(f"✓ {provider_name:12} - Available")
        return True
    except ImportError:
        print(f"✗ {provider_name:12} - Not installed")
        print(f"  Install: {install_cmd}")
        return False


def main():
    """Check all LLM providers."""
    print("=" * 60)
    print("LLM Provider Availability Check")
    print("=" * 60)
    print()
    
    providers = [
        ("OpenAI", "openai", "pip install openai"),
        ("Anthropic", "anthropic", "pip install anthropic"),
        ("Ollama", "ollama", "pip install ollama"),
    ]
    
    available = []
    missing = []
    
    for provider_name, package_name, install_cmd in providers:
        if check_provider(provider_name, package_name, install_cmd):
            available.append(provider_name)
        else:
            missing.append(provider_name)
        print()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Available: {', '.join(available) if available else 'None'}")
    print(f"Missing:   {', '.join(missing) if missing else 'None'}")
    
    if missing:
        print()
        print("To install all LLM providers:")
        print("  pip install 'ai-agent-framework[llm]'")
        print()
        print("Or install individually:")
        for provider_name, package_name, install_cmd in providers:
            if provider_name in missing:
                print(f"  {install_cmd}")
    
    print()
    
    # Check framework
    print("=" * 60)
    print("Framework Check")
    print("=" * 60)
    try:
        import agent_framework
        print("✓ agent_framework is installed")
        print(f"  Version: {getattr(agent_framework, '__version__', 'unknown')}")
    except ImportError:
        print("✗ agent_framework is NOT installed")
        print("  Install: pip install -e .")
    
    print()
    
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
