#!/bin/bash
# Launch Agent Builder GUI

echo "🚀 Launching Agent Builder GUI..."
echo ""
echo "Opening browser at http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

# Change to AI-Agent-Builder root directory
cd "$(dirname "$0")/.."

# Launch Streamlit
streamlit run gui/app.py
