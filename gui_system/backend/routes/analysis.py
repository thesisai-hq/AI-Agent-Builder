"""Stock analysis routes - REFACTORED with unified evaluator and formatters."""

from fastapi import APIRouter
from datetime import datetime

from ..models import AnalysisRequest, AnalysisResponse, DataQualityInfo
from ..storage import storage
from ..data_service import data_service
from ..tools import tool_registry
from ..evaluator import condition_evaluator
from ..formatters import DataFormatter
from ..errors import AgentNotFoundError, InvalidTickerError, DataFetchError, AnalysisError


router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    """Analyze a stock using an agent.
    
    Args:
        request: Analysis request with ticker and agent_id
        
    Returns:
        Analysis result with signal and data used
    """
    # Get agent
    agent_data = storage.get_agent(request.agent_id)
    if not agent_data:
        raise AgentNotFoundError(request.agent_id)
    
    # Validate ticker
    ticker_upper = request.ticker.upper()
    if not data_service.validate_ticker(ticker_upper):
        raise InvalidTickerError(ticker_upper)
    
    # Fetch stock data
    try:
        data = data_service.get_stock_data(ticker_upper)
        if not data:
            raise DataFetchError(ticker_upper, "No data returned from source")
    except Exception as e:
        raise DataFetchError(ticker_upper, str(e))
    
    # Analyze data quality
    data_quality = _analyze_data_quality(data)
    
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
            timestamp=datetime.now(),
            data_used=data,
            data_quality=data_quality
        )
    except Exception as e:
        raise AnalysisError(str(e), {"ticker": ticker_upper, "agent_id": request.agent_id})


def _analyze_data_quality(data: dict) -> DataQualityInfo:
    """Analyze data quality and identify missing/zero fields."""
    key_fields = [
        'pe_ratio', 'pb_ratio', 'peg_ratio',
        'dividend_yield', 'payout_ratio',
        'revenue_growth', 'earnings_growth',
        'profit_margin', 'roe', 'roa',
        'debt_to_equity', 'current_ratio', 'quick_ratio',
        'eps', 'book_value_per_share', 'price', 'market_cap'
    ]
    
    missing_fields = []
    zero_value_fields = []
    populated_fields = 0
    
    for field in key_fields:
        value = data.get(field)
        if value is None:
            missing_fields.append(field)
        elif value == 0 or value == 0.0:
            zero_value_fields.append(field)
        else:
            populated_fields += 1
    
    return DataQualityInfo(
        total_fields=len(key_fields),
        populated_fields=populated_fields,
        missing_fields=missing_fields,
        zero_value_fields=zero_value_fields,
        data_source="yfinance"
    )


def _run_agent_analysis(agent_data, ticker: str, data: dict) -> dict:
    """Run agent analysis logic."""
    if agent_data.type == "rule_based":
        return _run_rule_based_analysis(agent_data, ticker, data)
    else:
        return _run_llm_based_analysis(agent_data, ticker, data)


def _run_rule_based_analysis(agent_data, ticker: str, data: dict) -> dict:
    """Run rule-based analysis using unified evaluator.
    
    SIMPLIFIED: Uses condition_evaluator instead of duplicate logic.
    """
    for rule in agent_data.rules:
        # ONE LINE - evaluates all conditions
        if condition_evaluator.evaluate_all(rule.conditions, data):
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


def _run_llm_based_analysis(agent_data, ticker: str, data: dict) -> dict:
    """Run LLM-based analysis with tool support."""
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
    
    # Execute tools if enabled
    tool_data_str = ""
    if enabled_tools:
        tool_data_sections = []
        
        for tool_name in enabled_tools:
            try:
                result = tool_registry.execute(tool_name, ticker=ticker)
                tool_data_sections.append(f"=== {tool_name.upper()} ===\n{result}")
            except Exception as e:
                tool_data_sections.append(f"=== {tool_name.upper()} ===\nError: {e}")
        
        tool_data_str = "\n\n".join(tool_data_sections)
    
    # Create LLM client
    try:
        llm_cfg = LLMConfig(
            provider=agent_data.llm_config.provider,
            model=agent_data.llm_config.model,
            temperature=agent_data.llm_config.temperature,
            max_tokens=agent_data.llm_config.max_tokens,
            system_prompt=agent_data.llm_config.system_prompt or _get_default_system_prompt(agent_data)
        )
        llm = LLMClient(llm_cfg)
    except Exception as e:
        return {
            'direction': 'neutral',
            'confidence': 0.0,
            'reasoning': f'Error initializing LLM: {str(e)}'
        }
    
    # Format data using DataFormatter
    formatted_data = DataFormatter.for_llm(data)
    
    # Build prompt
    prompt = f"""{formatted_data}

{tool_data_str}

Based on the above data, provide your investment recommendation for {ticker}.

Respond in this EXACT format:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your detailed analysis]
"""
    
    # Call LLM
    try:
        response = llm.chat(prompt)
        return _parse_llm_response(response)
    except Exception as e:
        return {
            'direction': 'neutral',
            'confidence': 0.0,
            'reasoning': f'LLM analysis failed: {str(e)}'
        }


def _get_default_system_prompt(agent_data) -> str:
    """Generate default system prompt."""
    return f"""You are a professional financial analyst.

Goal: {agent_data.goal}

Analyze the provided stock data and respond in this EXACT format:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your detailed analysis]
"""


def _parse_llm_response(response: str) -> dict:
    """Parse LLM response to extract signal, confidence, and reasoning."""
    import re
    
    # Default values
    direction = 'neutral'
    confidence = 0.5
    reasoning = response
    
    # Parse structured response
    signal_match = re.search(r'SIGNAL:\s*(bullish|bearish|neutral)', response, re.IGNORECASE)
    if signal_match:
        direction = signal_match.group(1).lower()
    
    conf_match = re.search(r'CONFIDENCE:\s*([0-9.]+)', response, re.IGNORECASE)
    if conf_match:
        try:
            confidence = max(0.0, min(1.0, float(conf_match.group(1))))
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
