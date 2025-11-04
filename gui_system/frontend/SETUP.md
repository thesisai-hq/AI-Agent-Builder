# Frontend Setup Guide

## What's Been Created

Complete SvelteKit frontend with:
- ✅ TypeScript configuration
- ✅ Tailwind CSS styling
- ✅ Home page with template cards
- ✅ API client for backend communication
- ✅ Global state management with Svelte stores
- ✅ Responsive layout with navigation
- ✅ Loading and error states

## Installation & Running

### 1. Install Dependencies

```bash
cd gui_system/frontend
npm install
```

This will install:
- SvelteKit 2.x
- TypeScript
- Tailwind CSS
- Lucide icons
- Other utilities

**Expected time:** 1-2 minutes

### 2. Start Development Server

**Make sure backend is running first!**

```bash
# In one terminal - start backend
cd gui_system
python run.py

# In another terminal - start frontend
cd gui_system/frontend
npm run dev
```

The frontend will be available at: **http://localhost:5173**

### 3. Verify Everything Works

Open http://localhost:5173 and you should see:
- ✅ "AI Agent Builder" header
- ✅ Stats showing 0 agents (initially)
- ✅ "Create New Agent" and "View My Agents" buttons
- ✅ Template cards (Value Investing, Dividend Income, Growth Momentum)

## Troubleshooting

### Port 5173 already in use

```bash
# Kill the process
lsof -ti:5173 | xargs kill -9

# Or change port in vite.config.js
```

### "Failed to load templates"

Make sure backend is running on http://localhost:8000

```bash
# Check backend health
curl http://localhost:8000/api/health

# Should return: {"status":"healthy","version":"1.0.0",...}
```

### CORS errors in browser console

This means backend is not configured properly. Check `backend/main.py` CORS settings.

### TypeScript errors

```bash
npm run check
```

This will show any type errors.

## Project Structure

```
frontend/
├── src/
│   ├── routes/              # Pages
│   │   ├── +layout.svelte  # Main layout (header, footer)
│   │   └── +page.svelte    # Home page ✅
│   │
│   ├── lib/
│   │   ├── api.ts          # API client ✅
│   │   ├── components/
│   │   │   └── TemplateCard.svelte  # Template card ✅
│   │   └── stores/
│   │       └── agents.ts   # Global state ✅
│   │
│   ├── app.html            # HTML template
│   └── app.css             # Global styles (Tailwind)
│
├── static/                 # Static assets
├── package.json           # Dependencies
├── svelte.config.js       # SvelteKit config
├── vite.config.js         # Vite config
├── tailwind.config.js     # Tailwind config
└── tsconfig.json          # TypeScript config
```

## What's Next

Now that the home page is working, we'll build:

1. **Agent List Page** (`/agents`)
   - Display all created agents
   - Delete functionality
   - Quick actions

2. **Create Agent Page** (`/create`)
   - Multi-step wizard
   - Template selection
   - **Visual Rule Builder** (priority!)
   - LLM configuration

3. **Agent Detail Page** (`/agents/[id]`)
   - View agent details
   - Test with stock tickers
   - Export code

## Development Tips

### Hot Module Replacement (HMR)

Any changes to `.svelte` files automatically refresh in the browser without losing state.

### Tailwind CSS Classes

This project uses Tailwind utility classes:
```svelte
<div class="bg-white p-6 rounded-lg shadow-md">
  <h1 class="text-2xl font-bold text-gray-900">Title</h1>
</div>
```

### Svelte Reactivity

Variables with `$state` are reactive:
```svelte
<script lang="ts">
  let count = $state(0); // Reactive
  
  function increment() {
    count++; // UI updates automatically
  }
</script>
```

### API Calls

Use the `api` client:
```typescript
import { api } from '$lib/api';

const templates = await api.listTemplates();
const agents = await api.listAgents();
```

## Build for Production

```bash
npm run build
```

This creates optimized production bundle in `build/` directory.

To preview production build:
```bash
npm run preview
```

## Current Features

### ✅ Completed
- Home page with templates
- Template cards with icons
- Stats dashboard
- Navigation layout
- API integration
- Loading states
- Error handling

### 🔄 Next Steps
- Agent list page
- Create agent wizard
- **Visual rule builder** 
- Agent detail/test page
- Code export functionality
