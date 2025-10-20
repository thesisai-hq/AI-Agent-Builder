"""
Advanced Fundamental Analyst - Configuration File

All tunable parameters in one place for easy customization.
Modify these values to adjust the analyst's behavior.

Each parameter includes:
- Default value
- Valid range
- Justification
- Reference
"""

from dataclasses import dataclass, field
from typing import Dict


# ============================================================================
# STAGE 1: QUANTITATIVE ANALYSIS THRESHOLDS
# ============================================================================


@dataclass
class ValuationThresholds:
    """
    P/E Ratio thresholds for scoring

    Source: Graham & Dodd (2009), Damodaran (2012)
    Valid range: 5-100 (practical limits)
    """

    excellent: float = 15.0  # Below historical market average
    good: float = 20.0  # Traditional value threshold
    fair: float = 25.0  # S&P 500 average
    expensive: float = 35.0  # Historical underperformance threshold

    def score(self, pe_ratio: float) -> int:
        """Convert P/E to score (0-10)"""
        if pe_ratio < self.excellent:
            return 10
        elif pe_ratio < self.good:
            return 8
        elif pe_ratio < self.fair:
            return 6
        elif pe_ratio < self.expensive:
            return 4
        else:
            return 2


@dataclass
class ProfitabilityThresholds:
    """
    ROE and Profit Margin thresholds

    Source: Buffett criteria, Piotroski (2000)
    Valid range: 0-100 (percentage)
    """

    roe_excellent: float = 20.0  # Top quartile S&P 500
    roe_good: float = 15.0  # Buffett's minimum for "moat"
    roe_acceptable: float = 10.0  # Industry average

    margin_excellent: float = 20.0  # Significant competitive advantage
    margin_good: float = 15.0  # Above-average profitability
    margin_acceptable: float = 10.0  # Industry average

    def score(self, roe: float, profit_margin: float) -> int:
        """Convert profitability to score (0-10)"""
        score = 0

        # ROE component (0-5)
        if roe > self.roe_excellent:
            score += 5
        elif roe > self.roe_good:
            score += 4
        elif roe > self.roe_acceptable:
            score += 3
        else:
            score += 1

        # Margin component (0-5)
        if profit_margin > self.margin_excellent:
            score += 5
        elif profit_margin > self.margin_good:
            score += 4
        elif profit_margin > self.margin_acceptable:
            score += 3
        else:
            score += 1

        return score


@dataclass
class GrowthThresholds:
    """
    Revenue growth thresholds

    Source: Chan et al. (2003), S&P 500 percentiles
    Valid range: -50 to 100 (percentage)
    """

    exceptional: float = 20.0  # Top 10% of companies
    strong: float = 15.0  # Above GDP + inflation
    good: float = 10.0  # Sustainable growth
    moderate: float = 5.0  # Keeps pace with inflation

    def score(self, revenue_growth: float) -> int:
        """Convert growth to score (0-10)"""
        if revenue_growth > self.exceptional:
            return 10
        elif revenue_growth > self.strong:
            return 8
        elif revenue_growth > self.good:
            return 7
        elif revenue_growth > self.moderate:
            return 5
        elif revenue_growth > 0:
            return 3
        else:
            return 1


@dataclass
class FinancialHealthThresholds:
    """
    Debt and liquidity thresholds

    Source: Altman (1968), Accounting standards
    Valid range: 0-10 (ratio)
    """

    debt_excellent: float = 0.5  # Conservative leverage
    debt_good: float = 1.0  # Moderate leverage
    debt_concerning: float = 1.5  # High leverage

    liquidity_excellent: float = 2.0  # 2:1 working capital rule
    liquidity_good: float = 1.5  # Adequate liquidity
    liquidity_minimum: float = 1.0  # Bare minimum

    def score(self, debt_to_equity: float, current_ratio: float) -> int:
        """Convert financial health to score (0-10)"""
        score = 0

        # Debt component (0-5)
        if debt_to_equity < self.debt_excellent:
            score += 5
        elif debt_to_equity < self.debt_good:
            score += 4
        elif debt_to_equity < self.debt_concerning:
            score += 3
        else:
            score += 1

        # Liquidity component (0-5)
        if current_ratio > self.liquidity_excellent:
            score += 5
        elif current_ratio > self.liquidity_good:
            score += 4
        elif current_ratio > self.liquidity_minimum:
            score += 3
        else:
            score += 1

        return score


@dataclass
class IncomeThresholds:
    """
    Dividend yield thresholds

    Source: Siegel (2005), Market averages
    Valid range: 0-15 (percentage)
    """

    high: float = 3.0  # Above market average
    moderate: float = 2.0  # Near market average
    low: float = 1.0  # Some income

    def score(self, dividend_yield: float) -> int:
        """Convert dividend to score (0-8)"""
        if dividend_yield > self.high:
            return 8
        elif dividend_yield > self.moderate:
            return 6
        elif dividend_yield > self.low:
            return 4
        else:
            return 2


# ============================================================================
# STAGE 1: SCORING WEIGHTS
# ============================================================================


@dataclass
class QuantitativeWeights:
    """
    Weights for overall quantitative score

    Source: Empirical testing, Financial theory
    Must sum to 1.0
    """

    valuation: float = 0.25  # Entry price / return potential
    profitability: float = 0.30  # Most important long-term (HIGHEST)
    growth: float = 0.25  # Future cash flow driver
    financial_health: float = 0.15  # Downside protection
    income: float = 0.05  # Nice-to-have (LOWEST)

    def __post_init__(self):
        total = sum(
            [
                self.valuation,
                self.profitability,
                self.growth,
                self.financial_health,
                self.income,
            ]
        )
        assert abs(total - 1.0) < 0.01, f"Weights must sum to 1.0, got {total}"

    # Preset configurations
    @classmethod
    def growth_focused(cls):
        """For growth stock portfolios"""
        return cls(
            valuation=0.15,
            profitability=0.25,
            growth=0.40,  # Emphasize growth
            financial_health=0.15,
            income=0.05,
        )

    @classmethod
    def value_focused(cls):
        """For value stock portfolios"""
        return cls(
            valuation=0.40,  # Emphasize valuation
            profitability=0.25,
            growth=0.15,
            financial_health=0.15,
            income=0.05,
        )

    @classmethod
    def income_focused(cls):
        """For dividend/income portfolios"""
        return cls(
            valuation=0.20,
            profitability=0.25,
            growth=0.10,
            financial_health=0.20,
            income=0.25,  # Emphasize dividend
        )


@dataclass
class QuantitativeSignalThresholds:
    """
    Score thresholds for quantitative signal

    Source: Percentile-based (empirical)
    Valid range: 0-10
    """

    bullish: float = 7.5  # Top quartile (75th percentile)
    bearish: float = 5.5  # Bottom quartile threshold

    # Between bearish and bullish = neutral


# ============================================================================
# STAGE 2: RAG CONFIGURATION
# ============================================================================


@dataclass
class RAGConfiguration:
    """
    RAG system parameters

    Source: Empirical testing, Performance benchmarks
    """

    # Embedding configuration
    embedding_provider: str = "sentence-transformers"
    embedding_model: str = "all-MiniLM-L6-v2"  # 384 dims, fast, good quality

    # Vector store configuration
    vectorstore: str = "faiss"  # Fastest option

    # Search parameters
    top_k_per_query: int = 2  # Excerpts per query (balance coverage/quality)
    max_total_excerpts: int = 8  # Total excerpts to LLM (context limit)

    # Search queries - covers key aspects
    search_queries: list = field(
        default_factory=lambda: [
            "revenue growth strategy and business expansion plans",
            "competitive advantages and market position",
            "key risks and challenges facing the business",
            "profitability trends and margin improvements",
        ]
    )

    # LLM parameters for theme extraction
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2"
    llm_temperature: float = 0.3  # Low for consistency
    llm_max_tokens: int = 500  # Sufficient for themes


@dataclass
class KeywordFallback:
    """
    Keyword-based fallback when LLM unavailable

    Source: Loughran & McDonald (2011) financial sentiment
    """

    positive_keywords: list = field(
        default_factory=lambda: [
            "growth",
            "expansion",
            "strong",
            "increased",
            "improved",
            "competitive advantage",
            "innovation",
            "market leader",
            "accelerating",
            "momentum",
            "opportunity",
        ]
    )

    negative_keywords: list = field(
        default_factory=lambda: [
            "risk",
            "challenge",
            "decline",
            "decreased",
            "competition",
            "uncertainty",
            "headwind",
            "pressure",
            "concern",
            "volatility",
        ]
    )

    # Multiplier for signal threshold
    # 1.5 means positive_count must be 50% higher than negative
    signal_multiplier: float = 1.5  # Accounts for negativity bias


# ============================================================================
# STAGE 3: AI SYNTHESIS CONFIGURATION
# ============================================================================


@dataclass
class SynthesisConfiguration:
    """
    LLM synthesis parameters

    Source: OpenAI best practices, Empirical testing
    """

    llm_provider: str = "ollama"
    llm_model: str = "llama3.2"
    temperature: float = 0.3  # Low for analytical consistency
    max_tokens: int = 600  # Enough for detailed reasoning

    # System prompt
    system_prompt: str = """You are an experienced stock market analyst with deep expertise in fundamental analysis.

Your analysis should be:
- Concise and actionable
- Data-driven and objective
- Clear about confidence levels
- Honest about limitations

Format your response as:
SIGNAL: [BULLISH/BEARISH/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASONING: [Your analysis in 2-3 sentences]"""


# ============================================================================
# STAGE 4: FINAL RECOMMENDATION WEIGHTS
# ============================================================================


@dataclass
class FinalWeights:
    """
    Weights for final ensemble

    Source: Empirical optimization (Sharpe ratio maximization)
    Must sum to 1.0
    """

    quantitative: float = 0.40  # Objective, proven track record
    qualitative: float = 0.30  # RAG + LLM analysis
    ai_synthesis: float = 0.30  # Full integration

    # Fallback weights when LLM unavailable
    quantitative_fallback: float = 0.60
    qualitative_fallback: float = 0.40

    def __post_init__(self):
        total = self.quantitative + self.qualitative + self.ai_synthesis
        assert abs(total - 1.0) < 0.01, f"Weights must sum to 1.0, got {total}"

        fallback_total = self.quantitative_fallback + self.qualitative_fallback
        assert abs(fallback_total - 1.0) < 0.01, f"Fallback weights must sum to 1.0"

    # Preset configurations
    @classmethod
    def trust_quant(cls):
        """Higher trust in quantitative metrics"""
        return cls(quantitative=0.50, qualitative=0.25, ai_synthesis=0.25)

    @classmethod
    def trust_ai(cls):
        """Higher trust in AI analysis"""
        return cls(quantitative=0.30, qualitative=0.30, ai_synthesis=0.40)

    @classmethod
    def balanced(cls):
        """Equal weighting (for comparison)"""
        return cls(quantitative=0.33, qualitative=0.33, ai_synthesis=0.34)


@dataclass
class FinalSignalThresholds:
    """
    Final signal determination thresholds

    Source: Backtesting optimization, Loss aversion theory
    Valid range: 0.0-1.0
    """

    bullish: float = 0.65  # Need 65%+ for buy signal
    bearish: float = 0.35  # Below 35% for sell signal

    # Conservative vs. Aggressive presets
    @classmethod
    def conservative(cls):
        """Harder to get bullish signal"""
        return cls(bullish=0.75, bearish=0.25)

    @classmethod
    def aggressive(cls):
        """Easier to get bullish signal"""
        return cls(bullish=0.55, bearish=0.35)

    @classmethod
    def balanced(cls):
        """Symmetric thresholds"""
        return cls(bullish=0.60, bearish=0.40)


# ============================================================================
# SECTOR-SPECIFIC CONFIGURATIONS
# ============================================================================


@dataclass
class SectorConfig:
    """Sector-specific threshold adjustments"""

    name: str
    valuation_thresholds: ValuationThresholds
    growth_thresholds: GrowthThresholds
    weights: QuantitativeWeights


# Predefined sector configurations
SECTOR_CONFIGS = {
    "Technology": SectorConfig(
        name="Technology",
        valuation_thresholds=ValuationThresholds(
            excellent=25.0,  # Higher P/E acceptable
            good=35.0,
            fair=45.0,
            expensive=60.0,
        ),
        growth_thresholds=GrowthThresholds(
            exceptional=30.0,  # Higher growth expected
            strong=20.0,
            good=15.0,
            moderate=10.0,
        ),
        weights=QuantitativeWeights.growth_focused(),
    ),
    "Utilities": SectorConfig(
        name="Utilities",
        valuation_thresholds=ValuationThresholds(
            excellent=12.0, good=15.0, fair=18.0, expensive=22.0  # Lower P/E expected
        ),
        growth_thresholds=GrowthThresholds(
            exceptional=10.0,  # Lower growth expected
            strong=7.0,
            good=5.0,
            moderate=3.0,
        ),
        weights=QuantitativeWeights.income_focused(),
    ),
    "Financial Services": SectorConfig(
        name="Financial Services",
        valuation_thresholds=ValuationThresholds(
            excellent=10.0, good=12.0, fair=15.0, expensive=20.0
        ),
        growth_thresholds=GrowthThresholds(
            exceptional=15.0, strong=10.0, good=7.0, moderate=5.0
        ),
        weights=QuantitativeWeights(),  # Default
    ),
}


# ============================================================================
# MASTER CONFIGURATION
# ============================================================================


@dataclass
class AnalystConfiguration:
    """
    Master configuration for Advanced Fundamental Analyst

    Usage:
        config = AnalystConfiguration()
        config = AnalystConfiguration.aggressive()
        config = AnalystConfiguration.for_sector("Technology")
    """

    # Stage 1: Quantitative
    valuation: ValuationThresholds = field(default_factory=ValuationThresholds)
    profitability: ProfitabilityThresholds = field(
        default_factory=ProfitabilityThresholds
    )
    growth: GrowthThresholds = field(default_factory=GrowthThresholds)
    financial_health: FinancialHealthThresholds = field(
        default_factory=FinancialHealthThresholds
    )
    income: IncomeThresholds = field(default_factory=IncomeThresholds)

    quant_weights: QuantitativeWeights = field(default_factory=QuantitativeWeights)
    quant_signal: QuantitativeSignalThresholds = field(
        default_factory=QuantitativeSignalThresholds
    )

    # Stage 2: RAG
    rag: RAGConfiguration = field(default_factory=RAGConfiguration)
    keywords: KeywordFallback = field(default_factory=KeywordFallback)

    # Stage 3: AI Synthesis
    synthesis: SynthesisConfiguration = field(default_factory=SynthesisConfiguration)

    # Stage 4: Final
    final_weights: FinalWeights = field(default_factory=FinalWeights)
    final_signal: FinalSignalThresholds = field(default_factory=FinalSignalThresholds)

    # Presets
    @classmethod
    def conservative(cls):
        """Conservative configuration (harder to get bullish)"""
        return cls(
            final_signal=FinalSignalThresholds.conservative(),
            quant_weights=QuantitativeWeights(),  # Default weights
        )

    @classmethod
    def aggressive(cls):
        """Aggressive configuration (easier to get bullish)"""
        return cls(
            final_signal=FinalSignalThresholds.aggressive(),
            quant_weights=QuantitativeWeights.growth_focused(),
        )

    @classmethod
    def for_sector(cls, sector: str):
        """Sector-specific configuration"""
        if sector in SECTOR_CONFIGS:
            sector_config = SECTOR_CONFIGS[sector]
            return cls(
                valuation=sector_config.valuation_thresholds,
                growth=sector_config.growth_thresholds,
                quant_weights=sector_config.weights,
            )
        else:
            # Default configuration
            return cls()

    def to_dict(self) -> Dict:
        """Export configuration as dictionary"""
        return {
            "quantitative": {
                "valuation": vars(self.valuation),
                "profitability": vars(self.profitability),
                "growth": vars(self.growth),
                "weights": vars(self.quant_weights),
            },
            "rag": vars(self.rag),
            "synthesis": vars(self.synthesis),
            "final": {
                "weights": vars(self.final_weights),
                "thresholds": vars(self.final_signal),
            },
        }


# ============================================================================
# ADDITIONAL HELPER CLASSES
# ============================================================================


@dataclass
class FinancialHealthThresholds:
    """Financial health thresholds (needed for completeness)"""

    debt_excellent: float = 0.5
    debt_good: float = 1.0
    debt_concerning: float = 1.5
    liquidity_excellent: float = 2.0
    liquidity_good: float = 1.5
    liquidity_minimum: float = 1.0

    def score(self, debt_to_equity: float, current_ratio: float) -> int:
        score = 0
        if debt_to_equity < self.debt_excellent:
            score += 5
        elif debt_to_equity < self.debt_good:
            score += 4
        elif debt_to_equity < self.debt_concerning:
            score += 3
        else:
            score += 1

        if current_ratio > self.liquidity_excellent:
            score += 5
        elif current_ratio > self.liquidity_good:
            score += 4
        elif current_ratio > self.liquidity_minimum:
            score += 3
        else:
            score += 1

        return score


@dataclass
class IncomeThresholds:
    """Income thresholds (dividend)"""

    high: float = 3.0
    moderate: float = 2.0
    low: float = 1.0

    def score(self, dividend_yield: float) -> int:
        if dividend_yield > self.high:
            return 8
        elif dividend_yield > self.moderate:
            return 6
        elif dividend_yield > self.low:
            return 4
        else:
            return 2


@dataclass
class GrowthThresholds:
    """Growth thresholds"""

    exceptional: float = 20.0
    strong: float = 15.0
    good: float = 10.0
    moderate: float = 5.0

    def score(self, revenue_growth: float) -> int:
        if revenue_growth > self.exceptional:
            return 10
        elif revenue_growth > self.strong:
            return 8
        elif revenue_growth > self.good:
            return 7
        elif revenue_growth > self.moderate:
            return 5
        elif revenue_growth > 0:
            return 3
        else:
            return 1


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    """
    Examples of using different configurations
    """

    print("=" * 70)
    print("CONFIGURATION EXAMPLES")
    print("=" * 70)

    # Example 1: Default configuration
    print("\n1️⃣ Default Configuration:")
    config_default = AnalystConfiguration()
    print(f"   Valuation weight: {config_default.quant_weights.valuation}")
    print(f"   Bullish threshold: {config_default.final_signal.bullish}")

    # Example 2: Conservative configuration
    print("\n2️⃣ Conservative Configuration:")
    config_conservative = AnalystConfiguration.conservative()
    print(f"   Bullish threshold: {config_conservative.final_signal.bullish}")
    print(f"   (Harder to get bullish signal)")

    # Example 3: Growth-focused
    print("\n3️⃣ Growth-Focused Configuration:")
    config_growth = AnalystConfiguration.aggressive()
    print(f"   Growth weight: {config_growth.quant_weights.growth}")
    print(f"   Valuation weight: {config_growth.quant_weights.valuation}")

    # Example 4: Technology sector
    print("\n4️⃣ Technology Sector Configuration:")
    config_tech = AnalystConfiguration.for_sector("Technology")
    print(f"   P/E 'excellent' threshold: {config_tech.valuation.excellent}")
    print(f"   (Higher P/E acceptable for tech)")

    # Example 5: Custom configuration
    print("\n5️⃣ Custom Configuration:")
    config_custom = AnalystConfiguration(
        quant_weights=QuantitativeWeights(
            valuation=0.30,
            profitability=0.30,
            growth=0.30,
            financial_health=0.10,
            income=0.0,  # No dividend requirement
        ),
        final_signal=FinalSignalThresholds(
            bullish=0.70, bearish=0.30  # Very selective
        ),
    )
    print(f"   Custom weights: {vars(config_custom.quant_weights)}")

    # Export configuration
    print("\n6️⃣ Export Configuration as Dict:")
    config_dict = config_default.to_dict()
    print(f"   Keys: {list(config_dict.keys())}")

    print("\n" + "=" * 70)
    print("✅ Configuration examples complete")
    print("=" * 70 + "\n")
