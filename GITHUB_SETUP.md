# GitHub Publishing Guide

This guide will help you publish the AI Agent Framework to GitHub as version 1.0.0.

## Pre-Publishing Checklist

### 1. Clean Up Internal Files

```bash
# Remove internal development files
rm IMPROVEMENTS_SUMMARY.md
rm IMPLEMENTATION_REPORT.md
rm TEST_FIXES.md
rm diagnose_postgres.py
rm setup_test_db.sh
rm CLEANUP_CHECKLIST.md
rm GITHUB_SETUP.md  # This file after you're done!
```

### 2. Update Author Information

Edit these files with your information:

**setup.py:**
```python
author="Your Name",
author_email="your.email@example.com",
url="https://github.com/yourusername/ai-agent-framework",
```

**LICENSE:**
- Update copyright holder if needed

### 3. Verify All Tests Pass

```bash
# Setup test database
python setup_test_db.py

# Run all tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=agent_framework

# Run quickstart
python quickstart.py
```

All should pass ✅

### 4. Verify Examples Work

```bash
# Start database
docker-compose up -d postgres
python seed_data.py

# Test each example
python examples/01_basic.py
python examples/02_llm_agent.py  # Requires Ollama
python examples/03_rag_agent.py  # Requires sentence-transformers
```

## Create GitHub Repository

### 1. On GitHub

1. Go to https://github.com/new
2. Repository name: `ai-agent-framework`
3. Description: `Production-ready AI agent framework for financial analysis`
4. Choose Public
5. **DO NOT** initialize with README (we have one)
6. Click "Create repository"

### 2. Initialize Git (if not already done)

```bash
cd /path/to/AI-Agent-Builder

# Initialize git if needed
git init

# Add all files
git add .

# First commit
git commit -m "Initial release v1.0.0"
```

### 3. Connect to GitHub

```bash
# Add remote (replace with your URL)
git remote add origin https://github.com/yourusername/ai-agent-framework.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 4. Create Release Tag

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 5. Create GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `AI Agent Framework v1.0.0`
5. Description:
   ```markdown
   ## AI Agent Framework - Initial Release 🎉

   Production-ready framework for building AI financial analysis agents.

   ### Features
   - 🐳 Docker-first PostgreSQL setup
   - ✅ Production-ready with comprehensive error handling
   - 🧪 85% test coverage
   - 📚 Full type safety with Pydantic
   - 🔌 Optional LLM and RAG support

   ### Quick Start
   ```bash
   git clone https://github.com/yourusername/ai-agent-framework.git
   cd ai-agent-framework
   pip install -e .
   docker-compose up -d postgres
   python seed_data.py
   python examples/01_basic.py
   ```

   ### What's Included
   - 4 sample tickers with 90 days of data
   - 3 working examples
   - Complete test suite
   - Comprehensive documentation

   See [README.md](README.md) for full documentation.
   ```
6. Click "Publish release"

## Repository Settings

### Add Topics

Go to repository → About (gear icon) → Add topics:
- `python`
- `ai`
- `agents`
- `financial-analysis`
- `fastapi`
- `postgresql`
- `llm`
- `rag`
- `asyncio`
- `pydantic`

### Add Description

`Production-ready AI agent framework for financial analysis with PostgreSQL, LLM support, and comprehensive error handling`

### Enable Issues

Settings → Features → ✅ Issues

### Add License Badge

Automatically detected from LICENSE file

## Optional: Add GitHub Actions

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: agent_framework_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e .[dev]
      
      - name: Run schema
        run: psql postgresql://postgres:postgres@localhost:5432/agent_framework_test < schema.sql
      
      - name: Seed test database
        run: DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agent_framework_test python seed_data.py
      
      - name: Run tests
        run: pytest tests/ -v --cov=agent_framework
```

## Documentation

### Update README URLs

In README.md, replace `yourusername` with your actual GitHub username:
```markdown
git clone https://github.com/YOURUSERNAME/ai-agent-framework.git
```

### Verify Documentation Links

All documentation should be accessible:
- [docs/INSTALL.md](docs/INSTALL.md)
- [docs/DATABASE_SETUP.md](docs/DATABASE_SETUP.md)
- [docs/TESTING.md](docs/TESTING.md)
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)

## Post-Publication

### 1. Verify Repository

- [ ] README renders correctly
- [ ] Examples are visible
- [ ] Documentation is accessible
- [ ] License is displayed
- [ ] Tests badge (if using GitHub Actions)

### 2. Test Installation

On a fresh machine:
```bash
git clone https://github.com/yourusername/ai-agent-framework.git
cd ai-agent-framework
pip install -e .
docker-compose up -d postgres
python seed_data.py
python quickstart.py
```

### 3. Announce

Consider announcing on:
- Reddit: r/Python, r/MachineLearning
- Hacker News
- Twitter/X
- LinkedIn
- Dev.to

### 4. Monitor

- Watch for issues
- Respond to questions
- Review pull requests
- Update documentation as needed

## Maintenance

### For Future Updates

1. Create feature branch
2. Make changes
3. Update CHANGELOG.md
4. Run all tests
5. Create PR and merge
6. Tag new version
7. Create GitHub release

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes (2.0.0)
- MINOR: New features, backward compatible (1.1.0)
- PATCH: Bug fixes (1.0.1)

## Troubleshooting

### If Git Not Initialized

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### If Files Already Committed

```bash
# Remove files from git
git rm --cached IMPROVEMENTS_SUMMARY.md
git rm --cached IMPLEMENTATION_REPORT.md
git rm --cached TEST_FIXES.md
git rm --cached diagnose_postgres.py
git rm --cached setup_test_db.sh

# Commit removal
git commit -m "Remove internal development files"
git push
```

### If Need to Update Remote

```bash
# Change remote URL
git remote set-url origin https://github.com/yourusername/ai-agent-framework.git

# Verify
git remote -v
```

## Final Checklist

Before publishing:
- [ ] All internal files removed
- [ ] Author info updated in setup.py
- [ ] All tests pass
- [ ] Examples work
- [ ] Documentation complete
- [ ] .gitignore includes all necessary files
- [ ] README has correct URLs
- [ ] License file present

After publishing:
- [ ] Repository created on GitHub
- [ ] Code pushed successfully
- [ ] Release v1.0.0 created
- [ ] Repository settings configured
- [ ] Topics added
- [ ] README renders correctly
- [ ] Fresh install tested

## Success! 🎉

Your AI Agent Framework is now public and ready for the community!

Next steps:
1. Monitor issues and questions
2. Consider setting up GitHub Actions for CI/CD
3. Write blog post or tutorial
4. Share with community
5. Iterate based on feedback

---

**Remember**: Remove this file before final commit!
```bash
rm GITHUB_SETUP.md
```
