"""
VADER Sentiment Analyzer
"""

from agent_builder.sentiment.base import SentimentAnalyzer, SentimentResult
from typing import List
import logging

logger = logging.getLogger(__name__)


class VADERAnalyzer(SentimentAnalyzer):
    """
    VADER (Valence Aware Dictionary and sEntiment Reasoner)

    Features:
    - Rule-based (fast)
    - Good for social media and news
    - No model loading required
    - Works offline

    Pros:
    - ✅ Very fast (< 1ms per text)
    - ✅ No setup required
    - ✅ Good for short texts
    - ✅ Handles emojis and slang

    Cons:
    - ⚠️ Less accurate than ML models
    - ⚠️ Not specialized for finance

    Setup:
        pip install vaderSentiment

    Usage:
        analyzer = VADERAnalyzer()
        result = analyzer.analyze("Stock prices surge on earnings beat")
        print(result.sentiment, result.score)
    """

    def __init__(self):
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

            self.vader = SentimentIntensityAnalyzer()
            logger.info("✅ VADER sentiment analyzer initialized")
        except ImportError:
            logger.error(
                "vaderSentiment not installed. Run: pip install vaderSentiment"
            )
            self.vader = None

    def analyze(self, text: str) -> SentimentResult:
        """
        Analyze sentiment using VADER

        Returns score from -1.0 (very negative) to 1.0 (very positive)
        """
        if not self.vader:
            return SentimentResult(text, "neutral", 0.0, 0.0)

        # Get VADER scores
        scores = self.vader.polarity_scores(text)

        # Compound score: -1 to 1
        compound = scores["compound"]

        # Classify sentiment
        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return SentimentResult(
            text=text, sentiment=sentiment, score=compound, confidence=abs(compound)
        )

    def analyze_batch(self, texts: List[str]) -> List[SentimentResult]:
        """Analyze multiple texts"""
        return [self.analyze(text) for text in texts]
