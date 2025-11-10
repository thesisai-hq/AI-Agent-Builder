"""Agent management routes."""

from fastapi import APIRouter
from ..models import (
    AgentCreate, AgentUpdate, AgentResponse, 
    AgentListResponse, ExportCodeResponse
)
from ..storage import storage
from ..code_generator import code_generator
from ..errors import AgentNotFoundError, APIError


router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentResponse, status_code=201)
async def create_agent(agent: AgentCreate):
    """Create a new agent.
    
    Args:
        agent: Agent creation data
        
    Returns:
        Created agent with ID and timestamps
    """
    try:
        return storage.create_agent(agent)
    except Exception as e:
        raise APIError(500, "Failed to create agent", {"reason": str(e)})


@router.get("", response_model=AgentListResponse)
async def list_agents():
    """List all agents.
    
    Returns:
        List of all agents
    """
    try:
        agents = storage.list_agents()
        return AgentListResponse(agents=agents, total=len(agents))
    except Exception as e:
        raise APIError(500, "Failed to list agents", {"reason": str(e)})


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get agent by ID.
    
    Args:
        agent_id: Agent ID
        
    Returns:
        Agent details
    """
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, update: AgentUpdate):
    """Update an existing agent.
    
    Args:
        agent_id: Agent ID
        update: Fields to update
        
    Returns:
        Updated agent
    """
    agent = storage.update_agent(agent_id, update)
    if not agent:
        raise AgentNotFoundError(agent_id)
    return agent


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: str):
    """Delete an agent.
    
    Args:
        agent_id: Agent ID
    """
    success = storage.delete_agent(agent_id)
    if not success:
        raise AgentNotFoundError(agent_id)


@router.get("/{agent_id}/export", response_model=ExportCodeResponse)
async def export_agent_code(agent_id: str):
    """Export agent as Python code.
    
    Args:
        agent_id: Agent ID
        
    Returns:
        Python code for the agent
    """
    agent = storage.get_agent(agent_id)
    if not agent:
        raise AgentNotFoundError(agent_id)
    
    # Generate Python code using code generator
    code = code_generator.generate(agent)
    filename = f"{agent.name.lower().replace(' ', '_').replace('-', '_')}_agent.py"
    
    return ExportCodeResponse(code=code, filename=filename)
