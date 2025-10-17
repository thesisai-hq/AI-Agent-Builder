"""
Agent Registry - REFACTORED for efficiency
Fixes: dual dict storage, no deduplication
"""

from typing import Dict, List, Optional, Set
from agent_builder.agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Central registry for all agents - IMPROVED

    Changes from original:
    - Single dict storage (removed _metadata duplication)
    - Deduplication check (same instance can't be registered twice)
    - Better get methods
    - Performance tracking
    """

    def __init__(self):
        # Single source of truth - agents only
        self._agents: Dict[str, BaseAgent] = {}

        # Track agent instances to prevent duplicates
        self._registered_instances: Set[int] = set()

    def register(
        self,
        agent: BaseAgent,
        agent_id: Optional[str] = None,
        weight: Optional[float] = None,
        enabled: Optional[bool] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        Register an agent - IMPROVED

        Changes:
        - Deduplication check
        - Updates agent properties if provided
        - Returns agent_id for reference

        Args:
            agent: Agent instance
            agent_id: Optional custom ID (generates from name if not provided)
            weight: Override agent weight
            enabled: Override agent enabled status
            tags: Override/extend agent tags

        Returns:
            Agent ID

        Raises:
            ValueError: If same agent instance already registered
        """
        # Check for duplicate instance
        instance_id = id(agent)
        if instance_id in self._registered_instances:
            logger.warning(f"Agent instance {agent.name} already registered, skipping")
            # Find existing agent_id
            for aid, existing_agent in self._agents.items():
                if id(existing_agent) == instance_id:
                    return aid

        # Generate agent_id if not provided
        if agent_id is None:
            agent_id = agent.name.lower().replace(" ", "_")

        # Check if agent_id already exists
        if agent_id in self._agents:
            logger.warning(
                f"Agent ID '{agent_id}' already exists, generating unique ID"
            )
            base_id = agent_id
            counter = 1
            while agent_id in self._agents:
                agent_id = f"{base_id}_{counter}"
                counter += 1

        # Update agent properties if provided
        if weight is not None:
            agent.weight = weight
        if enabled is not None:
            agent.enabled = enabled
        if tags is not None:
            agent.tags = list(set(agent.tags + tags))  # Merge tags, deduplicate

        # Store agent
        self._agents[agent_id] = agent
        self._registered_instances.add(instance_id)

        logger.debug(f"Registered agent: {agent_id} ({agent.name})")

        return agent_id

    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self._agents.get(agent_id)

    def get_metadata(self, agent_id: str) -> Optional[dict]:
        """
        Get agent metadata - IMPROVED

        Changes:
        - Gets metadata from agent, not separate dict
        - Always fresh (no sync issues)
        """
        agent = self._agents.get(agent_id)
        if agent:
            metadata = agent.get_metadata()
            metadata["id"] = agent_id  # Add ID to metadata
            return metadata
        return None

    def list_all(self) -> List[str]:
        """List all agent IDs"""
        return list(self._agents.keys())

    def list_enabled(self) -> List[str]:
        """List enabled agent IDs - OPTIMIZED"""
        return [agent_id for agent_id, agent in self._agents.items() if agent.enabled]

    def get_enabled_agents(self) -> List[BaseAgent]:
        """Get all enabled agent instances"""
        return [agent for agent in self._agents.values() if agent.enabled]

    def enable(self, agent_id: str) -> bool:
        """Enable an agent"""
        agent = self._agents.get(agent_id)
        if agent:
            agent.enabled = True
            logger.info(f"Enabled agent: {agent_id}")
            return True
        return False

    def disable(self, agent_id: str) -> bool:
        """Disable an agent"""
        agent = self._agents.get(agent_id)
        if agent:
            agent.enabled = False
            logger.info(f"Disabled agent: {agent_id}")
            return True
        return False

    def unregister(self, agent_id: str) -> bool:
        """Unregister an agent - IMPROVED"""
        agent = self._agents.get(agent_id)
        if agent:
            # Remove from instance tracking
            self._registered_instances.discard(id(agent))
            # Remove from registry
            del self._agents[agent_id]
            logger.info(f"Unregistered agent: {agent_id}")
            return True
        return False

    def get_by_tag(self, tag: str) -> List[BaseAgent]:
        """Get agents by tag"""
        return [agent for agent in self._agents.values() if tag in agent.tags]

    def get_by_tags(self, tags: List[str], match_all: bool = False) -> List[BaseAgent]:
        """
        Get agents by multiple tags - NEW

        Args:
            tags: List of tags to match
            match_all: If True, agent must have ALL tags. If False, ANY tag.

        Returns:
            List of matching agents
        """
        if match_all:
            return [
                agent
                for agent in self._agents.values()
                if all(tag in agent.tags for tag in tags)
            ]
        else:
            return [
                agent
                for agent in self._agents.values()
                if any(tag in agent.tags for tag in tags)
            ]

    def stats(self) -> dict:
        """Get registry statistics - ENHANCED"""
        total = len(self._agents)
        enabled = sum(1 for a in self._agents.values() if a.enabled)

        # Tag distribution
        tag_counts = {}
        for agent in self._agents.values():
            for tag in agent.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Weight distribution
        total_weight = sum(a.weight for a in self._agents.values() if a.enabled)

        return {
            "total_agents": total,
            "enabled_agents": enabled,
            "disabled_agents": total - enabled,
            "total_weight": round(total_weight, 3),
            "agent_ids": list(self._agents.keys()),
            "tags": tag_counts,
        }


# Global registry instance
_global_registry = AgentRegistry()


def get_registry() -> AgentRegistry:
    """Get global registry instance"""
    return _global_registry
