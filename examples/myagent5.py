"""Auto-generated RAG-powered agent: MyAgent5



DEPENDENCIES:
This agent requires LLM + RAG dependencies. Install with:
  pip install 'ai-agent-framework[llm,rag]'

Or install separately:
  pip install ollama sentence-transformers

To check installed providers:
  python3 gui/check_llm_deps.py
"""

import asyncio
from agent_framework import (
    Agent, AgentConfig, LLMConfig, RAGConfig,
    Database, Config, calculate_sentiment_score
)


class MyAgent5(Agent):
    """
    
    Uses RAG (Retrieval Augmented Generation) to analyze documents.
    """
    
    def __init__(self):
        """Initialize agent with RAG and LLM configuration."""
        config = AgentConfig(
            name="MyAgent5",
            description="",
            rag=RAGConfig(
                chunk_size=300,
                chunk_overlap=50,
                top_k=3
            ),
            llm=LLMConfig(
                provider='ollama',
                model='llama3.2',
                temperature=0.5,
                max_tokens=1000,
                system_prompt="""You are a financial document analyst."""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict):
        """Not used - RAG agents use analyze_async."""
        raise NotImplementedError("Use analyze_async for RAG-powered analysis")
    
    async def analyze_async(self, ticker: str, document_text: str) -> dict:
        """Analyze document using RAG.
        
        Args:
            ticker: Stock ticker symbol
            document_text: Document to analyze (SEC filing, news, etc.)
            
        Returns:
            Dict with direction, confidence, reasoning, and insights
        """
        if not document_text:
            return {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': 'No document text provided',
                'insights': []
            }
        
        try:
            # Add document to RAG system
            chunks_added = self.rag.add_document(document_text)
            print(f"  📄 Processed {chunks_added} chunks")
            
            # Query key aspects
            queries = [
                "What are the key financial metrics and performance?",
                "What are the main risks or challenges?",
                "What are the growth opportunities and strategies?"
            ]
            
            insights = []
            for query in queries:
                # Retrieve relevant context
                context = self.rag.query(query)
                
                # Use LLM with context
                try:
                    response = self.llm.chat(
                        message=f"Based on the document, answer: {query}",
                        context=context
                    )
                    insights.append(response)
                except Exception as e:
                    print(f"  ⚠️  LLM query failed: {e}")
                    insights.append(f"[Error] {context[:200]}...")
            
            # Synthesize signal from insights
            full_analysis = "\n".join(insights)
            direction, confidence = calculate_sentiment_score(full_analysis)
            
            # Clear RAG for next document
            self.rag.clear()
            
            return {
                'direction': direction,
                'confidence': confidence,
                'reasoning': full_analysis[:300] + "...",
                'insights': insights
            }
        
        except Exception as e:
            print(f"  ❌ RAG analysis failed: {e}")
            return {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': f'Analysis error: {str(e)}',
                'insights': []
            }


async def main():
    """Example usage of RAG agent."""
    print(f"{'=' * 60}")
    print(f"MyAgent5 - RAG-Powered Document Analysis")
    print(f"{'=' * 60}\n")
    
    # Connect to database
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        # Create agent
        agent = MyAgent5()
        
        # Analyze SEC filings or news
        for ticker in ['AAPL', 'TSLA']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {ticker}")
                continue
            
            # Get SEC filing or news text
            filing = await db.get_filing(ticker)
            
            if not filing:
                print(f"⚠️  No filing for {ticker}")
                continue
            
            print(f"\n📊 Analyzing {ticker} filing...")
            result = await agent.analyze_async(ticker, filing)
            
            print(f"{result['direction'].upper()} ({result['confidence']:.0%})")
            print(f"{result['reasoning']}\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
