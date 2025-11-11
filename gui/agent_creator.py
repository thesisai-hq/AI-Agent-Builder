"""Agent Creator - Generate agent code from templates"""

from typing import List, Dict, Optional


class AgentCreator:
    """Generates agent code from user specifications."""
    
    def generate_agent_code(
        self,
        agent_name: str,
        description: str,
        agent_type: str,
        rules: Optional[List[Dict]] = None,
        llm_provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        top_k: Optional[int] = None
    ) -> str:
        """Generate complete agent code.
        
        Args:
            agent_name: Agent class name
            description: Agent description
            agent_type: Type of agent (Rule-Based, LLM-Powered, Hybrid)
            rules: List of rules for rule-based logic
            llm_provider: LLM provider (openai, anthropic, ollama)
            temperature: LLM temperature
            max_tokens: LLM max tokens
            system_prompt: LLM system prompt
            
        Returns:
            Complete Python code for the agent
        """
        if agent_type == "Rule-Based":
            return self._generate_rule_based_agent(agent_name, description, rules)
        elif agent_type == "LLM-Powered":
            return self._generate_llm_agent(
                agent_name, description, llm_provider,
                temperature, max_tokens, system_prompt
            )
        elif agent_type == "RAG-Powered":
            return self._generate_rag_agent(
                agent_name, description, llm_provider,
                temperature, max_tokens, system_prompt,
                chunk_size, chunk_overlap, top_k
            )
        else:  # Hybrid
            return self._generate_hybrid_agent(
                agent_name, description, rules, llm_provider,
                temperature, max_tokens, system_prompt
            )
    
    def _generate_rule_based_agent(
        self,
        agent_name: str,
        description: str,
        rules: List[Dict]
    ) -> str:
        """Generate rule-based agent code."""
        
        # Generate rule logic
        rule_conditions = []
        for i, rule in enumerate(rules or []):
            metric = rule['metric']
            operator = rule['operator']
            threshold = rule['threshold']
            direction = rule['direction']
            confidence = rule['confidence']
            
            rule_conditions.append(f"""
        if data.get('{metric}', 0) {operator} {threshold}:
            return Signal(
                direction='{direction}',
                confidence={confidence},
                reasoning=f"{metric.replace('_', ' ').title()} {{{metric}:.1f}} is {direction}"
            )""")
        
        rules_code = "".join(rule_conditions)
        
        return f'''"""Auto-generated agent: {agent_name}

{description}
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config


class {agent_name}(Agent):
    """{description}"""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze based on defined rules.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Extract metrics from data
        {self._generate_metric_extraction(rules)}
        
        # Apply rules{rules_code}
        
        # Default fallback
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No rules matched'
        )


async def main():
    """Example usage of the agent."""
    print(f"{{'-' * 60}}")
    print(f"{agent_name} - Example Usage")
    print(f"{{'-' * 60}}\\n")
    
    # Connect to database
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        # Create agent
        agent = {agent_name}()
        
        # Analyze a few tickers
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            signal = agent.analyze(ticker, data)
            
            print(f"📊 {{ticker}}: {{signal.direction.upper()}} "
                  f"({{signal.confidence:.0%}})")
            print(f"   {{signal.reasoning}}\\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_llm_agent(
        self,
        agent_name: str,
        description: str,
        llm_provider: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str
    ) -> str:
        """Generate LLM-powered agent code."""
        
        return f'''"""Auto-generated LLM-powered agent: {agent_name}

{description}

DEPENDENCIES:
This agent requires LLM dependencies. Install with:
  pip install 'ai-agent-framework[llm]'

Or install specific provider:
  pip install {llm_provider}

To check which providers are installed:
  python3 gui/check_llm_deps.py
"""

import asyncio
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig,
    Database, Config, parse_llm_signal, format_fundamentals
)


class {agent_name}(Agent):
    """{description}"""
    
    def __init__(self):
        """Initialize agent with LLM configuration."""
        config = AgentConfig(
            name="{agent_name}",
            description="{description}",
            llm=LLMConfig(
                provider='{llm_provider}',
                temperature={temperature},
                max_tokens={max_tokens},
                system_prompt="""{system_prompt or 'You are a financial analyst.'}"""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using LLM with configured personality.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Format fundamentals for LLM
        fundamentals_text = format_fundamentals(data)
        
        # Build prompt
        prompt = f"""Analyze {{ticker}} with the following data:

{{fundamentals_text}}

Provide your investment recommendation.
Format: DIRECTION|CONFIDENCE|REASONING
Example: bullish|75|Strong growth with healthy margins"""
        
        try:
            # Query LLM
            response = self.llm.chat(prompt)
            return parse_llm_signal(response, f"Analysis of {{ticker}}")
        
        except Exception as e:
            print(f"⚠️  LLM error: {{e}}")
            # Fallback to simple rule
            pe = data.get('pe_ratio', 0)
            growth = data.get('revenue_growth', 0)
            
            if pe < 20 and growth > 10:
                return Signal(
                    direction='bullish',
                    confidence=0.6,
                    reasoning=f'LLM unavailable ({{type(e).__name__}}), using fallback: PE={{pe:.1f}}, Growth={{growth:.1f}}%'
                )
            elif pe > 30:
                return Signal(
                    direction='bearish',
                    confidence=0.5,
                    reasoning=f'LLM unavailable ({{type(e).__name__}}), using fallback: High PE={{pe:.1f}}'
                )
            return Signal(
                direction='neutral',
                confidence=0.4,
                reasoning=f'LLM unavailable ({{type(e).__name__}}), insufficient data for fallback'
            )


async def main():
    """Example usage of the LLM-powered agent."""
    print(f"{{'-' * 60}}")
    print(f"{agent_name} - LLM-Powered Analysis")
    print(f"{{'-' * 60}}\\n")
    
    # Connect to database
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        # Create agent
        agent = {agent_name}()
        
        # Analyze tickers
        for ticker in ['AAPL', 'TSLA']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            print(f"📊 Analyzing {{ticker}}...")
            signal = agent.analyze(ticker, data)
            
            print(f"{{signal.direction.upper()}} ({{signal.confidence:.0%}})")
            print(f"{{signal.reasoning}}\\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_rag_agent(
        self,
        agent_name: str,
        description: str,
        llm_provider: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str,
        chunk_size: int,
        chunk_overlap: int,
        top_k: int
    ) -> str:
        """Generate RAG-powered agent code."""
        
        return f'''"""Auto-generated RAG-powered agent: {agent_name}

{description}

DEPENDENCIES:
This agent requires LLM + RAG dependencies. Install with:
  pip install 'ai-agent-framework[llm,rag]'

Or install separately:
  pip install {llm_provider} sentence-transformers

To check installed providers:
  python3 gui/check_llm_deps.py
"""

import asyncio
from agent_framework import (
    Agent, AgentConfig, LLMConfig, RAGConfig,
    Database, Config, calculate_sentiment_score
)


class {agent_name}(Agent):
    """{description}
    
    Uses RAG (Retrieval Augmented Generation) to analyze documents.
    """
    
    def __init__(self):
        """Initialize agent with RAG and LLM configuration."""
        config = AgentConfig(
            name="{agent_name}",
            description="{description}",
            rag=RAGConfig(
                chunk_size={chunk_size},
                chunk_overlap={chunk_overlap},
                top_k={top_k}
            ),
            llm=LLMConfig(
                provider='{llm_provider}',
                temperature={temperature},
                max_tokens={max_tokens},
                system_prompt="""{system_prompt or 'You are a financial document analyst.'}"""
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
            return {{
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': 'No document text provided',
                'insights': []
            }}
        
        try:
            # Add document to RAG system
            chunks_added = self.rag.add_document(document_text)
            print(f"  📄 Processed {{chunks_added}} chunks")
            
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
                        message=f"Based on the document, answer: {{query}}",
                        context=context
                    )
                    insights.append(response)
                except Exception as e:
                    print(f"  ⚠️  LLM query failed: {{e}}")
                    insights.append(f"[Error] {{context[:200]}}...")
            
            # Synthesize signal from insights
            full_analysis = "\n".join(insights)
            direction, confidence = calculate_sentiment_score(full_analysis)
            
            # Clear RAG for next document
            self.rag.clear()
            
            return {{
                'direction': direction,
                'confidence': confidence,
                'reasoning': full_analysis[:300] + "...",
                'insights': insights
            }}
        
        except Exception as e:
            print(f"  ❌ RAG analysis failed: {{e}}")
            return {{
                'direction': 'neutral',
                'confidence': 0.3,
                'reasoning': f'Analysis error: {{str(e)}}',
                'insights': []
            }}


async def main():
    """Example usage of RAG agent."""
    print(f"{{'=' * 60}}")
    print(f"{agent_name} - RAG-Powered Document Analysis")
    print(f"{{'=' * 60}}\\n")
    
    # Connect to database
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        # Create agent
        agent = {agent_name}()
        
        # Analyze SEC filings or news
        for ticker in ['AAPL', 'TSLA']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            # Get SEC filing or news text
            filing = await db.get_filing(ticker)
            
            if not filing:
                print(f"⚠️  No filing for {{ticker}}")
                continue
            
            print(f"\\n📊 Analyzing {{ticker}} filing...")
            result = await agent.analyze_async(ticker, filing)
            
            print(f"{{result['direction'].upper()}} ({{result['confidence']:.0%}})")
            print(f"{{result['reasoning']}}\\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_hybrid_agent(
        self,
        agent_name: str,
        description: str,
        rules: List[Dict],
        llm_provider: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str
    ) -> str:
        """Generate hybrid agent with both rules and LLM."""
        
        # Generate rule checks
        rule_checks = []
        for rule in rules or []:
            metric = rule['metric']
            operator = rule['operator']
            threshold = rule['threshold']
            
            rule_checks.append(
                f"data.get('{metric}', 0) {operator} {threshold}"
            )
        
        rules_condition = " or ".join(rule_checks) if rule_checks else "False"
        
        return f'''"""Auto-generated hybrid agent: {agent_name}

{description}

Uses rule-based logic for clear signals, LLM for complex analysis.

DEPENDENCIES:
This agent requires LLM dependencies. Install with:
  pip install 'ai-agent-framework[llm]'

Or install specific provider:
  pip install {llm_provider}

To check which providers are installed:
  python3 gui/check_llm_deps.py
"""

import asyncio
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig,
    Database, Config, parse_llm_signal, format_fundamentals
)


class {agent_name}(Agent):
    """{description}"""
    
    def __init__(self):
        """Initialize agent with LLM configuration."""
        config = AgentConfig(
            name="{agent_name}",
            description="{description}",
            llm=LLMConfig(
                provider='{llm_provider}',
                temperature={temperature},
                max_tokens={max_tokens},
                system_prompt="""{system_prompt or 'You are a financial analyst.'}"""
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Hybrid analysis: rules first, then LLM for complex cases.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Check if any rule-based conditions are met
        if {rules_condition}:
            # Use LLM for detailed analysis
            return self._llm_analysis(ticker, data)
        
        # Default neutral signal
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No significant indicators, holding neutral stance'
        )
    
    def _llm_analysis(self, ticker: str, data: dict) -> Signal:
        """Perform LLM-based analysis."""
        fundamentals_text = format_fundamentals(data)
        
        prompt = f"""Analyze {{ticker}}:

{{fundamentals_text}}

Provide detailed reasoning for your recommendation.
Format: DIRECTION|CONFIDENCE|REASONING"""
        
        try:
            response = self.llm.chat(prompt)
            return parse_llm_signal(response, f"Hybrid analysis of {{ticker}}")
        except Exception as e:
            print(f"⚠️  LLM error: {{e}}")
            return Signal(
                direction='neutral',
                confidence=0.5,
                reasoning=f'LLM error: {{str(e)[:100]}}'
            )


async def main():
    """Example usage of the hybrid agent."""
    print(f"{{'-' * 60}}")
    print(f"{agent_name} - Hybrid Analysis")
    print(f"{{'-' * 60}}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'MSFT']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            print(f"📊 {{ticker}}")
            signal = agent.analyze(ticker, data)
            print(f"{{signal.direction.upper()}} ({{signal.confidence:.0%}})")
            print(f"{{signal.reasoning}}\\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_metric_extraction(self, rules: List[Dict]) -> str:
        """Generate metric extraction code."""
        if not rules:
            return "# No metrics to extract"
        
        metrics = set(rule['metric'] for rule in rules)
        extractions = [f"{m} = data.get('{m}', 0)" for m in metrics]
        return "\n        ".join(extractions)
