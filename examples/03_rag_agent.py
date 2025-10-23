"""Example 3: RAG-powered agent analyzing SEC filings."""

from agent_framework import Agent, Signal, AgentConfig, RAGConfig, LLMConfig, MockDatabase


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
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze SEC filing using RAG."""
        # Get SEC filing from database
        from agent_framework import MockDatabase
        db = MockDatabase()
        filing_text = db.get_filing(ticker)
        
        if not filing_text:
            return Signal('neutral', 0.3, 'No SEC filing available')
        
        # Add filing to RAG system
        self.rag.add_document(filing_text)
        
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
            response = self.llm.chat(
                message=f"Based on this SEC filing excerpt, answer: {query}",
                context=context
            )
            insights.append(response)
        
        # Synthesize signal
        full_analysis = "\n".join(insights)
        
        # Simple sentiment based on keywords
        positive_words = ['growth', 'strong', 'improved', 'increase', 'expansion']
        negative_words = ['risk', 'decline', 'challenge', 'decrease', 'competition']
        
        pos_count = sum(word in full_analysis.lower() for word in positive_words)
        neg_count = sum(word in full_analysis.lower() for word in negative_words)
        
        if pos_count > neg_count + 2:
            direction = 'bullish'
            confidence = min(0.8, 0.5 + (pos_count - neg_count) * 0.05)
        elif neg_count > pos_count + 2:
            direction = 'bearish'
            confidence = min(0.7, 0.5 + (neg_count - pos_count) * 0.05)
        else:
            direction = 'neutral'
            confidence = 0.6
        
        # Clear RAG for next analysis
        self.rag.clear()
        
        return Signal(
            direction=direction,
            confidence=confidence,
            reasoning=full_analysis[:300] + "...",
            metadata={'insights': insights}
        )


class RiskAnalystAgent(Agent):
    """Focuses on risk factors from filings."""
    
    def __init__(self):
        config = AgentConfig(
            name="Risk Analyst",
            description="Identifies and assesses risk factors",
            rag=RAGConfig(chunk_size=400, top_k=5)
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Extract and analyze risk factors."""
        from agent_framework import MockDatabase
        db = MockDatabase()
        filing = db.get_filing(ticker)
        
        if not filing:
            return Signal('neutral', 0.3, 'No filing data')
        
        self.rag.add_document(filing)
        
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
        
        return Signal(direction, confidence, reasoning)


def main():
    """Demonstrate RAG-powered SEC filing analysis."""
    print("=" * 60)
    print("AI Agent Framework - RAG Example")
    print("SEC Filing Analysis with Document Retrieval")
    print("=" * 60)
    
    # Initialize
    db = MockDatabase()
    sec_analyst = SECAnalystAgent()
    risk_analyst = RiskAnalystAgent()
    
    # Analyze filings
    for ticker in ['AAPL', 'TSLA']:
        data = db.get_fundamentals(ticker)
        
        print(f"\n{'='*60}")
        print(f"📄 Analyzing {ticker} - {data['name']} SEC 10-K Filing")
        print(f"{'='*60}")
        
        # SEC analyst
        print(f"\n📊 SEC Filing Analyst:")
        sec_signal = sec_analyst.analyze(ticker, data)
        print(f"   {sec_signal.direction.upper()} ({sec_signal.confidence:.0%})")
        print(f"   {sec_signal.reasoning}")
        
        # Risk analyst
        print(f"\n⚠️  Risk Analyst:")
        risk_signal = risk_analyst.analyze(ticker, data)
        print(f"   {risk_signal.direction.upper()} ({risk_signal.confidence:.0%})")
        print(f"   {risk_signal.reasoning}")
    
    print("\n" + "=" * 60)
    print("✅ RAG enables deep analysis of long documents!")
    print("=" * 60)


if __name__ == "__main__":
    main()