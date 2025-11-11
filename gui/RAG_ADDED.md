# RAG Support Added to GUI

## Summary

RAG (Retrieval Augmented Generation) agent support has been added to the Agent Builder GUI. You can now create agents that analyze documents using vector-based retrieval.

## What is RAG?

**RAG = Retrieval Augmented Generation**

Instead of analyzing just numbers (like PE ratio), RAG agents analyze text documents:
- SEC 10-K filings
- Earnings call transcripts
- News articles
- Research reports

**How it works:**
1. Splits documents into chunks (e.g., 300 words)
2. Creates vector embeddings of each chunk
3. Retrieves most relevant chunks for a query
4. Uses LLM to synthesize insights from retrieved content

## New Features in GUI

### 1. RAG-Powered Agent Type

Now available in "Create Agent":
- Rule-Based
- LLM-Powered
- Hybrid
- **RAG-Powered** ← NEW

### 2. RAG Configuration Options

When creating RAG agents:
- **Chunk Size** (100-1000): How much text per chunk (default: 300)
- **Chunk Overlap** (0-200): Overlap between chunks (default: 50)
- **Top K** (1-10): Number of chunks to retrieve (default: 3)

### 3. Generated Code

Creates complete async RAG agents with:
- Document processing
- Vector search
- LLM synthesis
- Error handling

## Example Usage

### Create RAG Agent in GUI

1. **Navigate:** ➕ Create Agent

2. **Configure:**
   ```
   Agent Name: SECAnalystAgent
   Description: Analyzes SEC 10-K filings for insights
   Type: RAG-Powered
   
   LLM Configuration:
   - Provider: ollama
   - Temperature: 0.5
   - Max Tokens: 2000
   - System Prompt: "You are an SEC filing expert..."
   
   RAG Configuration:
   - Chunk Size: 300
   - Chunk Overlap: 50
   - Top K: 3
   ```

3. **Generate → Save**

### Use the Generated Agent

```python
import asyncio
from examples.sec_analyst_agent import SECAnalystAgent

async def main():
    agent = SECAnalystAgent()
    
    # Analyze a document
    filing_text = """... SEC 10-K filing text ..."""
    
    result = await agent.analyze_async('AAPL', filing_text)
    
    print(f"{result['direction']}: {result['reasoning']}")
    for insight in result['insights']:
        print(f"- {insight}")

asyncio.run(main())
```

## Dependencies

### Installing RAG Dependencies

```bash
# Option 1: Install both LLM and RAG
pip install 'ai-agent-framework[llm,rag]'

# Option 2: Install separately
pip install ollama sentence-transformers

# Check what's installed
python3 gui/check_llm_deps.py
```

### What Gets Installed

- **LLM packages:** openai, anthropic, or ollama
- **RAG packages:** sentence-transformers (for embeddings)

## Agent Types Summary

| Type | Use Case | Input | Output | Dependencies |
|------|----------|-------|--------|--------------|
| Rule-Based | Value screening | Financial metrics | Signal | None |
| LLM-Powered | General analysis | Financial data | Signal | LLM |
| Hybrid | Smart screening | Financial data | Signal | LLM |
| **RAG-Powered** | **Document analysis** | **Text documents** | **Dict with insights** | **LLM + RAG** |

## Key Differences

### Traditional Agents
```python
# Input: Financial data dict
signal = agent.analyze('AAPL', {
    'pe_ratio': 20.0,
    'revenue_growth': 15.0
})

# Output: Signal
# direction: 'bullish'
# confidence: 0.8
# reasoning: "Undervalued at PE=20"
```

### RAG Agents
```python
# Input: Text document
result = await agent.analyze_async('AAPL', filing_text)

# Output: Dict with insights
# direction: 'bullish'
# confidence: 0.7
# reasoning: "Strong growth prospects based on filing analysis"
# insights: [
#   "Revenue increased 15% YoY...",
#   "Main risks include supply chain...",
#   "Expansion into new markets..."
# ]
```

## Use Cases

### Rule-Based Agent
```
Best for: "Buy if PE < 15"
Input: Numbers
Speed: Very fast
```

### LLM-Powered Agent
```
Best for: "Analyze this company's fundamentals"
Input: Numbers
Speed: Slow (API call)
```

### RAG-Powered Agent
```
Best for: "What does the CEO say about growth?"
Input: Document text
Speed: Slow (embedding + API)
```

## Integration with thesis-ai

RAG agents work great with thesis-ai's sentiment analysis:

```python
# In thesis-ai orchestrator
from AI-Agent-Builder.examples.sec_analyst_agent import SECAnalystAgent

class Orchestrator:
    def __init__(self):
        self.rag_agent = SECAnalystAgent()
    
    async def analyze_with_rag(self, ticker):
        # Get SEC filing from database
        filing = await db.get_filing(ticker)
        
        # Analyze with RAG
        result = await self.rag_agent.analyze_async(ticker, filing)
        
        return result
```

## Files Changed

1. ✅ `gui/app.py` - Added RAG-Powered option and configuration
2. ✅ `gui/agent_creator.py` - Added `_generate_rag_agent()` method
3. ✅ `gui/agent_loader.py` - Detects RAG agents
4. ✅ `gui/README.md` - Documented RAG support

## Testing

### Check RAG Dependencies

```bash
# Check what's installed
python3 gui/check_llm_deps.py

# Install RAG dependencies
pip install sentence-transformers
```

### Create Test RAG Agent

1. Launch GUI: `./gui/launch.sh`
2. Create Agent → RAG-Powered
3. Generate and save
4. Test with sample document

## Notes

- RAG agents use `analyze_async()` instead of `analyze()`
- They return a dict with `insights` array
- Require async/await in calling code
- Best for text-heavy analysis
- Complement traditional fundamental/technical agents

---

**Status:** Implemented ✅  
**Version:** 1.1.0  
**Date:** 2025-01-23
