# PDF Upload for RAG Agents - Complete Guide

## Overview

**NEW:** You can now test RAG agents by uploading PDF documents directly in the GUI!

Students can drag and drop PDFs containing:
- SEC 10-K filings
- Earnings call transcripts
- News articles
- Research reports
- Any financial documents

## How It Works

### Architecture

```
1. Student uploads PDF via drag-and-drop
   ↓
2. GUI extracts text using PyPDF2
   ↓
3. Text passed to RAG agent
   ↓
4. Agent:
   - Chunks the document
   - Creates embeddings
   - Retrieves relevant chunks
   - LLM synthesizes insights
   ↓
5. Results displayed with insights
```

### For Traditional Agents
- Input: Mock financial data (numbers)
- Method: `agent.analyze(ticker, data)`
- Output: Single signal

### For RAG Agents
- Input: PDF document (text)
- Method: `agent.analyze_async(ticker, document_text)`
- Output: Signal + detailed insights array

## Complete Workflow

### Creating a RAG Agent

**Step 1: In GUI → Create Agent**
```
Agent Name: SECAnalystAgent
Type: RAG-Powered
Provider: ollama
Temperature: 0.5
Max Tokens: 2000

RAG Config:
  Chunk Size: 300
  Chunk Overlap: 50
  Top K: 3

System Prompt:
  "You are an SEC filing analyst.
   Extract key insights:
   - Financial performance
   - Risk factors
   - Growth strategies"
```

**Step 2: Generate → Save**

File saved to: `examples/sec_analyst_agent.py`

### Testing the RAG Agent

**Step 1: In GUI → Test Agent**
```
Select Agent: SECAnalystAgent
Ticker: AAPL
```

**Step 2: Upload PDF**
- Drag and drop SEC filing PDF
- Preview shows first 3 pages
- Full document will be analyzed

**Step 3: Run Analysis**
- Click "🚀 Run Analysis"
- Wait for processing (10-30 seconds for large docs)

**Step 4: View Results**
```
Signal: 🟢 BULLISH
Confidence: 75%
Reasoning: Strong revenue growth and positive outlook...

Detailed Insights:
  Insight 1: Financial performance shows 15% YoY growth...
  Insight 2: Main risks include supply chain challenges...
  Insight 3: Expansion into AI-powered services...
```

## Sample PDFs for Testing

### Where to Get Test Documents

**SEC EDGAR (Free):**
- Go to: https://www.sec.gov/edgar/searchedgar/companysearch
- Search company (e.g., "Apple")
- Download 10-K filing as PDF

**Example URLs:**
- Apple 10-K: Search "AAPL" on SEC.gov
- Tesla 10-K: Search "TSLA" on SEC.gov
- Microsoft 10-K: Search "MSFT" on SEC.gov

**Test with Sample Text:**
If you don't have a PDF, create a simple .txt file and upload:
```
Apple Inc. Annual Report 2024

Financial Performance:
- Revenue increased 15% year-over-year to $400B
- Net income grew to $95B, up 12%
- Services revenue reached record $85B

Risk Factors:
- Supply chain dependencies in Asia
- Intense competition in smartphone market
- Regulatory challenges in multiple jurisdictions

Growth Strategies:
- Expansion of AI capabilities across product line
- Investment in augmented reality platforms
- Growing services ecosystem
```

Save as `sample_filing.txt`, but note: **GUI currently only accepts PDF** - see workaround below.

## Technical Details

### PDF Text Extraction

```python
# In agent_tester.py
from PyPDF2 import PdfReader

# Extract all pages
pdf_reader = PdfReader(uploaded_file)
document_text = ""

for page in pdf_reader.pages:
    document_text += page.extract_text() + "\n"

# Pass to RAG agent
result = await agent.analyze_async(ticker, document_text)
```

### RAG Processing

```python
# Inside RAG agent (auto-generated)
# 1. Chunk document
chunks = self.rag.add_document(document_text)

# 2. Query for insights
context = self.rag.query("What are the key financial metrics?")

# 3. LLM synthesis
response = self.llm.chat(
    message="Based on this filing, answer: ...",
    context=context  # Retrieved relevant chunks
)

# 4. Return structured insights
return {
    'direction': 'bullish',
    'confidence': 0.75,
    'reasoning': '...',
    'insights': [insight1, insight2, insight3]
}
```

### Async Execution

RAG agents use `async/await` because:
- Document processing is I/O heavy
- LLM calls are async
- Better performance for large documents

## Dependencies

### Required for RAG Testing

```bash
# Core framework
pip install -e .

# GUI with PDF support
pip install streamlit pypdf2

# LLM provider
pip install ollama  # or openai, anthropic

# RAG embeddings
pip install sentence-transformers

# All-in-one
pip install 'ai-agent-framework[llm,rag]' streamlit pypdf2
```

### Check What's Installed

```bash
# Check LLM providers
python3 gui/check_llm_deps.py

# Check PDF support
python3 -c "import PyPDF2; print('PyPDF2 installed')"

# Check RAG support
python3 -c "from sentence_transformers import SentenceTransformer; print('RAG installed')"
```

## File Formats

### Currently Supported
✅ **PDF** - Full support with drag-and-drop

### Future Support (Not Yet)
- ❌ .txt files
- ❌ .docx files
- ❌ .html files
- ❌ Multiple files at once

### Workaround for .txt Files

Convert to PDF:
```bash
# Linux/Mac
enscript -p - my_file.txt | ps2pdf - my_file.pdf

# Or use online converter
# https://www.adobe.com/acrobat/online/txt-to-pdf.html
```

## UI Components Added

### In Test Page

**For RAG Agents:**
- File uploader widget (drag-and-drop)
- PDF preview (first 3 pages)
- Page count display
- File size indicator
- Insights expandable sections

**For Traditional Agents:**
- Mock data inputs (unchanged)
- Same as before

### Auto-Detection

GUI automatically detects agent type:
- Checks for `RAGConfig` in code
- Shows PDF upload for RAG agents
- Shows mock data for other agents

## Error Handling

### Common Issues

**"No module named 'PyPDF2'"**
```bash
pip install pypdf2
```

**"No text extracted from PDF"**
- PDF may be scanned image (OCR needed)
- Try different PDF with selectable text
- Check PDF preview - if blank, text extraction failed

**"RAG agent requires PDF"**
- You clicked Run without uploading PDF
- Upload a document first

**"ImportError: sentence-transformers"**
```bash
pip install sentence-transformers
```

## Performance

### Expected Processing Times

| Document Size | Pages | Time |
|--------------|-------|------|
| Small | 1-10 | 5-10s |
| Medium | 10-50 | 15-30s |
| Large | 50-100 | 30-60s |
| Very Large | 100+ | 60s+ |

**Why it takes time:**
1. PDF text extraction (1-2s per 10 pages)
2. Document chunking (1-2s)
3. Embedding generation (2-5s per chunk batch)
4. Vector search (1s)
5. LLM synthesis (5-20s depending on provider)

### Optimization Tips

- Use smaller chunk sizes for faster processing
- Reduce Top K to retrieve fewer chunks
- Use faster LLM provider (OpenAI > Anthropic > Ollama)
- Upload smaller PDFs (first 50 pages often sufficient)

## Integration with thesis-ai

### Using GUI-Created RAG Agents

```python
# In thesis-ai/server/multi_agent_system/advisor/orchestrator.py
from ....AI-Agent-Builder.examples.sec_analyst_agent import SECAnalystAgent

class Orchestrator:
    def __init__(self):
        self.rag_agent = SECAnalystAgent()
    
    async def analyze_with_documents(self, ticker):
        # Get SEC filing from your database
        filing_text = await self.db.get_filing(ticker)
        
        # Analyze with RAG
        result = await self.rag_agent.analyze_async(ticker, filing_text)
        
        return {
            'direction': result['direction'],
            'confidence': result['confidence'],
            'reasoning': result['reasoning'],
            'insights': result['insights']
        }
```

### Document Sources in Production

```python
# Option 1: From your PostgreSQL database
filing = await db.get_filing(ticker)

# Option 2: From SEC Edgar API
import requests
url = f"https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={acc}"
response = requests.get(url)
filing_text = response.text

# Option 3: From file storage
with open(f'filings/{ticker}_10K.txt') as f:
    filing_text = f.read()

# Then pass to RAG agent
result = await rag_agent.analyze_async(ticker, filing_text)
```

## Files Changed

1. ✅ `gui/app.py` - Added PDF upload UI and RAG-specific testing
2. ✅ `gui/agent_tester.py` - Added PDF extraction and async RAG testing
3. ✅ `gui/requirements.txt` - Added pypdf2 dependency
4. ✅ `gui/setup.sh` - Auto-install pypdf2
5. ✅ `GUI_QUICK_START.md` - Documented PDF upload workflow

## Summary

**What students can now do:**
1. ✅ Create RAG agents in GUI
2. ✅ Upload PDF documents
3. ✅ Test RAG agents immediately
4. ✅ See detailed insights
5. ✅ No coding required!

**What you need:**
```bash
# Install dependencies
pip install 'ai-agent-framework[llm,rag]' streamlit pypdf2

# Launch GUI
./gui/launch.sh

# Create RAG agent → Upload PDF → Test!
```

---

**Status:** Implemented ✅  
**Version:** 1.2.0  
**Date:** 2025-01-23
