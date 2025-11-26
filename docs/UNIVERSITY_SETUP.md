# University & Classroom Setup Guide

Guide for professors and IT staff deploying AI-Agent-Builder in educational environments.

---

## 🎓 Overview

AI-Agent-Builder is designed for finance education. This guide helps you:
- Deploy for entire classes (1-100+ students)
- Integrate into course curriculum
- Create assignments and projects
- Manage student access

---

## 🚀 Quick Setup (Lab Deployment)

### Option A: Individual Student Installations (Recommended)

**Each student on their own computer:**

```bash
# Students run these commands:
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
./gui/setup.sh   # Installs all dependencies
./gui/launch.sh  # Opens GUI at http://localhost:8501
```

**Advantages:**
- ✅ No server setup needed
- ✅ Students have full control
- ✅ Works on Mac, Linux, Windows (WSL2)
- ✅ Can work offline after setup
- ✅ No resource contention

**Time:** 10-15 minutes per student

---

### Option B: Centralized Server (For Computer Labs)

**Deploy once, students access via web browser:**

```bash
# On lab server (one-time setup)
git clone https://github.com/thesisai-hq/AI-Agent-Builder.git
cd AI-Agent-Builder
./gui/setup.sh

# Configure server access
nano .streamlit/config.toml
```

**config.toml:**
```toml
[server]
port = 8501
address = "0.0.0.0"  # Allow external access
headless = true

[browser]
gatherUsageStats = false
```

**Start server:**
```bash
./gui/launch.sh

# Students access at:
# http://your-server-ip:8501
```

**Advantages:**
- ✅ One installation for all students
- ✅ Centralized updates
- ✅ Lower system requirements per student
- ✅ Browser-based (no installation for students)

**Disadvantages:**
- ❌ Requires server management
- ❌ Students share resources
- ❌ Network dependency

---

## 📚 Course Integration

### Suggested Course Structures

#### Course 1: Introduction to Quantitative Investing (Undergrad)

**Duration:** 8 weeks

**Syllabus:**

| Week | Topic | Agent Focus | Assignment |
|------|-------|-------------|------------|
| 1-2 | Value Investing Fundamentals | Rule-based | Build Buffett-style agent |
| 3-4 | Growth Investing & GARP | Score-based rules | Build Lynch-style agent |
| 5-6 | Technical Analysis | Rules + momentum | Create momentum strategy |
| 7-8 | Multi-Factor Models | Combine agents | Capstone: Custom strategy |

**Learning Outcomes:**
- Understand valuation metrics (PE, PB, PEG)
- Apply investment frameworks (Buffett, Lynch, Graham)
- Build quantitative models
- Test hypotheses with data
- Compare strategy performance

---

#### Course 2: AI in Financial Analysis (Grad/Advanced Undergrad)

**Duration:** 8 weeks

**Syllabus:**

| Week | Topic | Technology | Assignment |
|------|-------|------------|------------|
| 1-2 | LLM Fundamentals | Ollama basics | Create AI analyst agent |
| 3-4 | Prompt Engineering | Temperature, prompts | Optimize AI reasoning |
| 5-6 | RAG Systems | Document analysis | Analyze SEC filings |
| 7-8 | Hybrid Systems | Rules + AI | Build production-scale system |

**Learning Outcomes:**
- Understand large language models
- Apply prompt engineering techniques
- Implement RAG for documents
- Optimize AI costs (hybrid approach)
- Build real-world AI systems

---

#### Course 3: Investment Analysis with Python (CS + Finance)

**Duration:** 12 weeks

**Syllabus:**

| Week | Topic | Skills | Deliverable |
|------|-------|--------|-------------|
| 1-2 | Python Basics | Data types, functions | Simple rule agent |
| 3-4 | Data Analysis | Pandas, NumPy | Multi-factor agent |
| 5-6 | APIs & Databases | REST, PostgreSQL | Real data integration |
| 7-8 | AI Integration | LLMs, prompts | AI-powered agent |
| 9-10 | Document Processing | RAG, PDFs | SEC filing analyzer |
| 11-12 | Final Project | Full stack | Custom investment system |

**Learning Outcomes:**
- Learn Python through finance applications
- Work with real financial data
- Integrate AI models
- Build complete applications
- Portfolio-ready project

---

## 📝 Sample Assignments

### Assignment 1: Value Investor (Beginner)

**Objective:** Create rule-based value investing agent

**Instructions:**
1. Research Warren Buffett's investment criteria
2. Define 3-5 quantitative rules
3. Create agent in GUI
4. Test on 10 different companies
5. Write 2-page reflection on results

**Grading Rubric:**
- Rule selection (30%): Appropriate value criteria
- Implementation (20%): Agent works correctly
- Testing (20%): Comprehensive test scenarios
- Analysis (30%): Insights from results

**Example submission:**
```
Agent Name: BuffettValueAgent
Rules:
- PE < 20 (undervalued)
- ROE > 15% (quality)
- Debt/Equity < 1.0 (safety)
- Profit Margin > 12% (profitability)

Test Results:
- Tested on 10 companies
- 4 bullish, 2 bearish, 4 neutral
- Average confidence: 72%

Reflection:
My agent tends to favor established, profitable companies
with reasonable valuations. It correctly avoided high-debt
companies (value traps). However, it might be too conservative
and miss growth opportunities...
```

---

### Assignment 2: AI-Powered Analyst (Intermediate)

**Objective:** Create LLM agent with custom reasoning

**Instructions:**
1. Set up Ollama (use LLM Setup Wizard)
2. Define investment philosophy (value, growth, quality, etc.)
3. Write effective system prompt
4. Create LLM agent
5. Test on 5 real companies (yfinance)
6. Compare with rule-based version
7. Write 3-page analysis

**Grading Rubric:**
- Setup (15%): Successfully configured LLM
- Prompt quality (25%): Clear, specific investment philosophy
- Testing (20%): Real data, multiple scenarios
- Comparison (20%): Thoughtful rule vs AI analysis
- Writing (20%): Clear explanation of findings

**Example submission:**
```
Investment Philosophy: Quality Growth
System Prompt: "You are a quality growth investor. Focus on
sustainable competitive advantages, expanding margins, and
reasonable valuations relative to growth (PEG < 2)."

Test Results:
Company | LLM Signal | Rule Signal | Difference
AAPL    | Bullish 75%| Neutral 50%| AI saw quality depth
TSLA    | Neutral 60%| Bullish 80%| AI concerned about valuation
...

Key Finding: LLM agents provide more nuanced analysis,
especially for complex tradeoffs like high growth but
high valuation. Rule-based is faster but misses context.
```

---

### Assignment 3: Document Analysis (Advanced)

**Objective:** Use RAG to analyze SEC filings

**Instructions:**
1. Download 10-K filing from sec.gov
2. Create RAG agent
3. Configure chunk size and top_k appropriately
4. Extract:
   - Financial performance trends
   - Risk factors
   - Growth strategies
   - Competitive position
5. Write 5-page investment memo

**Grading Rubric:**
- RAG setup (15%): Correct configuration
- Information extraction (30%): Key points identified
- Analysis depth (25%): Insightful interpretation
- Investment thesis (20%): Clear recommendation with evidence
- Writing quality (10%): Professional, well-organized

---

### Assignment 4: Multi-Agent System (Capstone)

**Objective:** Build comprehensive analysis system

**Instructions:**
1. Create 3 different agent types:
   - Rule-based screener
   - LLM quality analyst  
   - RAG document analyzer
2. Analyze 3 companies comprehensively
3. Combine signals from all agents
4. Develop consensus framework
5. Present findings (10-minute presentation + 8-page report)

**Grading Rubric:**
- Agent diversity (20%): Different types, complementary
- Integration (20%): Effective signal combination
- Analysis depth (25%): Thorough company research
- Presentation (20%): Clear communication
- Code quality (15%): If viewing code, is it well-structured?

---

## 🛠️ Technical Requirements

### Minimum Student Computer Specs

**For Rule-Based Agents Only:**
- CPU: Any modern processor
- RAM: 4GB
- Storage: 2GB free
- OS: Windows (WSL2), Mac, Linux

**For LLM/RAG Agents (with Ollama):**
- CPU: Multi-core (4+ cores recommended)
- RAM: 8GB (16GB recommended)
- Storage: 10GB free (for AI models)
- OS: Windows (WSL2), Mac, Linux

**For Cloud AI (OpenAI/Anthropic):**
- Any computer with internet
- API budget (~$5-20 per student per semester)

---

### Server Specs (Centralized Deployment)

**For 20-50 students:**
- CPU: 8+ cores
- RAM: 32GB
- Storage: 100GB SSD
- Network: 100Mbps+

**For 50-100 students:**
- CPU: 16+ cores
- RAM: 64GB
- Storage: 200GB SSD
- Network: 1Gbps
- Consider load balancing

---

## 📊 Data Management

### Included Sample Data

**Database contains:**
- 4 sample stocks (AAPL, MSFT, TSLA, JPM)
- Basic fundamentals (PE, ROE, margins, etc.)
- Mock SEC filings
- Sufficient for learning

**Students can also:**
- Use mock data (unlimited fictional scenarios)
- Fetch real data with yfinance (free)
- Upload their own PDF documents

### Adding More Sample Data

```bash
# Edit seed_data.py to add companies
nano seed_data.py

# Re-run seeding
python seed_data.py
```

---

## 🔒 Security & Privacy

### Student Data

**What is stored:**
- Agent code files (in `examples/` folder)
- Database has sample data only

**What is NOT stored:**
- No student personal information
- No real trading data
- No API keys in repository

**Privacy:**
- Ollama runs locally (no data sent to cloud)
- OpenAI/Anthropic: Data sent to their servers (review their policies)
- Recommend Ollama for privacy-sensitive environments

### API Key Management

**For OpenAI/Anthropic:**
- Each student uses their own API key (personal responsibility)
- Or department provides shared key (monitor costs!)
- Never commit API keys to git

**Best practice:**
```bash
# Each student creates own .env file
cp .env.example .env
nano .env  # Add their own API key
```

---

## 💰 Cost Considerations

### Free Option (Recommended for Classes)

**Using Ollama:**
- Installation: Free
- Models: Free
- Usage: Unlimited
- **Total cost per student:** $0

**Requirements:**
- Students need decent computers (8GB+ RAM)
- Or use lab computers with Ollama installed

---

### Paid Option (Cloud AI)

**Using OpenAI:**
- API key: Free to create
- Usage: ~$0.01-0.02 per stock analysis
- **Estimated cost per student:** $10-30 per semester
  - Assumes 500-1500 analyses per semester
  - Conservative for typical course workload

**Who pays?**
- Option A: Department provides budget
- Option B: Students pay (like textbook cost)
- Option C: Free credits (OpenAI offers educational credits)

**Apply for educational credits:**
- OpenAI: https://openai.com/form/researcher-access-program
- Anthropic: Contact education@anthropic.com

---

## 🎯 Best Practices

### For First Class Session

**Pre-class:**
1. Test installation on lab computers
2. Prepare demo agent
3. Have troubleshooting guide ready

**In class:**
1. Show GUI demo (10 min)
2. Students install (20 min)
3. Everyone creates first agent (20 min)
4. Troubleshoot issues (10 min)

**Expected issues:**
- Docker not installed → Use mock data only
- Ollama installation problems → Use OpenAI with class key
- Python environment conflicts → Use conda/venv

---

### Managing Student Progress

**Track progress via:**
- Agent files in examples/ folder
- Git commits (if using version control)
- Assignment submissions
- Class discussions

**Encourage:**
- Experimentation (it's okay to fail!)
- Code viewing (learn Python gradually)
- Sharing strategies (learn from each other)
- Questions (no question is too basic)

---

### Preventing Common Issues

**Issue 1: Students can't install dependencies**

**Solution:**
- Provide pre-configured lab computers
- Or detailed troubleshooting guide
- Or use Docker container (see below)

**Issue 2: Ollama too resource-intensive**

**Solution:**
- Use cloud AI (OpenAI) instead
- Or use lab computers with better specs
- Or use smaller models (phi instead of llama3.2)

**Issue 3: Students confused by code**

**Solution:**
- Emphasize: Coding is optional
- GUI creates working code
- Use educational annotations feature
- Start with simple rule-based agents

---

## 🐳 Docker Deployment (Advanced)

For consistent environment across all students:

```bash
# Build image
docker compose build

# Run for students
docker compose up gui

# Access at http://localhost:8501
```

**docker-compose.yml for education:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: agent_framework
      POSTGRES_USER: student
      POSTGRES_PASSWORD: education
    ports:
      - "5432:5432"
    volumes:
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql

  gui:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - postgres
    environment:
      - DB_HOST=postgres
      - DB_USER=student
      - DB_PASSWORD=education
```

---

## 📚 Suggested Curriculum

### Week-by-Week Breakdown (8-Week Course)

**Week 1: Introduction**
- Lecture: Investment analysis basics
- Lab: Install software, create first rule-based agent
- Assignment: Build simple value screener
- Reading: docs/CHOOSING_AGENT_TYPE.md

**Week 2: Value Investing**
- Lecture: Buffett, Graham principles
- Lab: Multi-factor value agents (score-based)
- Assignment: Implement Benjamin Graham strategy
- Reading: examples/05_buffett_quality.py (code walkthrough)

**Week 3: Growth Investing**
- Lecture: Lynch, GARP methodology
- Lab: Growth-focused agents
- Assignment: Build PEG-based strategy
- Reading: examples/06_lynch_garp.py

**Week 4: AI Fundamentals**
- Lecture: Introduction to LLMs
- Lab: Set up Ollama, create first AI agent
- Assignment: Compare rule-based vs AI analysis
- Reading: docs/LLM_CUSTOMIZATION.md

**Week 5: Prompt Engineering**
- Lecture: Effective AI prompts
- Lab: Experiment with temperature and system prompts
- Assignment: Create AI agent with specific personality
- Reading: "🎨 Customizing Prompts" tab in GUI

**Week 6: Document Analysis**
- Lecture: Information extraction, RAG systems
- Lab: Create RAG agent, analyze 10-K filing
- Assignment: Extract insights from 3 company filings
- Reading: examples/04_rag_agent.py

**Week 7: Optimization & Scale**
- Lecture: Hybrid systems, cost optimization
- Lab: Build hybrid agent (rules + AI)
- Assignment: Optimize for 500-stock universe
- Reading: docs/HYBRID_AGENTS.md

**Week 8: Final Project**
- Students build complete multi-agent system
- Analyze 5 companies comprehensively
- Present findings to class
- Submit code + report

---

### Alternative: Workshop Format (1-Day Intensive)

**9:00 AM - Introduction (30 min)**
- What are investment agents?
- Why automate analysis?
- Course overview

**9:30 AM - Hands-on: Rule-Based (90 min)**
- Install software
- Create first agent
- Test with data
- Understand signals

**11:00 AM - Break (15 min)**

**11:15 AM - Investment Strategies (75 min)**
- Value investing principles
- Growth investing principles
- Build strategy agents
- Compare results

**12:30 PM - Lunch (60 min)**

**1:30 PM - AI Integration (90 min)**
- LLM setup
- Create AI agent
- Prompt engineering
- Test and compare

**3:00 PM - Break (15 min)**

**3:15 PM - Advanced Topics (75 min)**
- Document analysis with RAG
- Hybrid systems
- Multi-agent approaches
- Real data integration

**4:30 PM - Wrap-up (30 min)**
- Best practices
- Resources for continued learning
- Q&A

**5:00 PM - End**

---

## 🎯 Learning Assessments

### Formative Assessment (During Course)

**Weekly quizzes:**
- Investment concept understanding
- Agent configuration knowledge
- Signal interpretation
- Code reading comprehension (optional)

**Lab participation:**
- Successfully create agents
- Test with various scenarios
- Thoughtful experimentation
- Help peers troubleshoot

---

### Summative Assessment (End of Course)

**Option A: Agent Portfolio**
- Create 5 agents (rule, LLM, hybrid, RAG, custom)
- Document strategy for each
- Test on real companies
- Analyze results
- Weight: 40%

**Option B: Research Project**
- Choose investment theme
- Build specialized agent
- Analyze 10+ companies
- Write professional report
- Present to class
- Weight: 60%

**Option C: Code Contribution**
- Improve existing agent
- Add new example strategy
- Enhance documentation
- Submit pull request
- Weight: Bonus 20%

---

## 🛠️ Troubleshooting for Educators

### Common Student Issues

#### "Can't install dependencies"

**Cause:** Python environment conflicts

**Solution:**
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -e ".[all]"
```

Or use conda:
```bash
conda create -n agents python=3.11
conda activate agents
pip install -e ".[all]"
```

---

#### "Docker won't start"

**Cause:** Port conflict or Docker not running

**Solution:**
```bash
# Check if port 5432 is in use
lsof -i :5432

# Kill conflicting process or change port in .env
DB_PORT=5433
```

---

#### "Ollama is too slow"

**Cause:** Computer doesn't have enough resources

**Solution:**
- Use smaller model: `ollama pull phi`
- Or use cloud AI (OpenAI)
- Or upgrade computer RAM

---

#### "Don't understand the code"

**Cause:** No programming background

**Solution:**
- Emphasize: **Coding is optional**
- Focus on GUI and concepts
- Use educational annotations ("👁️ View" button)
- Pair programming (students help each other)

---

### Class Management Tips

**Git for submissions (optional):**
```bash
# Students fork repository
# Submit via pull request
# You review code in GitHub
```

**Shared Google Drive:**
```bash
# Students export agents
# Upload to shared folder
# You download and test
```

**In-class demos:**
```bash
# Screen share GUI
# Show agent creation process
# Run analysis together
# Discuss results
```

---

## 📞 Support for Educators

### Resources

- **Documentation:** Complete guides in docs/
- **Examples:** Reference implementations in examples/
- **Community:** [GitHub Discussions](https://github.com/thesisai-hq/AI-Agent-Builder/discussions)

### Educational Resources

**Available:**
- Complete documentation in docs/
- Sample syllabi (this document)
- Assignment templates (see above)
- Grading rubrics (see above)
- Video tutorials (in development)

---

## 🎓 Success Stories

*Share your course experience via [GitHub Discussions](https://github.com/thesisai-hq/AI-Agent-Builder/discussions)*

---

## 🔄 Updates & Maintenance

### Keeping Up to Date

```bash
# Update to latest version
git pull origin main

# Reinstall dependencies
pip install -e ".[all]"

# Update database schema if needed
python seed_data.py
```

### Version for Semester

**Recommendation:** Pin to specific version for consistency

```bash
# At semester start
git checkout v1.0.0-edu
# Students all use same version

# Update between semesters
git checkout main
git pull
```

---

## 💡 Tips for Success

### For Professors

✅ **Start simple:** Begin with rule-based agents  
✅ **Show, then do:** Demo first, students follow  
✅ **Embrace failures:** Debugging is learning  
✅ **Real examples:** Use actual companies students know  
✅ **Connect theory:** Link agents to lecture concepts  
✅ **Iterate:** Start basic, build complexity  

### For TAs

✅ **Test everything first:** Run through all assignments yourself  
✅ **Office hours:** Be ready for installation issues  
✅ **Sample solutions:** Have working examples ready  
✅ **Common errors:** Keep troubleshooting cheat sheet  
✅ **Be patient:** Remember students are learning  

### For IT Staff

✅ **Test deployment:** Verify on fresh system  
✅ **Document setup:** Keep internal notes  
✅ **Resource monitoring:** Check CPU/RAM if centralized  
✅ **Backup plan:** Have USB drives with installers  
✅ **Network access:** Ensure students can reach PyPI, GitHub  

---

## 📊 Recommended Timeline

### Semester Preparation (2-3 Weeks Before)

- [ ] Test installation on lab computers
- [ ] Prepare course materials
- [ ] Set up LLM provider (Ollama or class API key)
- [ ] Create sample assignments
- [ ] Test all examples

### First Week

- [ ] Installation session (computer lab)
- [ ] GUI walkthrough
- [ ] Create first agent together
- [ ] Assign homework: Simple value agent

### Throughout Semester

- [ ] Weekly lab sessions (hands-on)
- [ ] Progressive complexity
- [ ] Monitor student progress
- [ ] Address issues quickly

### Final Week

- [ ] Project presentations
- [ ] Code reviews (optional)
- [ ] Retrospective discussion
- [ ] Gather feedback for next semester

---

## 🤝 Contributing to Education

### Share Your Experience

If you use this in your course:
- Share syllabus (we'll link from docs)
- Provide student feedback
- Suggest improvements
- Contribute examples

**Your input helps improve education for everyone!**

### Academic Citations

If you publish research using this tool:

```bibtex
@software{ai_agent_builder,
  title = {AI-Agent-Builder: Educational Framework for Investment Analysis},
  author = {ThesisAI LLC},
  year = {2025},
  url = {https://github.com/thesisai-hq/AI-Agent-Builder},
  note = {Educational tool for learning quantitative investing and AI}
}
```

---

## 📞 Get Help

**Documentation:**
- [Data Flow](DATA_FLOW.md) - How agents work transparently ⭐
- [Multi-Agent Systems](MULTI_AGENT_SYSTEMS.md) - Advanced orchestration ⭐
- [Getting Started](GETTING_STARTED.md) - Installation
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues

**Technical issues:** [GitHub Issues](https://github.com/thesisai-hq/AI-Agent-Builder/issues)  
**Questions & Discussion:** [GitHub Discussions](https://github.com/thesisai-hq/AI-Agent-Builder/discussions)  

---

<p align="center">
  <sub>Built with ❤️ for students and educators</sub><br>
  <sub>Educational Use Only | MIT License</sub>
</p>
