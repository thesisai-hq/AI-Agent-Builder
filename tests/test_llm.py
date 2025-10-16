"""
Test LLM Providers
"""

import sys

sys.path.insert(0, ".")

from agent_builder.llm.ollama import OllamaProvider
from agent_builder.llm.groq import GroqProvider
from agent_builder.llm.factory import get_llm_provider
import os


def test_ollama():
    """Test Ollama provider"""
    print("\n" + "=" * 60)
    print("Testing Ollama Provider")
    print("=" * 60)

    llm = OllamaProvider(model="llama3.2")

    # Check if available
    print("\n1️⃣ Checking Ollama availability...")
    if llm.is_available():
        print("   ✅ Ollama is running")

        # List models
        models = llm.list_models()
        print(f"   Available models: {', '.join(models[:5])}")
    else:
        print("   ❌ Ollama not running")
        print("   Start with: ollama serve")
        return False

    # Test generation
    print("\n2️⃣ Testing text generation...")
    response = llm.generate("Say 'test successful' and nothing else", max_tokens=20)
    print(f"   Response: {response}")

    if response:
        print("   ✅ Generation working")
    else:
        print("   ❌ Generation failed")
        return False

    # Test chat
    print("\n3️⃣ Testing chat completion...")
    chat_response = llm.chat(
        [{"role": "user", "content": "What is 2+2? Answer with just the number."}],
        max_tokens=10,
    )
    print(f"   Response: {chat_response}")

    if chat_response:
        print("   ✅ Chat working")

    print("\n✅ Ollama tests passed!")
    return True


def test_groq():
    """Test Groq provider"""
    print("\n" + "=" * 60)
    print("Testing Groq Provider")
    print("=" * 60)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("\n⚠️  GROQ_API_KEY not set")
        print("   Get free key from: console.groq.com")
        print("   Add to .env: GROQ_API_KEY=gsk_...")
        return False

    llm = GroqProvider(api_key=api_key)

    # Check if available
    print("\n1️⃣ Checking Groq availability...")
    if llm.is_available():
        print("   ✅ Groq API accessible")
    else:
        print("   ❌ Cannot connect to Groq")
        print("   Check your API key")
        return False

    # Test generation
    print("\n2️⃣ Testing text generation...")
    response = llm.generate("Say 'test successful' and nothing else", max_tokens=20)
    print(f"   Response: {response}")

    if response:
        print("   ✅ Generation working")
    else:
        print("   ❌ Generation failed")
        return False

    # Test chat
    print("\n3️⃣ Testing chat completion...")
    chat_response = llm.chat(
        [{"role": "user", "content": "What is 2+2? Answer with just the number."}],
        max_tokens=10,
    )
    print(f"   Response: {chat_response}")

    if chat_response:
        print("   ✅ Chat working")

    print("\n✅ Groq tests passed!")
    return True


def test_factory():
    """Test LLM factory"""
    print("\n" + "=" * 60)
    print("Testing LLM Factory")
    print("=" * 60)

    llm = get_llm_provider()

    if llm:
        print(f"\n✅ Provider: {llm.__class__.__name__}")
        print(f"   Model: {llm.model}")

        # Quick test
        response = llm.generate("Hello", max_tokens=10)
        if response:
            print(f"   Response: {response[:50]}...")
            print("   ✅ Factory working")
        else:
            print("   ⚠️  No response from LLM")
    else:
        print("\n❌ No LLM provider configured")
        print("   Set LLM_PROVIDER in .env")
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 LLM Provider Tests")
    print("=" * 60)

    provider = os.getenv("LLM_PROVIDER", "ollama")

    if provider == "ollama":
        test_ollama()
    elif provider == "groq":
        test_groq()
    else:
        print(f"Unknown provider: {provider}")

    # Test factory
    test_factory()

    print("\n" + "=" * 60)
    print("✅ LLM tests complete!")
    print("=" * 60)
