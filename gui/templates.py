"""Strategy Templates - Pre-built proven investment strategies"""

from typing import Dict, Any


class StrategyTemplates:
    """Pre-built templates for famous investment strategies."""
    
    @staticmethod
    def get_all_templates() -> Dict[str, Dict[str, Any]]:
        """Get all available templates.
        
        Returns:
            Dict of template name to configuration
        """
        return {
            "Warren Buffett Quality": StrategyTemplates.buffett_quality(),
            "Peter Lynch GARP": StrategyTemplates.lynch_garp(),
            "Benjamin Graham Value": StrategyTemplates.graham_value(),
            "Dividend Aristocrat": StrategyTemplates.dividend_aristocrat(),
            "Growth Screener": StrategyTemplates.growth_screener(),
            "Momentum Strategy": StrategyTemplates.momentum_strategy(),
            "Quality at Fair Price": StrategyTemplates.quality_fair_price(),
            "Conservative Income": StrategyTemplates.conservative_income(),
        }
    
    @staticmethod
    def buffett_quality():
        """Warren Buffett's quality investing approach."""
        return {
            "agent_name": "BuffettQualityAgent",
            "description": "Warren Buffett-style quality investing: High ROE, strong margins, low debt",
            "agent_type": "Rule-Based",
            "rule_style": "Score-Based",
            "rules": [{
                "type": "score",
                "criteria": [
                    {"metric": "roe", "operator": ">", "threshold": 15, "points": 2},
                    {"metric": "profit_margin", "operator": ">", "threshold": 15, "points": 2},
                    {"metric": "debt_to_equity", "operator": "<", "threshold": 0.5, "points": 1},
                    {"metric": "revenue_growth", "operator": ">", "threshold": 10, "points": 1},
                    {"metric": "current_ratio", "operator": ">", "threshold": 1.5, "points": 1},
                ],
                "bullish_threshold": 4,
                "bullish_confidence": 0.85,
                "bearish_threshold": 1,
                "bearish_confidence": 0.6
            }],
            "strategy_description": """
**Warren Buffett Quality Strategy**

Focus on high-quality businesses with:
- Strong returns on equity (ROE > 15%)
- High profit margins (> 15%)
- Low debt (Debt/Equity < 0.5)
- Consistent growth (> 10%)
- Financial stability (Current Ratio > 1.5)

Score >= 4: Bullish (high quality)
Score <= 1: Bearish (low quality)
            """
        }
    
    @staticmethod
    def lynch_garp():
        """Peter Lynch's Growth at Reasonable Price strategy."""
        return {
            "agent_name": "LynchGARPAgent",
            "description": "Peter Lynch GARP: Growth at reasonable price with PEG ratio focus",
            "agent_type": "Rule-Based",
            "rule_style": "Advanced Rules",
            "rules": [
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "peg_ratio", "operator": "<", "threshold": 1.0},
                        {"metric": "revenue_growth", "operator": ">", "threshold": 15},
                        {"metric": "profit_margin", "operator": ">", "threshold": 10}
                    ],
                    "logic": "AND",
                    "direction": "bullish",
                    "confidence": 0.9
                },
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "revenue_growth", "operator": ">", "threshold": 25},
                        {"metric": "pe_ratio", "operator": "<", "threshold": 30}
                    ],
                    "logic": "AND",
                    "direction": "bullish",
                    "confidence": 0.75
                }
            ],
            "strategy_description": """
**Peter Lynch GARP Strategy**

Growth at Reasonable Price:
- PEG ratio < 1.0 (growth cheaper than PE suggests)
- Strong revenue growth (> 15%)
- Healthy margins (> 10%)

Also considers high-growth companies (> 25%) if PE < 30
            """
        }
    
    @staticmethod
    def graham_value():
        """Benjamin Graham's value investing principles."""
        return {
            "agent_name": "GrahamValueAgent",
            "description": "Benjamin Graham value investing: Low PE, low PB, margin of safety",
            "agent_type": "Rule-Based",
            "rule_style": "Score-Based",
            "rules": [{
                "type": "score",
                "criteria": [
                    {"metric": "pe_ratio", "operator": "<", "threshold": 15, "points": 2},
                    {"metric": "pb_ratio", "operator": "<", "threshold": 1.5, "points": 1},
                    {"metric": "debt_to_equity", "operator": "<", "threshold": 1.0, "points": 1},
                    {"metric": "current_ratio", "operator": ">", "threshold": 2.0, "points": 1},
                    {"metric": "dividend_yield", "operator": ">", "threshold": 2.0, "points": 1},
                ],
                "bullish_threshold": 3,
                "bullish_confidence": 0.8,
                "bearish_threshold": 0,
                "bearish_confidence": 0.6
            }],
            "strategy_description": """
**Benjamin Graham Value Strategy**

Classic value investing principles:
- Low PE ratio (< 15)
- Low price-to-book (< 1.5)
- Conservative debt (< 1.0)
- Strong liquidity (Current Ratio > 2.0)
- Dividend income (> 2%)

Score >= 3: Strong value candidate
            """
        }
    
    @staticmethod
    def dividend_aristocrat():
        """Dividend growth and income strategy."""
        return {
            "agent_name": "DividendAristocratAgent",
            "description": "Dividend Aristocrat strategy: High yield, stable companies, consistent payments",
            "agent_type": "Rule-Based",
            "rule_style": "Score-Based",
            "rules": [{
                "type": "score",
                "criteria": [
                    {"metric": "dividend_yield", "operator": ">", "threshold": 3.0, "points": 2},
                    {"metric": "debt_to_equity", "operator": "<", "threshold": 1.0, "points": 1},
                    {"metric": "current_ratio", "operator": ">", "threshold": 1.5, "points": 1},
                    {"metric": "roe", "operator": ">", "threshold": 10, "points": 1},
                    {"metric": "revenue_growth", "operator": ">", "threshold": 3, "points": 1},
                ],
                "bullish_threshold": 4,
                "bullish_confidence": 0.85,
                "bearish_threshold": 1,
                "bearish_confidence": 0.6
            }],
            "strategy_description": """
**Dividend Aristocrat Strategy**

Focus on stable dividend payers:
- High dividend yield (> 3%)
- Low debt (< 1.0)
- Financial stability
- Consistent returns (ROE > 10%)
- Modest growth (> 3%)

Ideal for income investors
            """
        }
    
    @staticmethod
    def growth_screener():
        """High-growth company screener."""
        return {
            "agent_name": "GrowthScreenerAgent",
            "description": "Growth screener: High revenue growth with expanding margins",
            "agent_type": "Rule-Based",
            "rule_style": "Advanced Rules",
            "rules": [
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "revenue_growth", "operator": ">", "threshold": 30},
                        {"metric": "profit_margin", "operator": ">", "threshold": 10},
                        {"metric": "roe", "operator": ">", "threshold": 20}
                    ],
                    "logic": "AND",
                    "direction": "bullish",
                    "confidence": 0.9
                },
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "revenue_growth", "operator": "<", "threshold": 5},
                        {"metric": "profit_margin", "operator": "<", "threshold": 5}
                    ],
                    "logic": "OR",
                    "direction": "bearish",
                    "confidence": 0.7
                }
            ],
            "strategy_description": """
**Growth Screener Strategy**

Aggressive growth focus:
- Very high revenue growth (> 30%)
- Expanding margins (> 10%)
- Strong returns (ROE > 20%)

Avoid slow-growers or unprofitable companies
            """
        }
    
    @staticmethod
    def momentum_strategy():
        """Momentum-based strategy."""
        return {
            "agent_name": "MomentumAgent",
            "description": "Momentum strategy: Strong growth trends with quality metrics",
            "agent_type": "Rule-Based",
            "rule_style": "Advanced Rules",
            "rules": [
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "revenue_growth", "operator": ">", "threshold": 20},
                        {"metric": "roe", "operator": ">", "threshold": 15}
                    ],
                    "logic": "AND",
                    "direction": "bullish",
                    "confidence": 0.8
                }
            ],
            "strategy_description": """
**Momentum Strategy**

Ride the winners:
- Strong revenue growth (> 20%)
- Quality returns (ROE > 15%)

Simple but effective for trending markets
            """
        }
    
    @staticmethod
    def quality_fair_price():
        """Quality companies at fair valuations."""
        return {
            "agent_name": "QualityFairPriceAgent",
            "description": "Quality at fair price: Strong fundamentals with reasonable valuation",
            "agent_type": "Rule-Based",
            "rule_style": "Advanced Rules",
            "rules": [
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "quality_score", "operator": ">", "threshold": 20},
                        {"metric": "pe_ratio", "operator": "<", "threshold": 25}
                    ],
                    "logic": "AND",
                    "direction": "bullish",
                    "confidence": 0.85
                },
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "roe", "operator": ">", "threshold": 18},
                        {"metric": "profit_margin", "operator": ">", "threshold": 15},
                        {"metric": "debt_to_equity", "operator": "<", "threshold": 0.8}
                    ],
                    "logic": "AND",
                    "direction": "bullish",
                    "confidence": 0.8
                }
            ],
            "strategy_description": """
**Quality at Fair Price**

Balance quality and valuation:
- High quality score (> 20)
- Reasonable PE (< 25)
- Strong fundamentals (ROE, Margins, Low Debt)

Best of both value and quality
            """
        }
    
    @staticmethod
    def conservative_income():
        """Conservative income-focused strategy."""
        return {
            "agent_name": "ConservativeIncomeAgent",
            "description": "Conservative income: Stable dividends, low risk, defensive positioning",
            "agent_type": "Rule-Based",
            "rule_style": "Advanced Rules",
            "rules": [
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "dividend_yield", "operator": ">", "threshold": 3.5},
                        {"metric": "debt_to_equity", "operator": "<", "threshold": 1.0},
                        {"metric": "current_ratio", "operator": ">", "threshold": 1.5}
                    ],
                    "logic": "AND",
                    "direction": "bullish",
                    "confidence": 0.8
                },
                {
                    "type": "advanced",
                    "conditions": [
                        {"metric": "debt_to_equity", "operator": ">", "threshold": 2.0}
                    ],
                    "logic": "AND",
                    "direction": "bearish",
                    "confidence": 0.7
                }
            ],
            "strategy_description": """
**Conservative Income Strategy**

Safety-first income investing:
- High dividend yield (> 3.5%)
- Low debt (< 1.0)
- Strong liquidity (Current Ratio > 1.5)

Avoid over-leveraged companies
Ideal for retirement portfolios
            """
        }
