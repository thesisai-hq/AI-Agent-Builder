"""Safe formula evaluation for custom analytical models.

Uses simpleeval library for secure mathematical expression evaluation.
No eval() - prevents code injection attacks.
"""

import re
import logging
from typing import Dict, Any, Tuple, Optional
import math
from simpleeval import simple_eval, FunctionNotDefined, NameNotDefined

logger = logging.getLogger(__name__)


class FormulaEvaluator:
    """Safe formula evaluator for financial calculations."""
    
    # Allowed functions
    SAFE_FUNCTIONS = {
        'sqrt': math.sqrt,
        'abs': abs,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'pow': pow,
        'max': max,
        'min': min,
        'round': round,
    }
    
    def validate_formula(
        self,
        formula: str,
        variables: Dict[str, str]
    ) -> Tuple[bool, Optional[str]]:
        """Validate formula syntax and variables.
        
        Args:
            formula: Mathematical formula string
            variables: Variable name to data field mapping
            
        Returns:
            (is_valid, error_message)
        """
        if not formula or not formula.strip():
            return False, "Formula cannot be empty"
        
        # Extract variable names from formula
        var_pattern = r'\b([A-Z_][A-Z0-9_]*)\b'
        formula_vars = set(re.findall(var_pattern, formula))
        
        # Check all variables are defined
        undefined_vars = []
        for var in formula_vars:
            if var not in variables and var not in self.SAFE_FUNCTIONS:
                undefined_vars.append(var)
        
        if undefined_vars:
            return False, f"Undefined variables: {', '.join(undefined_vars)}. Please map them in variables."
        
        # Try to parse with dummy values
        try:
            test_namespace = {var: 1.0 for var in formula_vars if var not in self.SAFE_FUNCTIONS}
            self._safe_eval(formula, test_namespace)
            return True, None
        except NameNotDefined as e:
            return False, f"Undefined name in formula: {e}"
        except FunctionNotDefined as e:
            return False, f"Unknown function: {e}. Available: {', '.join(self.SAFE_FUNCTIONS.keys())}"
        except Exception as e:
            return False, f"Invalid formula syntax: {str(e)}"
    
    def evaluate(
        self,
        formula: str,
        variables: Dict[str, str],
        data: Dict[str, Any]
    ) -> Tuple[bool, Optional[float], Optional[str]]:
        """Evaluate formula with actual data.
        
        Args:
            formula: Mathematical formula
            variables: Variable to data field mapping
            data: Actual stock data
            
        Returns:
            (success, result, error_message)
        """
        try:
            # Build namespace with actual values
            namespace = {}
            
            # Map variables to data values
            for var_name, data_field in variables.items():
                value = data.get(data_field)
                if value is None:
                    logger.warning(f"Data field '{data_field}' not found for variable '{var_name}'")
                    return False, None, f"Data field '{data_field}' not found in stock data"
                
                # Convert to float
                try:
                    namespace[var_name] = float(value)
                except (TypeError, ValueError) as e:
                    logger.error(f"Cannot convert '{data_field}' to number: {value}")
                    return False, None, f"Cannot convert '{data_field}' to number: {value}"
            
            # Evaluate formula
            result = self._safe_eval(formula, namespace)
            logger.info(f"Formula '{formula}' evaluated to {result}")
            return True, float(result), None
        
        except Exception as e:
            logger.error(f"Formula evaluation error: {e}", exc_info=True)
            return False, None, f"Formula evaluation error: {str(e)}"
    
    def _safe_eval(self, expression: str, namespace: Dict[str, float]) -> float:
        """Safely evaluate mathematical expression using simpleeval.
        
        Args:
            expression: Math expression
            namespace: Variable values
            
        Returns:
            Evaluated result
            
        Raises:
            Various simpleeval exceptions for invalid expressions
        """
        result = simple_eval(
            expression,
            names=namespace,
            functions=self.SAFE_FUNCTIONS
        )
        
        return float(result)
    
    def get_formula_description(
        self,
        formula: str,
        variables: Dict[str, str]
    ) -> str:
        """Generate human-readable description of formula.
        
        Args:
            formula: Formula string
            variables: Variable mappings
            
        Returns:
            Human-readable description
        """
        description = formula
        
        # Replace variable names with descriptions
        for var_name, data_field in variables.items():
            # Convert data_field to readable name
            readable = data_field.replace('_', ' ').title()
            description = description.replace(var_name, readable)
        
        return description


# Global evaluator instance
formula_evaluator = FormulaEvaluator()


# Common formula templates
FORMULA_TEMPLATES = {
    "peg_ratio": {
        "name": "PEG Ratio",
        "description": "Price/Earnings to Growth ratio - valuation metric",
        "formula": "PE_RATIO / GROWTH_RATE",
        "variables": {
            "PE_RATIO": "pe_ratio",
            "GROWTH_RATE": "revenue_growth"
        },
        "category": "valuation",
        "example": "PEG < 1 indicates undervalued growth stock"
    },
    "graham_number": {
        "name": "Graham Number",
        "description": "Benjamin Graham's intrinsic value formula",
        "formula": "sqrt(22.5 * EPS * BVPS)",
        "variables": {
            "EPS": "eps",
            "BVPS": "book_value_per_share"
        },
        "category": "valuation",
        "example": "If PRICE < Graham Number, stock may be undervalued"
    },
    "altman_z_score": {
        "name": "Altman Z-Score",
        "description": "Bankruptcy prediction model",
        "formula": "1.2*WC + 1.4*RE + 3.3*EBIT + 0.6*MVE + 1.0*SALES",
        "variables": {
            "WC": "working_capital_to_assets",
            "RE": "retained_earnings_to_assets",
            "EBIT": "ebit_to_assets",
            "MVE": "market_value_to_liabilities",
            "SALES": "sales_to_assets"
        },
        "category": "risk",
        "example": "Z > 3 = Safe, Z < 1.8 = High bankruptcy risk"
    },
    "magic_formula": {
        "name": "Magic Formula (Greenblatt)",
        "description": "Combined earnings yield and return on capital",
        "formula": "(EBIT / EV) * 100 + ROC * 100",
        "variables": {
            "EBIT": "ebit",
            "EV": "enterprise_value",
            "ROC": "return_on_capital"
        },
        "category": "valuation",
        "example": "Higher score = better value + quality combination"
    },
    "sharpe_ratio": {
        "name": "Sharpe Ratio",
        "description": "Risk-adjusted return metric",
        "formula": "(RETURN - RISK_FREE) / VOLATILITY",
        "variables": {
            "RETURN": "annual_return",
            "RISK_FREE": "risk_free_rate",
            "VOLATILITY": "annual_volatility"
        },
        "category": "risk",
        "example": "Higher Sharpe = better risk-adjusted returns"
    },
    "price_to_graham": {
        "name": "Price to Graham Number Ratio",
        "description": "Current price relative to intrinsic value",
        "formula": "PRICE / sqrt(22.5 * EPS * BVPS)",
        "variables": {
            "PRICE": "price",
            "EPS": "eps",
            "BVPS": "book_value_per_share"
        },
        "category": "valuation",
        "example": "< 1 = Undervalued, > 1 = Overvalued"
    }
}
