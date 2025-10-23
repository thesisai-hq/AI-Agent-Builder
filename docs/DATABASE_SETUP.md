# Database Setup Guide

This guide covers setting up PostgreSQL for the AI Agent Framework using Docker (recommended) or local installation.

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Python 3.10+ with the framework installed

### 3-Step Setup

```bash
# 1. Start PostgreSQL (maps to port 5433 on host to avoid conflicts)
docker-compose up -d postgres

# 2. Seed with sample data
python seed_data.py

# 3. Verify
python quickstart.py
```

Done! Your database is ready with 4 sample tickers.

## Docker Configuration

### docker-compose.yml

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: agent_framework_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: agent_framework
    ports:
      - "5433:5432"  # Mapped to 5433 to avoid conflicts
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./schema.sql:/docker-entrypoint-initdb.d/01_schema.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Connection String

```bash
# For Docker (port 5433 on host)
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agent_framework

# For local PostgreSQL (port 5432)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agent_framework
```

## Database Management

### Starting and Stopping

```bash
# Start database
docker-compose up -d postgres

# Check status
docker-compose ps

# View logs
docker-compose logs postgres

# Stop database
docker-compose down

# Stop and remove data (WARNING: deletes all data)
docker-compose down -v
```

### Accessing Database

```bash
# Using psql inside container
docker exec -it agent_framework_db psql -U postgres -d agent_framework

# Run SQL file
docker exec -i agent_framework_db psql -U postgres agent_framework < schema.sql

# Create backup
docker exec agent_framework_db pg_dump -U postgres agent_framework > backup.sql

# Restore backup
docker exec -i agent_framework_db psql -U postgres agent_framework < backup.sql
```

## Database Schema

### Tables

**fundamentals** - Company metrics
```sql
CREATE TABLE fundamentals (
    ticker VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    market_cap BIGINT,
    pe_ratio NUMERIC(10, 2),
    pb_ratio NUMERIC(10, 2),
    roe NUMERIC(10, 2),
    profit_margin NUMERIC(10, 2),
    revenue_growth NUMERIC(10, 2),
    debt_to_equity NUMERIC(10, 2),
    current_ratio NUMERIC(10, 2),
    dividend_yield NUMERIC(10, 2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**prices** - Historical prices
```sql
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(10, 2),
    high NUMERIC(10, 2),
    low NUMERIC(10, 2),
    close NUMERIC(10, 2),
    volume BIGINT,
    FOREIGN KEY (ticker) REFERENCES fundamentals(ticker),
    UNIQUE(ticker, date)
);
```

**news** - News headlines
```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    headline TEXT NOT NULL,
    sentiment VARCHAR(20),
    source VARCHAR(100),
    FOREIGN KEY (ticker) REFERENCES fundamentals(ticker)
);
```

**sec_filings** - SEC 10-K filings
```sql
CREATE TABLE sec_filings (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    filing_type VARCHAR(20) NOT NULL,
    filing_date DATE NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (ticker) REFERENCES fundamentals(ticker)
);
```

### Sample Data Included

- **4 tickers:** AAPL, MSFT, TSLA, JPM
- **90 days** of price history per ticker
- **3 news items** per ticker
- **1 SEC 10-K filing** per ticker (~2000 words each)

## Connection Pooling

The framework uses asyncpg connection pooling for optimal performance:

```python
from agent_framework import Database, DatabaseConfig

config = DatabaseConfig(
    connection_string='postgresql://...',
    min_pool_size=2,      # Minimum connections
    max_pool_size=10,     # Maximum connections
    command_timeout=60,   # Query timeout
    max_queries=50000,    # Recycle after N queries
)

db = Database(connection_string, config)
```

**Benefits:**
- **9x faster** than creating new connections
- Automatic connection reuse
- Connection health monitoring
- Graceful degradation under load

## Transactions

For atomic operations:

```python
async with db.transaction() as conn:
    await conn.execute("INSERT INTO trades ...")
    await conn.execute("UPDATE positions ...")
    # Commits automatically on success
    # Rolls back on error
```

## Health Monitoring

```python
# Check database health
health = await db.health_check()
print(f"Database healthy: {health}")

# Get connection pool stats
if db._pool:
    print(f"Pool size: {db._pool.get_size()}")
    print(f"Idle connections: {db._pool.get_idle_size()}")
```

## Local PostgreSQL Setup (Alternative)

If you prefer not to use Docker:

### macOS
```bash
brew install postgresql@16
brew services start postgresql@16
createdb agent_framework
psql agent_framework < schema.sql
python seed_data.py
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb agent_framework
sudo -u postgres psql agent_framework < schema.sql
python seed_data.py
```

### Windows
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run installer
3. Use pgAdmin or psql to create database and run schema

## Test Database

For testing, use a separate database:

```bash
# Create test database
docker exec agent_framework_db createdb -U postgres agent_framework_test

# Configure in .env
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agent_framework_test
```

The framework automatically uses the test database in tests:

```python
from agent_framework import Config

# Uses TEST_DATABASE_URL if set
test_db_url = Config.get_test_database_url()
```

## Common Issues & Solutions

### Connection Refused

**Problem:** `connection refused` error

**Solution:** 
```bash
# Check if Docker is running
docker ps

# Check if PostgreSQL container is up
docker-compose ps

# Restart if needed
docker-compose restart postgres
```

### Port Already in Use

**Problem:** Port 5433 already in use

**Solution:** Change port in docker-compose.yml
```yaml
ports:
  - "5434:5432"  # Use different host port
```

Then update DATABASE_URL:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/agent_framework
```

### Database Does Not Exist

**Problem:** `database "agent_framework" does not exist`

**Solution:**
```bash
# Check database exists
docker exec agent_framework_db psql -U postgres -c "\l"

# Create if missing
docker exec agent_framework_db createdb -U postgres agent_framework

# Run schema
docker exec -i agent_framework_db psql -U postgres agent_framework < schema.sql
```

### No Data in Database

**Problem:** Database exists but has no data

**Solution:**
```bash
python seed_data.py
```

### Permission Denied

**Problem:** Permission errors when accessing database

**Solution:**
```bash
# Grant permissions
docker exec agent_framework_db psql -U postgres -c "
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
"
```

## Production Setup

For production deployments:

### 1. Use Managed PostgreSQL
- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL
- DigitalOcean Managed Databases

### 2. Configure Connection Pooling
```python
config = DatabaseConfig(
    connection_string=os.getenv('DATABASE_URL'),
    min_pool_size=5,
    max_pool_size=20,
    command_timeout=60,
    max_queries=50000,
)
```

### 3. Enable SSL
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

### 4. Set Up Read Replicas
For high-traffic applications, use read replicas for queries.

### 5. Monitor Performance
```python
# Log slow queries
import logging
logging.getLogger('asyncpg').setLevel(logging.DEBUG)
```

## Backup & Restore

### Automated Backups

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec agent_framework_db pg_dump -U postgres agent_framework > backup_$DATE.sql
echo "Backup created: backup_$DATE.sql"
EOF

chmod +x backup.sh

# Add to crontab for daily backups
# 0 2 * * * /path/to/backup.sh
```

### Manual Backup

```bash
# Full backup
docker exec agent_framework_db pg_dump -U postgres agent_framework > backup.sql

# Schema only
docker exec agent_framework_db pg_dump --schema-only -U postgres agent_framework > schema_backup.sql

# Data only
docker exec agent_framework_db pg_dump --data-only -U postgres agent_framework > data_backup.sql
```

### Restore

```bash
# Drop and recreate
docker exec agent_framework_db dropdb -U postgres agent_framework
docker exec agent_framework_db createdb -U postgres agent_framework

# Restore
docker exec -i agent_framework_db psql -U postgres agent_framework < backup.sql
```

## Performance Optimization

### 1. Add Indexes
```sql
-- Already included in schema.sql
CREATE INDEX idx_prices_ticker_date ON prices(ticker, date DESC);
CREATE INDEX idx_news_ticker_date ON news(ticker, date DESC);
CREATE INDEX idx_filings_ticker_date ON sec_filings(ticker, filing_date DESC);
```

### 2. Analyze Queries
```sql
EXPLAIN ANALYZE SELECT * FROM prices WHERE ticker = 'AAPL' ORDER BY date DESC LIMIT 30;
```

### 3. Regular Maintenance
```bash
# Vacuum and analyze
docker exec agent_framework_db psql -U postgres agent_framework -c "VACUUM ANALYZE;"

# Check table sizes
docker exec agent_framework_db psql -U postgres agent_framework -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

## Migration to Production

When moving from Docker to production:

1. Export data:
```bash
docker exec agent_framework_db pg_dump -U postgres agent_framework > production_migration.sql
```

2. Set up managed database

3. Configure connection:
```bash
export DATABASE_URL="postgresql://user:pass@production-host:5432/agent_framework?sslmode=require"
```

4. Import data:
```bash
psql $DATABASE_URL < production_migration.sql
```

5. Verify:
```bash
python quickstart.py
```

## Resources

- PostgreSQL Documentation: https://www.postgresql.org/docs/
- asyncpg Documentation: https://magicstack.github.io/asyncpg/
- Docker Compose: https://docs.docker.com/compose/
- Framework Documentation: See README.md

## Support

For issues:
1. Check Docker is running: `docker ps`
2. Check logs: `docker-compose logs postgres`
3. Verify connection: `python quickstart.py`
4. Review this guide for common issues
