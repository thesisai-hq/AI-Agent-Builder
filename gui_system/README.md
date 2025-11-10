# AI Agent Builder - GUI System

Web-based graphical interface for creating and managing AI investment agents.

## Overview

This GUI system provides a user-friendly interface for:
- Creating rule-based and LLM-powered investment agents
- Using pre-built strategy templates
- Managing and testing agents
- Exporting agents as Python code

## Tech Stack

**Backend:**
- FastAPI (Python 3.10+)
- JSON file storage
- Enhanced with caching and performance optimizations
- Extends `agent_framework` library

**Frontend:**
- SvelteKit + TypeScript
- Tailwind CSS
- shadcn-svelte components

## Quick Start

### 1. Install Backend Dependencies

```bash
cd AI-Agent-Builder

# Install agent_framework (if not already installed)
pip install -e .

# Install GUI backend dependencies
cd gui_system
pip install -r requirements.txt
```

### 2. Setup Frontend

```bash
cd gui_system/frontend
npm install
```

### 3. Run Development Server

**Option A: Backend + Frontend (Recommended)**
```bash
# From AI-Agent-Builder/gui_system directory
python run.py --frontend --no-browser
```

This will:
- Start FastAPI backend on http://localhost:8000
- Start SvelteKit dev server on http://localhost:5173

**Option B: Backend Only**
```bash
python run.py
```

Then start frontend separately:
```bash
cd frontend
npm run dev
```

## Project Structure

```
gui_system/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── models.py           # Pydantic models
│   ├── storage.py          # JSON storage manager
│   ├── data_cache.py       # Caching system
│   ├── code_generator.py   # Template-based code generation
│   ├── constants.py        # Configuration constants
│   ├── tools/              # Tool implementations
│   │   ├── web_search.py   # News search
│   │   ├── financial_data.py # Financial analysis
│   │   ├── calculator.py   # Valuation models
│   │   └── rag.py          # Document analysis (RAG)
│   ├── templates/          # Code generation templates
│   └── routes/             # API routes
│       ├── agents.py       # Agent CRUD
│       ├── templates.py    # Template management
│       ├── analysis.py     # Stock analysis
│       ├── formulas.py     # Formula validation
│       └── documents.py    # Document upload (RAG)
│
├── frontend/               # SvelteKit frontend
│   ├── src/
│   │   ├── routes/        # Pages (file-based routing)
│   │   ├── lib/           # Components and utilities
│   │   └── app.html       # HTML template
│   ├── package.json
│   └── svelte.config.js
│
├── storage/                # Data persistence
│   ├── agents/            # User-created agents (JSON)
│   │   └── {agent_id}/    # Per-agent storage
│   │       ├── config.json      # Agent configuration
│   │       ├── documents/       # Uploaded documents (RAG)
│   │       └── embeddings/      # Vector embeddings (RAG)
│   └── templates/         # Pre-built templates (JSON)
│
├── requirements.txt        # Backend dependencies
├── run.py                 # Launcher script
├── FORMULA_GUIDE.md       # Formula system documentation
└── README.md              # This file
```

## Features

### LLM Agent Tools
When creating LLM-powered agents, you can enable these tools:

1. **Web Search** - Fetches latest company news and developments
2. **Financial Data** - Comprehensive financial statements and analyst data
3. **Calculator** - Financial valuation models (DCF, Graham Number, Altman Z-Score, P/E)
4. **Document Analysis (RAG)** - Query uploaded PDF/TXT/DOC files for custom knowledge

### RAG System
- Upload documents per agent (PDFs, TXT, DOC files)
- Automatic embedding generation with ChromaDB
- Query relevant context during analysis
- No external database required - all stored locally

## API Endpoints

**Health Check:**
- `GET /api/health` - Detailed system health status

**Agents:**
- `POST /api/agents` - Create agent
- `GET /api/agents` - List all agents
- `GET /api/agents/{id}` - Get agent details
- `PATCH /api/agents/{id}` - Update agent
- `DELETE /api/agents/{id}` - Delete agent
- `GET /api/agents/{id}/export` - Export as Python code

**Documents (RAG):**
- `POST /api/agents/{id}/documents` - Upload document
- `GET /api/agents/{id}/documents` - List documents
- `DELETE /api/agents/{id}/documents/{filename}` - Delete document
- `POST /api/agents/{id}/documents/query` - Query documents

**Templates:**
- `GET /api/templates` - List all templates
- `GET /api/templates/{id}` - Get template details

**Analysis:**
- `POST /api/analysis` - Analyze stock with agent

**Formulas:**
- `POST /api/formulas/validate` - Validate formula
- `GET /api/formulas/templates` - List formula templates

**Cache:**
- `GET /api/cache/stats` - Cache statistics
- `POST /api/cache/clear` - Clear cache

## Development

### Backend Development

```bash
# Run with auto-reload
python run.py

# Or directly with uvicorn
uvicorn backend.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### API Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## Testing

### Test Backend Tools
```bash
cd gui_system
python test_tools.py
```

### Test RAG System
```bash
cd gui_system
python test_rag.py
```

## Creating Templates

Templates are JSON files in `storage/templates/`. See existing templates for examples.

## Troubleshooting

**Backend won't start:**
- Ensure `agent_framework` is installed: `pip install -e ../`
- Check Python version: `python --version` (need 3.10+)

**Frontend won't start:**
- Install dependencies: `cd frontend && npm install`
- Check Node version: `node --version` (need 18+)
- Verify `src/lib/` directory exists (should not be gitignored)

**CORS errors:**
- Backend allows localhost:5173 by default
- Check `backend/main.py` CORS configuration

**Slow performance:**
- Check cache stats: `curl http://localhost:8000/api/cache/stats`
- Clear cache if needed: `curl -X POST http://localhost:8000/api/cache/clear`

**RAG not working:**
- Ensure ChromaDB is installed: `pip install chromadb`
- Check that documents are uploaded successfully
- Verify embeddings directory exists in `storage/agents/{id}/embeddings/`

## Performance

- **Health checks**: <10ms (optimized, no API calls)
- **Cached queries**: ~50ms (98% faster than uncached)
- **First-time queries**: 2-3s (normal yfinance fetch)
- **Cache cleanup**: Automatic every 5 minutes

## Contributing

This GUI system extends the core `agent_framework`. See main repo for contribution guidelines.

## License

MIT License - See LICENSE file in main repository.
