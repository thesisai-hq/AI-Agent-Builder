# Thesis AI
Research tool for stocks. Deep insights using AI for decision making.

## Requirements for local project
`brew install git` or https://git-scm.com/downloads

`brew install nvm` or https://github.com/nvm-sh/nvm

`nvm install 24.7.0`

`brew install --cask dbeaver-community` or https://dbeaver.io/

## Requirements for infrastructure
`brew install terraform` or https://www.terraform.io/downloads

`brew install awscli` or https://aws.amazon.com/cli/

## Install
`npm i`

## Environment variables
Create `.env` file

Copy `.env.example` into `.env`

Update variables as needed

## Database Setup

We use **PostgreSQL** for both development and production.

### Option A: Using Docker (Recommended)
```bash
# Start PostgreSQL container
docker-compose up -d

# Use this DATABASE_URL in .env:
DATABASE_URL="postgresql://dev:dev@localhost:5433/thesis_ai_dev?schema=public"
```

**Note:** Docker PostgreSQL runs on port 5433 (not 5432) to avoid conflicts with system PostgreSQL.

### Option B: Using Homebrew (No Docker)
```bash
# Install PostgreSQL
brew install postgresql@17

# Start PostgreSQL service
brew services start postgresql@17

# Add to PATH (for createdb command)
echo 'export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Create database
createdb thesis_ai_dev

# Use this DATABASE_URL in .env (replace with your username):
DATABASE_URL="postgresql://YOUR_USERNAME@localhost:5432/thesis_ai_dev?schema=public"
# Find your username by running: whoami
```

### Run Migrations
```bash
npm run db:migrate
```
Creates all database tables automatically.

### View/Edit Database
```bash
npm run db:studio
```
Opens at `http://localhost:5555` - beautiful visual database browser, no SQL required!

**Or use DBeaver or any PostgreSQL client:**
- Host: `localhost`, Port: `5433` (Docker) or `5432` (Homebrew)
- Database: `thesis_ai_dev`
- Username: `dev`, Password: `dev` (Docker) or your system username (Homebrew)

### Connecting to Production Database

The production RDS database is not publicly accessible. To connect from your local machine:

1. **Install AWS Session Manager plugin:**
   ```bash
   brew install --cask session-manager-plugin
   ```

2. **Start SSH tunnel:**
   ```bash
   aws ssm start-session --target i-0f9c6f9d3799170f1 \
     --document-name AWS-StartPortForwardingSessionToRemoteHost \
     --parameters '{"host":["thesis-ai-prod-postgres.c2d64eack4n5.us-east-1.rds.amazonaws.com"],"portNumber":["5432"],"localPortNumber":["5433"]}'
   ```
   Keep this terminal window open.

3. **Connect via DBeaver or psql:**
   - Host: `localhost`
   - Port: `5433`
   - Database: `thesis_ai_prod`
   - Username: `thesis_admin`
   - Password: Get from `cd terraform && terraform output -raw db_instance_password`

## Airflow Data Pipelines

We use Apache Airflow to orchestrate daily data collection for market prices, news, macro indicators, and SEC filings.

### Setup Airflow (One-Time)

1. **Create Python virtual environment for Airflow:**
   ```bash
   python3 -m venv airflow_venv
   source airflow_venv/bin/activate
   ```

2. **Install Airflow and dependencies:**
   ```bash
   pip install apache-airflow psycopg2-binary yfinance pandas requests beautifulsoup4 vaderSentiment pendulum
   ```

3. **Configure Airflow home directory:**
   ```bash
   export AIRFLOW_HOME=~/airflow
   ```
   
   Add to your shell profile for persistence:
   ```bash
   echo 'export AIRFLOW_HOME=~/airflow' >> ~/.bashrc  # or ~/.zshrc for macOS
   source ~/.bashrc
   ```

4. **Initialize Airflow database:**
   ```bash
   airflow db init
   ```

5. **Update Airflow configuration:**
   ```bash
   # Point to your DAGs folder (replace YOUR_USERNAME with actual username)
   sed -i "s|dags_folder = .*|dags_folder = $HOME/code/thesis-ai/server/airflow/dags|g" ~/airflow/airflow.cfg
   
   # Disable example DAGs
   sed -i 's/load_examples = True/load_examples = False/g' ~/airflow/airflow.cfg
   ```

### Running Airflow

**Start Airflow (includes webserver + scheduler):**
```bash
source airflow_venv/bin/activate
airflow standalone
```

**Access Airflow UI:**
- Open: `http://localhost:8080`
- Username: `admin`
- Password: Found in `~/airflow/simple_auth_manager_passwords.json.generated`
  ```bash
  cat ~/airflow/simple_auth_manager_passwords.json.generated
  ```

### Available DAGs

All DAGs run automatically on weekdays (Monday-Friday):

| DAG Name | Schedule | Description | Runtime |
|----------|----------|-------------|---------|
| `daily_stock_prices` | 6:00 AM EST | Load OHLC prices for 500+ stocks from S&P 500 | ~15 min |
| `daily_index_data` | 7:00 AM EST | Load major indices (S&P 500, NASDAQ, Dow) and sector ETFs (XLK, XLV, XLF, etc.) | ~2 min |
| `daily_news_data` | 9:00 AM EST | Fetch news articles with VADER sentiment analysis | ~20 min |
| `daily_macro_data` | 7:00 AM EST | Load FRED economic indicators (CPI, unemployment, treasury yields) | ~2 min |
| `daily_sec_filings` | 8:00 AM EST | Fetch SEC regulatory filings (10-K annual, 10-Q quarterly, 8-K events) | ~5 min |

### Initial Data Loading

After setting up the database for the first time, manually trigger DAGs to populate initial data:

1. **Start Airflow** (if not already running):
   ```bash
   source airflow_venv/bin/activate
   airflow standalone
   ```

2. **Access Airflow UI:** `http://localhost:8080`

3. **Enable and trigger DAGs** in this order:
   - Toggle each DAG ON (switch on the left side)
   - Click the ▶️ play button to trigger manually
   - Monitor progress in the Graph view

   **Recommended order:**
   1. `daily_stock_prices` - Loads stock universe (required for other DAGs)
   2. `daily_index_data` - Loads market indices and sectors
   3. `daily_macro_data` - Loads economic indicators
   4. `daily_news_data` - Loads news for all stocks
   5. `daily_sec_filings` - Loads SEC regulatory filings

4. **Verify data loaded:**
   ```bash
   npm run db:studio
   ```
   Check these tables have data:
   - `StockPrice` - Should have ~50,000+ records
   - `IndexPrice` - Should have ~1,000+ records
   - `NewsArticle` - Should have ~2,500+ records
   - `MacroIndicator` - Should have ~500+ records
   - `SECFilingDocument` - Should have records (if filings available)

### Environment Variables for DAGs

DAGs automatically read from `.env` file in project root:

```bash
# Required for DAG database connections
DB_HOST=localhost
DB_PORT=5433           # Use 5433 for Docker, 5432 for Homebrew
DB_NAME=thesis_ai_dev
DB_USER=dev            # Use 'dev' for Docker, your username for Homebrew
DB_PASSWORD=dev        # Use 'dev' for Docker, leave empty for Homebrew

# Optional API keys for enhanced data
FRED_API_KEY=your-fred-api-key              # Get from https://fred.stlouisfed.org/docs/api/api_key.html
POLYGON_API_KEY=your-polygon-api-key        # Get from https://polygon.io/
```

### Monitoring DAGs

**View DAG status:**
- Green = Success
- Red = Failed
- Yellow = Running
- Gray = Queued

**Check task logs:**
1. Click on any DAG
2. Click on a task in the Graph view
3. Click "Log" button to see detailed output

**Common success indicators:**
- Stock prices: "Total loaded: X records"
- News: "Successfully loaded X articles"
- Indices: "Successfully loaded X index records"
- Macro: "Successfully loaded X macro records"

### Troubleshooting Airflow

**DAGs not showing up:**
```bash
# Verify DAGs folder path
grep dags_folder ~/airflow/airflow.cfg

# Should show: /your/path/thesis-ai/server/airflow/dags
```

**Database connection errors:**
```bash
# Make sure Docker PostgreSQL is running
docker-compose ps

# Verify environment variables
echo $DB_HOST
echo $DB_PORT  
echo $DB_NAME

# Test connection manually
PGPASSWORD=dev psql -h localhost -p 5433 -U dev -d thesis_ai_dev -c "SELECT 1;"
```

**DAG failures:**
- Check logs in Airflow UI by clicking on failed task
- Common issues:
  - **API rate limiting:** Yahoo Finance, FRED, or SEC blocking requests → Wait 10-30 minutes and retry
  - **Network timeouts:** Temporary connectivity issues → Retry the task
  - **Missing data:** Some stocks/indices may not have data for certain dates → This is normal

**Clear task instance to retry:**
- Click on failed task → "Clear" button → "Yes" to rerun

**Reset Airflow completely:**
```bash
# Stop Airflow (Ctrl+C)
airflow db reset
# Re-run configuration steps 4-5 from Setup section above
```

### Stopping Airflow

```bash
# Press Ctrl+C in the terminal where 'airflow standalone' is running

# Or force kill if needed:
pkill -f "airflow standalone"
```

### DAG Development Tips

- **Test changes:** Use `airflow dags test <dag_id>` to test without scheduling
- **Check syntax:** DAGs appear in UI only if Python syntax is valid
- **Logs location:** `~/airflow/logs/` contains all execution logs
- **Database location:** `~/airflow/airflow.db` (SQLite metadata database)

## Build watch

`npm run build:watch` # UI

`npm run start:watch` # Server

## Linting
`npm run lint`

`npm run lint:fix`

## Testing
`npm test`

`npm run test:coverage` # Runs against both server & ui

# Troubleshooting

## Database connection errors

**For Docker:**
```bash
docker-compose ps           # Check if running
docker-compose logs postgres # View logs
docker-compose restart postgres # Restart
```

**For Homebrew PostgreSQL:**
```bash
brew services list          # Check if PostgreSQL is running
brew services restart postgresql@17 # Restart
psql postgres -c "SELECT version();" # Test connection
```

**Permission denied errors:**
```bash
# Make sure DATABASE_URL uses your username
whoami  # Get your username
# Update .env: DATABASE_URL="postgresql://YOUR_USERNAME@localhost:5432/thesis_ai_dev?schema=public"
```

**Port conflicts:**
```bash
# If both Docker and system PostgreSQL are running on same port
# Docker uses 5433, system uses 5432 - they should not conflict
# If issues persist, stop one:
sudo systemctl stop postgresql  # Stop system PostgreSQL
# OR
docker-compose down            # Stop Docker PostgreSQL
```

**Reset everything:**

For Docker:
```bash
docker-compose down -v      # Delete all data
docker-compose up -d        # Start fresh
npm run db:migrate          # Recreate tables
```

For Homebrew PostgreSQL:
```bash
dropdb thesis_ai_dev        # Delete database
createdb thesis_ai_dev      # Recreate database
npm run db:migrate          # Recreate tables
```

## General troubleshooting
`npm i`

Delete database (see reset commands above)

`npm run db:migrate`

`npm run build:watch` # UI

`npm run start:watch` # Server

## AI Coding

`npm install -g @anthropic-ai/claude-code`

claude --dangerously-skip-permissions

## CICD

We use github actions

## Infrastructure & Deployment

We use Terraform for AWS infrastructure and GitHub Actions for automated deployment.

### 🚀 Fully Automated Deployment (Recommended)

**Just push to `main` and everything happens automatically!**

#### Setup (One-Time):

1. Create AWS IAM user with deployment permissions
   - **See: [AWS-SETUP-GUIDE.md](./AWS-SETUP-GUIDE.md) for complete instructions**
   - Creates IAM user with right permissions
   - Generates access keys

2. Add AWS credentials to GitHub Secrets:
   - Go to: **Settings → Secrets and variables → Actions**
   - Add `AWS_ACCESS_KEY_ID`
   - Add `AWS_SECRET_ACCESS_KEY`

3. Enable GitHub Container Registry:
   - Go to: **Settings → Actions → General**
   - Select "Read and write permissions"

4. Push to main:
   ```bash
   git push origin main
   ```

That's it! Every push to `main` will:
- ✅ Check/create infrastructure with Terraform
- ✅ Build Docker image and push to GHCR
- ✅ Deploy to EC2 via **AWS Systems Manager (SSM)** - no SSH keys needed!
- ✅ Run health checks

**Benefits of SSM:**
- ✅ No SSH keys to manage
- ✅ No SSH port (22) to secure
- ✅ 100% free (no logging costs)
- ✅ IAM-based authentication
- ✅ Full deployment logs in GitHub Actions

See `.github/workflows/deploy.yml` for the automated deployment workflow.

**Required GitHub Secrets:**
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key

That's it - just 2 secrets!

### Manual Infrastructure Management (Optional)

For local Terraform control:

1. Add AWS credentials to `.env`:
   ```
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_DEFAULT_REGION=us-east-1
   ```

2. Run Terraform commands:
   ```bash
   npm run infra:setup     # Full automated setup
   npm run infra:init      # Initialize Terraform
   npm run infra:plan      # Preview changes
   npm run infra:apply     # Create infrastructure
   npm run infra:destroy   # Tear down infrastructure
   npm run infra:output    # View outputs
   ```

## Project Structure

```
thesis-ai/
├── ui/                     # Frontend Svelte app
├── server/
│   ├── server.mjs         # Express server
│   ├── auth.mjs           # Authentication
│   ├── api/               # API routes
│   ├── airflow/dags/      # Data pipeline DAGs
│   └── prisma/
│       ├── schema.prisma  # Database schema
│       └── migrations/    # Database migrations
├── terraform/             # AWS infrastructure
├── docker-compose.yml     # Local PostgreSQL database
└── Dockerfile            # Production container
```

## Tech Stack

- **Frontend:** Svelte + Vite
- **Backend:** Node.js + Express
- **Database:** PostgreSQL + Prisma ORM
- **Data Pipelines:** Apache Airflow + Python
- **Auth:** JWT
- **Deployment:** Docker + AWS
- **CI/CD:** GitHub Actions

## Build watch

`npm run build:watch` # UI

`npm run start:watch` # Server

## Linting
`npm run lint`

`npm run lint:fix`

## Testing
`npm test`

`npm run test:coverage` # Runs against both server & ui

# Troubleshooting

## Database connection errors

**For Docker:**
```bash
docker-compose ps           # Check if running
docker-compose logs postgres # View logs
docker-compose restart postgres # Restart
```

**For Homebrew PostgreSQL:**
```bash
brew services list          # Check if PostgreSQL is running
brew services restart postgresql@17 # Restart
psql postgres -c "SELECT version();" # Test connection
```

**Permission denied errors:**
```bash
# Make sure DATABASE_URL uses correct credentials
# Docker: DATABASE_URL="postgresql://dev:dev@localhost:5433/thesis_ai_dev?schema=public"
# Homebrew: DATABASE_URL="postgresql://YOUR_USERNAME@localhost:5432/thesis_ai_dev?schema=public"
```

**Port conflicts:**
```bash
# Docker uses port 5433, system PostgreSQL uses 5432 (no conflict)
# If you see port conflicts:
sudo systemctl stop postgresql  # Stop system PostgreSQL
# OR
docker-compose down            # Stop Docker PostgreSQL
```

**Reset everything:**

For Docker:
```bash
docker-compose down -v      # Delete all data
docker-compose up -d        # Start fresh
npm run db:migrate          # Recreate tables
# Then run Airflow DAGs to reload data
```

For Homebrew PostgreSQL:
```bash
dropdb thesis_ai_dev        # Delete database
createdb thesis_ai_dev      # Recreate database
npm run db:migrate          # Recreate tables
```

## Airflow Troubleshooting

**DAGs not appearing in UI:**
```bash
# Verify DAGs folder path in config
grep dags_folder ~/airflow/airflow.cfg

# Should point to your project's DAG folder
# If not, update it:
nano ~/airflow/airflow.cfg
# Find 'dags_folder' and set to: /path/to/thesis-ai/server/airflow/dags
```

**DAG import errors:**
```bash
# Check DAG syntax and imports
python server/airflow/dags/daily_stock_prices.py

# Install missing dependencies in airflow_venv
source airflow_venv/bin/activate
pip install <missing-package>
```

**Database connection errors from DAGs:**
```bash
# Verify .env file has correct database credentials
cat .env | grep DB_

# Test database connection
PGPASSWORD=dev psql -h localhost -p 5433 -U dev -d thesis_ai_dev -c "SELECT 1;"
```

**DAG task failures:**
- **API rate limiting (Yahoo Finance, FRED, SEC):**
  - Wait 10-30 minutes
  - Click failed task → "Clear" → Retry
  
- **Network timeouts:**
  - Check internet connection
  - Retry the failed task

- **Missing data for certain stocks:**
  - Normal - not all stocks have data every day
  - DAG will continue processing other stocks

**Clear task to retry:**
1. Click on failed task in Graph view
2. Click "Clear" button
3. Select "Yes" to rerun

**View detailed logs:**
1. Click on task
2. Click "Log" button
3. Scroll to see error details

**Reset Airflow metadata:**
```bash
airflow db reset
# Re-run Airflow configuration steps from Setup section
```

## General troubleshooting
`npm i`

Delete database (see reset commands above)

`npm run db:migrate`

`npm run build:watch` # UI

`npm run start:watch` # Server

## AI Coding

`npm install -g @anthropic-ai/claude-code`

claude --dangerously-skip-permissions