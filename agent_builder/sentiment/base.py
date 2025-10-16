"""
Base Sentiment Analyzer Interface
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class SentimentResult:
    """Sentiment analysis result"""

    def __init__(
        self,
        text: str,
        sentiment: str,  # positive, negative, neutral
        score: float,  # -1.0 to 1.0
        confidence: float = 1.0,
    ):
        self.text = text
        self.sentiment = sentiment
        self.score = score
        self.confidence = confidence

    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "sentiment": self.sentiment,
            "score": self.score,
            "confidence": self.confidence,
        }


class SentimentAnalyzer(ABC):
    """Abstract base class for sentiment analyzers"""

    @abstractmethod
    def analyze(self, text: str) -> SentimentResult:
        """
        Analyze sentiment of text

        Args:
            text: Text to analyze

        Returns:
            SentimentResult with sentiment classification and score
        """
        pass

    @abstractmethod
    def analyze_batch(self, texts: List[str]) -> List[SentimentResult]:
        """
        Analyze multiple texts

        Args:
            texts: List of texts to analyze

        Returns:
            List of SentimentResult objects
        """
        pass
