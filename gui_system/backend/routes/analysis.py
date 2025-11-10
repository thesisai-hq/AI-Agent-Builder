"""Stock analysis routes with unified LLM handling and RAG support."""

import logging
from fastapi import APIRouter
from datetime import datetime

from ..models import AnalysisRequest, AnalysisResponse, DataQualityInfo
from ..storage import storage
from ..data_service import data_service
from ..tools import tool_registry
from ..evaluator import condition_evaluator
from ..llm_utils import parse_llm_signal_response, format_llm_prompt
from ..errors import AgentNotFoundError, InvalidTickerError, DataFetchError, AnalysisError
from ..constants import NEUTRAL_DIRECTION, DEFAULT_CONFIDENCE, ERROR_CONFIDENCE

logger = logging.getLogger(__name__)


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
    
    # Fetch stock data (validation is implicit - will fail if ticker invalid)
    ticker_upper = request.ticker.upper()
    try:
        data = data_service.get_stock_data(ticker_upper)
        if not data:
            raise InvalidTickerError(ticker_upper)
    except Exception as e:
        # If fetch fails, ticker is invalid or service unavailable
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


def _create_error_signal(reason: str) -> dict:
    """Create standardized error signal response.
    
    Args:
        reason: Error description
        
    Returns:
        Error signal dictionary
    """
    return {
        'direction': NEUTRAL_DIRECTION,
        'confidence': ERROR_CONFIDENCE,
        'reasoning': reason
    }


def _run_rule_based_analysis(agent_data, ticker: str, data: dict) -> dict:
    """Run rule-based analysis using unified evaluator."""
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
        'direction': NEUTRAL_DIRECTION,
        'confidence': DEFAULT_CONFIDENCE,
        'reasoning': 'No rules triggered'
    }


def _run_llm_based_analysis(agent_data, ticker: str, data: dict) -> dict:
    """Run LLM-based analysis with tool support including RAG."""
    try:
        from agent_framework import LLMClient, LLMConfig
    except ImportError:
        return _create_error_signal('Error: agent_framework not installed. Run: pip install -e ../')
    
    # Get enabled tools
    enabled_tools = agent_data.llm_config.tools or []
    
    # Execute tools if enabled
    tool_data_str = ""
    if enabled_tools:
        tool_data_sections = []
        
        for tool_name in enabled_tools:
            try:
                logger.info(f"Executing tool: {tool_name} for {ticker}")
                
                # Pass agent_id for document_analysis tool (RAG needs it)
                if tool_name == 'document_analysis':
                    result = tool_registry.execute(
                        tool_name,
                        ticker=ticker,
                        agent_id=agent_data.id  # Required for RAG
                    )
                else:
                    result = tool_registry.execute(tool_name, ticker=ticker)
                
                tool_data_sections.append(f"=== {tool_name.upper()} ===")
                tool_data_sections.append(result)
                tool_data_sections.append("")  # Empty line for separation
                
            except Exception as e:
                logger.error(f"Tool {tool_name} execution failed: {e}", exc_info=True)
                tool_data_sections.append(f"=== {tool_name.upper()} ===")
                tool_data_sections.append(f"Error: {e}")
                tool_data_sections.append("")  # Empty line for separation
        
        tool_data_str = "\n".join(tool_data_sections)
    
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
        return _create_error_signal(f'Error initializing LLM: {str(e)}')
    
    # Format prompt using shared utility
    prompt = format_llm_prompt(
        ticker=ticker,
        data=data,
        goal=agent_data.goal,
        tool_results=tool_data_str
    )
    
    # Call LLM
    try:
        response = llm.chat(prompt)
        # Use shared parser
        return parse_llm_signal_response(response)
    except Exception as e:
        return _create_error_signal(f'LLM analysis failed: {str(e)}')


def _get_default_system_prompt(agent_data) -> str:
    """Generate default system prompt."""
    return f"""You are a professional financial analyst.

Goal: {agent_data.goal}

Analyze the provided stock data and respond in this EXACT format:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your detailed analysis]
"""
