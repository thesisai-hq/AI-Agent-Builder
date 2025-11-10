"""Agent management routes."""

from fastapi import APIRouter
from typing import List
from ..models import (
    AgentCreate, AgentUpdate, AgentResponse, 
    AgentListResponse, ExportCodeResponse
)
from ..storage import storage
from ..errors import AgentNotFoundError, APIError


router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentResponse, status_code=201)
async def create_agent(agent: AgentCreate):
    """Create a new agent.
    
    Args:
        agent: Agent creation data
        
    Returns:
        Created agent with ID and timestamps
    """
    try:
        return storage.create_agent(agent)
    except Exception as e:
        raise APIError(500, "Failed to create agent", {"reason": str(e)})


@router.get("", response_model=AgentListResponse)
async def list_agents():
    """List all agents.
    
    Returns:
        List of all agents
    """
    try:
        agents = storage.list_agents()
        return AgentListResponse(agents=agents, total=len(agents))
    except Exception as e:
        raise APIError(500, "Failed to list agents", {"reason": str(e)})


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get agent by ID.
    
    Args:
        agent_id: Agent ID
        
    Returns:
        Agent details
    """
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, update: AgentUpdate):
    """Update an existing agent.
    
    Args:
        agent_id: Agent ID
        update: Fields to update
        
    Returns:
        Updated agent
    """
    agent = storage.update_agent(agent_id, update)
    if not agent:
        raise AgentNotFoundError(agent_id)
    return agent


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: str):
    """Delete an agent.
    
    Args:
        agent_id: Agent ID
    """
    success = storage.delete_agent(agent_id)
    if not success:
        raise AgentNotFoundError(agent_id)


@router.get("/{agent_id}/export", response_model=ExportCodeResponse)
async def export_agent_code(agent_id: str):
    """Export agent as Python code.
    
    Args:
        agent_id: Agent ID
        
    Returns:
        Python code for the agent
    """
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    
    # Generate Python code
    code = _generate_agent_code(agent)
    filename = f"{agent.name.lower().replace(' ', '_')}_agent.py"
    
    return ExportCodeResponse(code=code, filename=filename)


def _generate_agent_code(agent: AgentResponse) -> str:
    """Generate Python code for an agent.
    
    Args:
        agent: Agent to export
        
    Returns:
        Python code as string
    """
    if agent.type == "rule_based":
        return _generate_rule_based_code(agent)
    else:
        return _generate_llm_based_code(agent)


def _generate_rule_based_code(agent: AgentResponse) -> str:
    """Generate code for rule-based agent with formula support."""
    
    # Check if any formulas are used
    has_formulas = any(
        any(c.type == 'formula' for c in rule.conditions)
        for rule in agent.rules
    )
    
    rules_code = []
    for i, rule in enumerate(agent.rules):
        # Build condition checks
        condition_checks = []
        
        for c in rule.conditions:
            if c.type == 'formula':
                # Formula condition
                var_assignments = '\n        '.join([
                    f"{var_name} = data.get('{data_field}', 0)"
                    for var_name, data_field in (c.variables or {}).items()
                ])
                
                formula_eval = c.formula.replace('**', '**')  # Keep power operator
                
                condition_checks.append(f"""
        # Formula: {c.formula_description or c.formula}
        {var_assignments}
        formula_result = {formula_eval}
        if not (formula_result {c.formula_operator} {c.formula_threshold}):
            condition_met = False""")
            else:
                # Simple condition
                condition_checks.append(f"""
        if not (data.get('{c.indicator}', 0) {c.operator} {c.value}):
            condition_met = False""")
        
        conditions_code = '\n'.join(condition_checks)
        action = rule.action.action
        size = rule.action.size
        
        rules_code.append(f"""
    # Rule {i + 1}: {rule.description or f"Rule {i + 1}"}
    condition_met = True{conditions_code}
    
    if condition_met:
        return Signal('{action}', {size / 100:.2f}, 
                     '{rule.description or "Rule " + str(i + 1) + " triggered"}')
""")
    
    # Add math import if formulas are used
    math_import = "import math\n" if has_formulas else ""
    
    code = f'''"""
{agent.name}
{agent.description or ''}

Generated from AI-Agent-Builder GUI
"""

from agent_framework import Agent, Signal
from typing import Dict, Any
{math_import}

class {agent.name.replace(" ", "")}Agent(Agent):
    """{agent.goal}"""
    
    def analyze(self, ticker: str, data: Dict[str, Any]) -> Signal:
        """Analyze stock data and generate signal.
        
        Args:
            ticker: Stock ticker
            data: Market/fundamental data
            
        Returns:
            Trading signal
        """
{"".join(rules_code)}
        
        # Default: neutral
        return Signal('neutral', 0.5, 'No rules triggered')


# Usage example
if __name__ == "__main__":
    import asyncio
    from agent_framework import Database, Config
    
    async def main():
        db = Database(Config.get_database_url())
        await db.connect()
        
        agent = {agent.name.replace(" ", "")}Agent()
        data = await db.get_fundamentals('AAPL')
        signal = agent.analyze('AAPL', data)
        
        print(f"{{signal.direction.upper()}}: {{signal.reasoning}}")
        await db.disconnect()
    
    asyncio.run(main())
'''
    return code


def _generate_llm_based_code(agent: AgentResponse) -> str:
    """Generate code for LLM-based agent."""
    llm_config = agent.llm_config
    
    # Build system prompt - avoid nested f-strings
    if llm_config.system_prompt:
        system_prompt = llm_config.system_prompt
    else:
        system_prompt = f"""You are a financial analyst agent.
Goal: {agent.goal}

Analyze the provided stock data and respond with:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your analysis]
"""
    
    # Escape quotes in system prompt for code generation
    system_prompt_escaped = system_prompt.replace('"""', '\\"\\"\\"')
    
    code = f'''"""
{agent.name}
{agent.description or ''}

Generated from AI-Agent-Builder GUI
"""

from agent_framework import Agent, Signal, LLMConfig, AgentConfig
from typing import Dict, Any


class {agent.name.replace(" ", "")}Agent(Agent):
    """{agent.goal}"""
    
    def __init__(self):
        system_prompt = """{system_prompt_escaped}"""
        
        config = AgentConfig(
            name="{agent.name}",
            description="{agent.description or agent.goal}",
            llm=LLMConfig(
                provider="{llm_config.provider}",
                model="{llm_config.model}",
                temperature={llm_config.temperature},
                max_tokens={llm_config.max_tokens},
                system_prompt=system_prompt
            )
        )
        super().__init__(config)
    
    def analyze(self, ticker: str, data: Dict[str, Any]) -> Signal:
        """Analyze stock data using LLM.
        
        Args:
            ticker: Stock ticker
            data: Market/fundamental data
            
        Returns:
            Trading signal
        """
        # Format data for LLM
        from agent_framework import format_fundamentals
        formatted_data = format_fundamentals(data)
        
        prompt = f"""Analyze {{ticker}}:
        
{{formatted_data}}

Provide your signal, confidence, and reasoning."""
        
        # Call LLM
        response = self.llm.generate(prompt)
        
        # Parse response
        from agent_framework import parse_llm_signal
        return parse_llm_signal(response)


# Usage example
if __name__ == "__main__":
    import asyncio
    from agent_framework import Database, Config
    
    async def main():
        db = Database(Config.get_database_url())
        await db.connect()
        
        agent = {agent.name.replace(" ", "")}Agent()
        data = await db.get_fundamentals('AAPL')
        signal = agent.analyze('AAPL', data)
        
        print(f"{{signal.direction.upper()}}: {{signal.reasoning}}")
        await db.disconnect()
    
    asyncio.run(main())
'''
    return code
