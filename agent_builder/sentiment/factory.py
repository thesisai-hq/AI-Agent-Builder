"""
Sentiment Analyzer Factory
"""

from agent_builder.sentiment.base import SentimentAnalyzer
from agent_builder.sentiment.vader import VADERAnalyzer
from agent_builder.sentiment.finbert import FinBERTAnalyzer
from agent_builder.config import Config
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)


def get_sentiment_analyzer(
    analyzer_name: Optional[str] = None,
) -> Optional[SentimentAnalyzer]:
    """
    Get sentiment analyzer based on configuration

    Args:
        analyzer_name: 'vader' or 'finbert' (defaults to config)

    Returns:
        SentimentAnalyzer instance

    Usage:
        analyzer = get_sentiment_analyzer()
        result = analyzer.analyze("Stock prices surge!")
        print(result.sentiment, result.score)
    """
    analyzer_name = analyzer_name or os.getenv("SENTIMENT_ANALYZER", "vader")

    if analyzer_name == "vader":
        logger.info("Using VADER sentiment analyzer (fast, rule-based)")
        return VADERAnalyzer()

    elif analyzer_name == "finbert":
        logger.info("Using FinBERT sentiment analyzer (accurate, ML-based)")
        return FinBERTAnalyzer()

    else:
        logger.warning(
            f"Unknown sentiment analyzer: {analyzer_name}, defaulting to VADER"
        )
        return VADERAnalyzer()
