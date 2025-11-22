"""Create Agent - Build new investment agents visually.

Streamlit multipage format: File will appear as "➕ Create Agent" in navigation.
"""

import sys
from pathlib import Path

import streamlit as st

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gui.agent_loader import AgentLoader
from gui.agent_creator import AgentCreator
from gui.agent_creation_helpers import (
    AgentCreationState,
    show_basic_info_section,
    show_agent_type_section,
    show_llm_configuration,
    show_rag_configuration,
    show_analysis_logic_section,
    show_generated_code_section,
)
from gui.sidebar_info import show_sidebar_info

# Page config
st.set_page_config(page_title="Create Agent", page_icon="➕", layout="wide")

# Initialize session state if needed
if "agent_loader" not in st.session_state:
    examples_dir = Path(__file__).parent.parent.parent / "examples"
    examples_dir = examples_dir.resolve()
    st.session_state.agent_loader = AgentLoader(examples_dir)
    st.session_state.examples_dir = examples_dir


def show_create_page():
    """Display agent creation interface."""
    # Show sidebar info on all pages
    show_sidebar_info()

    st.title("➕ Create New Agent")

    st.info(
        "💡 **Tip:** Browse the examples directory to see strategy templates "
        "(Buffett, Lynch, Graham, etc.). Duplicate them to create variations!"
    )

    # Initialize session state
    if "generated_code" not in st.session_state:
        AgentCreationState.clear_generated_code()

    creator = AgentCreator()
    loader = st.session_state.agent_loader

    # Basic Info and Agent Type (Side by Side)
    col1, col2 = st.columns(2)

    with col1:
        basic_info = show_basic_info_section()

    with col2:
        type_config = show_agent_type_section()
        agent_type = type_config["agent_type"]

        # LLM Configuration (if needed)
        llm_config = None
        if agent_type in ["LLM-Powered", "Hybrid", "RAG-Powered"]:
            llm_config = show_llm_configuration()

        # RAG Configuration (if needed)
        rag_config = None
        if agent_type == "RAG-Powered":
            rag_config = show_rag_configuration()

    # Analysis Logic
    rules = show_analysis_logic_section(agent_type)

    # Code Generation
    st.markdown("---")
    st.subheader("Preview Generated Code")

    if st.button("Generate Code", type="primary", use_container_width=True):
        with st.spinner("Generating agent code..."):
            code = creator.generate_agent_code(
                agent_name=basic_info["agent_name"],
                description=basic_info["description"],
                agent_type=agent_type,
                rules=rules,
                llm_provider=llm_config["provider"] if llm_config else None,
                llm_model=llm_config["model"] if llm_config else None,
                temperature=llm_config["temperature"] if llm_config else None,
                max_tokens=llm_config["max_tokens"] if llm_config else None,
                system_prompt=llm_config["system_prompt"] if llm_config else None,
                user_prompt_instructions=llm_config["user_instructions"] if llm_config else None,
                chunk_size=rag_config["chunk_size"] if rag_config else None,
                chunk_overlap=rag_config["chunk_overlap"] if rag_config else None,
                top_k=rag_config["top_k"] if rag_config else None,
            )

            AgentCreationState.set_generated_code(code)
            AgentCreationState.set_filename(basic_info["filename"])

        st.success(f"✅ Agent code generated successfully! ({len(code)} characters)")
        st.info(f"📝 Agent Type: **{agent_type}** | File: `{basic_info['filename']}`")
        st.balloons()

    # Display Generated Code (if available)
    generated_code = AgentCreationState.get_generated_code()
    if generated_code:
        show_generated_code_section(generated_code, basic_info["filename"], loader)


# Run the page
show_create_page()
