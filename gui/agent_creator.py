"""Agent Creator - Generate agent code from templates

Now supports:
- Simple rules (single conditions)
- Advanced rules (multi-condition with AND/OR)
- Score-based rules (point accumulation)
"""

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
            agent_type: Type of agent
            rules: List of rules for rule-based logic
            llm_provider: LLM provider
            temperature: LLM temperature
            max_tokens: LLM max tokens
            system_prompt: LLM system prompt
            chunk_size: RAG chunk size
            chunk_overlap: RAG chunk overlap
            top_k: RAG top k results
            
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
        
        if not rules:
            return self._generate_empty_agent(agent_name, description)
        
        # Determine rule type
        rule_type = rules[0].get('type', 'simple')
        
        if rule_type == 'simple':
            return self._generate_simple_rules_agent(agent_name, description, rules)
        elif rule_type == 'advanced':
            return self._generate_advanced_rules_agent(agent_name, description, rules)
        elif rule_type == 'score':
            return self._generate_score_based_agent(agent_name, description, rules[0])
        else:
            return self._generate_simple_rules_agent(agent_name, description, rules)
    
    def _generate_simple_rules_agent(
        self,
        agent_name: str,
        description: str,
        rules: List[Dict]
    ) -> str:
        """Generate simple single-condition rules agent."""
        
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

Strategy: Simple rule-based conditions
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
        # Extract metrics
        {self._generate_metric_extraction(rules)}
        
        # Apply rules{rules_code}
        
        # Default fallback
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No rules matched'
        )


async def main():
    """Example usage."""
    print(f"{{'-' * 60}}")
    print(f"{agent_name} - Example Usage")
    print(f"{{'-' * 60}}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            signal = agent.analyze(ticker, data)
            print(f"📊 {{ticker}}: {{signal.direction.upper()}} ({{signal.confidence:.0%}})")
            print(f"   {{signal.reasoning}}\\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_advanced_rules_agent(
        self,
        agent_name: str,
        description: str,
        rules: List[Dict]
    ) -> str:
        """Generate agent with multi-condition rules (AND/OR logic)."""
        
        # Generate rule logic with AND/OR
        rule_conditions = []
        for i, rule in enumerate(rules):
            conditions = rule['conditions']
            logic = rule['logic']
            direction = rule['direction']
            confidence = rule['confidence']
            
            # Build condition string
            cond_parts = []
            for cond in conditions:
                metric = cond['metric']
                operator = cond['operator']
                threshold = cond['threshold']
                
                # Handle calculated metrics
                if metric == 'peg_ratio':
                    cond_parts.append(
                        f"(pe_ratio / max(revenue_growth, 0.1) {operator} {threshold})"
                    )
                elif metric == 'quality_score':
                    cond_parts.append(
                        f"((roe * 0.4 + profit_margin * 0.3 + (1.0 / max(debt_to_equity, 0.1)) * 0.3) {operator} {threshold})"
                    )
                else:
                    cond_parts.append(f"(data.get('{metric}', 0) {operator} {threshold})")
            
            logic_op = " and " if logic == "AND" else " or "
            full_condition = logic_op.join(cond_parts)
            
            # Build reasoning string
            cond_desc = f" {logic} ".join([f"{c['metric']} {c['operator']} {c['threshold']}" for c in conditions])
            
            rule_conditions.append(f"""
        # Rule {i+1}: {cond_desc}
        if {full_condition}:
            return Signal(
                direction='{direction}',
                confidence={confidence},
                reasoning=f"{{'{direction}'.capitalize()}} signal: {cond_desc}"
            )""")
        
        rules_code = "".join(rule_conditions)
        
        return f'''"""Auto-generated agent: {agent_name}

{description}

Strategy: Advanced multi-condition rules with AND/OR logic
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config


class {agent_name}(Agent):
    """{description}"""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using advanced multi-condition rules.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Extract all metrics
        pe_ratio = data.get('pe_ratio', 0)
        revenue_growth = data.get('revenue_growth', 0)
        profit_margin = data.get('profit_margin', 0)
        roe = data.get('roe', 0)
        debt_to_equity = data.get('debt_to_equity', 0)
        dividend_yield = data.get('dividend_yield', 0)
        pb_ratio = data.get('pb_ratio', 0)
        current_ratio = data.get('current_ratio', 0)
        
        # Apply advanced rules{rules_code}
        
        # Default fallback
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No rules matched'
        )


async def main():
    """Example usage."""
    print(f"{{'-' * 60}}")
    print(f"{agent_name} - Advanced Rules")
    print(f"{{'-' * 60}}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            signal = agent.analyze(ticker, data)
            print(f"📊 {{ticker}}: {{signal.direction.upper()}} ({{signal.confidence:.0%}})")
            print(f"   {{signal.reasoning}}\\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_score_based_agent(
        self,
        agent_name: str,
        description: str,
        rule_config: Dict
    ) -> str:
        \"\"\"Generate score-based agent.\"\"\"
        
        criteria = rule_config['criteria']
        bullish_threshold = rule_config['bullish_threshold']
        bullish_confidence = rule_config['bullish_confidence']
        bearish_threshold = rule_config['bearish_threshold']
        bearish_confidence = rule_config['bearish_confidence']
        
        # Generate scoring logic
        score_checks = []
        for criterion in criteria:
            metric = criterion['metric']
            operator = criterion['operator']
            threshold = criterion['threshold']
            points = criterion['points']
            
            score_checks.append(f"""
        # {metric} {operator} {threshold} = {points:+d} points
        if data.get('{metric}', 0) {operator} {threshold}:
            score += {points}
            reasons.append(f\"{metric.replace('_', ' ').title()} {{{metric}:.1f}} {operator} {threshold} ({points:+d} pts)\")""")
        
        score_code = "".join(score_checks)
        
        return f'''"""Auto-generated agent: {agent_name}

{description}

Strategy: Score-based point accumulation
- Bullish if score >= {bullish_threshold}
- Bearish if score <= {bearish_threshold}
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config


class {agent_name}(Agent):
    """{description}"""
    
    def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using score-based strategy.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with direction, confidence, and reasoning
        """
        # Initialize score and reasons
        score = 0
        reasons = []
        
        # Extract metrics
        {self._generate_metric_extraction_for_score(criteria)}
        
        # Calculate score{score_code}
        
        # Determine signal based on score
        if score >= {bullish_threshold}:
            return Signal(
                direction='bullish',
                confidence={bullish_confidence},
                reasoning=f'Score: {{score}} (bullish threshold: {bullish_threshold}). ' + '; '.join(reasons)
            )
        elif score <= {bearish_threshold}:
            return Signal(
                direction='bearish',
                confidence={bearish_confidence},
                reasoning=f'Score: {{score}} (bearish threshold: {bearish_threshold}). ' + '; '.join(reasons)
            )
        else:
            return Signal(
                direction='neutral',
                confidence=0.5,
                reasoning=f'Score: {{score}} (between {bearish_threshold} and {bullish_threshold}). ' + '; '.join(reasons) if reasons else 'Neutral score'
            )


async def main():
    """Example usage."""
    print(f"{{'-' * 60}}")
    print(f"{agent_name} - Score-Based Strategy")
    print(f"{{'-' * 60}}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            signal = agent.analyze(ticker, data)
            print(f"📊 {{ticker}}: {{signal.direction.upper()}} ({{signal.confidence:.0%}})")
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
            full_analysis = "\\n".join(insights)
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
        """Generate metric extraction code for simple rules."""
        if not rules:
            return "# No metrics to extract"
        
        metrics = set(rule.get('metric') for rule in rules if rule.get('metric'))
        extractions = [f"{m} = data.get('{m}', 0)" for m in metrics]
        return "\n        ".join(extractions)
    
    def _generate_metric_extraction_for_score(self, criteria: List[Dict]) -> str:
        """Generate metric extraction code for score-based rules."""
        if not criteria:
            return "# No metrics to extract"
        
        metrics = set(c['metric'] for c in criteria)
        extractions = [f"{m} = data.get('{m}', 0)" for m in metrics]
        return "\n        ".join(extractions)
