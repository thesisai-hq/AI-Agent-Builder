"""Example 3: RAG-powered agent analyzing SEC filings from PostgreSQL."""

import asyncio
import os
from agent_framework import (
    Agent, AgentConfig, RAGConfig, LLMConfig,
    Config, calculate_sentiment_score
)
from agent_framework.database import Database


class SECAnalystAgent(Agent):
    """SEC filing analyst using RAG for document analysis."""
    
    def __init__(self):
        """Initialize with RAG configuration."""
        config = AgentConfig(
            name="SEC Filing Analyst",
            description="Analyzes 10-K filings for investment insights",
            rag=RAGConfig(
                chunk_size=300,
                chunk_overlap=50,
                top_k=3
            ),
            llm=LLMConfig(
                provider='ollama',
                model='llama3.2',
                system_prompt="""You are an expert SEC filing analyst.
                
Extract key insights from 10-K filings:
- Financial performance trends
- Risk factors
- Strategic initiatives
- Competitive positioning

Provide clear, actionable analysis."""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> dict:
        """This method is not used for async RAG analysis."""
        raise NotImplementedError("Use analyze_async for RAG-powered analysis")
    
    async def analyze_async(self, ticker: str, filing_text: str) -> dict:
        """Analyze SEC filing using RAG (async version).
        
        Returns:
            Dict with direction, confidence, reasoning, and insights
        """
        if not filing_text:
            return {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': 'No SEC filing available',
                'insights': []
            }
        
        try:
            # Add filing to RAG system
            chunks_added = self.rag.add_document(filing_text)
            print(f"  📄 Processed {chunks_added} chunks from filing")
            
            # Query specific aspects
            queries = [
                "What are the key financial performance metrics?",
                "What are the main risk factors?",
                "What are the strategic initiatives and growth drivers?"
            ]
            
            insights = []
            for query in queries:
                context = self.rag.query(query)
                
                # Use LLM with RAG context
                try:
                    response = self.llm.chat(
                        message=f"Based on this SEC filing excerpt, answer: {query}",
                        context=context
                    )
                    insights.append(response)
                except Exception as e:
                    print(f"  ⚠️  LLM query failed: {e}")
                    insights.append(f"[LLM Error] Context: {context[:200]}...")
            
            # Synthesize signal using sentiment analysis
            full_analysis = "\n".join(insights)
            direction, confidence = calculate_sentiment_score(full_analysis)
            
            # Clear RAG for next analysis
            self.rag.clear()
            
            return {
                'direction': direction,
                'confidence': confidence,
                'reasoning': full_analysis[:300] + "...",
                'insights': insights
            }
        
        except Exception as e:
            print(f"  ❌ Analysis failed: {e}")
            return {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': f'Analysis error: {str(e)}',
                'insights': []
            }


class RiskAnalystAgent(Agent):
    """Focuses on risk factors from filings."""
    
    def __init__(self):
        config = AgentConfig(
            name="Risk Analyst",
            description="Identifies and assesses risk factors",
            rag=RAGConfig(chunk_size=400, top_k=5)
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> dict:
        """This method is not used for async RAG analysis."""
        raise NotImplementedError("Use analyze_async for RAG-powered analysis")
    
    async def analyze_async(self, ticker: str, filing_text: str) -> dict:
        """Extract and analyze risk factors (async version)."""
        if not filing_text:
            return {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': 'No filing data'
            }
        
        try:
            self.rag.add_document(filing_text)
            
            # Query risk-related content
            risk_context = self.rag.query(
                "What are the major risks, challenges, and concerns mentioned?"
            )
            
            # Count risk indicators
            risk_keywords = ['risk', 'uncertain', 'challenge', 'depend', 'may', 'could']
            risk_score = sum(keyword in risk_context.lower() for keyword in risk_keywords)
            
            if risk_score > 10:
                direction = 'bearish'
                confidence = 0.7
                reasoning = f"High risk exposure identified ({risk_score} risk indicators found)"
            elif risk_score > 5:
                direction = 'neutral'
                confidence = 0.6
                reasoning = f"Moderate risk profile ({risk_score} risk indicators)"
            else:
                direction = 'bullish'
                confidence = 0.6
                reasoning = f"Low risk profile ({risk_score} risk indicators)"
            
            self.rag.clear()
            
            return {
                'direction': direction,
                'confidence': confidence,
                'reasoning': reasoning
            }
        
        except Exception as e:
            print(f"  ❌ Risk analysis failed: {e}")
            return {
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': f'Analysis error: {str(e)}'
            }


async def main():
    """Demonstrate RAG-powered SEC filing analysis."""
    print("=" * 60)
    print("AI Agent Framework - RAG Example")
    print("SEC Filing Analysis with Document Retrieval")
    print("=" * 60)
    
    # Connect to database
    connection_string = Config.get_database_url()
    
    print("\n📌 Connecting to database...")
    db = Database(connection_string)
    
    try:
        await db.connect()
        print("✅ Connected!")
        
        # Initialize agents
        print("\n🤖 Initializing RAG agents...")
        sec_analyst = SECAnalystAgent()
        risk_analyst = RiskAnalystAgent()
        print("✅ Agents ready!")
        
        # Analyze filings
        for ticker in ['AAPL', 'TSLA']:
            data = await db.get_fundamentals(ticker)
            filing = await db.get_filing(ticker)
            
            if not data:
                print(f"\n⚠️  No data for {ticker}")
                continue
            
            print(f"\n{'='*60}")
            print(f"📄 Analyzing {ticker} - {data['name']} SEC 10-K Filing")
            print(f"{'='*60}")
            
            if not filing:
                print(f"⚠️  No SEC filing available for {ticker}")
                continue
            
            # SEC analyst
            print(f"\n📊 SEC Filing Analyst:")
            sec_result = await sec_analyst.analyze_async(ticker, filing)
            print(f"   {sec_result['direction'].upper()} ({sec_result['confidence']:.0%})")
            print(f"   {sec_result['reasoning']}")
            
            # Risk analyst
            print(f"\n⚠️  Risk Analyst:")
            risk_result = await risk_analyst.analyze_async(ticker, filing)
            print(f"   {risk_result['direction'].upper()} ({risk_result['confidence']:.0%})")
            print(f"   {risk_result['reasoning']}")
        
        print("\n" + "=" * 60)
        print("✅ RAG enables deep analysis of long documents!")
        print("=" * 60)
        print("\n💡 Note: For production with many documents, use a vector database")
        print("   like pgvector, Pinecone, or Weaviate for better performance.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
