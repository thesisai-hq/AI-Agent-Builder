# Database Guide - Where Your Stock Data Lives

**What is a database?** Think of it as an organized filing cabinet that stores all your stock information (prices, company data, news, etc.).

This guide explains how to set up and use the database. **Don't worry - we make it easy with Docker!**

## The Easy Way: Using Docker

**What is Docker?** Software that runs programs in isolated "containers". Think of it as a virtual box that contains the database.

**Why Docker?** Without it, setting up PostgreSQL is complicated (installing, configuring, permissions, etc.). With Docker, it's one command!

### Setup (3 Commands)

```bash
# 1. Start the database (takes 10 seconds)
docker-compose up -d postgres

# 2. Add sample stock data
python seed_data.py

# 3. Verify it works
python quickstart.py
```

Done! ✨ You now have a database with Apple, Microsoft, Tesla, and JPMorgan data.

## What's Inside the Database?

The database has 4 "tables" (like sheets in Excel):

### 1. Fundamentals Table (Company Basics)

**What it stores:** Company financial metrics

```
Ticker | Name        | PE Ratio | Growth | Margin | Sector
-------|-------------|----------|--------|--------|------------
AAPL   | Apple Inc.  | 28.5     | 8.5%   | 25.3%  | Technology
MSFT   | Microsoft   | 32.1     | 12.3%  | 36.7%  | Technology
```

**What you can ask:**
- "What's Apple's PE ratio?"
- "Which companies have high profit margins?"
- "Show me all tech stocks"

### 2. Prices Table (Stock Prices)

**What it stores:** Daily stock prices (last 90 days)

```
Ticker | Date       | Open    | High    | Low     | Close   | Volume
-------|------------|---------|---------|---------|---------|------------
AAPL   | 2025-01-15 | 175.20  | 178.50  | 174.80  | 177.30  | 85,000,000
AAPL   | 2025-01-16 | 177.50  | 180.00  | 176.90  | 179.20  | 92,000,000
```

**What you can ask:**
- "What was Apple's closing price yesterday?"
- "Show me last 30 days of prices for Microsoft"
- "What was the highest price this week?"

### 3. News Table (Headlines)

**What it stores:** Recent news about companies

```
Ticker | Date       | Headline                           | Sentiment
-------|------------|------------------------------------|-----------
AAPL   | 2025-01-20 | Apple unveils new AI features     | positive
TSLA   | 2025-01-22 | Tesla deliveries miss estimates   | negative
```

**What you can ask:**
- "What's the latest news about Tesla?"
- "Show me positive news about Apple"
- "Any recent headlines for Microsoft?"

### 4. SEC Filings Table (Company Reports)

**What it stores:** Excerpts from official company reports (like 10-K annual reports)

```
Ticker | Filing Type | Filing Date | Content (excerpt)
-------|-------------|-------------|----------------------------------------
AAPL   | 10-K        | 2024-11-01  | "Apple Inc. designs, manufactures, and
       |             |             | markets smartphones, personal computers..."
```

**What you can ask:**
- "What does Apple say about risks?"
- "Show me Microsoft's business overview"
- "Extract financial highlights from the filing"

## Managing the Database

### Start and Stop

```bash
# Start database (do this every time you begin work)
docker-compose up -d postgres

# Check if it's running
docker ps

# Should see: agent_framework_db ... Up ... 0.0.0.0:5433->5432/tcp

# Stop database (when you're done for the day)
docker-compose down
```

**When to start:** Every time you turn on your computer and want to work on your agents.

**When to stop:** When you're done working (optional - it doesn't hurt to leave it running).

### View Logs (If Something's Wrong)

```bash
# See what the database is doing
docker-compose logs postgres

# Follow logs in real-time
docker-compose logs -f postgres
```

**What logs show:** Database startup messages, any errors, query activity.

### Reset Database (Start Fresh)

```bash
# WARNING: This deletes all your data!
docker-compose down -v

# Start fresh
docker-compose up -d postgres
python seed_data.py
```

**When to reset:** If something is corrupted, or you want to start over.

## Accessing Data in Your Code

### Connect to Database

```python
from agent_framework import Database, Config

# Connect
db = Database(Config.get_database_url())
await db.connect()

# Always disconnect when done!
await db.disconnect()
```

**Best practice:** Always disconnect when finished to free up resources.

### Get Company Fundamentals

```python
# Get Apple's data
data = await db.get_fundamentals('AAPL')

print(f"Company: {data['name']}")
print(f"PE Ratio: {data['pe_ratio']}")
print(f"Profit Margin: {data['profit_margin']}%")
print(f"Revenue Growth: {data['revenue_growth']}%")
```

**Returns:** Dictionary with all the company's metrics.

### Get Price History

```python
# Get last 30 days of Apple prices
prices = await db.get_prices('AAPL', days=30)

# First price is most recent
latest = prices[0]
print(f"Latest close: ${latest['close']}")
print(f"Volume: {latest['volume']:,}")

# Loop through all prices
for price in prices:
    print(f"{price['date']}: ${price['close']}")
```

**Returns:** List of price records, newest first.

### Get News

```python
# Get 10 latest news items for Apple
news = await db.get_news('AAPL', limit=10)

for item in news:
    print(f"{item['date']}: {item['headline']}")
    print(f"  Sentiment: {item['sentiment']}")
```

**Returns:** List of news headlines with sentiment.

### Get SEC Filings

```python
# Get latest 10-K filing for Apple
filing = await db.get_filing('AAPL')

print(filing)  # Prints text of the filing
```

**Returns:** Text content of the filing (useful for AI analysis).

### List All Stocks

```python
# See what's in the database
tickers = await db.list_tickers()

print(f"We have data for: {', '.join(tickers)}")
# Output: We have data for: AAPL, MSFT, TSLA, JPM
```

## Database Settings (.env file)

Settings that control how to connect:

```bash
# Where is the database?
DB_HOST=localhost      # Your computer

# Which port?
DB_PORT=5433          # Default (5433 to avoid conflicts)

# Login
DB_USER=postgres      # Username
DB_PASSWORD=postgres  # Password (change for security!)

# Database name
DB_NAME=agent_framework
```

**Don't need to change these for Docker!** The defaults work fine.

**Only change if:**
- Port 5433 is already in use (try 5434, 5435, etc.)
- Connecting to a remote database
- Need better security (change password)

## Advanced: Connection Pooling

**What is connection pooling?** Instead of creating a new connection each time (slow), we keep a "pool" of ready connections (fast).

**Why it matters:** 9x faster queries!

```python
# The framework does this automatically
# You can customize if needed:

from agent_framework import DatabaseConfig

config = DatabaseConfig(
    connection_string='postgresql://...',
    min_pool_size=2,     # Keep 2 connections always ready
    max_pool_size=10,    # Never use more than 10 at once
)

db = Database(connection_string, config)
```

**Most users don't need to change these!** Defaults work great.

**When to adjust:**
- Many users: Increase `max_pool_size` to 20-50
- Slow computer: Decrease to 5
- Getting timeout errors: Increase `command_timeout`

## Backup Your Data

**Why backup?** So you don't lose your data if something goes wrong.

### Create Backup

```bash
# Create a backup file
docker exec agent_framework_db pg_dump -U postgres agent_framework > backup.sql

# This creates backup.sql with all your data
```

### Restore from Backup

```bash
# First, clear the current database
docker exec agent_framework_db dropdb -U postgres agent_framework
docker exec agent_framework_db createdb -U postgres agent_framework

# Restore from backup
docker exec -i agent_framework_db psql -U postgres agent_framework < backup.sql
```

**Pro tip:** Back up before making big changes!

## Troubleshooting

### "Can't connect to database"

**Problem:** Code says "connection refused" or "can't connect"

**Solutions:**

1. **Is Docker running?**
   ```bash
   docker ps
   ```
   If you see "Cannot connect to Docker daemon" → Start Docker Desktop

2. **Is database running?**
   ```bash
   docker-compose ps
   ```
   Should show `agent_framework_db` with status "Up"
   
   If not: `docker-compose up -d postgres`

3. **Wait a bit**
   Database takes 10 seconds to start. Wait, then try again.

4. **Wrong port?**
   Check `.env` file has `DB_PORT=5433`

### "Database does not exist"

**Problem:** Error says database "agent_framework" doesn't exist

**Solution:**
```bash
# Create the database
docker exec agent_framework_db createdb -U postgres agent_framework

# Add the structure (schema)
docker exec -i agent_framework_db psql -U postgres agent_framework < schema.sql

# Add sample data
python seed_data.py
```

### "No data found"

**Problem:** Code runs but says "no data for AAPL"

**Solution:**
```bash
# Re-add the sample data
python seed_data.py
```

### "Port already in use"

**Problem:** Error about port 5433 being in use

**Solution:**

1. Edit `docker-compose.yml`:
   ```yaml
   ports:
     - "5434:5432"  # Change to 5434 or another number
   ```

2. Edit `.env`:
   ```bash
   DB_PORT=5434
   ```

3. Restart:
   ```bash
   docker-compose down
   docker-compose up -d postgres
   ```

### Database is slow

**Problem:** Queries take a long time

**Solutions:**

1. **Check Docker resources**
   - Docker Desktop → Settings → Resources
   - Give Docker more RAM (4GB minimum)

2. **Restart database**
   ```bash
   docker-compose restart postgres
   ```

3. **Reduce pool size** (if on slow computer)
   Edit `.env`:
   ```bash
   DB_MAX_POOL_SIZE=5  # Default is 10
   ```

## Don't Want Docker?

You can install PostgreSQL directly on your computer:

### Mac
```bash
brew install postgresql@16
brew services start postgresql@16
createdb agent_framework
psql agent_framework < schema.sql
python seed_data.py
```

### Windows
1. Download from https://www.postgresql.org/download/windows/
2. Install and start
3. Use pgAdmin to create database
4. Run schema.sql
5. Run `python seed_data.py`

### Linux
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb agent_framework
sudo -u postgres psql agent_framework < schema.sql
python seed_data.py
```

**But Docker is much easier!** 

## What You Don't Need to Worry About

- **SQL syntax** - The framework handles all queries for you
- **Indexes** - Already set up for fast queries
- **Connections** - Pooling handled automatically
- **Transactions** - Framework manages them
- **Security** - Default settings fine for learning

**Just focus on your agents!** The database "just works."

## Next Steps

Now that your database is set up:

1. ✅ Run the examples: `python examples/01_basic.py`
2. ✅ Try querying data yourself
3. ✅ Build your first agent
4. ✅ Experiment and have fun!

## More Help

- **Installation guide**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Settings explained**: [CONFIGURATION.md](CONFIGURATION.md)
- **Quick snippets**: [../QUICK_REFERENCE.md](../QUICK_REFERENCE.md)

---

**Remember:** The database is just a tool to store data. Focus on building great agents - that's the fun part! 🚀
