"""Test Agent - Test agents on mock or real data.

Streamlit multipage format: File will appear as "🧪 Test Agent" in navigation.
Uses async test executor for better performance.
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import streamlit as st

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gui.agent_loader import AgentLoader
from gui.business_logic.test_executor import TestExecutor
from gui.components.results_display import display_error_with_solution, display_test_results
from gui.components.test_config import TestDataConfig, configure_test_data
from gui.sidebar_info import show_sidebar_info

# Page config
st.set_page_config(page_title="Test Agent", page_icon="🧪", layout="wide")

# Initialize session state if needed
if "agent_loader" not in st.session_state:
    examples_dir = Path(__file__).parent.parent.parent / "examples"
    examples_dir = examples_dir.resolve()
    st.session_state.agent_loader = AgentLoader(examples_dir)
    st.session_state.examples_dir = examples_dir


def show_test_page():
    """Test agent - async-enhanced coordinator."""
    # Show sidebar info on all pages
    show_sidebar_info()
    
    st.title("🧪 Test Agent")

    # Select agent
    agent_selection = select_agent()
    if not agent_selection:
        show_no_agents_message()
        return

    agent_name, agent_info = agent_selection

    # Get ticker
    ticker = get_ticker_input()

    # Configure test data
    test_config = configure_test_data(agent_info["type"], ticker)
    if not test_config:
        return

    # Show disclaimer
    show_test_disclaimer()

    # Run analysis button
    if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
        execute_and_display_test(agent_info, test_config)


def select_agent() -> Optional[Tuple[str, Dict]]:
    """Agent selection dropdown."""
    loader = st.session_state.agent_loader
    agents = loader.list_agents()

    if not agents:
        return None

    agent_names = [a["name"] for a in agents]
    selected_agent = st.selectbox("Select Agent", agent_names)

    agent_info = next(a for a in agents if a["name"] == selected_agent)

    st.info(f"Agent Type: **{agent_info['type']}**")

    return selected_agent, agent_info


def show_no_agents_message():
    """Display message when no agents available."""
    st.info("No agents available to test. Create one first!")


def get_ticker_input() -> str:
    """Get ticker symbol from user."""
    return st.text_input("Ticker Symbol", value="AAPL")


def show_test_disclaimer():
    """Display testing disclaimer."""
    st.markdown("---")
    st.warning(
        """
    ⚠️ **Testing Reminder:**
    - This is a theoretical test using mock data
    - Results are for educational purposes only
    - Do not use these signals for real trading
    - Always consult financial professionals for investment decisions
    """
    )


def execute_and_display_test(agent_info: Dict, test_config: TestDataConfig):
    """Execute test and display results with progress tracking.
    
    Uses async executor for better performance and proper error handling.
    """
    # Prepare data
    data = prepare_test_data(test_config)

    # Check if data preparation failed
    if test_config.source == "yfinance" and data is None:
        st.error("Cannot run analysis - data fetch failed. Please check the error message above.")
        return

    # Show progress indicator
    progress_placeholder = st.empty()

    with progress_placeholder.container():
        progress_bar = st.progress(0.0)
        status_text = st.empty()
        status_text.text("🔄 Initializing test...")

        progress_bar.progress(0.2)
        status_text.text("🔄 Loading agent...")

        # Execute test ASYNCHRONOUSLY
        executor = TestExecutor()

        progress_bar.progress(0.6)
        status_text.text("🔄 Running analysis...")

        # Run async executor in sync context (Streamlit compatibility)
        result = asyncio.run(
            executor.execute_test_async(
                agent_info=agent_info, test_config=test_config, data=data
            )
        )

        progress_bar.progress(1.0)
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)

    progress_placeholder.empty()

    # Display results
    if result["success"]:
        display_test_results(result)
    else:
        display_error_with_solution(result)


def prepare_test_data(config: TestDataConfig) -> Optional[Dict]:
    """Prepare test data based on configuration."""
    if config.source == "mock":
        return {"name": f"Mock Company ({config.ticker})", **config.data}
    elif config.source == "yfinance":
        return config.data
    elif config.source == "database":
        return None  # Will be fetched by executor
    elif config.source == "pdf":
        return None  # PDF handling done by executor
    return None


# Run the page
show_test_page()
