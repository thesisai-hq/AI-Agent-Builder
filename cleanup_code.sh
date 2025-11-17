#!/bin/bash

# Clean up all ruff warnings (whitespace and formatting)

echo "🧹 Cleaning Code with Ruff..."
echo "=============================="
echo ""

# Check if ruff is installed
if ! command -v ruff &> /dev/null; then
    echo "📦 Installing ruff..."
    pip install ruff
fi

echo "🔍 Running ruff check with auto-fix..."
ruff check --fix --unsafe-fixes .

echo ""
echo "✨ Running ruff format..."
ruff format .

echo ""
echo "🧪 Verifying no remaining issues..."
ruff check .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Code is clean!"
    echo ""
    echo "Changes made:"
    echo "  - Removed trailing whitespace"
    echo "  - Fixed import organization"
    echo "  - Consistent code formatting"
    echo "  - Fixed blank line whitespace"
    echo ""
    echo "📝 Review changes:"
    echo "  git diff"
    echo ""
    echo "💾 Commit if looks good:"
    echo "  git add ."
    echo "  git commit -m 'Code cleanup with ruff'"
else
    echo ""
    echo "⚠️  Some issues remain. Review output above."
fi
