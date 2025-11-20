#!/bin/bash
# GUI Test Runner Script
# Runs all GUI tests with coverage reporting

set -e  # Exit on error

echo "=================================="
echo "GUI Test Suite Runner"
echo "=================================="
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing test dependencies..."
    pip install pytest pytest-asyncio pytest-cov pytest-mock
fi

# Navigate to tests directory
cd "$(dirname "$0")"

echo "📍 Current directory: $(pwd)"
echo ""

# Run tests with different configurations
echo "=================================="
echo "Running All Tests"
echo "=================================="
pytest -v --asyncio-mode=auto

echo ""
echo "=================================="
echo "Running with Coverage"
echo "=================================="
pytest --cov=../../gui \
       --cov-report=term \
       --cov-report=html \
       --asyncio-mode=auto \
       -v

echo ""
echo "=================================="
echo "Test Summary by Category"
echo "=================================="

echo ""
echo "🔐 Security Tests:"
pytest test_security.py -v --tb=short

echo ""
echo "⚡ Async Tests:"
pytest test_async_utils.py -v --tb=short

echo ""
echo "🧩 Component Tests:"
pytest test_components.py -v --tb=short

echo ""
echo "🔗 Integration Tests:"
pytest test_integration.py -v --tb=short --asyncio-mode=auto

echo ""
echo "=================================="
echo "Coverage Report Generated"
echo "=================================="
echo "📊 HTML Report: tests/gui/htmlcov/index.html"
echo "📄 Open in browser: file://$(pwd)/htmlcov/index.html"

echo ""
echo "=================================="
echo "✅ Test Suite Complete!"
echo "=================================="
