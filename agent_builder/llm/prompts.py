"""Prompt Templates for Stock Analysis"""


class PromptTemplates:
    """
    Reusable prompt templates for stock analysis

    Usage:
        system = PromptTemplates.ANALYST_SYSTEM
        prompt = PromptTemplates.stock_analysis("AAPL", fundamentals_data)
    """

    # ========================================================================
    # SYSTEM PROMPTS (Define agent personality/role)
    # ========================================================================

    ANALYST_SYSTEM = """You are an experienced stock market analyst with deep expertise in fundamental analysis, technical indicators, and market sentiment.

Your analysis should be:
- Concise and actionable
- Data-driven and objective
- Clear about confidence levels
- Honest about limitations

Format your response as:
SIGNAL: [BULLISH/BEARISH/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASONING: [Your analysis in 2-3 sentences]"""

    FUNDAMENTAL_ANALYST = """You are a fundamental analyst specializing in financial metrics and company valuations.

Focus on:
- P/E ratio, ROE, profit margins
- Revenue and earnings growth
- Balance sheet health
- Competitive positioning

Be conservative and value-focused."""

    TECHNICAL_ANALYST = """You are a technical analyst specializing in price action and chart patterns.

Focus on:
- Moving averages and trends
- RSI and momentum indicators
- Support and resistance levels
- Volume analysis

Be objective and data-driven."""

    SENTIMENT_ANALYST = """You are a market sentiment analyst specializing in news and social sentiment.

Focus on:
- News sentiment and impact
- Analyst opinions and ratings
- Insider activity signals
- Market positioning

Be aware of noise vs signal."""

    # ========================================================================
    # ANALYSIS PROMPTS
    # ========================================================================

    @staticmethod
    def stock_analysis(ticker: str, data: dict) -> str:
        """
        General stock analysis prompt

        Args:
            ticker: Stock ticker
            data: Dictionary with fundamental/technical/sentiment data

        Returns:
            Formatted prompt string
        """
        return f"""Analyze {ticker} stock and provide a trading signal.

Available Data:
{PromptTemplates._format_data(data)}

Provide your analysis in this format:
SIGNAL: [BULLISH/BEARISH/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASONING: [Your analysis]"""

    @staticmethod
    def fundamental_analysis(ticker: str, fundamentals: dict) -> str:
        """Fundamental analysis prompt"""
        return f"""Analyze {ticker} based on fundamental metrics.

Metrics:
- P/E Ratio: {fundamentals.get('pe_ratio', 'N/A')}
- ROE: {fundamentals.get('roe', 'N/A')}%
- Profit Margin: {fundamentals.get('profit_margin', 'N/A')}%
- Revenue Growth: {fundamentals.get('revenue_growth', 'N/A')}%
- Debt/Equity: {fundamentals.get('debt_to_equity', 'N/A')}

Provide SIGNAL, CONFIDENCE, and REASONING."""

    @staticmethod
    def technical_analysis(ticker: str, prices: list) -> str:
        """Technical analysis prompt"""
        if not prices:
            return f"No price data available for {ticker}"

        latest = prices[0] if prices else {}
        return f"""Analyze {ticker} based on technical indicators.

Current Data:
- Price: ${latest.get('close', 'N/A')}
- SMA 20: ${latest.get('sma_20', 'N/A')}
- SMA 50: ${latest.get('sma_50', 'N/A')}
- RSI: {latest.get('rsi_14', 'N/A')}

Provide SIGNAL, CONFIDENCE, and REASONING."""

    @staticmethod
    def news_analysis(ticker: str, news: list) -> str:
        """News sentiment analysis prompt"""
        if not news:
            return f"No news available for {ticker}"

        headlines = "\\n".join(
            [
                f"- {n.get('headline', '')} (sentiment: {n.get('sentiment_score', 0):.2f})"
                for n in news[:5]
            ]
        )

        return f"""Analyze sentiment for {ticker} based on recent news.

Recent Headlines:
{headlines}

Provide SIGNAL, CONFIDENCE, and REASONING."""

    @staticmethod
    def sec_filing_analysis(ticker: str, filing_text: str) -> str:
        """SEC filing analysis prompt"""
        # Truncate if too long
        text = filing_text[:2000] + "..." if len(filing_text) > 2000 else filing_text

        return f"""Analyze {ticker} based on SEC filing excerpt.

Filing Excerpt:
{text}

Focus on: management tone, risks mentioned, financial outlook.

Provide SIGNAL, CONFIDENCE, and REASONING."""

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    @staticmethod
    def _format_data(data: dict) -> str:
        """Format data dictionary for prompt"""
        lines = []
        for key, value in data.items():
            if isinstance(value, (int, float)):
                lines.append(f"- {key}: {value}")
            elif isinstance(value, str):
                lines.append(f"- {key}: {value}")
        return "\\n".join(lines) if lines else "No data available"

    @staticmethod
    def parse_llm_response(response_text: str) -> dict:
        """
        Parse LLM response into structured data

        Args:
            response_text: Raw LLM response

        Returns:
            Dict with signal, confidence, reasoning
        """
        lines = response_text.strip().split("\\n")
        result = {"signal": "neutral", "confidence": 0.5, "reasoning": response_text}

        for line in lines:
            line = line.strip()
            if line.startswith("SIGNAL:"):
                signal = line.split(":", 1)[1].strip().lower()
                if signal in ["bullish", "bearish", "neutral"]:
                    result["signal"] = signal

            elif line.startswith("CONFIDENCE:"):
                try:
                    conf = float(line.split(":", 1)[1].strip())
                    result["confidence"] = max(0.0, min(1.0, conf))
                except:
                    pass

            elif line.startswith("REASONING:"):
                result["reasoning"] = line.split(":", 1)[1].strip()

        return result
