@echo off
REM Launch Agent Builder GUI for Windows

echo 🚀 Launching Agent Builder GUI...
echo.
echo Opening browser at http://localhost:8501
echo Press Ctrl+C to stop
echo.

REM Change to AI-Agent-Builder root directory
cd /d "%~dp0\.."

REM Launch Streamlit
streamlit run gui\0_🏠_Home.py
