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
        system_prompt: Optional[str] = None
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
            if pe < 20:
                return Signal(
                    direction='neutral',
                    confidence=0.5,
                    reasoning=f'LLM unavailable, PE={{pe:.1f}}'
                )
            return Signal(
                direction='neutral',
                confidence=0.5,
                reasoning='LLM unavailable, insufficient data'
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
