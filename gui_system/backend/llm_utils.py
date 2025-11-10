"""Shared utilities for LLM operations in GUI system.

Wraps agent_framework utilities to provide consistent interface.
All parsing logic is delegated to agent_framework to ensure consistency.
"""

import re
import logging
from typing import Dict, Tuple, Any
from .constants import MIN_MODEL_NAME_LENGTH, NEUTRAL_DIRECTION, DEFAULT_CONFIDENCE, ERROR_CONFIDENCE

logger = logging.getLogger(__name__)

try:
    from agent_framework.utils import parse_llm_signal, format_fundamentals
    AGENT_FRAMEWORK_AVAILABLE = True
except ImportError:
    AGENT_FRAMEWORK_AVAILABLE = False


def parse_llm_signal_response(response: str) -> Dict[str, Any]:
    """Parse LLM response to extract signal, confidence, and reasoning.
    
    This is a wrapper around agent_framework.utils.parse_llm_signal
    that returns a dictionary for backwards compatibility with GUI code.
    
    Args:
        response: LLM response text
        
    Returns:
        Dictionary with direction, confidence, and reasoning
    """
    if AGENT_FRAMEWORK_AVAILABLE:
        # Use agent_framework parser (preferred)
        signal = parse_llm_signal(response, fallback_reasoning="Analysis completed")
        return {
            'direction': signal.direction,
            'confidence': signal.confidence,
            'reasoning': signal.reasoning
        }
    else:
        # Fallback implementation if agent_framework not installed
        return _fallback_parse_llm_response(response)


def _fallback_parse_llm_response(response: str) -> Dict[str, Any]:
    """Fallback parser when agent_framework is not available.
    
    This should rarely be used - agent_framework should be installed.
    """
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


def validate_llm_config(provider: str, model: str) -> Tuple[bool, str]:
    """Validate LLM configuration.
    
    Args:
        provider: LLM provider name
        model: Model name
        
    Returns:
        (is_valid, error_message)
    """
    # Supported providers
    supported_providers = ['openai', 'anthropic', 'cohere', 'azure']
    
    if provider not in supported_providers:
        return False, f"Unsupported provider: {provider}. Supported: {', '.join(supported_providers)}"
    
    # Basic model validation
    if not model or len(model) < MIN_MODEL_NAME_LENGTH:
        return False, "Invalid model name"
    
    return True, ""


def format_llm_prompt(
    ticker: str,
    data: Dict,
    goal: str,
    tool_results: str = ""
) -> str:
    """Format a standardized prompt for LLM analysis.
    
    Always uses agent_framework formatter for consistency.
    
    Args:
        ticker: Stock ticker
        data: Stock data dictionary
        goal: Agent's investment goal
        tool_results: Results from tool executions (optional)
        
    Returns:
        Formatted prompt string
    """
    if AGENT_FRAMEWORK_AVAILABLE:
        # Use agent_framework formatter (preferred)
        formatted_data = format_fundamentals(data)
    else:
        # Minimal fallback formatting if framework not available
        formatted_data = f"""
PE Ratio: {data.get('pe_ratio', 0):.1f}
PB Ratio: {data.get('pb_ratio', 0):.1f}
ROE: {data.get('roe', 0):.1f}%
Profit Margin: {data.get('profit_margin', 0):.1f}%
Revenue Growth: {data.get('revenue_growth', 0):.1f}%
Market Cap: ${data.get('market_cap', 0) / 1e9:.1f}B
""".strip()
    
    tool_section = f"\n\n{tool_results}" if tool_results else ""
    
    return f"""Analyze {ticker} based on the following goal:
{goal}

{formatted_data}{tool_section}

Provide your investment recommendation in this EXACT format:
SIGNAL: [bullish/bearish/neutral]
CONFIDENCE: [0.0-1.0]
REASONING: [your detailed analysis]
"""
