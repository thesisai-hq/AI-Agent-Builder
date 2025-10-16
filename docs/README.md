# Documentation

Complete documentation for the AI Investment Advisor framework.

---

## 📚 Documentation Structure

### Getting Started
- **[Getting Started Guide](getting-started.md)** - Installation, setup, first analysis
- **[Quickstart (root)](../QUICKSTART.md)** - 3-minute quick reference

### Core Guides
- **[Architecture Guide](architecture.md)** - System design, patterns, performance
- **[Creating Agents Guide](creating-agents.md)** - Build custom agents step-by-step
- **[API Reference](api-reference.md)** - Complete REST API documentation

### Additional Resources
- **[Main README](../README.md)** - Project overview
- **[Test Database Guide](../TEST_DATABASE.md)** - Mock database setup
- **[Project Summary](../PROJECT_SUMMARY.md)** - Complete system overview
- **[File Checklist](../FILE_CHECKLIST.md)** - Implementation guide

---

## 🎯 Quick Navigation

**I want to...**

| Goal | Document |
|------|----------|
| Install and setup | [Getting Started](getting-started.md) |
| Understand the architecture | [Architecture](architecture.md) |
| Create my first agent | [Creating Agents](creating-agents.md) |
| Use the API | [API Reference](api-reference.md) |
| Setup the database | [Test Database Guide](../TEST_DATABASE.md) |
| Quick reference | [Quickstart](../QUICKSTART.md) |
| See what's built | [Project Summary](../PROJECT_SUMMARY.md) |

---

## 📖 Documentation By Topic

### For Beginners

1. Start here: [Getting Started](getting-started.md)
2. Then: [Creating Agents](creating-agents.md)
3. Finally: [API Reference](api-reference.md)

### For Developers

1. Understand: [Architecture](architecture.md)
2. Build: [Creating Agents](creating-agents.md)
3. Extend: [Project Summary](../PROJECT_SUMMARY.md)

### For DevOps

1. Setup: [Getting Started](getting-started.md)
2. Deploy: [Architecture - Production](architecture.md#production-deployment)
3. Monitor: [API Reference - Health](api-reference.md#health-check)

---

## 🎓 Learning Path

### Week 1: Fundamentals
- [ ] Complete [Getting Started](getting-started.md)
- [ ] Read [Architecture](architecture.md)
- [ ] Study example agents in `../examples/`
- [ ] Run analyses on all 8 test stocks

### Week 2: Building
- [ ] Create first agent using [Creating Agents](creating-agents.md)
- [ ] Build 3-5 agents for your strategy
- [ ] Test agents individually
- [ ] Register and test via API

### Week 3: Integration
- [ ] Build agent portfolio (10-15 agents)
- [ ] Test with different stocks
- [ ] Integrate with frontend/dashboard
- [ ] Optimize agent weights

### Week 4: Production
- [ ] Replace mock data with real APIs
- [ ] Add authentication
- [ ] Deploy to cloud
- [ ] Set up monitoring

---

## 🔍 Document Details

### Getting Started (getting-started.md)
**Length:** ~1,500 lines  
**Topics:**
- Prerequisites
- Installation steps
- Database setup
- First analysis
- Troubleshooting

**Best for:** New users

### Architecture (architecture.md)
**Length:** ~2,000 lines  
**Topics:**
- System design
- Components breakdown
- Design patterns
- Performance optimization
- Security architecture
- Scalability

**Best for:** Understanding internals

### Creating Agents (creating-agents.md)
**Length:** ~2,500 lines  
**Topics:**
- Agent anatomy
- Design patterns
- Data access
- Testing
- Best practices
- Real-world examples

**Best for:** Building custom agents

### API Reference (api-reference.md)
**Length:** ~1,800 lines  
**Topics:**
- All endpoints
- Request/response schemas
- Error handling
- Usage examples
- Python client
- Best practices

**Best for:** API integration

---

## 🛠️ Tools & Resources

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Spec:** http://localhost:8000/openapi.json

### Example Code

All examples in `../examples/`:
- 61 complete agents
- Registration code
- Testing utilities

### Database Tools

- **pgAdmin:** http://localhost:5050 (if started with `--profile with-admin`)
- **psql:** `docker exec -it agent-test-db psql -U agent_user -d agent_test`

---

## 📊 Documentation Statistics

| Document | Lines | Words | Topics |
|----------|-------|-------|--------|
| Getting Started | ~1,500 | ~8,000 | 12 |
| Architecture | ~2,000 | ~10,000 | 15 |
| Creating Agents | ~2,500 | ~12,000 | 18 |
| API Reference | ~1,800 | ~9,000 | 14 |
| **Total** | **~7,800** | **~39,000** | **59** |

Plus root documentation (~3,000 lines)

**Grand Total:** ~10,800 lines of documentation! 📚

---

## 🤝 Contributing to Docs

Found an error or want to improve the docs?

1. Edit the markdown file
2. Test code examples
3. Submit a pull request
4. Follow the style guide below

### Documentation Style Guide

**Format:**
- Use H2 (##) for main sections
- Use H3 (###) for subsections
- Include code examples for concepts
- Add emojis for visual hierarchy
- Use tables for comparisons
- Include "Examples" sections

**Code Blocks:**
- Always specify language
- Include comments
- Show expected output
- Provide complete examples

**Links:**
- Use relative links for internal docs
- Use descriptive link text
- Check links work

---

## 📞 Support

**Found a bug?** Open an issue on GitHub

**Have a question?** Check existing documentation first:
1. Search this docs folder
2. Check [Troubleshooting](getting-started.md#troubleshooting)
3. Review [API Reference](api-reference.md)
4. Ask in GitHub Discussions

**Want to contribute?** Pull requests welcome!

---

## 🗺️ Documentation Roadmap

### Planned Additions

- [ ] Video tutorials
- [ ] Jupyter notebook examples
- [ ] Performance tuning guide
- [ ] Security best practices
- [ ] Deployment templates (AWS, GCP, Azure)
- [ ] Frontend integration guide
- [ ] Backtesting tutorial
- [ ] Real data integration guide

---

**Start learning:** [Getting Started Guide](getting-started.md) →