"""AI Agent Builder - Main Page

This is the home page for the AI Agent Builder application.
Use the sidebar navigation to access different features.
"""

import sys
from pathlib import Path

import streamlit as st

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from gui.agent_loader import AgentLoader

# Page configuration
st.set_page_config(
    page_title="AI Agent Builder",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def show_disclaimer():
    """Show disclaimer on first visit."""
    if "disclaimer_accepted" not in st.session_state:
        st.session_state.disclaimer_accepted = False

    if not st.session_state.disclaimer_accepted:
        st.error("⚠️ IMPORTANT DISCLAIMER - PLEASE READ")

        st.markdown("""
        ### Educational Use Only

        This software is for **learning purposes only** and is **NOT intended for real trading**.

        **By using this application, you acknowledge that:**

        - ❌ **NOT FINANCIAL ADVICE:** This tool does not provide investment recommendations
        - ❌ **NO WARRANTIES:** Software provided "as is" with no guarantees of accuracy
        - ❌ **THEORETICAL ONLY:** Agents have not been validated for real trading
        - ❌ **SAMPLE DATA:** All included data is synthetic or simplified
        - ⚠️ **INVESTMENT RISKS:** All investments carry risk of loss
        - ✅ **EDUCATIONAL PURPOSE:** For learning investment concepts only

        **You should:**
        - Consult licensed financial advisors before making investment decisions
        - Never trade with money you cannot afford to lose
        - Understand that past performance does not guarantee future results
        - Review the full [DISCLAIMER.md](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/DISCLAIMER.md) for complete legal terms

        ---

        **Interested in production trading tools?** We're building [thesis-app](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/THESIS_APP.md) (coming soon)
        """)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "✅ I Understand - Continue to Application",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.disclaimer_accepted = True
                st.rerun()

        st.stop()


def initialize_session_state():
    """Initialize all session state variables."""
    if "agent_loader" not in st.session_state:
        examples_dir = Path(__file__).parent.parent / "examples"
        examples_dir = examples_dir.resolve()
        st.session_state.agent_loader = AgentLoader(examples_dir)
        st.session_state.examples_dir = examples_dir


def main():
    """Main home page."""
    # Show disclaimer first
    show_disclaimer()
    
    # Initialize session state
    initialize_session_state()
    
    # Home page content
    st.title("🤖 AI Agent Builder")
    st.markdown("### Create and manage AI investment agents")
    
    # Show reminder banner
    st.warning(
        "📚 **Educational Tool** | Not for real trading | "
        "[Read Full Disclaimer](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/DISCLAIMER.md)"
    )
    
    st.markdown("---")
    
    # Welcome message
    st.markdown("""
    ## Welcome to AI Agent Builder! 👋
    
    This tool helps you learn investment analysis by building AI-powered agents.
    
    ### 🚀 Quick Start
    
    Use the **sidebar navigation** to access different features:
    
    - **📋 Browse Agents** - View and manage existing agents
    - **➕ Create Agent** - Build new investment agents
    - **🧪 Test Agent** - Test agents on mock or real data
    - **📚 How to Use Agents** - Learn how to use the framework
    - **⚙️ LLM Setup** - Configure AI providers (OpenAI, Anthropic, Ollama)
    
    ### 📊 Quick Stats
    """)
    
    # Show statistics
    loader = st.session_state.agent_loader
    agents = loader.list_agents()
    
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
    
    st.markdown("---")
    
    # Getting started guide
    st.markdown("""
    ### 🎓 Learning Path
    
    **New to AI Agent Builder?** Follow this path:
    
    1. **Browse Agents** - Look at example strategies (Buffett, Lynch, Graham)
    2. **How to Use** - Read the documentation
    3. **Create Agent** - Build your first agent using the visual interface
    4. **Test Agent** - Run your agent on mock data
    5. **Experiment** - Modify and improve your strategies!
    
    ### 💡 Tips
    
    - Start with **Rule-Based** agents (simplest)
    - Duplicate existing examples to learn
    - Use **Mock Data** for quick testing
    - View generated code to learn Python
    
    ### 📍 Save Location
    
    Your agents are saved to: `{st.session_state.examples_dir}`
    """)
    
    st.markdown("---")
    
    # Footer info
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.info("""
        **🚀 Ready for Production?**
        
        Check out [thesis-app](https://thesisai.app) for:
        - Real-time market data
        - Multi-agent orchestration
        - Risk management
        - Production support
        """)
    
    with col_b:
        st.info("""
        **📖 Resources**
        
        - [GitHub Repository](https://github.com/thesisai-hq/AI-Agent-Builder)
        - [Documentation](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/README.md)
        - [Full Disclaimer](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/DISCLAIMER.md)
        - [MIT License](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/LICENSE)
        """)


if __name__ == "__main__":
    main()
