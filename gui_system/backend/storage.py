"""Storage manager for agents and templates using JSON files."""

import json
import uuid
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .models import (
    AgentCreate, AgentUpdate, AgentResponse, 
    TemplateResponse, Rule, LLMConfigModel
)


class StorageManager:
    """Manages JSON file storage for agents and templates."""
    
    def __init__(self, storage_path: str = "storage"):
        """Initialize storage manager.
        
        Args:
            storage_path: Base path for storage directory
        """
        self.base_path = Path(storage_path)
        self.agents_path = self.base_path / "agents"
        self.templates_path = self.base_path / "templates"
        
        # Ensure directories exist
        self.agents_path.mkdir(parents=True, exist_ok=True)
        self.templates_path.mkdir(parents=True, exist_ok=True)
    
    # Agent operations
    def create_agent(self, agent_data: AgentCreate) -> AgentResponse:
        """Create a new agent.
        
        Args:
            agent_data: Agent creation data
            
        Returns:
            Created agent with ID and timestamps
        """
        agent_id = str(uuid.uuid4())
        now = datetime.now()
        
        agent = AgentResponse(
            id=agent_id,
            name=agent_data.name,
            type=agent_data.type,
            description=agent_data.description,
            goal=agent_data.goal,
            template_id=agent_data.template_id,
            rules=agent_data.rules,
            llm_config=agent_data.llm_config,
            created_at=now,
            updated_at=now,
        )
        
        # Save to file
        file_path = self.agents_path / f"{agent_id}.json"
        with open(file_path, 'w') as f:
            json.dump(agent.model_dump(mode='json'), f, indent=2, default=str)
        
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[AgentResponse]:
        """Get agent by ID.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent if found, None otherwise
        """
        file_path = self.agents_path / f"{agent_id}.json"
        if not file_path.exists():
            return None
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return AgentResponse(**data)
    
    def list_agents(self) -> List[AgentResponse]:
        """List all agents.
        
        Returns:
            List of all agents
        """
        agents = []
        for file_path in self.agents_path.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                agents.append(AgentResponse(**data))
            except Exception as e:
                print(f"Error loading agent {file_path}: {e}")
                continue
        
        # Sort by creation date (newest first)
        agents.sort(key=lambda a: a.created_at, reverse=True)
        return agents
    
    def update_agent(self, agent_id: str, update_data: AgentUpdate) -> Optional[AgentResponse]:
        """Update an existing agent.
        
        Args:
            agent_id: Agent ID
            update_data: Fields to update
            
        Returns:
            Updated agent if found, None otherwise
        """
        agent = self.get_agent(agent_id)
        if not agent:
            return None
        
        # Update fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(agent, field, value)
        
        agent.updated_at = datetime.now()
        
        # Save to file
        file_path = self.agents_path / f"{agent_id}.json"
        with open(file_path, 'w') as f:
            json.dump(agent.model_dump(mode='json'), f, indent=2, default=str)
        
        return agent
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            True if deleted, False if not found
        """
        file_path = self.agents_path / f"{agent_id}.json"
        if not file_path.exists():
            return False
        
        file_path.unlink()
        return True
    
    # Template operations
    def get_template(self, template_id: str) -> Optional[TemplateResponse]:
        """Get template by ID.
        
        Args:
            template_id: Template ID
            
        Returns:
            Template if found, None otherwise
        """
        file_path = self.templates_path / f"{template_id}.json"
        if not file_path.exists():
            return None
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return TemplateResponse(**data)
    
    def list_templates(self) -> List[TemplateResponse]:
        """List all templates.
        
        Returns:
            List of all templates
        """
        templates = []
        for file_path in self.templates_path.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                templates.append(TemplateResponse(**data))
            except Exception as e:
                print(f"Error loading template {file_path}: {e}")
                continue
        
        return templates
    
    def create_template(self, template: TemplateResponse) -> TemplateResponse:
        """Create a new template (admin operation).
        
        Args:
            template: Template data
            
        Returns:
            Created template
        """
        file_path = self.templates_path / f"{template.id}.json"
        with open(file_path, 'w') as f:
            json.dump(template.model_dump(mode='json'), f, indent=2, default=str)
        
        return template


# Global storage instance - use path relative to this file
_current_dir = Path(__file__).parent.parent
storage = StorageManager(storage_path=str(_current_dir / "storage"))
