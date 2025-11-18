#!/bin/bash
# AI-Agent-Builder One-Click Installer
# Compatible with: Linux, macOS, WSL2

set -e  # Exit on error

echo "🤖 AI Agent Builder - Automated Installation"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

# Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "   Please install Python 3.10+ first:"
    echo "   → macOS: brew install python@3.11"
    echo "   → Ubuntu/Debian: sudo apt install python3.11"
    echo "   → Download: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check Python version >= 3.10
if [ "$(echo "$PYTHON_VERSION < 3.10" | bc)" -eq 1 ]; then
    echo -e "${RED}❌ Python 3.10+ required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

# Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found${NC}"
    echo "   Please install Docker first:"
    echo "   → macOS: https://docs.docker.com/desktop/install/mac-install/"
    echo "   → Linux: https://docs.docker.com/engine/install/"
    echo "   → Windows: Use WSL2 + Docker Desktop"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Check if Docker is running
if ! docker ps &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker is installed but not running${NC}"
    echo "   Please start Docker and run this script again."
    echo ""
    echo "   → macOS: Open Docker Desktop application"
    echo "   → Linux: sudo systemctl start docker"
    exit 1
fi
echo -e "${GREEN}✅ Docker running${NC}"

echo ""
echo "🔧 Setting up environment..."
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install framework
echo "📦 Installing AI Agent Builder..."
echo "   (This may take 2-3 minutes...)"
pip install -e ".[all]" > /dev/null 2>&1
echo -e "${GREEN}✅ Framework installed${NC}"
echo ""

# Setup database
echo "🗄️  Setting up PostgreSQL database..."

# Copy environment config if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   Created .env configuration"
fi

# Start PostgreSQL
echo "   Starting PostgreSQL container..."
docker compose up -d postgres

# Wait for PostgreSQL to be ready
echo "   Waiting for database to initialize (10 seconds)..."
sleep 10

# Seed database
echo "   Adding sample data (AAPL, MSFT, TSLA, JPM)..."
python seed_data.py > /dev/null 2>&1
echo -e "${GREEN}✅ Database ready with sample data${NC}"
echo ""

# Success message
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Starting GUI in 3 seconds..."
echo "   URL: http://localhost:8501"
echo ""
echo "📖 First time? Follow the tutorial in the GUI"
echo "❓ Need help? Check docs/ folder"
echo ""

# Wait 3 seconds
sleep 3

# Launch GUI
./gui/launch.sh
