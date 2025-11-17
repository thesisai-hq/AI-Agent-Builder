#!/bin/bash

# Clean up internal implementation documents
# Keep only public-facing documentation

echo "🧹 Cleaning Internal Documents..."
echo "================================="
echo ""

# List of internal documents to remove
INTERNAL_DOCS=(
    "IMPLEMENTATION_CHECKLIST.md"
    "IMPLEMENTATION_PLAN.md"
    "IMPLEMENTATION_STATUS.md"
    "IMPLEMENTATION_SUMMARY.md"
    "WIZARD_IMPLEMENTATION.md"
    "WIZARD_COMPLETE.md"
    "RELEASE_GUIDE.md"
    "THIS_STATUS.md"
    "TESTING_INSTRUCTIONS.md"
    "ASYNC_DESIGN_CHANGE.md"
    "HYBRID_TYPE_FIX.md"
    "QUICK_REFERENCE.md"
    "test_wizard_integration.sh"
    "test_wizard.sh"
    "test_wizard_python.py"
    "test_gui.sh"
    "test_phase1.sh"
    "TEST_PHASE1.sh"
)

# Count files
TOTAL=0
REMOVED=0

for file in "${INTERNAL_DOCS[@]}"; do
    TOTAL=$((TOTAL + 1))
    if [ -f "$file" ]; then
        echo "🗑️  Removing: $file"
        rm "$file"
        REMOVED=$((REMOVED + 1))
    else
        echo "⏭️  Skip: $file (not found)"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Cleanup Complete!"
echo "   Removed: $REMOVED/$TOTAL files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Remaining Documentation (Public):"
echo ""
echo "Root level:"
echo "  ✅ README.md - Main documentation"
echo "  ✅ QUICK_START.md - 5-minute setup"
echo "  ✅ GUI_QUICK_START.md - Visual GUI guide"
echo "  ✅ DISCLAIMER.md - Legal terms"
echo "  ✅ LICENSE - MIT License"
echo "  ✅ CONTRIBUTING.md - How to contribute"
echo "  ✅ CHANGELOG.md - Version history"
echo ""
echo "docs/ directory:"
echo "  ✅ GETTING_STARTED.md"
echo "  ✅ CHOOSING_AGENT_TYPE.md"
echo "  ✅ LLM_CUSTOMIZATION.md"
echo "  ✅ HYBRID_AGENTS.md"
echo "  ✅ CONFIGURATION.md"
echo "  ✅ DATABASE_SETUP.md"
echo "  ✅ TROUBLESHOOTING.md"
echo "  ✅ API_REFERENCE.md"
echo "  ✅ PROJECT_STRUCTURE.md"
echo "  ✅ AGENT_FILE_GUIDELINES.md"
echo ""
echo "✅ Documentation is clean and ready for public release!"
