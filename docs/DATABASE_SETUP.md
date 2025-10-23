# Database Setup Guide

This guide covers setting up PostgreSQL for the AI Agent Framework.

## Prerequisites

- PostgreSQL 12+ installed
- Python 3.10+ with asyncpg

## Quick Setup (3 Steps)

### 1. Install PostgreSQL

**macOS:**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Docker (Easiest):**
```bash
docker-compose up -d postgres
# Skip to step 3 (database is auto-created)
```

### 2. Create Database

```bash
# Create database
createdb agent_framework

# Or with sudo if needed
sudo -u postgres createdb agent_framework
```

### 3. Initialize Schema & Data

```bash
# Run schema
psql agent_framework < schema.sql # If using local psql
        or
docker exec -i agent_framework_db psql -U postgres agent_framework < schema.sql # If using Docker

# Seed with sample data
python seed_data.py
```

Done! Your database is ready with 4 sample tickers.

## Connection String

Set in `.env` file:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agent_framework
```

Format: `postgresql://user:password@host:port/database`

## Verify Setup

```bash
# Check tables exist
psql agent_framework -c "\dt"
        or
docker exec -i agent_framework_db psql -U postgres agent_framework -c "\dt"

# Check data loaded
psql agent_framework -c "SELECT ticker, name FROM fundamentals;"
        or
docker exec -i agent_framework_db psql -U postgres agent_framework -c "SELECT ticker, name FROM fundamentals;"

# Should show:
#  ticker |          name
# --------+------------------------
#  AAPL   | Apple Inc.
#  MSFT   | Microsoft Corporation
#  TSLA   | Tesla Inc.
#  JPM    | JPMorgan Chase & Co.
```

## Database Schema

### Tables

**fundamentals** - Company metrics
- ticker (PRIMARY KEY)
- name, sector, market_cap
- pe_ratio, pb_ratio, roe
- profit_margin, revenue_growth
- debt_to_equity, current_ratio
- dividend_yield

**prices** - Historical prices
- ticker, date (UNIQUE)
- open, high, low, close, volume

**news** - News headlines
- ticker, date, headline
- sentiment, source

**sec_filings** - SEC 10-K filings
- ticker, filing_type, filing_date
- content (TEXT)

### Sample Data Included

- **4 tickers:** AAPL, MSFT, TSLA, JPM
- **90 days** of price history per ticker
- **3 news items** per ticker
- **1 SEC 10-K filing** per ticker (~2000 words each)

## Connection Pooling

The framework uses asyncpg connection pooling:
- Min connections: 2
- Max connections: 10
- **9x faster** than creating new connections

Connection pool is managed automatically in the Database class.

## Docker Setup (Recommended for Development)

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: agent_framework
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

Run:
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Seed data
python seed_data.py

# Start API
docker-compose up api
```

## Common Issues

### Connection Refused

**Problem:** `connection refused` error

**Solution:** 
1. Check PostgreSQL is running: `pg_isready`
2. Check port: `netstat -an | grep 5432`
3. Start PostgreSQL: `brew services start postgresql@16`

### Authentication Failed

**Problem:** `password authentication failed`

**Solution:**
1. Update `pg_hba.conf` to allow local connections
2. Or use connection string with correct credentials
3. For Docker: default is `postgres/postgres`

### Database Does Not Exist

**Problem:** `database "agent_framework" does not exist`

**Solution:**
```bash
createdb agent_framework
psql agent_framework < schema.sql
```

### Permission Denied

**Problem:** `permission denied for schema public`

**Solution:**
```sql
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
```

## Production Setup

For production, use:

1. **Managed PostgreSQL** (AWS RDS, Google Cloud SQL, etc.)
2. **Connection SSL**
3. **Environment variables** for credentials
4. **Read replicas** for scaling

Example production connection string:
```bash
DATABASE_URL=postgresql://user:pass@production-db.region.rds.amazonaws.com:5432/agent_framework?sslmode=require
```

## Backup & Restore

### Backup

```bash
# Full backup
pg_dump agent_framework > backup.sql

# Schema only
pg_dump --schema-only agent_framework > schema_backup.sql

# Data only
pg_dump --data-only agent_framework > data_backup.sql
```

### Restore

```bash
# Drop and recreate
dropdb agent_framework
createdb agent_framework
psql agent_framework < backup.sql
```

## Database Migrations

For schema changes, create migration files:

```sql
-- migrations/001_add_sector_index.sql
CREATE INDEX idx_fundamentals_sector ON fundamentals(sector);
```

Apply:
```bash
psql agent_framework < migrations/001_add_sector_index.sql
```

## Performance Tips

1. **Use connection pooling** (already implemented)
2. **Add indexes** on frequently queried columns
3. **Use EXPLAIN ANALYZE** to optimize queries
4. **Regular VACUUM** for PostgreSQL maintenance
5. **Monitor with pg_stat_statements**

## Next Steps

1. ✅ Database setup complete
2. 🚀 Run examples: `python examples/01_basic.py`
3. 📊 Start API: `uvicorn agent_framework.api:app --reload`
4. 🧪 Run tests: `pytest tests/`

## Support

- PostgreSQL docs: https://www.postgresql.org/docs/
- asyncpg docs: https://magicstack.github.io/asyncpg/
- Docker Compose: https://docs.docker.com/compose/