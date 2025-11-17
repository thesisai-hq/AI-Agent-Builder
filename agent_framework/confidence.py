"""Enhanced confidence calculation algorithms for investment signals.

This module provides sophisticated confidence scoring based on:
1. How strongly criteria are met (distance from thresholds)
2. Number of supporting factors
3. Data quality and completeness
4. Signal strength indicators
"""

from typing import Any, Dict, List, Tuple


class ConfidenceCalculator:
    """Calculate confidence scores for investment signals with proper reasoning."""
    
    @staticmethod
    def calculate_rule_confidence(
        metric_value: float,
        threshold: float,
        operator: str,
        base_confidence: float = 0.7
    ) -> Tuple[float, str]:
        """Calculate confidence for a single rule based on how strongly it's met.
        
        Args:
            metric_value: Actual value of the metric
            threshold: Threshold value for the rule
            operator: Comparison operator ('<', '>', '<=', '>=')
            base_confidence: Base confidence when rule is just met
            
        Returns:
            Tuple of (confidence, reasoning)
            
        Example:
            PE ratio is 10, threshold is 15 (looking for PE < 15)
            Distance: 5 points below threshold
            Confidence: Higher because it's well below (not just barely)
        """
        # Calculate how far from threshold
        if operator in ['<', '<=']:
            # Lower is better
            if metric_value >= threshold:
                return 0.0, "Does not meet criterion"
            
            # Calculate distance below threshold
            distance_pct = (threshold - metric_value) / threshold if threshold != 0 else 0
            
        else:  # '>', '>='
            # Higher is better
            if metric_value <= threshold:
                return 0.0, "Does not meet criterion"
            
            # Calculate distance above threshold
            distance_pct = (metric_value - threshold) / max(abs(threshold), 1)
        
        # Scale confidence based on distance
        # Just barely met: base_confidence (e.g., 0.7)
        # Strongly met: up to 0.95
        if distance_pct < 0.05:  # Barely met (within 5%)
            confidence = base_confidence * 0.85  # ~60%
            strength = "barely"
        elif distance_pct < 0.15:  # Moderately met (5-15%)
            confidence = base_confidence  # 70%
            strength = "moderately"
        elif distance_pct < 0.30:  # Strongly met (15-30%)
            confidence = min(0.85, base_confidence * 1.15)  # ~80%
            strength = "strongly"
        else:  # Very strongly met (>30%)
            confidence = min(0.95, base_confidence * 1.3)  # ~90%
            strength = "very strongly"
        
        reasoning = f"Criterion {strength} met ({distance_pct*100:.1f}% from threshold)"
        return confidence, reasoning
    
    @staticmethod
    def calculate_multi_rule_confidence(
        rule_confidences: List[float],
        met_count: int,
        total_count: int
    ) -> Tuple[float, str]:
        """Calculate overall confidence when multiple rules are evaluated.
        
        Args:
            rule_confidences: List of confidence scores for rules that were met
            met_count: Number of rules that were met
            total_count: Total number of rules evaluated
            
        Returns:
            Tuple of (overall_confidence, reasoning)
            
        Algorithm:
            - Base confidence from average of met rules
            - Boost if many rules met (consensus)
            - Penalty if few rules met (weak signal)
        """
        if not rule_confidences:
            return 0.5, "No rules met - neutral by default"
        
        # Average confidence of met rules
        avg_confidence = sum(rule_confidences) / len(rule_confidences)
        
        # Consensus factor: boost if many rules agree
        consensus_pct = met_count / total_count if total_count > 0 else 0
        
        if consensus_pct >= 0.8:  # 80%+ rules met
            consensus_boost = 0.10
            consensus_desc = "strong consensus"
        elif consensus_pct >= 0.5:  # 50-80% rules met
            consensus_boost = 0.05
            consensus_desc = "moderate consensus"
        elif consensus_pct >= 0.3:  # 30-50% rules met
            consensus_boost = 0.0
            consensus_desc = "weak consensus"
        else:  # <30% rules met
            consensus_boost = -0.10
            consensus_desc = "very few rules met"
        
        # Calculate final confidence
        final_confidence = min(0.95, avg_confidence + consensus_boost)
        
        reasoning = (
            f"{met_count}/{total_count} rules met ({consensus_desc}), "
            f"average strength {avg_confidence:.0%}"
        )
        
        return final_confidence, reasoning
    
    @staticmethod
    def calculate_score_based_confidence(
        score: int,
        max_possible_score: int,
        min_possible_score: int,
        threshold: int,
        signal_type: str
    ) -> Tuple[float, str]:
        """Calculate confidence for score-based strategies.
        
        Args:
            score: Actual score achieved
            max_possible_score: Maximum possible score
            min_possible_score: Minimum possible score  
            threshold: Threshold for this signal type
            signal_type: 'bullish' or 'bearish'
            
        Returns:
            Tuple of (confidence, reasoning)
            
        Algorithm:
            - How far past threshold (margin)
            - Score relative to possible range
            - Distance from neutral zone
        """
        # Calculate how far past threshold
        if signal_type == 'bullish':
            margin = score - threshold
            max_margin = max_possible_score - threshold
        else:  # bearish
            margin = threshold - score
            max_margin = threshold - min_possible_score
        
        if margin <= 0:
            return 0.5, "Score at threshold boundary"
        
        # Calculate margin percentage
        margin_pct = margin / max(max_margin, 1) if max_margin > 0 else 0
        
        # Calculate confidence based on margin
        if margin_pct < 0.2:  # Just past threshold
            confidence = 0.60
            strength = "barely"
        elif margin_pct < 0.4:  # Moderately past
            confidence = 0.70
            strength = "moderately"
        elif margin_pct < 0.6:  # Strongly past
            confidence = 0.80
            strength = "strongly"
        else:  # Very strongly past
            confidence = 0.90
            strength = "very strongly"
        
        reasoning = (
            f"Score {score} is {strength} {signal_type} "
            f"(margin: {margin} points, {margin_pct*100:.0f}% of max margin)"
        )
        
        return confidence, reasoning
    
    @staticmethod
    def calculate_data_quality_adjustment(data: Dict[str, Any]) -> Tuple[float, str]:
        """Adjust confidence based on data quality and completeness.
        
        Args:
            data: Financial data dictionary
            
        Returns:
            Tuple of (quality_multiplier, quality_note)
            
        Algorithm:
            - Check for missing/zero values
            - Check for extreme values (likely errors)
            - Reduce confidence if data quality is poor
        """
        key_metrics = [
            'pe_ratio', 'roe', 'profit_margin', 
            'revenue_growth', 'debt_to_equity'
        ]
        
        missing_count = 0
        extreme_count = 0
        
        for metric in key_metrics:
            value = data.get(metric, 0)
            
            # Check if missing or zero
            if value == 0:
                missing_count += 1
                continue
            
            # Check for extreme values (likely errors or special cases)
            if metric == 'pe_ratio' and (value < 0 or value > 200):
                extreme_count += 1
            elif metric == 'roe' and (value < -50 or value > 200):
                extreme_count += 1
            elif metric == 'debt_to_equity' and value > 10:
                extreme_count += 1
        
        # Calculate quality multiplier
        issues = missing_count + extreme_count
        
        if issues == 0:
            return 1.0, "complete data"
        elif issues <= 1:
            return 0.95, "mostly complete data"
        elif issues <= 2:
            return 0.85, "some missing data"
        else:
            return 0.70, "significant missing/unreliable data"
    
    @staticmethod
    def calculate_llm_confidence_adjustment(
        raw_confidence: float,
        reasoning_length: int,
        has_specifics: bool
    ) -> Tuple[float, str]:
        """Adjust LLM confidence based on response quality.
        
        Args:
            raw_confidence: Confidence from LLM
            reasoning_length: Length of reasoning text
            has_specifics: Whether reasoning includes specific numbers/facts
            
        Returns:
            Tuple of (adjusted_confidence, adjustment_note)
            
        Algorithm:
            - Reduce confidence if reasoning is too short (vague)
            - Reduce confidence if no specific facts cited
            - Trust LLM more when detailed and specific
        """
        adjustments = []
        multiplier = 1.0
        
        # Check reasoning length
        if reasoning_length < 50:
            multiplier *= 0.85
            adjustments.append("vague reasoning")
        elif reasoning_length < 100:
            multiplier *= 0.95
        
        # Check for specifics
        if not has_specifics:
            multiplier *= 0.90
            adjustments.append("lacks specific data points")
        
        adjusted = min(0.95, raw_confidence * multiplier)
        
        if adjustments:
            note = f"adjusted down due to: {', '.join(adjustments)}"
        else:
            note = "detailed and specific"
        
        return adjusted, note


class EnhancedConfidenceCalculator:
    """High-level confidence calculator that combines multiple factors."""
    
    @staticmethod
    def for_rule_based_agent(
        rules_evaluated: List[Dict[str, Any]],
        data: Dict[str, Any]
    ) -> Tuple[str, float, str]:
        """Calculate confidence for rule-based agent with full reasoning.
        
        Args:
            rules_evaluated: List of dicts with 'metric', 'value', 'threshold', 
                           'operator', 'met', 'direction'
            data: Financial data dictionary
            
        Returns:
            Tuple of (direction, confidence, detailed_reasoning)
            
        Example:
            rules_evaluated = [
                {
                    'metric': 'pe_ratio',
                    'value': 10,
                    'threshold': 15,
                    'operator': '<',
                    'met': True,
                    'direction': 'bullish',
                    'base_confidence': 0.8
                },
                ...
            ]
        """
        calc = ConfidenceCalculator()
        
        # Calculate individual rule confidences
        rule_confidences = []
        rule_details = []
        
        for rule in rules_evaluated:
            if not rule.get('met', False):
                continue
            
            conf, reason = calc.calculate_rule_confidence(
                rule['value'],
                rule['threshold'],
                rule['operator'],
                rule.get('base_confidence', 0.7)
            )
            
            rule_confidences.append(conf)
            rule_details.append(f"{rule['metric']}: {reason}")
        
        # Calculate multi-rule confidence
        met_count = sum(1 for r in rules_evaluated if r.get('met', False))
        total_count = len(rules_evaluated)
        
        if not rule_confidences:
            return 'neutral', 0.5, "No rules met"
        
        base_conf, consensus_reason = calc.calculate_multi_rule_confidence(
            rule_confidences,
            met_count,
            total_count
        )
        
        # Adjust for data quality
        quality_mult, quality_note = calc.calculate_data_quality_adjustment(data)
        final_conf = base_conf * quality_mult
        
        # Determine direction (majority vote)
        directions = [r['direction'] for r in rules_evaluated if r.get('met', False)]
        if not directions:
            direction = 'neutral'
        else:
            # Count each direction
            bullish_count = directions.count('bullish')
            bearish_count = directions.count('bearish')
            neutral_count = directions.count('neutral')
            
            if bullish_count > bearish_count and bullish_count > neutral_count:
                direction = 'bullish'
            elif bearish_count > bullish_count and bearish_count > neutral_count:
                direction = 'bearish'
            else:
                direction = 'neutral'
        
        # Build detailed reasoning
        reasoning_parts = [
            consensus_reason,
            f"Data quality: {quality_note}",
            "Rule details: " + "; ".join(rule_details[:3])  # Top 3
        ]
        
        detailed_reasoning = " | ".join(reasoning_parts)
        
        return direction, final_conf, detailed_reasoning
    
    @staticmethod
    def for_score_based_agent(
        score: int,
        criteria_evaluated: List[Dict[str, Any]],
        bullish_threshold: int,
        bearish_threshold: int,
        data: Dict[str, Any]
    ) -> Tuple[str, float, str]:
        """Calculate confidence for score-based strategies.
        
        Args:
            score: Total score achieved
            criteria_evaluated: List of criteria with points awarded
            bullish_threshold: Score needed for bullish
            bearish_threshold: Score needed for bearish
            data: Financial data
            
        Returns:
            Tuple of (direction, confidence, detailed_reasoning)
        """
        calc = ConfidenceCalculator()
        
        # Determine direction and threshold margin
        if score >= bullish_threshold:
            direction = 'bullish'
            threshold = bullish_threshold
            max_score = sum(c['points'] for c in criteria_evaluated if c['points'] > 0)
            min_score = bullish_threshold
        elif score <= bearish_threshold:
            direction = 'bearish'
            threshold = bearish_threshold
            max_score = bearish_threshold
            min_score = sum(c['points'] for c in criteria_evaluated if c['points'] < 0)
        else:
            direction = 'neutral'
            # Calculate how close to thresholds
            distance_to_bullish = abs(score - bullish_threshold)
            distance_to_bearish = abs(score - bearish_threshold)
            
            # Confidence based on how far from action thresholds
            if min(distance_to_bullish, distance_to_bearish) <= 1:
                return 'neutral', 0.55, f"Score {score} is borderline (1 point from threshold)"
            else:
                return 'neutral', 0.65, f"Score {score} clearly in neutral zone"
        
        # Calculate score-based confidence
        base_conf, score_reason = calc.calculate_score_based_confidence(
            score,
            max_score,
            min_score,
            threshold,
            direction
        )
        
        # Adjust for data quality
        quality_mult, quality_note = calc.calculate_data_quality_adjustment(data)
        final_conf = base_conf * quality_mult
        
        # Count how many criteria contributed
        met_criteria = [c for c in criteria_evaluated if c.get('met', False)]
        total_criteria = len(criteria_evaluated)
        
        # Build detailed reasoning
        reasoning = (
            f"{score_reason} | "
            f"{len(met_criteria)}/{total_criteria} criteria met | "
            f"Data: {quality_note}"
        )
        
        return direction, final_conf, reasoning


# Convenience functions for backward compatibility

def calculate_simple_confidence(
    metric_value: float,
    threshold: float,
    operator: str
) -> float:
    """Simple confidence calculation (backward compatible).
    
    Returns just the confidence value without reasoning.
    """
    conf, _ = ConfidenceCalculator.calculate_rule_confidence(
        metric_value, threshold, operator
    )
    return conf if conf > 0 else 0.5


def enhanced_parse_llm_signal(response: str, fallback_reasoning: str = "") -> 'Signal':
    """Enhanced LLM signal parsing with confidence validation.
    
    Improves upon basic parse_llm_signal by:
    - Validating confidence makes sense
    - Checking reasoning quality
    - Adjusting confidence if reasoning is weak
    """
    from .utils import parse_llm_signal  # Original parser
    from .models import Signal
    
    # Use original parser
    signal = parse_llm_signal(response, fallback_reasoning)
    
    # Check reasoning quality
    has_numbers = any(char.isdigit() for char in signal.reasoning)
    has_metrics = any(
        word in signal.reasoning.lower() 
        for word in ['pe', 'roe', 'margin', 'growth', 'debt', 'ratio']
    )
    has_specifics = has_numbers and has_metrics
    
    # Adjust confidence based on reasoning quality
    calc = ConfidenceCalculator()
    adjusted_conf, note = calc.calculate_llm_confidence_adjustment(
        signal.confidence,
        len(signal.reasoning),
        has_specifics
    )
    
    # Return adjusted signal if confidence changed significantly
    if abs(adjusted_conf - signal.confidence) > 0.05:
        return Signal(
            direction=signal.direction,
            confidence=adjusted_conf,
            reasoning=f"{signal.reasoning} [Confidence {note}]",
            metadata=signal.metadata
        )
    
    return signal


# Example usage functions

def example_rule_confidence():
    """Example: How confidence changes with distance from threshold."""
    calc = ConfidenceCalculator()
    
    print("Example: PE Ratio Rule (Buy if PE < 15)")
    print("=" * 60)
    
    test_cases = [
        (14.5, "Just barely under threshold"),
        (12.0, "Moderately under"),
        (10.0, "Strongly under"),
        (5.0, "Very strongly under"),
    ]
    
    for pe_value, desc in test_cases:
        conf, reason = calc.calculate_rule_confidence(
            metric_value=pe_value,
            threshold=15.0,
            operator='<',
            base_confidence=0.7
        )
        print(f"\nPE = {pe_value:5.1f} | {desc}")
        print(f"  Confidence: {conf:.0%}")
        print(f"  Reasoning: {reason}")


def example_multi_rule():
    """Example: Multiple rules with consensus."""
    calc = ConfidenceCalculator()
    
    # Simulate 3 rules: 2 strongly met, 1 barely met
    rule_confidences = [0.85, 0.90, 0.62]  # Individual confidences
    
    conf, reason = calc.calculate_multi_rule_confidence(
        rule_confidences,
        met_count=3,
        total_count=5  # 3 met out of 5 total rules
    )
    
    print("\nExample: Multi-Rule Agent")
    print("=" * 60)
    print(f"Rules met: 3/5")
    print(f"Individual confidences: {rule_confidences}")
    print(f"\nFinal Confidence: {conf:.0%}")
    print(f"Reasoning: {reason}")


if __name__ == "__main__":
    print("Confidence Calculation Examples")
    print("=" * 60)
    
    example_rule_confidence()
    print("\n" + "=" * 60)
    example_multi_rule()
