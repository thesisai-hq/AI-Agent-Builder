"""Browse Agents - View and manage existing agents.

Streamlit multipage format: File will appear as "📋 Browse Agents" in navigation.
"""

import sys
from pathlib import Path
from typing import List, Dict

import streamlit as st

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gui.agent_loader import AgentLoader
from gui.code_viewer import CodeViewer
from gui.components.agent_card import render_agent_card, show_agent_stats
from gui.sidebar_info import show_sidebar_info

# Page config
st.set_page_config(page_title="Browse Agents", page_icon="📋", layout="wide")

# Initialize session state if needed
if "agent_loader" not in st.session_state:
    examples_dir = Path(__file__).parent.parent.parent / "examples"
    examples_dir = examples_dir.resolve()
    st.session_state.agent_loader = AgentLoader(examples_dir)
    st.session_state.examples_dir = examples_dir


def show_browse_page():
    """Browse existing agents - clean coordinator."""
    # Show sidebar info on all pages
    show_sidebar_info()
    
    st.title("📋 Browse Existing Agents")
    
    # Handle code viewer modal
    if st.session_state.get("current_viewing_file"):
        show_code_viewer()
        return
    
    # Handle any pending state changes
    handle_pending_view_actions()
    
    # Get filtered agents
    agents = get_filtered_agents()
    
    if not agents:
        show_empty_state()
        return
    
    # Display stats and search
    show_agent_stats(agents)
    st.markdown("---")
    
    # Search and display
    filtered = show_search_and_filter(agents)
    render_agent_grid(filtered)


def show_code_viewer():
    """Display agent code with educational annotations."""
    viewing_file = st.session_state.get("current_viewing_file")
    
    if not viewing_file:
        st.error("No file selected")
        return
    
    loader = st.session_state.agent_loader
    code = loader.get_agent_code(viewing_file)
    
    CodeViewer.show_with_annotations(code, viewing_file)


def handle_pending_view_actions():
    """Process any pending view actions from button clicks."""
    for key in list(st.session_state.keys()):
        if key.startswith("viewing_") and st.session_state[key]:
            filename = key.replace("viewing_", "")
            st.session_state.current_viewing_file = filename
            del st.session_state[key]
            st.rerun()


def get_filtered_agents() -> List[Dict]:
    """Get list of agents from loader."""
    loader = st.session_state.agent_loader
    return loader.list_agents()


def show_empty_state():
    """Display message when no agents found."""
    st.info("No agents found in examples/ directory")


def show_search_and_filter(agents: List[Dict]) -> List[Dict]:
    """Show search bar and filter agents."""
    search = st.text_input("🔍 Search agents", placeholder="Type to filter...")
    
    if search:
        agents = [
            a for a in agents
            if search.lower() in a["name"].lower() 
            or search.lower() in a["filename"].lower()
        ]
    
    st.caption(f"Showing {len(agents)} agent(s)")
    return agents


def render_agent_grid(agents: List[Dict]):
    """Render agents in a two-column grid."""
    cols = st.columns(2)
    loader = st.session_state.agent_loader
    
    for idx, agent_info in enumerate(agents):
        with cols[idx % 2]:
            render_agent_card(agent_info, loader)


# Run the page
show_browse_page()
