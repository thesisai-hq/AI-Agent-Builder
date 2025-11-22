"""Metric Definitions and Validation Rules

Educational tooltips and validation for financial metrics.
Designed for finance students and beginners.
"""

from typing import Dict, Optional, Tuple


class MetricDefinitions:
    """Definitions and validation rules for financial metrics with Finance 101 explanations."""

    @staticmethod
    def get_all_metrics() -> Dict[str, Dict[str, any]]:
        """Get all metric definitions with comprehensive educational tooltips.

        Returns:
            Dict of metric name to {description, min, max, good_range, example, tutorial}
        """
        return {
            "pe_ratio": {
                "name": "PE Ratio (Price-to-Earnings)",
                "description": "Shows how much investors pay for each dollar of company earnings",
                "tooltip": "📚 **What is PE Ratio?**\n"
                "PE Ratio = Stock Price ÷ Earnings Per Share\n\n"
                "**Think of it like:** Buying a rental property. If a house costs $300K and "
                "generates $15K/year in rent, the PE ratio is 20 (you'll recover your investment in 20 years).\n\n"
                "**What the numbers mean:**\n"
                "• Low (5-15): Stock is cheap relative to earnings (value stocks)\n"
                "• Medium (15-25): Fairly priced\n"
                "• High (25+): Expensive - investors expect high growth (growth stocks)\n\n"
                "**Real examples:**\n"
                "• Traditional banks: PE ~10 (mature, slow growth)\n"
                "• Apple, Microsoft: PE ~25-30 (solid growth)\n"
                "• Tesla, Nvidia: PE ~50-80 (high growth expectations)\n\n"
                "**When to use:**\n"
                "• Value investing: Look for PE < 15\n"
                "• Compare similar companies in same industry\n"
                "• Don't use for unprofitable companies (negative earnings)\n\n"
                "**Warren Buffett's view:** Prefers PE < 15 for a margin of safety",
                "min": 0,
                "max": 200,
                "typical_range": (10, 40),
                "good_value": 15,
                "example": "If stock = $50 and EPS = $2, then PE = 25",
                "finance_101": "Lower PE = cheaper stock. But 'cheap' isn't always good - might be cheap for a reason!",
            },
            "pb_ratio": {
                "name": "PB Ratio (Price-to-Book)",
                "description": "Compares stock price to the company's book value (assets minus liabilities)",
                "tooltip": "📚 **What is PB Ratio?**\n"
                "PB Ratio = Stock Price ÷ Book Value Per Share\n\n"
                "**Think of it like:** If a company liquidated today and sold everything, "
                "PB shows how much you'd pay vs what you'd get back.\n\n"
                "**What the numbers mean:**\n"
                "• PB < 1: Trading below book value (assets worth more than market price)\n"
                "• PB = 1-3: Reasonable premium for brand, customers, etc.\n"
                "• PB > 3: High premium - company has valuable intangibles\n\n"
                "**Real examples:**\n"
                "• Banks: PB ~1-1.5 (asset-heavy)\n"
                "• Manufacturers: PB ~2-3\n"
                "• Software companies: PB ~10-20 (few physical assets, high value)\n\n"
                "**When to use:**\n"
                "• Best for asset-heavy businesses (banks, real estate, manufacturing)\n"
                "• Less useful for service/tech companies (assets ≠ value)\n"
                "• Value investing: Look for PB < 1.5\n\n"
                "**Benjamin Graham's approach:** Sought PB < 1 for extra safety margin",
                "min": 0,
                "max": 50,
                "typical_range": (1, 5),
                "good_value": 1.5,
                "example": "If stock = $60 and book value = $40, then PB = 1.5",
                "finance_101": "Low PB = potential value. High PB = market believes assets will grow significantly.",
            },
            "revenue_growth": {
                "name": "Revenue Growth (%)",
                "description": "How fast company sales are growing year-over-year",
                "tooltip": "📚 **What is Revenue Growth?**\n"
                "Revenue Growth = (This Year Revenue - Last Year) ÷ Last Year × 100%\n\n"
                "**Think of it like:** If your lemonade stand made $100 last summer and "
                "$120 this summer, that's 20% growth.\n\n"
                "**What the numbers mean:**\n"
                "• Negative: Sales declining (red flag)\n"
                "• 0-5%: Slow growth (mature companies)\n"
                "• 10-20%: Healthy growth (good businesses)\n"
                "• 20%+: Fast growth (exciting, but can be risky)\n\n"
                "**Real examples:**\n"
                "• Utilities: 2-5% (steady, predictable)\n"
                "• Consumer goods: 5-10%\n"
                "• Tech startups: 30-100% (high growth phase)\n\n"
                "**When to use:**\n"
                "• Growth investing: Seek 15-30% growth\n"
                "• Compare to industry average\n"
                "• Check if growth is sustainable (can they keep it up?)\n\n"
                "**Peter Lynch's advice:** Look for 20-25% growth with low PE (PEG < 1)\n\n"
                "**⚠️ Warning:** High growth often slows down as companies get bigger",
                "min": -50,
                "max": 200,
                "typical_range": (0, 30),
                "good_value": 15,
                "example": "Revenue: $100M → $115M = 15% growth",
                "finance_101": "Higher growth = exciting, but make sure profits grow too (not just revenue)!",
            },
            "profit_margin": {
                "name": "Profit Margin (%)",
                "description": "What percentage of revenue becomes profit after all expenses",
                "tooltip": "📚 **What is Profit Margin?**\n"
                "Profit Margin = Net Income ÷ Revenue × 100%\n\n"
                "**Think of it like:** You sell lemonade for $1. Sugar, cups, lemons cost $0.75. "
                "Your profit margin is 25% ($0.25 profit ÷ $1 revenue).\n\n"
                "**What the numbers mean:**\n"
                "• 0-5%: Thin margins (tough business, lots of competition)\n"
                "• 5-15%: Acceptable margins\n"
                "• 15-25%: Good margins (competitive advantage)\n"
                "• 25%+: Excellent margins (strong pricing power)\n\n"
                "**Real examples:**\n"
                "• Grocery stores: 2-3% (volume business)\n"
                "• Retailers: 5-10%\n"
                "• Software companies: 20-40% (low costs to deliver)\n"
                "• Luxury brands: 15-25%\n\n"
                "**When to use:**\n"
                "• Compare companies in same industry only\n"
                "• Higher margins = better pricing power = stronger business\n"
                "• Check if margins are stable or improving over time\n\n"
                "**Warren Buffett's 'moat':** Companies with high margins have competitive advantages",
                "min": -50,
                "max": 100,
                "typical_range": (5, 25),
                "good_value": 15,
                "example": "Revenue $100M, Net Income $15M = 15% margin",
                "finance_101": "Higher margin = company keeps more of each sales dollar. This is the 'quality' of earnings!",
            },
            "roe": {
                "name": "ROE % (Return on Equity)",
                "description": "How much profit company generates with shareholder money",
                "tooltip": "📚 **What is ROE?**\n"
                "ROE = Net Income ÷ Shareholder Equity × 100%\n\n"
                "**Think of it like:** You invest $1,000 to start a business. If you make "
                "$150 profit this year, your ROE is 15%.\n\n"
                "**What the numbers mean:**\n"
                "• Below 10%: Poor returns (might be better off in bonds)\n"
                "• 10-15%: Acceptable returns\n"
                "• 15-20%: Good returns (quality company)\n"
                "• 20%+: Excellent returns (outstanding business)\n\n"
                "**Real examples:**\n"
                "• Banks: 10-15% (regulated, capital intensive)\n"
                "• Retailers: 15-20%\n"
                "• Tech giants: 30-50% (capital efficient)\n\n"
                "**When to use:**\n"
                "• Quality investing: Seek ROE > 15%\n"
                "• Compare similar companies\n"
                "• Check consistency over 5+ years (sustainable advantage)\n\n"
                "**Warren Buffett's filter:** He typically looks for ROE > 15% sustained over years\n\n"
                "**⚠️ Warning:** Very high ROE (>40%) might use lots of debt - check Debt-to-Equity too!",
                "min": -50,
                "max": 100,
                "typical_range": (10, 25),
                "good_value": 15,
                "example": "Net Income $10M, Equity $50M = 20% ROE",
                "finance_101": "ROE shows management efficiency. High ROE = they're good at turning your money into more money!",
            },
            "debt_to_equity": {
                "name": "Debt-to-Equity Ratio",
                "description": "How much debt company uses compared to shareholder equity",
                "tooltip": "📚 **What is Debt-to-Equity?**\n"
                "Debt-to-Equity = Total Debt ÷ Shareholder Equity\n\n"
                "**Think of it like:** Buying a $200K house with $50K down payment and $150K mortgage. "
                "Your debt-to-equity is 3.0 ($150K ÷ $50K).\n\n"
                "**What the numbers mean:**\n"
                "• 0-0.3: Very conservative (minimal debt)\n"
                "• 0.3-1.0: Moderate (acceptable leverage)\n"
                "• 1.0-2.0: Aggressive (higher risk)\n"
                "• 2.0+: High risk (vulnerable to economic downturns)\n\n"
                "**Real examples:**\n"
                "• Tech companies: 0.1-0.5 (don't need much debt)\n"
                "• Manufacturers: 0.5-1.5\n"
                "• Utilities/Telecoms: 1.0-2.5 (infrastructure needs capital)\n\n"
                "**When to use:**\n"
                "• Risk assessment: Lower = safer\n"
                "• Compare within industry (capital needs vary)\n"
                "• Check if company can cover interest payments\n\n"
                "**The double-edged sword:**\n"
                "• Debt amplifies returns when business is good\n"
                "• Debt amplifies losses when business struggles\n\n"
                "**⚠️ Be cautious:** High debt + economic recession = bankruptcy risk",
                "min": 0,
                "max": 10,
                "typical_range": (0.3, 2.0),
                "good_value": 0.5,
                "example": "Debt $40M, Equity $50M = 0.8 D/E ratio",
                "finance_101": "Lower debt = safer. Company won't struggle if business slows down.",
            },
            "dividend_yield": {
                "name": "Dividend Yield (%)",
                "description": "Annual dividend income as percentage of stock price",
                "tooltip": "📚 **What is Dividend Yield?**\n"
                "Dividend Yield = Annual Dividend ÷ Stock Price × 100%\n\n"
                "**Think of it like:** If you buy a stock for $100 and receive $4 in dividends "
                "this year, your dividend yield is 4%.\n\n"
                "**What the numbers mean:**\n"
                "• 0%: No dividend (company reinvests in growth)\n"
                "• 1-2%: Low yield (growth-focused)\n"
                "• 2-4%: Moderate yield (balanced approach)\n"
                "• 4-6%: High yield (income-focused)\n"
                "• 6%+: Very high yield (⚠️ might be risky - check sustainability!)\n\n"
                "**Real examples:**\n"
                "• Growth stocks (Amazon, Google): 0%\n"
                "• Balanced (Apple, Microsoft): 0.5-1%\n"
                "• Dividend stocks (Coca-Cola, P&G): 2-3%\n"
                "• Utilities, REITs: 4-6%\n\n"
                "**When to use:**\n"
                "• Income investing: Seek 3-5% yield\n"
                "• Retirement portfolios: Focus on dividend income\n"
                "• Check dividend history: 10+ years of increases = reliable\n\n"
                "**The trade-off:**\n"
                "• High dividends = steady income, lower growth\n"
                "• Low/no dividends = higher growth potential\n\n"
                "**⚠️ Warning:** Super high yield (>8%) often means stock price dropped = something's wrong!",
                "min": 0,
                "max": 20,
                "typical_range": (0, 6),
                "good_value": 3,
                "example": "$100 stock, $3 annual dividend = 3% yield",
                "finance_101": "Dividends = cash in your pocket while you hold the stock. Great for patient investors!",
            },
            "current_ratio": {
                "name": "Current Ratio",
                "description": "Can the company pay its short-term bills?",
                "tooltip": "📚 **What is Current Ratio?**\n"
                "Current Ratio = Current Assets ÷ Current Liabilities\n\n"
                "**Think of it like:** You have $1,500 in checking account and owe $1,000 in bills "
                "this month. Your current ratio is 1.5 - you can pay your bills and have cushion.\n\n"
                "**What the numbers mean:**\n"
                "• Below 1.0: Danger zone (can't pay short-term bills)\n"
                "• 1.0-1.5: Acceptable (tight but manageable)\n"
                "• 1.5-2.5: Healthy (comfortable cushion)\n"
                "• Above 3.0: Very safe (but might not be using cash efficiently)\n\n"
                "**Real examples:**\n"
                "• Retailers: 1.0-1.5 (fast inventory turnover)\n"
                "• Manufacturers: 1.5-2.5\n"
                "• Service companies: 1.0-2.0\n\n"
                "**When to use:**\n"
                "• Check financial health before investing\n"
                "• During economic downturns: Higher ratio = safer\n"
                "• Compare to industry standards\n\n"
                "**What it tells you:**\n"
                "• Can company survive if sales slow down?\n"
                "• Will company need emergency funding?\n"
                "• Is bankruptcy risk low?\n\n"
                "**⚠️ Red flag:** Current ratio < 1.0 = liquidity crisis risk",
                "min": 0,
                "max": 10,
                "typical_range": (1.0, 3.0),
                "good_value": 1.5,
                "example": "Assets $150M, Liabilities $100M = 1.5 ratio",
                "finance_101": "Higher ratio = company can weather storms. Think of it as a 'rainy day fund'.",
            },
            "peg_ratio": {
                "name": "PEG Ratio (PE-to-Growth)",
                "description": "Is the stock price justified by its growth rate?",
                "tooltip": "📚 **What is PEG Ratio?**\n"
                "PEG Ratio = PE Ratio ÷ Revenue Growth Rate\n\n"
                "**Think of it like:** You pay PE=30 for a stock growing 30%/year: PEG=1.0 (fair). "
                "But if growth is only 10%/year: PEG=3.0 (expensive for that growth!).\n\n"
                "**What the numbers mean:**\n"
                "• PEG < 1.0: Undervalued relative to growth (bargain)\n"
                "• PEG = 1.0: Fairly valued (growth justifies price)\n"
                "• PEG = 1.0-2.0: Slightly expensive but acceptable\n"
                "• PEG > 2.0: Overvalued (paying too much for growth)\n\n"
                "**Real examples:**\n"
                "• Value trap: PE=10, Growth=2% → PEG=5.0 (cheap for a reason!)\n"
                "• Growth bargain: PE=20, Growth=25% → PEG=0.8 (good deal)\n"
                "• Expensive growth: PE=50, Growth=15% → PEG=3.3 (overpriced)\n\n"
                "**When to use:**\n"
                "• Growth stock investing (Peter Lynch's favorite metric)\n"
                "• Compare similar growth companies\n"
                "• Don't use for slow-growing companies (PEG becomes meaningless)\n\n"
                "**Peter Lynch's rule:** Look for PEG < 1.0 for great growth investments\n\n"
                "**⚠️ Limitation:** Assumes growth continues - but growth rates change!",
                "min": 0,
                "max": 10,
                "typical_range": (0.5, 2.5),
                "good_value": 1.0,
                "example": "PE=25, Growth=20% → PEG=1.25",
                "finance_101": "PEG connects 'price' and 'growth' - the key question every investor asks!",
            },
            "quality_score": {
                "name": "Quality Score (Composite)",
                "description": "Overall business quality combining profitability, efficiency, and safety",
                "tooltip": "📚 **What is Quality Score?**\n"
                "A custom composite metric that combines:\n"
                "• 40% ROE (profitability)\n"
                "• 30% Profit Margin (efficiency)\n"
                "• 30% Safety (inverse of debt)\n\n"
                "**Think of it like:** A 'report card' for the business - combines multiple factors "
                "into one overall grade.\n\n"
                "**What the numbers mean:**\n"
                "• Below 15: Weak fundamentals (risky investment)\n"
                "• 15-25: Decent quality (acceptable)\n"
                "• 25-35: High quality (strong business)\n"
                "• Above 35: Exceptional quality (best-in-class)\n\n"
                "**Real examples:**\n"
                "• Low quality: Struggling retailer with debt issues\n"
                "• Medium quality: Stable manufacturer\n"
                "• High quality: Tech giant with strong margins and low debt\n\n"
                "**When to use:**\n"
                "• Quick quality screening\n"
                "• Compare many companies at once\n"
                "• Quality investing strategy (Buffett-style)\n\n"
                "**The Buffett approach:**\n"
                "Find high-quality businesses (score > 30) trading at reasonable prices\n\n"
                "**Components breakdown:**\n"
                "• High ROE = efficient use of capital\n"
                "• High margins = pricing power & competitive advantage\n"
                "• Low debt = financial safety & flexibility",
                "min": 0,
                "max": 100,
                "typical_range": (10, 40),
                "good_value": 25,
                "example": "ROE=20%, Margin=15%, D/E=0.5 → Score~28",
                "finance_101": "High quality = company that makes money efficiently and safely. These tend to compound wealth over decades!",
            },
        }

    @staticmethod
    def validate_value(metric: str, value: float) -> Tuple[bool, Optional[str]]:
        """Validate a metric value.

        Args:
            metric: Metric name
            value: Value to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        metrics = MetricDefinitions.get_all_metrics()

        if metric not in metrics:
            return True, None  # Unknown metric, don't validate

        metric_info = metrics[metric]
        min_val = metric_info["min"]
        max_val = metric_info["max"]

        # Check range
        if value < min_val:
            return False, f"{metric_info['name']} cannot be less than {min_val}"

        if value > max_val:
            return False, f"{metric_info['name']} cannot be greater than {max_val} (unrealistic)"

        return True, None

    @staticmethod
    def get_suggestion(metric: str, value: float, operator: str) -> Optional[str]:
        """Get suggestion for better rule configuration.

        Args:
            metric: Metric name
            value: Threshold value
            operator: Comparison operator

        Returns:
            Suggestion string or None
        """
        metrics = MetricDefinitions.get_all_metrics()

        if metric not in metrics:
            return None

        metric_info = metrics[metric]
        typical_min, typical_max = metric_info["typical_range"]
        good_value = metric_info["good_value"]

        # Suggest if value is outside typical range
        if operator in ["<", "<="] and value > typical_max:
            return f"💡 Tip: Most {metric_info['name']} values are below {typical_max}. Your threshold of {value} may never trigger."

        if operator in [">", ">="] and value < typical_min:
            return f"💡 Tip: Most {metric_info['name']} values are above {typical_min}. Your threshold of {value} may always trigger."

        # Suggest good values for common patterns
        if operator in ["<", "<="] and metric == "pe_ratio" and value > 20:
            return f"💡 For value investing, consider PE < {good_value} instead of < {value}"

        if operator in [">", ">="] and metric == "revenue_growth" and value < 5:
            return f"💡 For growth investing, consider Growth > {good_value}% instead of > {value}%"

        return None


class RuleValidator:
    """Validates rules for conflicts and issues."""

    @staticmethod
    def check_conflicts(rules: list) -> list:
        """Check for conflicting rules.

        Args:
            rules: List of rule dictionaries

        Returns:
            List of conflict warning messages
        """
        conflicts = []

        # Check for conflicting signals on same metric
        for i, rule1 in enumerate(rules):
            if rule1.get("type") != "simple":
                continue

            metric1 = rule1.get("metric")
            direction1 = rule1.get("direction")

            for j, rule2 in enumerate(rules[i + 1 :], i + 1):
                if rule2.get("type") != "simple":
                    continue

                metric2 = rule2.get("metric")
                direction2 = rule2.get("direction")

                # Same metric, opposite signals
                if metric1 == metric2 and direction1 != direction2:
                    if direction1 in ["bullish", "bearish"] and direction2 in [
                        "bullish",
                        "bearish",
                    ]:
                        conflicts.append(
                            f"⚠️ Rules {i + 1} and {j + 1}: {metric1} triggers both {direction1} and {direction2} signals"
                        )

        return conflicts

    @staticmethod
    def validate_threshold_logic(metric: str, operator: str, threshold: float) -> Optional[str]:
        """Validate that threshold makes logical sense.

        Args:
            metric: Metric name
            operator: Comparison operator
            threshold: Threshold value

        Returns:
            Warning message or None
        """
        # Percentage metrics shouldn't exceed 100%
        percentage_metrics = ["revenue_growth", "profit_margin", "roe", "dividend_yield"]

        if metric in percentage_metrics:
            if threshold > 100:
                return f"⚠️ {metric} is a percentage - values over 100% are very rare"

        # Ratios shouldn't be negative (except growth can be negative)
        if metric not in ["revenue_growth", "profit_margin"] and threshold < 0:
            return f"⚠️ {metric} cannot be negative"

        # PE ratio edge cases
        if metric == "pe_ratio":
            if operator in ["<", "<="] and threshold < 5:
                return f"⚠️ PE < {threshold} is extremely rare - may indicate troubled company"
            if operator in [">", ">="] and threshold > 100:
                return f"⚠️ PE > {threshold} is very high - may never trigger"

        # Debt warnings
        if metric == "debt_to_equity":
            if operator in ["<", "<="] and threshold > 3:
                return f"💡 Debt < {threshold} is very lenient - most companies qualify"
            if operator in [">", ">="] and threshold > 5:
                return f"⚠️ Debt > {threshold} indicates extreme leverage - very risky"

        return None
