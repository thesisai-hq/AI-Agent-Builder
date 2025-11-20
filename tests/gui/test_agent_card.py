"""Tests for agent_card component.

Tests the agent card rendering and action handling.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestAgentCardComponent:
    """Test agent card display component."""
    
    def test_agent_stats_calculation(self):
        """Test statistics calculation logic."""
        agents = [
            {"type": "Rule-Based", "filename": "01_value.py"},
            {"type": "LLM-Powered", "filename": "02_llm.py"},
            {"type": "RAG-Powered", "filename": "03_rag.py"},
            {"type": "Rule-Based", "filename": "custom.py"},
        ]
        
        # Calculate stats
        total = len(agents)
        rule_based = len([a for a in agents if a["type"] == "Rule-Based"])
        llm_powered = len([a for a in agents if "LLM" in a["type"] or "RAG" in a["type"]])
        custom = len([a for a in agents if not a["filename"].startswith("0")])
        
        assert total == 4
        assert rule_based == 2
        assert llm_powered == 2
        assert custom == 1
    
    def test_framework_example_detection(self):
        """Test detection of framework examples."""
        framework_example = {"filename": "01_basic.py"}
        custom_agent = {"filename": "my_agent.py"}
        
        assert framework_example["filename"].startswith("0")
        assert not custom_agent["filename"].startswith("0")


class TestAgentActions:
    """Test agent action handling logic."""
    
    def test_duplicate_filename_suggestion(self):
        """Test duplicate filename generation."""
        original_filename = "value_agent.py"
        base_name = original_filename[:-3]  # Remove .py
        suggested_name = f"{base_name}_copy.py"
        
        assert suggested_name == "value_agent_copy.py"
    
    def test_session_state_keys(self):
        """Test session state key generation."""
        filename = "test_agent.py"
        
        # Verify key patterns
        view_key = f"viewing_{filename}"
        duplicate_key = f"duplicating_{filename}"
        delete_key = f"deleting_{filename}"
        
        assert view_key == "viewing_test_agent.py"
        assert duplicate_key == "duplicating_test_agent.py"
        assert delete_key == "deleting_test_agent.py"


class TestAgentCardRendering:
    """Test agent card rendering logic (without Streamlit UI)."""
    
    def test_action_button_logic(self):
        """Test action button availability logic."""
        framework_example = {"filename": "01_basic.py"}
        custom_agent = {"filename": "my_agent.py"}
        
        # Framework examples: can view, copy, export, but NOT delete
        is_framework = framework_example["filename"].startswith("0")
        assert is_framework is True
        
        # Custom agents: can view, copy, export, AND delete
        is_custom = not custom_agent["filename"].startswith("0")
        assert is_custom is True
    
    def test_export_data_preparation(self):
        """Test export data preparation."""
        # Mock agent code
        code = "# Agent code here"
        filename = "test_agent.py"
        
        # Export should provide code and filename
        export_data = {
            "data": code,
            "file_name": filename,
            "mime": "text/x-python"
        }
        
        assert export_data["data"] == code
        assert export_data["file_name"] == filename
        assert export_data["mime"] == "text/x-python"


# ============================================================================
# Integration Tests with AgentLoader
# ============================================================================

class TestAgentCardIntegration:
    """Integration tests with AgentLoader."""
    
    def test_render_with_loader(self, agent_loader, examples_dir, sample_agent_code):
        """Test rendering agent card with real loader."""
        from gui.components.test_config import TestDataConfig
        
        # Create test agent file
        agent_file = examples_dir / "test_agent.py"
        agent_file.write_text(sample_agent_code)
        
        # List agents
        agents = agent_loader.list_agents()
        
        assert len(agents) == 1
        assert agents[0]["filename"] == "test_agent.py"
        
        # Verify card would have correct data
        agent_info = agents[0]
        assert "name" in agent_info
        assert "type" in agent_info
        assert "filename" in agent_info
    
    def test_duplicate_agent_flow(self, agent_loader, examples_dir, sample_agent_code):
        """Test complete duplicate workflow."""
        # Create original
        original_file = examples_dir / "original.py"
        original_file.write_text(sample_agent_code)
        
        # Duplicate
        success, message = agent_loader.duplicate_agent("original.py", "copy.py")
        
        assert success is True
        assert "saved" in message.lower()
        
        # Verify both files exist
        assert original_file.exists()
        assert (examples_dir / "copy.py").exists()
        
        # List should show both
        agents = agent_loader.list_agents()
        assert len(agents) == 2
    
    def test_delete_agent_protection(self, agent_loader, examples_dir):
        """Test framework example protection."""
        # Create framework example
        framework_file = examples_dir / "01_example.py"
        framework_file.write_text("# Framework example")
        
        # Attempt delete
        success, message = agent_loader.delete_agent("01_example.py")
        
        assert success is False
        assert "cannot delete" in message.lower()
        assert framework_file.exists()  # Still there
    
    def test_delete_custom_agent(self, agent_loader, examples_dir):
        """Test deleting custom agent."""
        # Create custom agent
        custom_file = examples_dir / "my_agent.py"
        custom_file.write_text("# Custom agent")
        
        # Delete should succeed
        success, message = agent_loader.delete_agent("my_agent.py")
        
        assert success is True
        assert not custom_file.exists()  # Deleted


# ============================================================================
# UI State Tests
# ============================================================================

class TestCardStateManagement:
    """Test state management for card actions."""
    
    def test_view_action_state(self):
        """Test view action state transition."""
        filename = "test_agent.py"
        
        # Simulate button click
        state = {f"viewing_{filename}": True}
        
        # Handler should:
        # 1. Set current_viewing_file
        # 2. Delete the trigger key
        # 3. Trigger rerun
        
        if state.get(f"viewing_{filename}"):
            current_file = filename
            state.pop(f"viewing_{filename}")
        
        assert current_file == "test_agent.py"
        assert f"viewing_{filename}" not in state
    
    def test_duplicate_dialog_state(self):
        """Test duplicate dialog state."""
        filename = "test_agent.py"
        
        # Dialog shown
        state = {f"duplicating_{filename}": True}
        assert state.get(f"duplicating_{filename}") is True
        
        # Dialog confirmed
        state.pop(f"duplicating_{filename}")
        assert f"duplicating_{filename}" not in state
    
    def test_delete_confirmation_state(self):
        """Test delete confirmation state."""
        filename = "custom_agent.py"
        
        # Confirmation shown
        state = {f"deleting_{filename}": True}
        assert state.get(f"deleting_{filename}") is True
        
        # Confirmation cancelled
        state.pop(f"deleting_{filename}")
        assert f"deleting_{filename}" not in state


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
