"""
FinBERT Sentiment Analyzer
"""

from agent_builder.sentiment.base import SentimentAnalyzer, SentimentResult
from typing import List
import logging

logger = logging.getLogger(__name__)


class FinBERTAnalyzer(SentimentAnalyzer):
    """
    FinBERT - BERT fine-tuned on financial text

    Features:
    - ML-based (accurate)
    - Specialized for financial language
    - Understands financial jargon
    - Pre-trained on financial news

    Pros:
    - ✅ Very accurate for financial text
    - ✅ Understands context
    - ✅ Handles complex sentences
    - ✅ Free and open source

    Cons:
    - ⚠️ Slower (100-200ms per text)
    - ⚠️ Requires model download (~500MB)
    - ⚠️ Needs more RAM

    Setup:
        pip install transformers torch
        # Model downloads automatically on first use

    Usage:
        analyzer = FinBERTAnalyzer()
        result = analyzer.analyze("Company reports strong quarterly earnings")
        print(result.sentiment, result.score)
    """

    def __init__(self, model_name: str = "ProsusAI/finbert"):
        """
        Initialize FinBERT

        Models:
        - ProsusAI/finbert (recommended - most popular)
        - yiyanghkust/finbert-tone (alternative)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            import torch

            logger.info(
                f"Loading FinBERT model: {model_name} (first time may take 2-3 minutes)..."
            )

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.eval()  # Set to evaluation mode

            # Check if GPU available
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)

            logger.info(f"✅ FinBERT initialized on {self.device}")

        except ImportError:
            logger.error(
                "transformers not installed. Run: pip install transformers torch"
            )
        except Exception as e:
            logger.error(f"Error loading FinBERT: {e}")

    def analyze(self, text: str) -> SentimentResult:
        """
        Analyze financial text sentiment

        Returns:
            SentimentResult with classification and confidence
        """
        if not self.model or not self.tokenizer:
            return SentimentResult(text, "neutral", 0.0, 0.0)

        try:
            import torch

            # Tokenize
            inputs = self.tokenizer(
                text, return_tensors="pt", truncation=True, max_length=512, padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # FinBERT outputs: [negative, neutral, positive]
            scores = predictions[0].cpu().numpy()

            # Get predicted class
            predicted_class = scores.argmax()
            confidence = float(scores[predicted_class])

            # Map to sentiment
            sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
            sentiment = sentiment_map[predicted_class]

            # Convert to -1 to 1 score
            score = float(scores[2] - scores[0])  # positive - negative

            return SentimentResult(
                text=text, sentiment=sentiment, score=score, confidence=confidence
            )

        except Exception as e:
            logger.error(f"FinBERT analysis error: {e}")
            return SentimentResult(text, "neutral", 0.0, 0.0)

    def analyze_batch(self, texts: List[str]) -> List[SentimentResult]:
        """
        Analyze multiple texts efficiently

        Uses batching for better performance
        """
        if not self.model or not self.tokenizer:
            return [SentimentResult(t, "neutral", 0.0, 0.0) for t in texts]

        try:
            import torch

            # Tokenize batch
            inputs = self.tokenizer(
                texts,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True,
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # Process results
            results = []
            for i, text in enumerate(texts):
                scores = predictions[i].cpu().numpy()
                predicted_class = scores.argmax()
                confidence = float(scores[predicted_class])

                sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
                sentiment = sentiment_map[predicted_class]
                score = float(scores[2] - scores[0])

                results.append(
                    SentimentResult(
                        text=text,
                        sentiment=sentiment,
                        score=score,
                        confidence=confidence,
                    )
                )

            return results

        except Exception as e:
            logger.error(f"FinBERT batch analysis error: {e}")
            return [SentimentResult(t, "neutral", 0.0, 0.0) for t in texts]
