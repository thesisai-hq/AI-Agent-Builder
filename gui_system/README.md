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
- Open your browser and check the URLs.

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
│   └── routes/             # API routes
│       ├── agents.py       # Agent CRUD
│       ├── templates.py    # Template management
│       └── analysis.py     # Stock analysis
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
│   └── templates/         # Pre-built templates (JSON)
│
├── requirements.txt        # Backend dependencies
├── run.py                 # Launcher script
└── README.md              # This file
```

## API Endpoints

**Health Check:**
- `GET /api/health` - System health status

**Agents:**
- `POST /api/agents` - Create agent
- `GET /api/agents` - List all agents
- `GET /api/agents/{id}` - Get agent details
- `PATCH /api/agents/{id}` - Update agent
- `DELETE /api/agents/{id}` - Delete agent
- `GET /api/agents/{id}/export` - Export as Python code

**Templates:**
- `GET /api/templates` - List all templates
- `GET /api/templates/{id}` - Get template details

**Analysis:**
- `POST /api/analysis` - Analyze stock with agent

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

## Creating Templates

Templates are JSON files in `storage/templates/`. Example:

```json
{
  "id": "my_template",
  "name": "My Strategy",
  "description": "Description here",
  "type": "rule_based",
  "icon": "chart",
  "color": "#3B82F6",
  "goal": "Investment goal",
  "category": "fundamental",
  "rules": [
    {
      "conditions": [
        {
          "indicator": "pe_ratio",
          "operator": "<",
          "value": 15
        }
      ],
      "action": {
        "action": "bullish",
        "size": 10
      },
      "description": "Rule description"
    }
  ]
}
```

## Troubleshooting

**Backend won't start:**
- Ensure `agent_framework` is installed: `pip install -e ../`
- Check Python version: `python --version` (need 3.10+)

**Frontend won't start:**
- Install dependencies: `cd frontend && npm install`
- Check Node version: `node --version` (need 18+)

**CORS errors:**
- Backend allows localhost:5173 by default
- Check `backend/main.py` CORS configuration

**Database connection errors:**
- GUI system doesn't require database for agent management
- Database is only needed for stock analysis
- Check `agent_framework` database setup in main repo

## Next Steps

After getting the GUI running:

1. **Explore Templates** - Check out pre-built strategies
2. **Create an Agent** - Use the wizard to build your first agent
3. **Test Analysis** - Analyze stocks with your agents
4. **Export Code** - Download Python code for your agents

## Contributing

This GUI system extends the core `agent_framework`. See main repo for contribution guidelines.

## License

MIT License - See LICENSE file in main repository.
