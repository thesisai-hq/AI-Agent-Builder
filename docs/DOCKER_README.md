# Docker Setup for Agent Builder

## 🚀 Quick Start

### Option 1: Automated (Recommended)
```bash
chmod +x docker_quickstart.sh
./docker_quickstart.sh
```

### Option 2: Manual with Make
```bash
make start      # Start database
make test       # Test connection
make seed       # Load mock data
```

## 📊 Connection Details

```
Host: localhost
Port: 5432
Database: agentbuilder
User: agent_user
Password: agent_password

Connection String:
postgresql://agent_user:agent_password@localhost:5432/agentbuilder
```

## 🔧 Useful Commands

```bash
# Start/Stop
make start
make stop
make restart

# Database
make shell      # PostgreSQL CLI
make logs       # View logs
make test       # Test connection
make seed       # Load data

# Maintenance
make backup     # Backup database
make clean      # Remove containers
make reset      # Complete reset
```

## 🆘 Troubleshooting


**Quick fixes:**
```bash
# Clean start
docker-compose down --remove-orphans
./docker_quickstart.sh

# Or use simple version (no compose)
./docker_simple.sh
```

## 📝 Next Steps

After database is running:
```bash
pip install -r requirements.txt
python main.py
```

Visit: http://localhost:8000/docs
