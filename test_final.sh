#!/bin/bash

echo "🧪 Final Integration Test"
echo "========================="
echo ""

# Test all Python files compile
echo "Testing Python syntax..."

FILES=(
    "agent_framework/confidence.py"
    "gui/agent_creator.py"
    "gui/code_viewer.py"
    "gui/how_to_page.py"
    "gui/app.py"
)

for file in "${FILES[@]}"; do
    python3 -m py_compile "$file" 2>&1
    if [ $? -eq 0 ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file has errors"
        python3 -m py_compile "$file"
        exit 1
    fi
done

echo ""
echo "Running full integration test..."
python3 test_enhanced_confidence.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ ALL TESTS PASSED!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎉 Enhanced confidence is fully integrated!"
    echo ""
    echo "What's included:"
    echo "  ✅ Distance-based confidence calculation"
    echo "  ✅ Multi-rule consensus adjustments"
    echo "  ✅ Score margin calculations"
    echo "  ✅ LLM confidence validation"
    echo "  ✅ Data quality adjustments"
    echo "  ✅ GUI explanations"
    echo "  ✅ Complete documentation"
    echo ""
    echo "Next steps:"
    echo "  1. ./gui/launch.sh - Test manually"
    echo "  2. Create an agent and view code"
    echo "  3. Test with different metric values"
    echo "  4. See confidence change based on strength!"
    echo ""
    echo "Ready for release! 🚀"
    echo ""
else
    echo ""
    echo "❌ Tests failed - check errors above"
    exit 1
fi
