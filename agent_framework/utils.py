"""Shared utility functions."""

from typing import Tuple
from .models import Signal


def parse_llm_signal(response: str, fallback_reasoning: str = "") -> Signal:
    """Parse LLM response into Signal.
    
    Expected format: DIRECTION|CONFIDENCE|REASONING
    Example: bullish|80|Strong growth with healthy margins
    
    Args:
        response: LLM response text
        fallback_reasoning: Reasoning to use if parsing fails
        
    Returns:
        Parsed Signal object
    """
    try:
        parts = response.split('|')
        if len(parts) >= 3:
            direction = parts[0].strip().lower()
            confidence = float(parts[1].strip()) / 100
            reasoning = parts[2].strip()
            
            # Validate direction
            if direction not in ('bullish', 'bearish', 'neutral'):
                direction = 'neutral'
            
            # Clamp confidence
            confidence = max(0.0, min(1.0, confidence))
            
            return Signal(direction=direction, confidence=confidence, reasoning=reasoning)
    except (ValueError, IndexError):
        pass
    
    # Fallback: return neutral signal with full response
    return Signal(
        direction='neutral',
        confidence=0.5,
        reasoning=fallback_reasoning or response[:200]
    )


def format_fundamentals(data: dict) -> str:
    """Format fundamental data for LLM prompts.
    
    Args:
        data: Fundamental data dictionary
        
    Returns:
        Formatted string for LLM context
    """
    return f"""
PE Ratio: {data.get('pe_ratio', 0):.1f}
PB Ratio: {data.get('pb_ratio', 0):.1f}
ROE: {data.get('roe', 0):.1f}%
Profit Margin: {data.get('profit_margin', 0):.1f}%
Revenue Growth: {data.get('revenue_growth', 0):.1f}%
Debt-to-Equity: {data.get('debt_to_equity', 0):.1f}
Current Ratio: {data.get('current_ratio', 0):.1f}
Dividend Yield: {data.get('dividend_yield', 0):.1f}%
Market Cap: ${data.get('market_cap', 0) / 1e9:.1f}B
""".strip()


def calculate_sentiment_score(text: str) -> Tuple[str, float]:
    """Calculate simple sentiment from text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Tuple of (direction, confidence)
    """
    text_lower = text.lower()
    
    positive_words = [
        'growth', 'strong', 'improved', 'increase', 'expansion',
        'profit', 'revenue', 'success', 'opportunity', 'bullish'
    ]
    negative_words = [
        'risk', 'decline', 'challenge', 'decrease', 'competition',
        'loss', 'concern', 'weakness', 'threat', 'bearish'
    ]
    
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)
    
    if pos_count > neg_count + 2:
        direction = 'bullish'
        confidence = min(0.8, 0.5 + (pos_count - neg_count) * 0.05)
    elif neg_count > pos_count + 2:
        direction = 'bearish'
        confidence = min(0.7, 0.5 + (neg_count - pos_count) * 0.05)
    else:
        direction = 'neutral'
        confidence = 0.6
    
    return direction, confidence