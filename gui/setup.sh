#!/bin/bash
# Setup script for Agent Builder GUI
# Installs ALL dependencies for full GUI functionality

set -e

echo "=================================="
echo "Agent Builder GUI Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✓ Python $python_version"
else
    echo "❌ Error: Python 3.10+ required (found $python_version)"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from AI-Agent-Builder root directory"
    echo "   Run from: ~/AI-Agent-Builder/"
    exit 1
fi

echo "✓ Correct directory"

# Install framework with ALL dependencies
echo ""
echo "Installing AI-Agent-Builder framework with all dependencies..."
echo "This includes: FastAPI, PostgreSQL, LLM providers, RAG support"
echo ""

pip install -e ".[all]" || {
    echo "❌ Framework installation failed"
    exit 1
}

echo "✓ Framework installed with all dependencies"

# Install GUI-specific dependencies
echo ""
echo "Installing GUI dependencies..."
pip install -r gui/requirements.txt || {
    echo "❌ GUI dependencies installation failed"
    exit 1
}

echo "✓ GUI dependencies installed"

# Verify critical packages
echo ""
echo "Verifying installations..."

# Check streamlit
python3 -c "import streamlit" 2>/dev/null && echo "✓ Streamlit" || echo "❌ Streamlit missing"

# Check PyPDF2
python3 -c "import PyPDF2" 2>/dev/null && echo "✓ PyPDF2" || echo "❌ PyPDF2 missing"

# Check LLM packages
python3 -c "import ollama" 2>/dev/null && echo "✓ Ollama" || echo "⚠  Ollama not installed (optional)"
python3 -c "import openai" 2>/dev/null && echo "✓ OpenAI" || echo "⚠  OpenAI not installed (optional)"
python3 -c "import anthropic" 2>/dev/null && echo "✓ Anthropic" || echo "⚠  Anthropic not installed (optional)"

# Check RAG packages
python3 -c "import sentence_transformers" 2>/dev/null && echo "✓ sentence-transformers" || echo "⚠  sentence-transformers not installed (optional)"

# Create examples directory if it doesn't exist
echo ""
if [ ! -d "examples" ]; then
    mkdir examples
    echo "✓ Created examples/ directory"
else
    echo "✓ examples/ directory exists"
fi

# Test file permissions
echo ""
echo "Testing file permissions..."
test_file="examples/.test_write_permission"
if touch "$test_file" 2>/dev/null; then
    rm "$test_file"
    echo "✓ Write permissions OK"
else
    echo "❌ Error: Cannot write to examples/ directory"
    echo "   Fix: chmod 755 examples/"
    exit 1
fi

# Run comprehensive setup verification
echo ""
echo "Running setup verification..."
python3 gui/test_setup.py || {
    echo "⚠  Setup test had warnings (check output above)"
}

# Test signal creation
echo ""
echo "Testing Signal creation..."
python3 gui/test_signal.py || {
    echo "❌ Signal test failed"
    exit 1
}

echo "✓ All tests passed"

# Show dependency summary
echo ""
echo "=================================="
echo "Dependency Summary"
echo "=================================="
echo ""
echo "Core Framework:"
echo "  ✓ FastAPI, Pydantic, AsyncPG"
echo ""
echo "LLM Providers (for LLM/Hybrid/RAG agents):"
python3 -c "import ollama" 2>/dev/null && echo "  ✓ Ollama" || echo "  ✗ Ollama (install: pip install ollama)"
python3 -c "import openai" 2>/dev/null && echo "  ✓ OpenAI" || echo "  ✗ OpenAI (install: pip install openai)"
python3 -c "import anthropic" 2>/dev/null && echo "  ✓ Anthropic" || echo "  ✗ Anthropic (install: pip install anthropic)"
echo ""
echo "RAG Support (for RAG agents):"
python3 -c "import sentence_transformers" 2>/dev/null && echo "  ✓ sentence-transformers" || echo "  ✗ sentence-transformers (install: pip install sentence-transformers)"
echo ""
echo "GUI:"
echo "  ✓ Streamlit"
echo "  ✓ PyPDF2"
echo ""

# Provide helpful next steps
echo "=================================="
echo "Setup Complete! ✅"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the GUI:"
echo "   ./gui/launch.sh"
echo "   or: streamlit run gui/app.py"
echo ""
echo "2. For LLM/Hybrid/RAG agents, you also need:"
echo ""

# Check what's still needed
needs_ollama=false
needs_rag=false

python3 -c "import ollama" 2>/dev/null || needs_ollama=true
python3 -c "import sentence_transformers" 2>/dev/null || needs_rag=true

if [ "$needs_ollama" = true ]; then
    echo "   Ollama (free, local AI):"
    echo "   - Install: curl https://ollama.ai/install.sh | sh"
    echo "   - Download model: ollama pull llama3.2"
    echo "   - Start service: ollama serve"
    echo ""
fi

if [ "$needs_rag" = true ]; then
    echo "   RAG support (for document analysis):"
    echo "   - Install: pip install sentence-transformers"
    echo ""
fi

if [ "$needs_ollama" = false ] && [ "$needs_rag" = false ]; then
    echo "   All optional dependencies installed! ✓"
    echo ""
fi

echo "3. Create your first agent:"
echo "   - Open GUI: ./gui/launch.sh"
echo "   - Navigate to '➕ Create Agent'"
echo "   - Start with Rule-Based (no LLM needed)"
echo ""
echo "Happy building! 🚀"
echo ""
