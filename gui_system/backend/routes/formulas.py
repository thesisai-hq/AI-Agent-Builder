"""Formula management and validation routes."""

from fastapi import APIRouter
from ..models import FormulaValidateRequest, FormulaValidateResponse
from ..formula_evaluator import formula_evaluator, FORMULA_TEMPLATES
from ..errors import ValidationError, APIError


router = APIRouter(prefix="/formulas", tags=["formulas"])


@router.post("/validate", response_model=FormulaValidateResponse)
async def validate_formula(request: FormulaValidateRequest):
    """Validate a mathematical formula.
    
    Args:
        request: Formula validation request
        
    Returns:
        Validation result with optional evaluation
    """
    # Validate syntax
    valid, error = formula_evaluator.validate_formula(
        request.formula,
        request.variables
    )
    
    if not valid:
        return FormulaValidateResponse(
            valid=False,
            error=error
        )
    
    # If sample data provided, try to evaluate
    result = None
    if request.sample_data:
        success, eval_result, eval_error = formula_evaluator.evaluate(
            request.formula,
            request.variables,
            request.sample_data
        )
        
        if success:
            result = eval_result
        else:
            return FormulaValidateResponse(
                valid=False,
                error=eval_error
            )
    
    # Generate readable description
    parsed = formula_evaluator.get_formula_description(
        request.formula,
        request.variables
    )
    
    return FormulaValidateResponse(
        valid=True,
        result=result,
        parsed_formula=parsed
    )


@router.get("/templates")
async def list_formula_templates():
    """List available formula templates.
    
    Returns:
        Dictionary of formula templates
    """
    return {
        "templates": FORMULA_TEMPLATES,
        "total": len(FORMULA_TEMPLATES)
    }


@router.get("/templates/{template_id}")
async def get_formula_template(template_id: str):
    """Get a specific formula template.
    
    Args:
        template_id: Template ID
        
    Returns:
        Formula template details
    """
    if template_id not in FORMULA_TEMPLATES:
        raise APIError(404, "Formula template not found", {"template_id": template_id})
    
    return FORMULA_TEMPLATES[template_id]
