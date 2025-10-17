"""Agent registry"""

from dataclasses import dataclass, field
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentMetadata:
    id: str
    name: str
    description: str
    weight: float = 1.0
    enabled: bool = True
    tags: list = field(default_factory=list)


class AgentRegistry:
    def __init__(self):
        self._agents = {}
        self._metadata = {}
    
    def register(self, agent, agent_id: Optional[str] = None, weight: float = 1.0, 
                 enabled: bool = True, tags: list = None):
        from agent_builder.core.security import Validator
        if agent_id is None:
            agent_id = agent.name.lower().replace(" ", "_")
        agent_id = Validator.agent_id(agent_id)
        self._agents[agent_id] = agent
        self._metadata[agent_id] = AgentMetadata(
            id=agent_id, name=agent.name, description=agent.description,
            weight=weight, enabled=enabled, tags=tags or []
        )
        logger.info(f"✅ Registered: {agent_id}")
        return agent_id
    
    def get(self, agent_id: str):
        return self._agents.get(agent_id)
    
    def get_metadata(self, agent_id: str):
        return self._metadata.get(agent_id)
    
    def list_all(self):
        return list(self._agents.keys())
    
    def list_enabled(self):
        return [aid for aid, meta in self._metadata.items() if meta.enabled]
    
    def get_enabled_agents(self):
        return [self._agents[aid] for aid in self.list_enabled()]
    
    def enable(self, agent_id: str):
        if agent_id in self._metadata:
            self._metadata[agent_id].enabled = True
    
    def disable(self, agent_id: str):
        if agent_id in self._metadata:
            self._metadata[agent_id].enabled = False
    
    def stats(self):
        return {"total": len(self._agents), "enabled": len(self.list_enabled())}


_registry = AgentRegistry()

def get_registry():
    return _registry
