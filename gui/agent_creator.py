"""Agent Creator - Generate agent code with enhanced confidence calculations

SECURITY: This version includes input sanitization to prevent code injection.

This version generates agents that use sophisticated confidence calculations
based on signal strength, not hardcoded values.
"""

import re
from typing import Dict, List, Optional


class AgentCreator:
    """Generates agent code with enhanced confidence calculations and security."""

    # ===================================================================
    # SECURITY: Input Sanitization Methods
    # ===================================================================

    @staticmethod
    def _sanitize_identifier(name: str) -> str:
        """Sanitize a Python identifier (class name, variable name).

        Args:
            name: Raw identifier from user input

        Returns:
            Safe identifier with only alphanumeric and underscores
        """
        # Remove any non-alphanumeric characters except underscores
        sanitized = re.sub(r"[^a-zA-Z0-9_]", "", name)

        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = "A" + sanitized

        # Return or provide default
        return sanitized if sanitized else "Agent"

    @staticmethod
    def _escape_string_literal(text: str) -> str:
        """Escape a string for safe inclusion in Python triple-quoted strings.

        This prevents code injection by escaping:
        - Backslashes (to prevent escape sequences)
        - Triple quotes (to prevent breaking out of string)
        - Other special characters

        Args:
            text: Raw text from user input

        Returns:
            Escaped text safe for triple-quoted strings
        """
        if not text:
            return ""

        # Escape backslashes first (must be done before other escapes)
        escaped = text.replace("\\", "\\\\")

        # Escape triple quotes to prevent breaking out of docstrings
        escaped = escaped.replace('"""', r"\"\"\"")

        # Also escape single triple quotes (for safety)
        escaped = escaped.replace("'''", r"\'\'\'")

        return escaped

    @staticmethod
    def _validate_numeric(value: any, default: float = 0.0) -> float:
        """Safely convert and validate numeric values.

        Args:
            value: Value to convert
            default: Default value if conversion fails

        Returns:
            Validated float
        """
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _validate_integer(value: any, default: int = 0) -> int:
        """Safely convert and validate integer values.

        Args:
            value: Value to convert
            default: Default value if conversion fails

        Returns:
            Validated integer
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    # ===================================================================
    # Main Generation Methods
    # ===================================================================

    def generate_agent_code(
        self,
        agent_name: str,
        description: str,
        agent_type: str,
        rules: Optional[List[Dict]] = None,
        llm_provider: Optional[str] = None,
        llm_model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
        user_prompt_instructions: Optional[str] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        top_k: Optional[int] = None,
        custom_queries: Optional[List[str]] = None,
    ) -> str:
        """Generate complete agent code with enhanced confidence.

        SECURITY: All user inputs are sanitized before code generation.
        """
        # Sanitize identifier inputs
        safe_agent_name = self._sanitize_identifier(agent_name)
        safe_description = self._escape_string_literal(description)

        # Sanitize LLM inputs
        safe_llm_provider = self._sanitize_identifier(llm_provider) if llm_provider else None
        safe_llm_model = self._escape_string_literal(llm_model) if llm_model else None
        safe_system_prompt = self._escape_string_literal(system_prompt) if system_prompt else None
        safe_user_instructions = (
            self._escape_string_literal(user_prompt_instructions)
            if user_prompt_instructions
            else None
        )

        # Validate numeric inputs
        safe_temperature = (
            self._validate_numeric(temperature, 0.7) if temperature is not None else None
        )
        safe_max_tokens = (
            self._validate_integer(max_tokens, 1000) if max_tokens is not None else None
        )
        safe_chunk_size = (
            self._validate_integer(chunk_size, 300) if chunk_size is not None else None
        )
        safe_chunk_overlap = (
            self._validate_integer(chunk_overlap, 50) if chunk_overlap is not None else None
        )
        safe_top_k = self._validate_integer(top_k, 3) if top_k is not None else None

        # Route to appropriate generator
        if agent_type == "Rule-Based":
            return self._generate_rule_based_agent(safe_agent_name, safe_description, rules)
        elif agent_type == "LLM-Powered":
            return self._generate_llm_agent(
                safe_agent_name,
                safe_description,
                safe_llm_provider,
                safe_llm_model,
                safe_temperature,
                safe_max_tokens,
                safe_system_prompt,
                safe_user_instructions,
            )
        elif agent_type == "RAG-Powered":
            # Sanitize custom queries
            safe_custom_queries = None
            if custom_queries:
                safe_custom_queries = [self._escape_string_literal(q) for q in custom_queries if q and q.strip()]
            
            return self._generate_rag_agent(
                safe_agent_name,
                safe_description,
                safe_llm_provider,
                safe_llm_model,
                safe_temperature,
                safe_max_tokens,
                safe_system_prompt,
                safe_user_instructions,
                safe_chunk_size,
                safe_chunk_overlap,
                safe_top_k,
                safe_custom_queries,
            )
        else:  # Hybrid
            return self._generate_hybrid_agent(
                safe_agent_name,
                safe_description,
                rules,
                safe_llm_provider,
                safe_llm_model,
                safe_temperature,
                safe_max_tokens,
                safe_system_prompt,
                safe_user_instructions,
            )

    def _generate_rule_based_agent(
        self, agent_name: str, description: str, rules: List[Dict]
    ) -> str:
        """Generate rule-based agent code.

        Note: agent_name and description are already sanitized by generate_agent_code.
        """
        if not rules:
            return self._generate_empty_agent(agent_name, description)

        rule_type = rules[0].get("type", "simple")

        if rule_type == "simple":
            return self._generate_simple_rules_agent(agent_name, description, rules)
        elif rule_type == "advanced":
            return self._generate_advanced_rules_agent(agent_name, description, rules)
        elif rule_type == "score":
            return self._generate_score_based_agent(agent_name, description, rules[0])
        else:
            return self._generate_simple_rules_agent(agent_name, description, rules)

    def _generate_simple_rules_agent(
        self, agent_name: str, description: str, rules: List[Dict]
    ) -> str:
        """Generate simple rules agent with enhanced confidence.

        SECURITY: All inputs already sanitized by caller.
        """

        # Generate rule logic with enhanced confidence
        rule_conditions = []
        for i, rule in enumerate(rules or []):
            # Sanitize rule parameters
            metric = self._sanitize_identifier(rule["metric"])
            operator = rule["operator"] if rule["operator"] in ["<", ">", "<=", ">=", "=="] else "<"
            threshold = self._validate_numeric(rule["threshold"])
            direction = (
                rule["direction"]
                if rule["direction"] in ["bullish", "bearish", "neutral"]
                else "neutral"
            )
            base_conf = self._validate_numeric(rule["confidence"], 0.5)

            rule_conditions.append(
                f"""
        # Rule {i+1}: {metric} {operator} {threshold}
        if {metric} {operator} {threshold}:
            # Enhanced confidence based on signal strength
            rule_conf, strength_reason = calc.calculate_rule_confidence(
                metric_value={metric},
                threshold={threshold},
                operator='{operator}',
                base_confidence={base_conf}
            )
            
            return Signal(
                direction='{direction}',
                confidence=rule_conf,
                reasoning=f"{metric.replace('_', ' ').title()} {{{metric}:.1f}} is {direction}. {{strength_reason}}"
            )"""
            )

        rules_code = "".join(rule_conditions)

        return f'''"""Auto-generated agent: {agent_name}

{description}

Strategy: Rule-based with enhanced confidence calculation

Confidence is calculated based on:
- How strongly criteria are met (distance from threshold)
- Barely met (within 5%): ~60% confidence
- Moderately met (5-15%): ~70% confidence
- Strongly met (15-30%): ~80% confidence
- Very strongly met (>30%): ~90% confidence
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config, ConfidenceCalculator


class {agent_name}(Agent):
    """{description}"""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze with enhanced confidence calculation.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with calculated confidence based on signal strength
        """
        # Extract metrics
        {self._generate_metric_extraction(rules)}
        
        # Initialize confidence calculator
        calc = ConfidenceCalculator()
        
        # Apply rules{rules_code}
        
        # Default fallback
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No rules matched'
        )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print(f"{agent_name} - Enhanced Confidence")
    print(f"{'-' * 60}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            signal = await agent.analyze(ticker, data)
            print(f"📊 {{ticker}}: {{signal.direction.upper()}} ({{signal.confidence:.0%}})")
            print(f"   {{signal.reasoning}}\\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''

    def _generate_score_based_agent(
        self, agent_name: str, description: str, rule_config: Dict
    ) -> str:
        """Generate score-based agent with enhanced confidence.

        SECURITY: All inputs already sanitized by caller.
        """

        criteria = rule_config["criteria"]
        bullish_threshold = self._validate_integer(rule_config["bullish_threshold"], 3)
        bearish_threshold = self._validate_integer(rule_config["bearish_threshold"], -2)

        # Generate scoring logic with sanitized inputs
        score_checks = []

        for i, criterion in enumerate(criteria):
            metric = self._sanitize_identifier(criterion["metric"])
            operator = (
                criterion["operator"] if criterion["operator"] in ["<", ">", "<=", ">="] else "<"
            )
            threshold = self._validate_numeric(criterion["threshold"])
            points = self._validate_integer(criterion["points"])

            score_checks.append(
                f"""
        # {metric} {operator} {threshold} = {points:+d} points
        if {metric} {operator} {threshold}:
            score += {points}
            criteria_met.append({{
                'metric': '{metric}',
                'points': {points},
                'met': True
            }})
            reasons.append(f"{metric.replace('_', ' ').title()} {{{metric}:.1f}} {operator} {threshold} ({points:+d} pts)")
        else:
            criteria_met.append({{
                'metric': '{metric}',
                'points': {points},
                'met': False
            }})"""
            )

        score_code = "".join(score_checks)

        return f'''"""Auto-generated agent: {agent_name}

{description}

Strategy: Score-based with enhanced confidence calculation

Confidence is calculated based on:
- Score margin past threshold (how far above/below)
- Percentage of max possible margin achieved
- Data quality and completeness

Scoring:
- Bullish if score >= {bullish_threshold}
- Bearish if score <= {bearish_threshold}
- Neutral otherwise
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config, EnhancedConfidenceCalculator


class {agent_name}(Agent):
    """{description}"""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using score-based strategy with enhanced confidence.
        
        Args:
            ticker: Stock ticker symbol
            data: Financial data dictionary
            
        Returns:
            Signal with calculated confidence based on score strength
        """
        # Initialize
        score = 0
        reasons = []
        criteria_met = []
        
        # Extract metrics
        {self._generate_metric_extraction_for_score(criteria)}
        
        # Calculate score{score_code}
        
        # Enhanced confidence calculation
        calc = EnhancedConfidenceCalculator()
        direction, confidence, detailed_reasoning = calc.for_score_based_agent(
            score=score,
            criteria_evaluated=criteria_met,
            bullish_threshold={bullish_threshold},
            bearish_threshold={bearish_threshold},
            data=data
        )
        
        # Add rule details to reasoning
        if reasons:
            full_reasoning = detailed_reasoning + " | " + "; ".join(reasons[:3])
        else:
            full_reasoning = detailed_reasoning
        
        return Signal(
            direction=direction,
            confidence=confidence,
            reasoning=full_reasoning
        )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print(f"{agent_name} - Score-Based with Enhanced Confidence")
    print(f"{'-' * 60}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            
            if not data:
                print(f"⚠️  No data for {{ticker}}")
                continue
            
            signal = await agent.analyze(ticker, data)
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
        llm_model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str,
        user_prompt_instructions: Optional[str] = None,
    ) -> str:
        """Generate LLM agent with enhanced confidence parsing.

        SECURITY: All inputs already sanitized by caller.
        Note: system_prompt and user_prompt_instructions are escaped for safe inclusion.
        """

        # Build user prompt template (already escaped)
        if user_prompt_instructions:
            prompt_content = f"""Analyze {{ticker}} with the following data:

{{fundamentals_text}}

{user_prompt_instructions}

Provide your investment recommendation.
Format: DIRECTION|CONFIDENCE|REASONING
Example: bullish|75|Strong growth with healthy margins"""
        else:
            prompt_content = """Analyze {ticker} with the following data:

{fundamentals_text}

Provide your investment recommendation.
Format: DIRECTION|CONFIDENCE|REASONING  
Example: bullish|75|Strong growth with healthy margins"""

        # Use escaped system_prompt (safe for triple quotes)
        safe_prompt = system_prompt or "You are a financial analyst."

        return f'''"""Auto-generated LLM-powered agent: {agent_name}

{description}

Uses enhanced_parse_llm_signal for confidence validation.

DEPENDENCIES:
  pip install 'ai-agent-framework[llm]' or pip install {llm_provider}
"""

import asyncio
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig,
    Database, Config, enhanced_parse_llm_signal, format_fundamentals
)


class {agent_name}(Agent):
    """{description}"""
    
    def __init__(self):
        config = AgentConfig(
            name="{agent_name}",
            description="{description}",
            llm=LLMConfig(
                provider='{llm_provider}',
                model='{llm_model}',
                temperature={temperature},
                max_tokens={max_tokens},
                system_prompt="""{safe_prompt}"""
            )
        )
        super().__init__(config)
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using LLM with enhanced confidence validation."""
        fundamentals_text = format_fundamentals(data)
        
        prompt = f"""{prompt_content}"""
        
        try:
            response = self.llm.chat(prompt)
            # Use enhanced parser that validates confidence quality
            return enhanced_parse_llm_signal(response, f"Analysis of {{ticker}}")
        except Exception as e:
            print(f"⚠️  LLM error: {{e}}")
            return Signal(
                direction='neutral',
                confidence=0.2,
                reasoning=f'LLM unavailable ({{type(e).__name__}}). Error: {{str(e)[:100]}}'
            )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print(f"{agent_name} - LLM Analysis")
    print(f"{'-' * 60}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'TSLA']:
            data = await db.get_fundamentals(ticker)
            if not data:
                continue
            
            signal = await agent.analyze(ticker, data)
            print(f"📊 {{ticker}}: {{signal.direction.upper()}} ({{signal.confidence:.0%}})")
            print(f"   {{signal.reasoning}}\\n")
    
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
        llm_model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str,
        user_prompt_instructions: Optional[str] = None,
        chunk_size: int = 300,
        chunk_overlap: int = 50,
        top_k: int = 3,
        custom_queries: Optional[List[str]] = None,
    ) -> str:
        """Generate RAG agent code.

        SECURITY: All inputs already sanitized by caller.
        """

        safe_prompt = system_prompt or "You are a financial document analyst."
        
        # Build queries list code
        if custom_queries and len(custom_queries) > 0:
            # User provided custom queries
            queries_code = "queries = [\n"
            for query in custom_queries:
                queries_code += f'                "{query}",\n'
            
            # If user_prompt_instructions provided, add as additional query
            if user_prompt_instructions and user_prompt_instructions.strip():
                queries_code += f'                "{user_prompt_instructions}",\n'
            
            queries_code += "            ]"
        else:
            # Use default queries
            queries_code = '''queries = [
                "What are the key financial metrics and performance?",
                "What are the main risks or challenges?",
                "What are the growth opportunities?"
            ]'''
            
            # If user_prompt_instructions provided, add as additional query
            if user_prompt_instructions and user_prompt_instructions.strip():
                queries_code = f'''queries = [
                "What are the key financial metrics and performance?",
                "What are the main risks or challenges?",
                "What are the growth opportunities?",
                "{user_prompt_instructions}"
            ]'''

        return f'''"""Auto-generated RAG-powered agent: {agent_name}

{description}

DEPENDENCIES:
  pip install 'ai-agent-framework[llm,rag]' or pip install {llm_provider} sentence-transformers
"""

import asyncio
from agent_framework import (
    Agent, AgentConfig, LLMConfig, RAGConfig, Signal,
    Database, Config, calculate_sentiment_score
)


class {agent_name}(Agent):
    """{description}"""
    
    def __init__(self):
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
                model='{llm_model}',
                temperature={temperature},
                max_tokens={max_tokens},
                system_prompt="""{safe_prompt}"""
            )
        )
        super().__init__(config)
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze document using RAG."""
        if isinstance(data, dict):
            document_text = data.get('document', '')
        else:
            document_text = str(data)
        
        if not document_text or len(document_text) < 100:
            return Signal(
                direction='neutral',
                confidence=0.3,
                reasoning='Document too short for analysis',
                metadata={{'insights': []}}
            )
        
        try:
            chunks_added = self.rag.add_document(document_text)
            print(f"  📄 Processed {{chunks_added}} chunks")
            
            # Query questions for document analysis
            {queries_code}
            
            insights = []
            for query in queries:
                context = self.rag.query(query)
                try:
                    response = self.llm.chat(
                        message=f"Based on the document, answer: {{query}}",
                        context=context
                    )
                    insights.append(response)
                except Exception as e:
                    print(f"  ⚠️  Query failed: {{e}}")
                    insights.append(f"[Error] {{context[:200]}}...")
            
            full_analysis = "\\n".join(insights)
            direction, confidence = calculate_sentiment_score(full_analysis)
            
            self.rag.clear()
            
            return Signal(
                direction=direction,
                confidence=confidence,
                reasoning=full_analysis[:400] + "..." if len(full_analysis) > 400 else full_analysis,
                metadata={{'insights': insights}}
            )
        
        except Exception as e:
            print(f"  ❌ RAG failed: {{e}}")
            return Signal(
                direction='neutral',
                confidence=0.3,
                reasoning=f'RAG error: {{str(e)}}',
                metadata={{'insights': []}}
            )


async def main():
    """Example usage."""
    print(f"{'=' * 60}")
    print(f"{agent_name} - RAG Analysis")
    print(f"{'=' * 60}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'TSLA']:
            data = await db.get_fundamentals(ticker)
            if not data:
                continue
            
            filing = await db.get_filing(ticker)
            if not filing:
                continue
            
            print(f"\\n📊 Analyzing {{ticker}} filing...")
            signal = await agent.analyze(ticker, filing)
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
        llm_model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str,
        user_prompt_instructions: Optional[str] = None,
    ) -> str:
        """Generate hybrid agent.

        SECURITY: All inputs already sanitized by caller.
        """

        # Build prompt template (already escaped)
        if user_prompt_instructions:
            prompt_content = f"""Analyze {{ticker}}:

{{fundamentals_text}}

{user_prompt_instructions}

Format: DIRECTION|CONFIDENCE|REASONING"""
        else:
            prompt_content = """Analyze {ticker}:

{fundamentals_text}

Format: DIRECTION|CONFIDENCE|REASONING"""

        # Generate rule checks with sanitized inputs
        rule_checks = []
        for rule in rules or []:
            metric = self._sanitize_identifier(rule["metric"])
            operator = rule["operator"] if rule["operator"] in ["<", ">", "<=", ">=", "=="] else "<"
            threshold = self._validate_numeric(rule["threshold"])
            rule_checks.append(f"data.get('{metric}', 0) {operator} {threshold}")

        rules_condition = " or ".join(rule_checks) if rule_checks else "False"
        safe_prompt = system_prompt or "You are a financial analyst."

        return f'''"""Auto-generated hybrid agent: {agent_name}

{description}

Uses enhanced confidence for both rules and LLM.

DEPENDENCIES:
  pip install 'ai-agent-framework[llm]' or pip install {llm_provider}
"""

import asyncio
from agent_framework import (
    Agent, Signal, AgentConfig, LLMConfig,
    Database, Config, enhanced_parse_llm_signal, format_fundamentals
)


class {agent_name}(Agent):
    """{description}"""
    
    def __init__(self):
        config = AgentConfig(
            name="{agent_name}",
            description="{description}",
            llm=LLMConfig(
                provider='{llm_provider}',
                model='{llm_model}',
                temperature={temperature},
                max_tokens={max_tokens},
                system_prompt="""{safe_prompt}"""
            )
        )
        super().__init__(config)
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Hybrid: rules filter, LLM analyzes with enhanced confidence."""
        if {rules_condition}:
            return await self._llm_analysis(ticker, data)
        
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No significant indicators'
        )
    
    async def _llm_analysis(self, ticker: str, data: dict) -> Signal:
        """LLM analysis with confidence validation."""
        fundamentals_text = format_fundamentals(data)
        
        prompt = f"""{prompt_content}"""
        
        try:
            response = self.llm.chat(prompt)
            return enhanced_parse_llm_signal(response, f"Hybrid analysis of {{ticker}}")
        except Exception as e:
            print(f"⚠️  LLM error: {{e}}")
            return Signal(
                direction='neutral',
                confidence=0.4,
                reasoning=f'LLM error: {{str(e)[:100]}}'
            )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print(f"{agent_name} - Hybrid Analysis")
    print(f"{'-' * 60}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        
        for ticker in ['AAPL', 'MSFT']:
            data = await db.get_fundamentals(ticker)
            if not data:
                continue
            
            signal = await agent.analyze(ticker, data)
            print(f"📊 {{ticker}}: {{signal.direction.upper()}} ({{signal.confidence:.0%}})")
            print(f"   {{signal.reasoning}}\\n")
    
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''

    def _generate_advanced_rules_agent(
        self, agent_name: str, description: str, rules: List[Dict]
    ) -> str:
        """Generate advanced rules agent.

        SECURITY: All inputs already sanitized by caller.
        """

        rule_conditions = []
        for i, rule in enumerate(rules):
            conditions = rule["conditions"]
            logic = rule["logic"]
            direction = (
                rule["direction"]
                if rule["direction"] in ["bullish", "bearish", "neutral"]
                else "neutral"
            )
            confidence = self._validate_numeric(rule["confidence"], 0.5)

            cond_parts = []
            for cond in conditions:
                metric = self._sanitize_identifier(cond["metric"])
                operator = (
                    cond["operator"] if cond["operator"] in ["<", ">", "<=", ">=", "=="] else "<"
                )
                threshold = self._validate_numeric(cond["threshold"])

                if metric == "peg_ratio":
                    cond_parts.append(
                        f"(pe_ratio / max(revenue_growth, 0.1) {operator} {threshold})"
                    )
                elif metric == "quality_score":
                    cond_parts.append(
                        f"((roe * 0.4 + profit_margin * 0.3 + (1.0 / max(debt_to_equity, 0.1)) * 0.3) {operator} {threshold})"
                    )
                else:
                    cond_parts.append(f"(data.get('{metric}', 0) {operator} {threshold})")

            logic_op = " and " if logic == "AND" else " or "
            full_condition = logic_op.join(cond_parts)
            cond_desc = f" {logic} ".join(
                [
                    f"{self._sanitize_identifier(c['metric'])} {c['operator']} {self._validate_numeric(c['threshold'])}"
                    for c in conditions
                ]
            )

            rule_conditions.append(
                f"""
        # Rule {i+1}: {cond_desc}
        if {full_condition}:
            return Signal(
                direction='{direction}',
                confidence={confidence},
                reasoning=f"{{'{direction}'.capitalize()}} signal: {cond_desc}"
            )"""
            )

        rules_code = "".join(rule_conditions)

        return f'''"""Auto-generated agent: {agent_name}

{description}

Strategy: Advanced multi-condition rules
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config


class {agent_name}(Agent):
    """{description}"""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze using advanced rules."""
        pe_ratio = data.get('pe_ratio', 0)
        revenue_growth = data.get('revenue_growth', 0)
        profit_margin = data.get('profit_margin', 0)
        roe = data.get('roe', 0)
        debt_to_equity = data.get('debt_to_equity', 0)
        dividend_yield = data.get('dividend_yield', 0)
        pb_ratio = data.get('pb_ratio', 0)
        current_ratio = data.get('current_ratio', 0)
        
        # Apply rules{rules_code}
        
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No rules matched'
        )


async def main():
    """Example usage."""
    print(f"{'-' * 60}")
    print(f"{agent_name}")
    print(f"{'-' * 60}\\n")
    
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        for ticker in ['AAPL', 'MSFT', 'GOOGL']:
            data = await db.get_fundamentals(ticker)
            if not data:
                continue
            signal = await agent.analyze(ticker, data)
            print(f"📊 {{ticker}}: {{signal.direction.upper()}} ({{signal.confidence:.0%}})")
            print(f"   {{signal.reasoning}}\\n")
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''

    def _generate_empty_agent(self, agent_name: str, description: str) -> str:
        """Generate template for agents with no rules.

        SECURITY: All inputs already sanitized by caller.
        """
        return f'''"""Auto-generated agent: {agent_name}

{description}
"""

import asyncio
from agent_framework import Agent, Signal, Database, Config


class {agent_name}(Agent):
    """{description}"""
    
    async def analyze(self, ticker: str, data: dict) -> Signal:
        """Analyze - implement your logic here."""
        return Signal(
            direction='neutral',
            confidence=0.5,
            reasoning='No analysis logic defined'
        )


async def main():
    """Example usage."""
    db = Database(Config.get_database_url())
    await db.connect()
    
    try:
        agent = {agent_name}()
        data = await db.get_fundamentals('AAPL')
        signal = await agent.analyze('AAPL', data)
        print(f"Signal: {{signal.direction}} ({{signal.confidence:.0%}})")
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
'''

    def _generate_metric_extraction(self, rules: List[Dict]) -> str:
        """Generate metric extraction code with sanitized metric names."""
        if not rules:
            return "# No metrics"

        metrics = set(
            self._sanitize_identifier(rule.get("metric", ""))
            for rule in rules
            if rule.get("metric")
        )
        metrics = [m for m in metrics if m]  # Remove empty strings
        extractions = [f"{m} = data.get('{m}', 0)" for m in metrics]
        return "\n        ".join(extractions)

    def _generate_metric_extraction_for_score(self, criteria: List[Dict]) -> str:
        """Generate metric extraction for score-based with sanitized names."""
        if not criteria:
            return "# No metrics"

        metrics = set(self._sanitize_identifier(c["metric"]) for c in criteria)
        metrics = [m for m in metrics if m]  # Remove empty strings
        extractions = [f"{m} = data.get('{m}', 0)" for m in metrics]
        return "\n        ".join(extractions)
