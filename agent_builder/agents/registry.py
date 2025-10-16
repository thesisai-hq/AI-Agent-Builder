"""
Agent Registry - Manages all available agents
"""

from typing import Dict, List, Optional
from agent_builder.agents.base_agent import BaseAgent


class AgentRegistry:
    """
    Central registry for all agents

    Allows API to discover and execute agents
    """

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._metadata: Dict[str, dict] = {}

    def register(
        self,
        agent: BaseAgent,
        agent_id: Optional[str] = None,
        weight: float = 0.1,
        enabled: bool = True,
        tags: List[str] = None,
    ) -> str:
        """
        Register an agent

        Args:
            agent: Agent instance
            agent_id: Optional custom ID (generates if not provided)
            weight: Agent weight for orchestration
            enabled: Whether agent is enabled
            tags: Optional tags for categorization

        Returns:
            Agent ID

        Example:
            registry = AgentRegistry()
            registry.register(my_agent.agent, weight=0.15)
        """
        if agent_id is None:
            # Generate ID from agent name
            agent_id = agent.name.lower().replace(" ", "_")

        # Store agent instance
        self._agents[agent_id] = agent

        # Store metadata
        self._metadata[agent_id] = {
            "id": agent_id,
            "name": agent.name,
            "weight": weight,
            "enabled": enabled,
            "tags": tags or [],
            "type": agent.__class__.__name__,
        }

        return agent_id

    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self._agents.get(agent_id)

    def get_metadata(self, agent_id: str) -> Optional[dict]:
        """Get agent metadata"""
        return self._metadata.get(agent_id)

    def list_all(self) -> List[str]:
        """List all agent IDs"""
        return list(self._agents.keys())

    def list_enabled(self) -> List[str]:
        """List enabled agent IDs"""
        return [
            agent_id
            for agent_id, meta in self._metadata.items()
            if meta.get("enabled", True)
        ]

    def get_enabled_agents(self) -> List[BaseAgent]:
        """Get all enabled agent instances"""
        return [self._agents[agent_id] for agent_id in self.list_enabled()]

    def enable(self, agent_id: str):
        """Enable an agent"""
        if agent_id in self._metadata:
            self._metadata[agent_id]["enabled"] = True

    def disable(self, agent_id: str):
        """Disable an agent"""
        if agent_id in self._metadata:
            self._metadata[agent_id]["enabled"] = False

    def unregister(self, agent_id: str) -> bool:
        """Unregister an agent"""
        if agent_id in self._agents:
            del self._agents[agent_id]
            del self._metadata[agent_id]
            return True
        return False

    def get_by_tag(self, tag: str) -> List[BaseAgent]:
        """Get agents by tag"""
        return [
            self._agents[agent_id]
            for agent_id, meta in self._metadata.items()
            if tag in meta.get("tags", [])
        ]

    def stats(self) -> dict:
        """Get registry statistics"""
        total = len(self._agents)
        enabled = len(self.list_enabled())

        return {
            "total_agents": total,
            "enabled_agents": enabled,
            "disabled_agents": total - enabled,
            "agent_ids": list(self._agents.keys()),
        }


# Global registry instance
_global_registry = AgentRegistry()


def get_registry() -> AgentRegistry:
    """Get global registry instance"""
    return _global_registry
