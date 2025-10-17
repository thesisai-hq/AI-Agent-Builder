#!/bin/bash
set -e

echo "=========================================="
echo "Agent Builder - Docker Quick Start"
echo "=========================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

echo "✅ Docker installed"

# Check Docker Compose (v1 or v2)
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
    echo "✅ Docker Compose v1 installed"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
    echo "✅ Docker Compose v2 installed"
else
    echo "❌ Docker Compose not found"
    exit 1
fi

echo ""

# Create .env
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.docker .env
    echo "✅ .env created"
else
    echo "ℹ️  .env already exists"
fi
echo ""

# Clean up any existing containers with issues
echo "🧹 Cleaning up old containers..."
$COMPOSE_CMD down --remove-orphans 2>/dev/null || true

echo "🐘 Starting fresh PostgreSQL database..."
$COMPOSE_CMD up -d postgres

echo "⏳ Waiting for database (30 seconds)..."
sleep 10

# Wait for healthy status
for i in {1..20}; do
    if $COMPOSE_CMD ps postgres | grep -q "Up"; then
        echo "✅ PostgreSQL is running!"
        break
    fi
    echo -n "."
    sleep 1
done

echo ""
echo ""
echo "=========================================="
echo "✨ Setup Complete!"
echo "=========================================="
echo ""
echo "📊 Database Connection:"
echo "   Host: localhost"
echo "   Port: 5432"
echo "   Database: agentbuilder"
echo "   User: agent_user"
echo "   Password: agent_password"
echo ""
echo "🔗 Connection String:"
echo "   postgresql://agent_user:agent_password@localhost:5432/agentbuilder"
echo ""
echo "📝 Next Steps:"
echo "   1. Test connection: docker exec agentbuilder_db psql -U agent_user -d agentbuilder -c 'SELECT 1'"
echo "   2. Install deps: pip install -r requirements.txt"
echo "   3. Run API: python main.py"
echo "   4. Visit: http://localhost:8000/docs"
echo ""
