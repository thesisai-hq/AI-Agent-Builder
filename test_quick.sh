#!/bin/bash

# Quick test of enhanced confidence integration

echo "🧪 Quick Enhanced Confidence Test"
echo "===================================="
echo ""

# Test Python syntax
echo "Testing Python syntax..."
python3 -m py_compile agent_framework/confidence.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ confidence.py compiles"
else
    echo "❌ confidence.py has syntax errors"
    exit 1
fi

python3 -m py_compile gui/agent_creator.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ agent_creator.py compiles"
else
    echo "❌ agent_creator.py has syntax errors"
    exit 1
fi

python3 -m py_compile gui/how_to_page.py 2>&1
if [ $? -eq 0 ]; then
    echo "✅ how_to_page.py compiles"
else
    echo "❌ how_to_page.py has syntax errors"
    exit 1
fi

echo ""
echo "Running full integration test..."
python3 test_enhanced_confidence.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ALL TESTS PASSED!"
    echo ""
    echo "Next: Launch GUI and test manually"
    echo "  ./gui/launch.sh"
    echo ""
else
    echo ""
    echo "❌ Tests failed - check errors above"
    exit 1
fi
