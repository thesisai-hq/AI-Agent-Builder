"""Metric Definitions and Validation Rules

Educational tooltips and validation for financial metrics.
"""

from typing import Dict, Tuple, Optional


class MetricDefinitions:
    """Definitions and validation rules for financial metrics."""
    
    @staticmethod
    def get_all_metrics() -> Dict[str, Dict[str, any]]:
        """Get all metric definitions with tooltips and validation.
        
        Returns:
            Dict of metric name to {description, min, max, good_range, example}
        """
        return {
            "pe_ratio": {
                "name": "PE Ratio",
                "description": "Price-to-Earnings ratio. Measures how expensive a stock is relative to its earnings.",
                "tooltip": "PE Ratio = Stock Price / Earnings Per Share\n\n"
                          "💡 Lower = Cheaper\n"
                          "Good: < 15 (undervalued)\n"
                          "Fair: 15-25 (reasonably priced)\n"
                          "Expensive: > 25 (overvalued)\n\n"
                          "Example: PE=20 means you pay $20 for every $1 of earnings",
                "min": 0,
                "max": 200,
                "typical_range": (10, 40),
                "good_value": 15,
                "example": "Apple: ~28, Tesla: ~65, Banks: ~10"
            },
            "pb_ratio": {
                "name": "PB Ratio",
                "description": "Price-to-Book ratio. Compares stock price to book value (assets - liabilities).",
                "tooltip": "PB Ratio = Stock Price / Book Value Per Share\n\n"
                          "💡 Lower = Better value\n"
                          "Good: < 1.5 (trading below book value)\n"
                          "Fair: 1.5-3.0\n"
                          "High: > 3.0 (premium to assets)\n\n"
                          "Example: PB=2 means paying $2 for every $1 of net assets",
                "min": 0,
                "max": 50,
                "typical_range": (1, 5),
                "good_value": 1.5,
                "example": "Value stocks: 1-2, Tech stocks: 5-15"
            },
            "revenue_growth": {
                "name": "Revenue Growth",
                "description": "Year-over-year revenue growth rate (percentage).",
                "tooltip": "Revenue Growth = (This Year - Last Year) / Last Year × 100%\n\n"
                          "💡 Higher = Better growth\n"
                          "Slow: < 5% (mature companies)\n"
                          "Good: 10-20% (solid growth)\n"
                          "High: > 20% (fast growing)\n\n"
                          "Example: 15% means revenue increased by 15% vs last year",
                "min": -50,
                "max": 200,
                "typical_range": (0, 30),
                "good_value": 15,
                "example": "Tech: 15-30%, Utilities: 2-5%"
            },
            "profit_margin": {
                "name": "Profit Margin",
                "description": "Net profit as percentage of revenue. Shows profitability.",
                "tooltip": "Profit Margin = Net Income / Revenue × 100%\n\n"
                          "💡 Higher = More profitable\n"
                          "Low: < 5% (thin margins)\n"
                          "Good: 10-20% (healthy)\n"
                          "Excellent: > 20% (very profitable)\n\n"
                          "Example: 15% means $15 profit from every $100 in sales",
                "min": -50,
                "max": 100,
                "typical_range": (5, 25),
                "good_value": 15,
                "example": "Software: 20-30%, Retail: 2-5%"
            },
            "roe": {
                "name": "ROE (Return on Equity)",
                "description": "Return on equity. Shows how efficiently company uses shareholder money.",
                "tooltip": "ROE = Net Income / Shareholder Equity × 100%\n\n"
                          "💡 Higher = Better returns\n"
                          "Poor: < 10% (inefficient)\n"
                          "Good: 15-20% (solid returns)\n"
                          "Excellent: > 20% (outstanding)\n\n"
                          "Example: ROE=18% means earning $18 for every $100 of equity",
                "min": -50,
                "max": 100,
                "typical_range": (10, 25),
                "good_value": 15,
                "example": "Tech: 25-40%, Banks: 10-15%"
            },
            "debt_to_equity": {
                "name": "Debt-to-Equity",
                "description": "Ratio of debt to shareholder equity. Measures financial leverage.",
                "tooltip": "Debt-to-Equity = Total Debt / Shareholder Equity\n\n"
                          "💡 Lower = Less risky\n"
                          "Conservative: < 0.5 (very safe)\n"
                          "Moderate: 0.5-1.5 (acceptable)\n"
                          "High: > 1.5 (risky)\n\n"
                          "Example: D/E=0.8 means $0.80 debt for every $1 equity",
                "min": 0,
                "max": 10,
                "typical_range": (0.3, 2.0),
                "good_value": 0.5,
                "example": "Tech: 0.2-0.5, Utilities: 1.0-2.0"
            },
            "dividend_yield": {
                "name": "Dividend Yield",
                "description": "Annual dividend as percentage of stock price. Shows income return.",
                "tooltip": "Dividend Yield = Annual Dividend / Stock Price × 100%\n\n"
                          "💡 Higher = More income\n"
                          "None: 0% (growth companies)\n"
                          "Moderate: 2-4% (balanced)\n"
                          "High: > 4% (income focus)\n\n"
                          "Example: 3% yield on $100 stock = $3/year dividend",
                "min": 0,
                "max": 20,
                "typical_range": (0, 6),
                "good_value": 3,
                "example": "Growth stocks: 0-1%, Value stocks: 3-5%"
            },
            "current_ratio": {
                "name": "Current Ratio",
                "description": "Current assets divided by current liabilities. Measures short-term liquidity.",
                "tooltip": "Current Ratio = Current Assets / Current Liabilities\n\n"
                          "💡 Higher = More liquid\n"
                          "Risky: < 1.0 (can't pay bills)\n"
                          "Acceptable: 1.0-2.0\n"
                          "Safe: > 2.0 (strong liquidity)\n\n"
                          "Example: 1.5 means $1.50 in assets for every $1 of debt",
                "min": 0,
                "max": 10,
                "typical_range": (1.0, 3.0),
                "good_value": 1.5,
                "example": "Manufacturing: 1.5-2.0, Retail: 1.0-1.5"
            },
            "peg_ratio": {
                "name": "PEG Ratio",
                "description": "PE ratio divided by growth rate. Shows if growth justifies the price.",
                "tooltip": "PEG Ratio = PE Ratio / Revenue Growth\n\n"
                          "💡 Lower = Better value for growth\n"
                          "Undervalued: < 1.0 (growth is cheap)\n"
                          "Fair: 1.0-2.0\n"
                          "Overvalued: > 2.0 (paying too much for growth)\n\n"
                          "Example: PE=25, Growth=25% → PEG=1.0 (fairly valued)",
                "min": 0,
                "max": 10,
                "typical_range": (0.5, 2.5),
                "good_value": 1.0,
                "example": "Calculated: PE / Growth"
            },
            "quality_score": {
                "name": "Quality Score",
                "description": "Composite quality metric combining ROE, margins, and debt.",
                "tooltip": "Quality Score = (ROE × 0.4) + (Margin × 0.3) + (1/Debt × 0.3)\n\n"
                          "💡 Higher = Better quality\n"
                          "Low: < 15 (weak fundamentals)\n"
                          "Good: 20-30 (solid company)\n"
                          "Excellent: > 30 (outstanding quality)\n\n"
                          "Example: Weights profitability, efficiency, safety",
                "min": 0,
                "max": 100,
                "typical_range": (10, 40),
                "good_value": 25,
                "example": "Calculated from ROE, Margin, Debt"
            }
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
        min_val = metric_info['min']
        max_val = metric_info['max']
        
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
        typical_min, typical_max = metric_info['typical_range']
        good_value = metric_info['good_value']
        
        # Suggest if value is outside typical range
        if operator in ['<', '<='] and value > typical_max:
            return f"💡 Tip: Most {metric_info['name']} values are below {typical_max}. Your threshold of {value} may never trigger."
        
        if operator in ['>', '>='] and value < typical_min:
            return f"💡 Tip: Most {metric_info['name']} values are above {typical_min}. Your threshold of {value} may always trigger."
        
        # Suggest good values for common patterns
        if operator in ['<', '<='] and metric == 'pe_ratio' and value > 20:
            return f"💡 For value investing, consider PE < {good_value} instead of < {value}"
        
        if operator in ['>', '>='] and metric == 'revenue_growth' and value < 5:
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
            if rule1.get('type') != 'simple':
                continue
                
            metric1 = rule1.get('metric')
            direction1 = rule1.get('direction')
            
            for j, rule2 in enumerate(rules[i+1:], i+1):
                if rule2.get('type') != 'simple':
                    continue
                    
                metric2 = rule2.get('metric')
                direction2 = rule2.get('direction')
                
                # Same metric, opposite signals
                if metric1 == metric2 and direction1 != direction2:
                    if direction1 in ['bullish', 'bearish'] and direction2 in ['bullish', 'bearish']:
                        conflicts.append(
                            f"⚠️ Rules {i+1} and {j+1}: {metric1} triggers both {direction1} and {direction2} signals"
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
        percentage_metrics = ['revenue_growth', 'profit_margin', 'roe', 'dividend_yield']
        
        if metric in percentage_metrics:
            if threshold > 100:
                return f"⚠️ {metric} is a percentage - values over 100% are very rare"
        
        # Ratios shouldn't be negative (except growth can be negative)
        if metric not in ['revenue_growth', 'profit_margin'] and threshold < 0:
            return f"⚠️ {metric} cannot be negative"
        
        # PE ratio edge cases
        if metric == 'pe_ratio':
            if operator in ['<', '<='] and threshold < 5:
                return f"⚠️ PE < {threshold} is extremely rare - may indicate troubled company"
            if operator in ['>', '>='] and threshold > 100:
                return f"⚠️ PE > {threshold} is very high - may never trigger"
        
        # Debt warnings
        if metric == 'debt_to_equity':
            if operator in ['<', '<='] and threshold > 3:
                return f"💡 Debt < {threshold} is very lenient - most companies qualify"
            if operator in ['>', '>='] and threshold > 5:
                return f"⚠️ Debt > {threshold} indicates extreme leverage - very risky"
        
        return None
