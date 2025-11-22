"""Shared sidebar components for all GUI pages.

Shows thesis-app info and resources consistently across all pages.
"""

import streamlit as st


def show_sidebar_info():
    """Show thesis-app promotion and resources in sidebar.

    Call this function at the start of every page to ensure
    consistent sidebar content across the entire application.
    """
    st.sidebar.markdown("---")

    # thesis-app promotion
    st.sidebar.markdown("### 🚀 Ready for Production?")
    st.sidebar.info(
        """
        **thesis-app** (coming soon)
        
        - Real-time market data
        - Multi-agent orchestration
        - Risk management
        - Production support
        
        [Learn More →](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/THESIS_APP.md)
        """
    )

    # Resources
    st.sidebar.markdown("### 📖 Resources")
    st.sidebar.markdown(
        """
        - [GitHub Repository](https://github.com/thesisai-hq/AI-Agent-Builder)
        - [Documentation](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/README.md)
        - [Full Disclaimer](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/DISCLAIMER.md)
        - [MIT License](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/LICENSE)
        """
    )
