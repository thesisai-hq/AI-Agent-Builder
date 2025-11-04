"""Stock analysis routes using agents."""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from ..models import AnalysisRequest, AnalysisResponse
from ..storage import storage
from ..formula_evaluator import formula_evaluator

# Import agent_framework (assuming it's installed)
try:
    from agent_framework import Database, Config, Signal
except ImportError:
    Database = None
    Config = None
    Signal = None


router = APIRouter(prefix="/analysis", tags=["analysis"])


async def get_database():
    """Dependency to get database connection."""
    if Database is None:
        raise HTTPException(
            status_code=500, 
            detail="agent_framework not installed. Run: pip install -e ../"
        )
    
    db = Database(Config.get_database_url())
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()


@router.post("", response_model=AnalysisResponse)
async def analyze_stock(
    request: AnalysisRequest,
    db: Database = Depends(get_database)
):
    """Analyze a stock using an agent.
    
    Args:
        request: Analysis request with ticker and agent_id
        db: Database connection
        
    Returns:
        Analysis result with signal
    """
    # Get agent
    agent_data = storage.get_agent(request.agent_id)
    if not agent_data:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Get stock data
    try:
        data = await db.get_fundamentals(request.ticker)
        if not data:
            raise HTTPException(
                status_code=404, 
                detail=f"No data found for ticker {request.ticker}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch data: {str(e)}"
        )
    
    # Run analysis
    try:
        signal = _run_agent_analysis(agent_data, request.ticker, data)
        
        return AnalysisResponse(
            ticker=request.ticker,
            agent_id=agent_data.id,
            agent_name=agent_data.name,
            direction=signal.direction,
            confidence=signal.confidence,
            reasoning=signal.reasoning,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )


def _run_agent_analysis(agent_data, ticker: str, data: dict) -> Signal:
    """Run agent analysis logic.
    
    Args:
        agent_data: Agent configuration
        ticker: Stock ticker
        data: Stock data
        
    Returns:
        Signal from analysis
    """
    if Signal is None:
        raise Exception("agent_framework not installed")
    
    if agent_data.type == "rule_based":
        return _run_rule_based_analysis(agent_data, ticker, data)
    else:
        return _run_llm_based_analysis(agent_data, ticker, data)


def _run_rule_based_analysis(agent_data, ticker: str, data: dict) -> Signal:
    """Run rule-based analysis with formula support.
    
    Args:
        agent_data: Agent with rules
        ticker: Stock ticker
        data: Stock data
        
    Returns:
        Signal based on rules
    """
    for rule in agent_data.rules:
        # Check all conditions
        all_conditions_met = True
        
        for condition in rule.conditions:
            # Handle formula-based conditions
            if condition.type == "formula":
                if not _evaluate_formula_condition(condition, data):
                    all_conditions_met = False
                    break
            else:
                # Handle simple conditions
                if not _evaluate_simple_condition(condition, data):
                    all_conditions_met = False
                    break
        
        # If all conditions met, return action
        if all_conditions_met:
            action = rule.action
            confidence = min(action.size / 100.0, 1.0)
            
            return Signal(
                direction=action.action,
                confidence=confidence,
                reasoning=rule.description or f"Rule triggered for {ticker}"
            )
    
    # No rules triggered
    return Signal(
        direction='neutral',
        confidence=0.5,
        reasoning='No rules triggered'
    )


def _evaluate_simple_condition(condition, data: dict) -> bool:
    """Evaluate a simple indicator-based condition.
    
    Args:
        condition: Simple condition
        data: Stock data
        
    Returns:
        True if condition is met
    """
    value = data.get(condition.indicator, 0)
    threshold = condition.value
    operator = condition.operator
    
    if operator == '<':
        return value < threshold
    elif operator == '>':
        return value > threshold
    elif operator == '=':
        return abs(value - threshold) < 0.01  # Float equality with tolerance
    elif operator == '<=':
        return value <= threshold
    elif operator == '>=':
        return value >= threshold
    else:
        return False


def _evaluate_formula_condition(condition, data: dict) -> bool:
    """Evaluate a formula-based condition.
    
    Args:
        condition: Formula condition
        data: Stock data
        
    Returns:
        True if formula condition is met
    """
    # Evaluate formula
    success, result, error = formula_evaluator.evaluate(
        condition.formula,
        condition.variables or {},
        data
    )
    
    if not success:
        print(f"Formula evaluation failed: {error}")
        return False
    
    # Compare result to threshold
    threshold = condition.formula_threshold
    operator = condition.formula_operator
    
    if operator == '<':
        return result < threshold
    elif operator == '>':
        return result > threshold
    elif operator == '=':
        return abs(result - threshold) < 0.01
    elif operator == '<=':
        return result <= threshold
    elif operator == '>=':
        return result >= threshold
    else:
        return False


def _run_llm_based_analysis(agent_data, ticker: str, data: dict) -> Signal:
    """Run LLM-based analysis.
    
    Args:
        agent_data: Agent with LLM config
        ticker: Stock ticker
        data: Stock data
        
    Returns:
        Signal from LLM analysis
    """
    from agent_framework import LLMClient, parse_llm_signal, format_fundamentals
    
    # Create LLM client
    llm = LLMClient(agent_data.llm_config)
    
    # Format prompt
    formatted_data = format_fundamentals(data)
    prompt = f"""Analyze {ticker}:

{formatted_data}

Goal: {agent_data.goal}

Provide your analysis in this format:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your detailed analysis]
"""
    
    # Generate response
    response = llm.generate(prompt)
    
    # Parse signal
    return parse_llm_signal(response)
