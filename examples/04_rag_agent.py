"""Example 4: RAG-Powered Agent for Document Analysis

This example demonstrates document analysis with AI:
- Retrieval Augmented Generation (RAG) for long documents
- Semantic search through document chunks
- LLM synthesis of relevant information
- Perfect for SEC filings, earnings reports, news articles

Learning Focus:
- RAG system for document processing
- Vector embeddings and semantic search
- Combining retrieval with LLM reasoning
- Analyzing unstructured text data

⚠️ DISCLAIMER: This is educational code for learning purposes only.
Do NOT use for real trading. Not financial advice. See DISCLAIMER.md for full terms.

DEPENDENCIES:
This example requires both LLM and RAG dependencies. Install with:
  pip install 'ai-agent-framework[llm,rag]'

Or install separately:
  pip install ollama sentence-transformers

Then download the model:
  ollama pull llama3.2
"""

import asyncio
from agent_framework import (
    Agent, AgentConfig, RAGConfig, LLMConfig,
    Database, Config, calculate_sentiment_score
)


class SECFilingAnalyst(Agent):
    """RAG-powered analyst for SEC filings and financial documents.
    
    Strategy: Analyzes long documents (10-K filings, earnings reports) using:
    1. Document chunking (break into smaller pieces)
    2. Vector embeddings (convert text to numbers)
    3. Semantic search (find relevant sections)
    4. LLM synthesis (analyze and summarize)
    
    Configuration:
    - Provider: Ollama (free, local, private)
    - Model: llama3.2 (latest Llama)
    - RAG chunk_size: 300 (characters per chunk)
    - RAG chunk_overlap: 50 (overlap between chunks)
    - RAG top_k: 3 (retrieve top 3 most relevant chunks)
    - Temperature: 0.5 (balanced analysis)
    - Max Tokens: 2000 (detailed responses)
    
    Why RAG?
    - SEC filings are 50+ pages (too long for LLM context)
    - RAG finds relevant sections automatically
    - More accurate than reading entire document
    - Faster and more cost-effective
    """
    
    def __init__(self):
        """Initialize RAG agent with full configuration."""
        config = AgentConfig(
            name="SEC Filing Analyst",
            description="Analyzes SEC filings and financial documents using RAG",
            rag=RAGConfig(
                chunk_size=300,          # Characters per chunk
                chunk_overlap=50,        # Overlap prevents cutting mid-sentence
                top_k=3                  # Retrieve 3 most relevant chunks
            ),
            llm=LLMConfig(
                provider='ollama',
                model='llama3.2',
                temperature=0.5,         # Balanced for factual analysis
                max_tokens=2000,         # Detailed responses
                system_prompt="""You are an expert SEC filing analyst with 20 years of experience.

Your expertise:
- Reading and interpreting 10-K, 10-Q filings
- Identifying key financial trends
- Spotting risk factors and red flags
- Evaluating management strategy
- Assessing competitive positioning

When analyzing document excerpts:
1. Focus on factual information from the filing
2. Identify specific numbers, metrics, and trends
3. Highlight both opportunities and risks
4. Be precise and cite specific details
5. Provide actionable investment insights

Be thorough but concise. Extract what matters most for investment decisions."""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> dict:
        """Not used - RAG agents use analyze_async for async document processing."""
        raise NotImplementedError(
            "RAG agents must use analyze_async() for document analysis. "
            "Call: result = await agent.analyze_async(ticker, document_text)"
        )
    
    async def analyze_async(self, ticker: str, document_text: str) -> dict:
        """Analyze financial document using RAG + LLM.
        
        Process:
        1. Chunk document into 300-character pieces
        2. Create vector embeddings for semantic search
        3. Query for specific insights (performance, risks, strategy)
        4. Use LLM to synthesize findings
        5. Generate investment signal
        
        Args:
            ticker: Stock ticker symbol
            document_text: Full document text (10-K filing, news, etc.)
            
        Returns:
            Dict with direction, confidence, reasoning, and detailed insights
        """
        if not document_text or len(document_text) < 100:
            return {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': 'Document too short or empty for RAG analysis',
                'insights': []
            }
        
        try:
            # STEP 1: Add document to RAG system (chunking + embedding)
            chunks_added = self.rag.add_document(document_text)
            print(f"  📄 Processed {chunks_added} chunks ({len(document_text):,} characters)")
            
            # STEP 2: Query specific aspects of the filing
            queries = [
                "What are the key financial performance metrics and trends?",
                "What are the main risk factors and challenges mentioned?",
                "What are the strategic initiatives and growth opportunities?"
            ]
            
            insights = []
            for i, query in enumerate(queries, 1):
                print(f"  🔍 Query {i}/{len(queries)}: {query[:50]}...")
                
                # STEP 3: Retrieve relevant chunks
                context = self.rag.query(query)
                
                # STEP 4: Use LLM to analyze retrieved context
                try:
                    response = self.llm.chat(
                        message=f"Based on the following excerpt from the SEC filing, answer: {query}",
                        context=context
                    )
                    insights.append(response)
                    print(f"  ✓ Generated insight ({len(response)} chars)")
                except Exception as e:
                    print(f"  ⚠️  LLM query failed: {e}")
                    # Fallback: Use the raw context
                    insights.append(f"[Context excerpt] {context[:300]}...")
            
            # STEP 5: Synthesize overall signal
            full_analysis = "\n\n".join(insights)
            direction, confidence = calculate_sentiment_score(full_analysis)
            
            # Clear RAG system for next document
            self.rag.clear()
            
            return {
                'direction': direction,
                'confidence': confidence,
                'reasoning': full_analysis[:400] + "..." if len(full_analysis) > 400 else full_analysis,
                'insights': insights
            }
        
        except Exception as e:
            print(f"  ❌ RAG analysis failed: {e}")
            return {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': f'RAG analysis error: {str(e)}',
                'insights': []
            }


async def main():
    """Example usage of RAG-powered agent."""
    print("=" * 70)
    print("Example 4: RAG-Powered Agent (Document Analysis)")
    print("=" * 70)
    print("\n📚 Learning: Analyze long documents with retrieval + AI")
    print("⚡ Speed: Slower (document processing + LLM)")
    print("💰 Cost: Free with Ollama, or API costs with OpenAI/Anthropic")
    print("📄 Use Case: SEC filings, earnings reports, news articles")
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    
    # Check LLM
    try:
        import ollama
        print("✅ Ollama package installed")
    except ImportError:
        print("❌ Ollama not installed. Run: pip install ollama")
        return
    
    # Check RAG (sentence-transformers)
    try:
        import sentence_transformers
        print("✅ sentence-transformers installed (for embeddings)")
    except ImportError:
        print("❌ sentence-transformers not installed")
        print("   Install with: pip install sentence-transformers")
        print("   Or: pip install 'ai-agent-framework[llm,rag]'")
        return
    
    # Connect to database
    connection_string = Config.get_database_url()
    
    print("\n📌 Connecting to database...")
    db = Database(connection_string)
    
    try:
        await db.connect()
        print("✅ Connected!")
        
        # Create agent
        print("\n🤖 Initializing RAG-Powered Agent...")
        agent = SECFilingAnalyst()
        print("   Provider: Ollama (llama3.2)")
        print("   RAG Config: chunk_size=300, chunk_overlap=50, top_k=3")
        print("   Purpose: Extract insights from SEC filings")
        
        # Analyze SEC filings
        for ticker in ['AAPL', 'TSLA', 'JPM']:
            print(f"\n{'='*70}")
            
            # Get fundamental data and filing
            data = await db.get_fundamentals(ticker)
            filing = await db.get_filing(ticker)
            
            if not data:
                print(f"⚠️  No data for {ticker}")
                continue
            
            if not filing:
                print(f"⚠️  No SEC filing for {ticker}")
                continue
            
            # Show company info
            print(f"📊 {ticker} - {data['name']}")
            print(f"   Sector: {data['sector']}")
            print(f"   Filing Length: {len(filing):,} characters")
            
            # Run RAG analysis
            print(f"\n🧠 Analyzing SEC filing with RAG...")
            result = await agent.analyze_async(ticker, filing)
            
            # Display result
            emoji = {'bullish': '🟢', 'bearish': '🔴', 'neutral': '🟡'}[result['direction']]
            print(f"\n   {emoji} {result['direction'].upper()} ({result['confidence']:.0%})")
            print(f"\n   Overall Assessment:")
            print(f"   {result['reasoning']}")
            
            # Show detailed insights
            if result.get('insights'):
                print(f"\n   📝 Detailed Insights:")
                for i, insight in enumerate(result['insights'], 1):
                    print(f"\n   {i}. {insight[:200]}...")
        
        print("\n" + "=" * 70)
        print("✅ Example completed!")
        print("\n💡 Key Takeaways:")
        print("   • RAG enables analysis of long documents (50+ pages)")
        print("   • Semantic search finds relevant sections automatically")
        print("   • More accurate than reading entire document")
        print("   • Combines information retrieval with AI reasoning")
        print("   • Perfect for SEC filings, research reports, news")
        print("\n🎯 RAG Process:")
        print("   1. Chunk document into small pieces")
        print("   2. Create vector embeddings (semantic meaning)")
        print("   3. Query for specific information")
        print("   4. Retrieve most relevant chunks")
        print("   5. LLM synthesizes insights from chunks")
        print("\n⚙️  Configuration Options:")
        print("   • chunk_size: Larger = more context, slower")
        print("   • chunk_overlap: Prevents cutting mid-sentence")
        print("   • top_k: More chunks = more context, slower")
        print("\n📖 Next Steps:")
        print("   • Try with your own PDFs (upload in GUI)")
        print("   • Experiment with chunk_size and top_k")
        print("   • Compare to reading entire document")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
