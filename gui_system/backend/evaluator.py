"""Unified condition evaluator - eliminates duplicated evaluation logic."""

from typing import Dict, Any, Callable, List
from .models import RuleCondition
from .formula_evaluator import formula_evaluator


class ConditionEvaluator:
    """Unified evaluator for both simple and formula-based conditions."""
    
    # Comparison operators
    OPERATORS: Dict[str, Callable[[float, float], bool]] = {
        '<': lambda a, b: a < b,
        '>': lambda a, b: a > b,
        '<=': lambda a, b: a <= b,
        '>=': lambda a, b: a >= b,
        '=': lambda a, b: abs(a - b) < 0.01,  # Float equality
        '==': lambda a, b: abs(a - b) < 0.01,
    }
    
    def evaluate(self, condition: RuleCondition, data: Dict[str, Any]) -> bool:
        """Evaluate a condition against data.
        
        Args:
            condition: Condition to evaluate
            data: Stock data dictionary
            
        Returns:
            True if condition is met
        """
        if condition.type == 'formula':
            return self._evaluate_formula(condition, data)
        return self._evaluate_simple(condition, data)
    
    def evaluate_all(self, conditions: List[RuleCondition], data: Dict[str, Any]) -> bool:
        """Evaluate multiple conditions with AND logic.
        
        Args:
            conditions: List of conditions
            data: Stock data
            
        Returns:
            True if ALL conditions are met
        """
        return all(self.evaluate(c, data) for c in conditions)
    
    def _evaluate_simple(self, condition: RuleCondition, data: Dict[str, Any]) -> bool:
        """Evaluate simple indicator condition."""
        value = data.get(condition.indicator, 0)
        threshold = condition.value
        operator = condition.operator
        
        if operator not in self.OPERATORS:
            return False
        
        try:
            return self.OPERATORS[operator](value, threshold)
        except (TypeError, ValueError):
            return False
    
    def _evaluate_formula(self, condition: RuleCondition, data: Dict[str, Any]) -> bool:
        """Evaluate formula condition."""
        success, result, error = formula_evaluator.evaluate(
            condition.formula,
            condition.variables or {},
            data
        )
        
        if not success:
            return False
        
        operator = condition.formula_operator
        threshold = condition.formula_threshold
        
        if operator not in self.OPERATORS:
            return False
        
        try:
            return self.OPERATORS[operator](result, threshold)
        except (TypeError, ValueError):
            return False


# Global instance
condition_evaluator = ConditionEvaluator()
