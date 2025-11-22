# Configuration Guide - Settings Explained

All settings are stored in a file called `.env` (think of it as your "settings page"). This guide explains each setting in plain English.

## What is the .env File?

The `.env` file stores your personal settings like passwords, database location, and AI API keys. It looks like this:

```bash
DB_PORT=5433
OPENAI_API_KEY=sk-your-key-here
```

**Important:** Never share your `.env` file with others (it contains your API keys)!

## Quick Setup

```bash
# Copy the example file
cp .env.example .env

# Edit it with any text editor
nano .env  # or use Notepad, TextEdit, VS Code, etc.
```

## Database Settings

These settings tell the framework where to find your stock data.

### Basic Settings (Most Important)

```bash
# Where is the database?
DB_HOST=localhost        # Your computer (change for remote database)

# Which port does it use?
DB_PORT=5433            # 5433 by default (avoid conflict with local PostgreSQL)

# Login credentials
DB_USER=postgres        # Username (default: postgres)
DB_PASSWORD=postgres    # Password (change this for security!)

# Database name
DB_NAME=agent_framework # Name of your database
```

**What do these mean?**

- **DB_HOST**: Where the database lives
  - `localhost` = on your computer
  - `192.168.1.100` = on another computer in your network
  - `database.mycompany.com` = on a remote server

- **DB_PORT**: Like an apartment number for the database
  - Default PostgreSQL uses 5432
  - We use 5433 to avoid conflicts
  - Change this if 5433 is already in use

- **DB_USER** and **DB_PASSWORD**: Login credentials
  - Like username/password for a website
  - Default is `postgres/postgres` (change for security)

- **DB_NAME**: The database's name
  - Like naming a folder
  - Use different names for test vs. production

### Advanced Database Settings (For Performance)

```bash
# How many connections to keep ready?
DB_MIN_POOL_SIZE=2      # Start with 2 connections ready

# Maximum connections allowed?
DB_MAX_POOL_SIZE=10     # Never more than 10 at once

# How long to wait for database?
DB_COMMAND_TIMEOUT=60   # 60 seconds before giving up
```

**When to change these:**

- **More users?** Increase `DB_MAX_POOL_SIZE` to 20-50
- **Slow computer?** Decrease to 5
- **Slow queries?** Increase `DB_COMMAND_TIMEOUT` to 120

**Most users don't need to change these!**

### Alternative: Full Connection String

Instead of individual settings, you can use one long string:

```bash
DATABASE_URL=postgresql://user:password@host:port/database_name
```

Example:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/agent_framework
```

**When to use this:** When connecting to hosted databases (Heroku, AWS, etc.) - they give you this string.

## API Settings

If you want to run the web API (optional):

```bash
# Where should the API listen?
API_HOST=0.0.0.0        # 0.0.0.0 means "accept connections from anywhere"

# Which port?
API_PORT=8000           # Default web port

# Show detailed error messages?
DEBUG=True              # True for development, False for production
```

**What do these mean?**

- **API_HOST**: 
  - `0.0.0.0` = anyone can connect
  - `127.0.0.1` = only you can connect (more secure)

- **API_PORT**: 
  - `8000` is standard
  - Change if port is already in use (try 8001, 8080, etc.)

- **DEBUG**: 
  - `True` = shows detailed errors (helps when learning)
  - `False` = hides details (use in production for security)

## AI Settings (Optional)

If you want to use ChatGPT, Claude, or other AI:

### OpenAI (ChatGPT)

```bash
# Your API key
OPENAI_API_KEY=sk-...                    # Get from platform.openai.com

# Which model to use?
OPENAI_MODEL=gpt-4                       # gpt-4 is smartest, gpt-3.5-turbo is cheaper

# How creative should responses be?
OPENAI_TEMPERATURE=0.7                   # 0 = focused, 1 = creative

# How long should responses be?
OPENAI_MAX_TOKENS=1000                   # 1000 = about 750 words
```

**Understanding these settings:**

- **API_KEY**: Like a password to use OpenAI
  - Get it from https://platform.openai.com/api-keys
  - Costs money per use
  - Keep it secret!

- **MODEL**: Which AI brain to use
  - `gpt-4` = Most capable, more expensive (~$0.03/1K words)
  - `gpt-3.5-turbo` = Fast and cheap (~$0.002/1K words)
  - `gpt-4-turbo` = Good balance

- **TEMPERATURE**: How creative vs. focused
  - `0.0-0.3` = Very focused, consistent (good for analysis)
  - `0.4-0.7` = Balanced (default)
  - `0.8-1.0` = Creative, varied (good for ideas)

- **MAX_TOKENS**: Response length limit
  - `500` = Brief (1-2 paragraphs)
  - `1000` = Standard (2-3 paragraphs)
  - `2000` = Detailed (full analysis)
  - More tokens = higher cost

### Anthropic (Claude)

```bash
# Your API key
ANTHROPIC_API_KEY=sk-ant-...             # Get from console.anthropic.com

# Which model?
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Latest model

# Creativity level
ANTHROPIC_TEMPERATURE=0.7

# Response length
ANTHROPIC_MAX_TOKENS=1000
```

**Claude models:**
- `claude-3-5-sonnet` = Best balance (recommended)
- `claude-3-opus` = Most capable
- `claude-3-haiku` = Fastest and cheapest

### Ollama (Free, Local AI)

```bash
# Where is Ollama running?
OLLAMA_BASE_URL=http://localhost:11434   # Default local installation

# Which model?
OLLAMA_MODEL=llama3.2                    # Free models: llama3.2, mistral, phi
```

**What is Ollama?**
- Runs AI models on YOUR computer
- Completely free
- No API keys needed
- Slower than cloud AI, but private

**Popular free models:**
- `llama3.2` = Good all-rounder (4GB RAM)
- `mistral` = Fast and capable (4GB RAM)
- `phi` = Tiny but decent (2GB RAM)

Install with: `curl https://ollama.ai/install.sh | sh`

## Logging Settings

```bash
# How detailed should logs be?
LOG_LEVEL=INFO          # INFO, DEBUG, WARNING, or ERROR
```

**What do these mean?**

- **DEBUG**: Shows everything (lots of detail)
  - Use when something isn't working
  - Very verbose

- **INFO**: Shows important events (default)
  - Good balance
  - Normal operations

- **WARNING**: Only shows potential problems
  - Production setting
  - Less noise

- **ERROR**: Only shows actual errors
  - Minimal logging
  - Production setting

## Real-World Examples

### Example 1: Beginner Setup (Local Everything)

```bash
# Database on your computer
DB_HOST=localhost
DB_PORT=5433
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=agent_framework

# Use free local AI
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Development settings
DEBUG=True
LOG_LEVEL=DEBUG
```

**Who this is for:** Learning and experimenting on your laptop.

### Example 2: Using ChatGPT

```bash
# Database (same as above)
DB_HOST=localhost
DB_PORT=5433

# ChatGPT for AI
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-3.5-turbo    # Cheaper option
OPENAI_TEMPERATURE=0.5        # Focused analysis
OPENAI_MAX_TOKENS=1500        # Detailed responses

DEBUG=True
```

**Who this is for:** Want better AI quality, willing to pay.

### Example 3: Production Setup

```bash
# Remote database
DB_HOST=database.mycompany.com
DB_PORT=5432
DB_USER=prod_user
DB_PASSWORD=strong_random_password_here
DB_NAME=agent_framework_prod

# More connections for traffic
DB_MIN_POOL_SIZE=10
DB_MAX_POOL_SIZE=50

# Production API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Minimal logging
LOG_LEVEL=WARNING

# Use ChatGPT
OPENAI_API_KEY=sk-production-key
OPENAI_MODEL=gpt-4
```

**Who this is for:** Running a real service for others to use.

## Quick Configuration Tasks

### Change Database Port

Port 5433 already in use? Just change one line:

```bash
DB_PORT=5434  # Use any number 5000-9000
```

Then restart:
```bash
docker-compose down
docker-compose up -d postgres
```

### Switch Between AI Providers

**Use Ollama (free):**
```python
llm=LLMConfig(provider='ollama', model='llama3.2')
```

**Use ChatGPT:**
```python
llm=LLMConfig(provider='openai', model='gpt-4')
```

**Use Claude:**
```python
llm=LLMConfig(provider='anthropic', model='claude-3-5-sonnet-20241022')
```

### Make AI More Creative or Focused

In your agent code:
```python
# Very focused (good for analysis)
llm=LLMConfig(provider='openai', temperature=0.2)

# Balanced (default)
llm=LLMConfig(provider='openai', temperature=0.7)

# Very creative (good for brainstorming)
llm=LLMConfig(provider='openai', temperature=0.9)
```

See [LLM_CUSTOMIZATION.md](LLM_CUSTOMIZATION.md) for details.

## Security Tips

### For Learning (Your Computer)
```bash
DB_PASSWORD=postgres    # Simple is fine
DEBUG=True              # See all details
```

### For Production (Real Use)
```bash
DB_PASSWORD=K8mN$9vL#pQ2x!Wf    # Use strong passwords!
DEBUG=False                      # Hide sensitive info
LOG_LEVEL=WARNING               # Only log problems

# Use environment-specific API keys
OPENAI_API_KEY=sk-production-key-not-test-key
```

**Never:**
- Share your `.env` file
- Commit `.env` to Git
- Use test API keys in production
- Use simple passwords in production

## Troubleshooting

### Can't Connect to Database

```bash
# Check these settings match docker-compose.yml
DB_HOST=localhost
DB_PORT=5433          # Must match docker-compose
DB_USER=postgres      # Must match docker-compose
DB_PASSWORD=postgres  # Must match docker-compose
```

### Port Already in Use

```bash
# Try a different port
DB_PORT=5434
API_PORT=8001
```

### API Key Not Working

```bash
# Make sure there are no spaces
OPENAI_API_KEY=sk-abc123  # ✅ Good
OPENAI_API_KEY= sk-abc123 # ❌ Bad (space after =)
OPENAI_API_KEY=sk-abc123  # ❌ Bad (space after key)
```

### Changes Not Taking Effect

**After changing `.env`:**
```bash
# Restart database
docker-compose down
docker-compose up -d postgres

# Restart your Python script
# (Ctrl+C and run again)
```

## Need More Help?

- **AI customization:** [LLM_CUSTOMIZATION.md](LLM_CUSTOMIZATION.md)
- **Database setup:** [DATABASE_SETUP.md](DATABASE_SETUP.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Quick start:** [../QUICK_START.md](../QUICK_START.md)

---

**Remember**: Start simple, change only what you need, and test after each change!
