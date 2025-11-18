@echo off
REM AI-Agent-Builder One-Click Installer for Windows
REM Requires: Python 3.10+, Docker Desktop

setlocal enabledelayedexpansion

echo.
echo 🤖 AI Agent Builder - Automated Installation
echo ==============================================
echo.

REM Check Python
echo 📋 Checking prerequisites...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    echo    Please install Python 3.10+ first:
    echo    → Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not found
    echo    Please install Docker Desktop:
    echo    → Download: https://docs.docker.com/desktop/install/windows-install/
    echo.
    pause
    exit /b 1
)
echo ✅ Docker found

REM Check if Docker is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker is installed but not running
    echo    Please start Docker Desktop and run this script again.
    echo.
    pause
    exit /b 1
)
echo ✅ Docker running

echo.
echo 🔧 Setting up environment...
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install framework
echo 📦 Installing AI Agent Builder...
echo    (This may take 2-3 minutes...)
pip install -e ".[all]" >nul 2>&1
echo ✅ Framework installed
echo.

REM Setup database
echo 🗄️ Setting up PostgreSQL database...

REM Copy environment config if not exists
if not exist .env (
    copy .env.example .env >nul
    echo    Created .env configuration
)

REM Start PostgreSQL
echo    Starting PostgreSQL container...
docker compose up -d postgres

REM Wait for PostgreSQL to be ready
echo    Waiting for database to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

REM Seed database
echo    Adding sample data (AAPL, MSFT, TSLA, JPM)...
python seed_data.py >nul 2>&1
echo ✅ Database ready with sample data
echo.

REM Success message
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✅ Installation Complete!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🚀 Starting GUI in 3 seconds...
echo    URL: http://localhost:8501
echo.
echo 📖 First time? Follow the tutorial in the GUI
echo ❓ Need help? Check docs\ folder
echo.

REM Wait 3 seconds
timeout /t 3 /nobreak >nul

REM Launch GUI
call gui\launch.bat
