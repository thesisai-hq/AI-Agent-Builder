"""Stock analysis routes using agents with yfinance data.

No database dependency - uses yfinance directly for live data.
Supports tool usage for LLM agents.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..models import AnalysisRequest, AnalysisResponse
from ..storage import storage
from ..formula_evaluator import formula_evaluator
from ..data_service import data_service
from ..tools import tool_registry


router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    """Analyze a stock using an agent with live data from yfinance.
    
    Args:
        request: Analysis request with ticker and agent_id
        
    Returns:
        Analysis result with signal
    """
    # Get agent
    agent_data = storage.get_agent(request.agent_id)
    if not agent_data:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Validate ticker
    ticker_upper = request.ticker.upper()
    if not data_service.validate_ticker(ticker_upper):
        raise HTTPException(
            status_code=404, 
            detail=f"Ticker '{ticker_upper}' not found or has no data. Please check the symbol."
        )
    
    # Fetch stock data from yfinance (no database needed!)
    try:
        data = data_service.get_stock_data(ticker_upper)
        if not data:
            raise HTTPException(
                status_code=404, 
                detail=f"Could not fetch data for {ticker_upper}. The ticker may be delisted or invalid."
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch data from Yahoo Finance: {str(e)}"
        )
    
    # Run analysis
    try:
        signal = _run_agent_analysis(agent_data, ticker_upper, data)
        
        return AnalysisResponse(
            ticker=ticker_upper,
            agent_id=agent_data.id,
            agent_name=agent_data.name,
            direction=signal['direction'],
            confidence=signal['confidence'],
            reasoning=signal['reasoning'],
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )


def _run_agent_analysis(agent_data, ticker: str, data: dict) -> dict:
    """Run agent analysis logic.
    
    Args:
        agent_data: Agent configuration
        ticker: Stock ticker
        data: Stock data from yfinance
        
    Returns:
        Signal dictionary with direction, confidence, reasoning
    """
    if agent_data.type == "rule_based":
        return _run_rule_based_analysis(agent_data, ticker, data)
    else:
        return _run_llm_based_analysis(agent_data, ticker, data)


def _run_rule_based_analysis(agent_data, ticker: str, data: dict) -> dict:
    """Run rule-based analysis with formula support.
    
    Args:
        agent_data: Agent with rules
        ticker: Stock ticker
        data: Stock data
        
    Returns:
        Signal dictionary
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
            
            return {
                'direction': action.action,
                'confidence': confidence,
                'reasoning': rule.description or f"Rule triggered for {ticker}"
            }
    
    # No rules triggered
    return {
        'direction': 'neutral',
        'confidence': 0.5,
        'reasoning': 'No rules triggered'
    }


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


def _run_llm_based_analysis(agent_data, ticker: str, data: dict) -> dict:
    """Run LLM-based analysis with tool support.
    
    Args:
        agent_data: Agent with LLM config
        ticker: Stock ticker
        data: Stock data
        
    Returns:
        Signal dictionary
    """
    try:
        from agent_framework import LLMClient, LLMConfig
    except ImportError:
        return {
            'direction': 'neutral',
            'confidence': 0.0,
            'reasoning': 'Error: agent_framework not installed. Run: pip install -e ../'
        }
    
    # Get enabled tools
    enabled_tools = agent_data.llm_config.tools or []
    
    # Gather tool data if tools are enabled
    tool_data_sections = []
    
    if 'web_search' in enabled_tools:
        news = tool_registry.execute('web_search', ticker=ticker)
        tool_data_sections.append(f"=== RECENT NEWS ===\n{news}\n")
    
    if 'financial_data' in enabled_tools:
        additional_data = tool_registry.execute('financial_data', ticker=ticker)
        tool_data_sections.append(f"=== ADDITIONAL METRICS ===\n{additional_data}\n")
    
    if 'document_analysis' in enabled_tools:
        doc_analysis = tool_registry.execute('document_analysis', ticker=ticker)
        tool_data_sections.append(f"=== EARNINGS DATA ===\n{doc_analysis}\n")
    
    # Build tool data string
    tool_data_str = "\n".join(tool_data_sections) if tool_data_sections else ""
    
    # Create LLM client with proper config
    try:
        llm_cfg = LLMConfig(
            provider=agent_data.llm_config.provider,
            model=agent_data.llm_config.model,
            temperature=agent_data.llm_config.temperature,
            max_tokens=agent_data.llm_config.max_tokens,
            system_prompt=agent_data.llm_config.system_prompt or f"""You are a professional financial analyst.

Goal: {agent_data.goal}

Analyze the provided stock data and respond in this EXACT format:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your detailed analysis]
"""
        )
        llm = LLMClient(llm_cfg)
    except Exception as e:
        return {
            'direction': 'neutral',
            'confidence': 0.0,
            'reasoning': f'Error initializing LLM: {str(e)}'
        }
    
    # Format basic data
    formatted_data = _format_data_for_llm(data)
    
    # Add tool descriptions if tools enabled
    tool_descriptions = tool_registry.get_tool_descriptions(enabled_tools)
    
    # Build comprehensive prompt
    prompt = f"""{formatted_data}

{tool_data_str}

Based on the above data, provide your investment recommendation for {ticker}.
{tool_descriptions}

Respond in this EXACT format:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your detailed analysis]
"""
    
    # Call LLM using chat() method
    try:
        response = llm.chat(prompt)
        
        # Parse the response to extract signal
        signal = _parse_llm_response(response)
        
        return signal
    except Exception as e:
        return {
            'direction': 'neutral',
            'confidence': 0.0,
            'reasoning': f'LLM analysis failed: {str(e)}'
        }


def _parse_llm_response(response: str) -> dict:
    """Parse LLM response to extract signal, confidence, and reasoning.
    
    Args:
        response: Raw LLM response text
        
    Returns:
        Dictionary with direction, confidence, reasoning
    """
    import re
    
    # Default values
    direction = 'neutral'
    confidence = 0.5
    reasoning = response
    
    # Try to parse structured response
    signal_match = re.search(r'SIGNAL:\s*(bullish|bearish|neutral)', response, re.IGNORECASE)
    if signal_match:
        direction = signal_match.group(1).lower()
    
    conf_match = re.search(r'CONFIDENCE:\s*([0-9.]+)', response, re.IGNORECASE)
    if conf_match:
        try:
            confidence = float(conf_match.group(1))
            confidence = max(0.0, min(1.0, confidence))  # Clamp to 0-1
        except ValueError:
            pass
    
    reason_match = re.search(r'REASONING:\s*(.+)', response, re.IGNORECASE | re.DOTALL)
    if reason_match:
        reasoning = reason_match.group(1).strip()
    
    return {
        'direction': direction,
        'confidence': confidence,
        'reasoning': reasoning
    }


def _format_data_for_llm(data: dict) -> str:
    """Format stock data for LLM consumption.
    
    Args:
        data: Stock data dictionary
        
    Returns:
        Formatted string for LLM
    """
    lines = [
        "=== FUNDAMENTAL DATA ===",
        f"Company: {data.get('company_name', 'Unknown')}",
        f"Sector: {data.get('sector', 'Unknown')}",
        f"Industry: {data.get('industry', 'Unknown')}",
        "",
        "Valuation:",
        f"  Price: ${data.get('price', 0):.2f}",
        f"  Market Cap: ${data.get('market_cap', 0):,.0f}",
        f"  P/E Ratio: {data.get('pe_ratio', 0):.2f}",
        f"  P/B Ratio: {data.get('pb_ratio', 0):.2f}",
        f"  PEG Ratio: {data.get('peg_ratio', 0):.2f}",
        "",
        "Profitability:",
        f"  Profit Margin: {data.get('profit_margin', 0):.2f}%",
        f"  ROE: {data.get('roe', 0):.2f}%",
        f"  ROA: {data.get('roa', 0):.2f}%",
        "",
        "Growth:",
        f"  Revenue Growth: {data.get('revenue_growth', 0):.2f}%",
        f"  Earnings Growth: {data.get('earnings_growth', 0):.2f}%",
        "",
        "Dividends:",
        f"  Dividend Yield: {data.get('dividend_yield', 0):.2f}%",
        f"  Payout Ratio: {data.get('payout_ratio', 0):.2f}%",
        "",
        "Financial Health:",
        f"  Debt/Equity: {data.get('debt_to_equity', 0):.2f}",
        f"  Current Ratio: {data.get('current_ratio', 0):.2f}",
    ]
    
    return '\n'.join(lines)
