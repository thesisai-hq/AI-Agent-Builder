"""Agent code generation module.

Generates Python code from agent configurations using Jinja2 templates.
Clean separation from API logic, easier to test and maintain.
"""

from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from .models import AgentResponse, Rule, RuleCondition


class AgentCodeGenerator:
    """Generate executable Python code from agent configurations."""
    
    def __init__(self):
        """Initialize generator with Jinja2 environment."""
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Register custom filters
        self.env.filters['sanitize_class_name'] = self._sanitize_class_name
        self.env.filters['escape_quotes'] = self._escape_quotes
    
    def generate(self, agent: AgentResponse) -> str:
        """Generate Python code for an agent.
        
        Args:
            agent: Agent configuration
            
        Returns:
            Executable Python code as string
        """
        if agent.type == "rule_based":
            return self._generate_rule_based(agent)
        else:
            return self._generate_llm_based(agent)
    
    def _generate_rule_based(self, agent: AgentResponse) -> str:
        """Generate code for rule-based agent."""
        template = self.env.get_template('rule_based_agent.py.jinja')
        
        # Check if formulas are used
        has_formulas = any(
            any(c.type == 'formula' for c in rule.conditions)
            for rule in agent.rules
        )
        
        # Prepare rule data
        rules_data = []
        for i, rule in enumerate(agent.rules):
            rules_data.append({
                'index': i + 1,
                'description': rule.description or f"Rule {i + 1}",
                'conditions': self._prepare_conditions(rule.conditions),
                'action': rule.action.action,
                'size': rule.action.size / 100.0,  # Convert to decimal
            })
        
        return template.render(
            agent=agent,
            has_formulas=has_formulas,
            rules=rules_data,
            class_name=self._sanitize_class_name(agent.name)
        )
    
    def _generate_llm_based(self, agent: AgentResponse) -> str:
        """Generate code for LLM-based agent."""
        template = self.env.get_template('llm_based_agent.py.jinja')
        
        llm_config = agent.llm_config
        
        # Build system prompt
        if llm_config.system_prompt:
            system_prompt = llm_config.system_prompt
        else:
            system_prompt = f"""You are a professional financial analyst.

Goal: {agent.goal}

Analyze the provided stock data and respond in this EXACT format:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your detailed analysis]"""
        
        return template.render(
            agent=agent,
            llm_config=llm_config,
            system_prompt=system_prompt,
            class_name=self._sanitize_class_name(agent.name)
        )
    
    def _prepare_conditions(self, conditions: list[RuleCondition]) -> list[Dict[str, Any]]:
        """Prepare condition data for template rendering."""
        prepared = []
        
        for condition in conditions:
            if condition.type == 'formula':
                # Formula condition
                var_assignments = [
                    f"{var_name} = data.get('{data_field}', 0)"
                    for var_name, data_field in (condition.variables or {}).items()
                ]
                
                prepared.append({
                    'type': 'formula',
                    'formula': condition.formula,
                    'description': condition.formula_description or condition.formula,
                    'var_assignments': var_assignments,
                    'operator': condition.formula_operator,
                    'threshold': condition.formula_threshold
                })
            else:
                # Simple condition
                prepared.append({
                    'type': 'simple',
                    'indicator': condition.indicator,
                    'operator': condition.operator,
                    'value': condition.value
                })
        
        return prepared
    
    @staticmethod
    def _sanitize_class_name(name: str) -> str:
        """Convert agent name to valid Python class name."""
        # Remove special characters and spaces
        sanitized = ''.join(c for c in name if c.isalnum() or c.isspace())
        # Convert to PascalCase
        return ''.join(word.capitalize() for word in sanitized.split())
    
    @staticmethod
    def _escape_quotes(text: str) -> str:
        """Escape quotes for Python string literals."""
        return text.replace('"""', '\\"\\"\\"').replace('"', '\\"')


# Global instance
code_generator = AgentCodeGenerator()
