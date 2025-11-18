#!/bin/bash

# Final Pre-Release Verification
# Run this before pushing to public GitHub

echo "🔍 Pre-Release Verification"
echo "============================"
echo ""

ISSUES=0

# 1. Check key documentation exists
echo "📚 Checking Documentation..."
REQUIRED_DOCS=(
    "README.md"
    "QUICK_START.md"
    "GUI_QUICK_START.md"
    "DISCLAIMER.md"
    "LICENSE"
    "CONTRIBUTING.md"
)

for doc in "${REQUIRED_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc"
    else
        echo "  ❌ MISSING: $doc"
        ISSUES=$((ISSUES + 1))
    fi
done

# 2. Check internal docs removed
echo ""
echo "🧹 Checking Internal Docs Removed..."
SHOULD_NOT_EXIST=(
    "IMPLEMENTATION_CHECKLIST.md"
    "IMPLEMENTATION_PLAN.md"
    "WIZARD_IMPLEMENTATION.md"
    "test_wizard.sh"
)

for doc in "${SHOULD_NOT_EXIST[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ⚠️  STILL EXISTS: $doc (should be removed)"
        ISSUES=$((ISSUES + 1))
    else
        echo "  ✅ Removed: $doc"
    fi
done

# 3. Check GUI files
echo ""
echo "🎨 Checking GUI Files..."
GUI_FILES=(
    "gui/app.py"
    "gui/how_to_page.py"
    "gui/llm_setup_wizard.py"
    "gui/code_viewer.py"
    "gui/agent_creator.py"
    "gui/agent_tester.py"
)

for file in "${GUI_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ MISSING: $file"
        ISSUES=$((ISSUES + 1))
    fi
done

# 4. Check examples exist
echo ""
echo "📋 Checking Example Agents..."
if [ -d "examples" ]; then
    NUM_EXAMPLES=$(ls examples/*.py 2>/dev/null | wc -l)
    if [ "$NUM_EXAMPLES" -gt 0 ]; then
        echo "  ✅ Found $NUM_EXAMPLES example agents"
    else
        echo "  ⚠️  No example agents found"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "  ❌ examples/ directory missing"
    ISSUES=$((ISSUES + 1))
fi

# 5. Check for sensitive info
echo ""
echo "🔒 Checking for Sensitive Information..."
if [ -f ".env" ]; then
    echo "  ⚠️  .env file exists (should not be committed)"
    if git ls-files --error-unmatch .env 2>/dev/null; then
        echo "  ❌ .env is tracked by git! Remove it!"
        ISSUES=$((ISSUES + 1))
    else
        echo "  ✅ .env not tracked (good)"
    fi
fi

if [ -f ".env.example" ]; then
    echo "  ✅ .env.example exists (good)"
else
    echo "  ⚠️  .env.example missing (should exist as template)"
fi

# 6. Check .gitignore
echo ""
echo "📝 Checking .gitignore..."
if [ -f ".gitignore" ]; then
    if grep -q ".env" .gitignore; then
        echo "  ✅ .env in .gitignore"
    else
        echo "  ⚠️  .env not in .gitignore (add it!)"
    fi
    
    if grep -q "__pycache__" .gitignore; then
        echo "  ✅ __pycache__ in .gitignore"
    else
        echo "  ⚠️  __pycache__ not in .gitignore"
    fi
else
    echo "  ❌ .gitignore missing!"
    ISSUES=$((ISSUES + 1))
fi

# 7. Check for TODO/FIXME in public docs
echo ""
echo "📌 Checking for TODOs in Public Docs..."
if grep -r "TODO\|FIXME" README.md QUICK_START.md GUI_QUICK_START.md 2>/dev/null; then
    echo "  ⚠️  Found TODO/FIXME in public docs"
    ISSUES=$((ISSUES + 1))
else
    echo "  ✅ No TODOs in public documentation"
fi

# 8. Check Python syntax
echo ""
echo "🐍 Checking Python Syntax..."
python3 -m py_compile gui/llm_setup_wizard.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ llm_setup_wizard.py syntax OK"
else
    echo "  ❌ Syntax error in llm_setup_wizard.py"
    ISSUES=$((ISSUES + 1))
fi

python3 -m py_compile gui/code_viewer.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ code_viewer.py syntax OK"
else
    echo "  ❌ Syntax error in code_viewer.py"
    ISSUES=$((ISSUES + 1))
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $ISSUES -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED!"
    echo ""
    echo "📦 Ready for public release!"
    echo ""
    echo "Next steps:"
    echo "  1. git add ."
    echo "  2. git commit -m 'Public release v1.0.0-edu'"
    echo "  3. git tag v1.0.0-edu"
    echo "  4. git push origin main"
    echo "  5. git push origin v1.0.0-edu"
    echo "  6. Create GitHub release"
    echo ""
    exit 0
else
    echo "❌ FOUND $ISSUES ISSUE(S)"
    echo ""
    echo "Please fix the issues above before releasing."
    echo ""
    exit 1
fi
