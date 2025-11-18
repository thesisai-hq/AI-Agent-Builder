#!/bin/bash

# One-command release execution
# Run this when you're ready to go public

echo "🚀 AI-Agent-Builder Public Release"
echo "===================================="
echo ""
echo "This will prepare your repository for public release."
echo ""
read -p "Ready to proceed? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Step 1: Clean
echo ""
echo "Step 1/4: Cleaning internal documents..."
chmod +x clean_internal_docs.sh
./clean_internal_docs.sh

echo ""
echo "Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete
echo "✅ Clean complete"

# Step 2: Verify
echo ""
echo "Step 2/4: Running verification..."
chmod +x verify_release.sh
./verify_release.sh

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Verification failed. Fix issues before releasing."
    exit 1
fi

# Step 3: Git
echo ""
echo "Step 3/4: Git commit and tag..."
git add .
git commit -m "Public release v1.0.0-edu: Educational investment analysis tool

Features:
- Visual GUI for agent creation (no coding required)
- Interactive LLM setup wizard
- Educational code viewer with annotations  
- Comprehensive 8-tab tutorial
- Support for Rule/LLM/RAG/Hybrid agents
- Mock and real data (YFinance)
- Complete documentation for students and universities"

git tag -a v1.0.0-edu -m "Educational release for finance students"

echo "✅ Committed and tagged"

# Step 4: Ready to push
echo ""
echo "Step 4/4: Ready to push to GitHub"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Repository is ready for public release!"
echo ""
echo "Next commands to run:"
echo ""
echo "  git push origin main"
echo "  git push origin v1.0.0-edu"
echo ""
echo "Then create GitHub release at:"
echo "  https://github.com/yourusername/AI-Agent-Builder/releases/new"
echo ""
echo "Tag: v1.0.0-edu"
echo "Title: AI Agent Builder v1.0.0 - Educational Release"
echo ""
echo "Copy description from: PUBLIC_RELEASE_CHECKLIST.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
