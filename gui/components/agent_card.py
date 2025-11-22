"""Agent card component - displays single agent with actions.

Simple, focused component for rendering an agent card in a grid.
Handles display only - delegates actions to parent.
"""

from pathlib import Path
from typing import Dict, List

import streamlit as st


def show_agent_stats(agents: List[Dict]) -> None:
    """Display summary statistics for agents.
    
    Args:
        agents: List of agent info dictionaries
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Agents", len(agents))
    
    with col2:
        rule_based = len([a for a in agents if a["type"] == "Rule-Based"])
        st.metric("Rule-Based", rule_based)
    
    with col3:
        llm_powered = len([a for a in agents if "LLM" in a["type"] or "RAG" in a["type"]])
        st.metric("LLM/RAG", llm_powered)
    
    with col4:
        custom = len([a for a in agents if not a["filename"].startswith("0")])
        st.metric("Your Agents", custom)


def render_agent_card(agent_info: Dict, loader) -> None:
    """Render single agent card with action buttons.
    
    Args:
        agent_info: Agent information dict with name, type, filename
        loader: AgentLoader instance for operations
    """
    filename = agent_info["filename"]
    is_framework_example = filename.startswith("0")
    
    with st.expander(f"**{agent_info['name']}**", expanded=False):
        st.markdown(f"**File:** `{filename}`")
        st.markdown(f"**Type:** {agent_info['type']}")
        
        _render_action_buttons(agent_info, is_framework_example)
        _render_duplicate_dialog(agent_info, loader)
        _render_delete_confirmation(agent_info, loader, is_framework_example)


def _render_action_buttons(agent_info: Dict, is_framework_example: bool) -> None:
    """Render the four action buttons for an agent.
    
    Args:
        agent_info: Agent information dict
        is_framework_example: Whether this is a protected example
    """
    filename = agent_info["filename"]
    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        if st.button("👁️ View", key=f"view_{filename}", use_container_width=True):
            st.session_state[f"viewing_{filename}"] = True
            st.rerun()
    
    with col_b:
        if st.button("📋 Copy", key=f"dup_{filename}", use_container_width=True):
            st.session_state[f"duplicating_{filename}"] = True
    
    with col_c:
        # Export is always allowed
        loader = st.session_state.agent_loader
        code = loader.get_agent_code(filename)
        st.download_button(
            "⬇️ Export",
            data=code,
            file_name=filename,
            mime="text/x-python",
            key=f"export_{filename}",
            use_container_width=True,
        )
    
    with col_d:
        if is_framework_example:
            st.button(
                "🔒 Protected",
                disabled=True,
                key=f"del_{filename}",
                use_container_width=True,
            )
        else:
            if st.button(
                "🗑️ Delete",
                key=f"del_{filename}",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state[f"deleting_{filename}"] = True


def _render_duplicate_dialog(agent_info: Dict, loader) -> None:
    """Render duplicate agent dialog if active.
    
    Args:
        agent_info: Agent information dict
        loader: AgentLoader instance
    """
    filename = agent_info["filename"]
    
    if not st.session_state.get(f"duplicating_{filename}"):
        return
    
    st.markdown("---")
    st.markdown("**Duplicate Agent**")
    
    base_name = filename[:-3]  # Remove .py
    suggested_name = f"{base_name}_copy.py"
    
    new_name = st.text_input(
        "New filename:",
        value=suggested_name,
        key=f"new_name_{filename}",
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Duplicate", key=f"confirm_dup_{filename}"):
            success, message = loader.duplicate_agent(filename, new_name)
            if success:
                st.success(message)
                del st.session_state[f"duplicating_{filename}"]
                st.rerun()
            else:
                st.error(message)
    
    with col2:
        if st.button("Cancel", key=f"cancel_dup_{filename}"):
            del st.session_state[f"duplicating_{filename}"]
            st.rerun()


def _render_delete_confirmation(agent_info: Dict, loader, is_framework_example: bool) -> None:
    """Render delete confirmation dialog if active.
    
    Args:
        agent_info: Agent information dict
        loader: AgentLoader instance
        is_framework_example: Whether this is a protected example
    """
    if is_framework_example:
        return  # Can't delete framework examples
    
    filename = agent_info["filename"]
    
    if not st.session_state.get(f"deleting_{filename}"):
        return
    
    st.markdown("---")
    st.warning("⚠️ **Confirm Deletion**")
    st.markdown(f"Are you sure you want to delete `{filename}`?")
    st.caption("This action cannot be undone.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Confirm Delete", key=f"confirm_del_{filename}", type="primary"):
            success, message = loader.delete_agent(filename)
            if success:
                st.success(message)
                del st.session_state[f"deleting_{filename}"]
                st.rerun()
            else:
                st.error(message)
    
    with col2:
        if st.button("Cancel", key=f"cancel_del_{filename}"):
            del st.session_state[f"deleting_{filename}"]
            st.rerun()
