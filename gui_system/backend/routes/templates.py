"""Template management routes."""

from fastapi import APIRouter, HTTPException
from ..models import TemplateResponse, TemplateListResponse
from ..storage import storage


router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("", response_model=TemplateListResponse)
async def list_templates():
    """List all available templates.
    
    Returns:
        List of agent templates
    """
    try:
        templates = storage.list_templates()
        return TemplateListResponse(templates=templates, total=len(templates))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str):
    """Get template by ID.
    
    Args:
        template_id: Template ID
        
    Returns:
        Template details
    """
    template = storage.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template
