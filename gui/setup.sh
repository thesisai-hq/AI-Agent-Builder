#!/bin/bash
# Setup script for Agent Builder GUI

set -e

echo "=================================="
echo "Agent Builder GUI Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from AI-Agent-Builder root directory"
    exit 1
fi

# Install framework if not already installed
echo ""
echo "Installing AI-Agent-Builder framework..."
pip install -e . > /dev/null 2>&1 || pip install -e .
echo "✓ Framework installed"

# Install GUI dependencies
echo ""
echo "Installing GUI dependencies..."
pip install -r gui/requirements.txt > /dev/null 2>&1 || pip install -r gui/requirements.txt
echo "✓ GUI dependencies installed"

# Create examples directory if it doesn't exist
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
    echo "   Run: chmod 755 examples/"
    exit 1
fi

# Run setup test
echo ""
echo "Running setup verification..."
python3 gui/test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Testing Signal creation..."
    python3 gui/test_signal.py
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Start the GUI with:"
echo "  streamlit run gui/app.py"
echo ""
echo "Or use the launch script:"
echo "  ./gui/launch.sh"
echo ""
