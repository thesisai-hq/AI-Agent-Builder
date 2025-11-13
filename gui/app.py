"""Agent Builder GUI - Main Streamlit Application

Simple, maintainable interface for creating and managing AI agents.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from gui.agent_loader import AgentLoader
from gui.agent_creator import AgentCreator
from gui.agent_tester import AgentTester
from gui.backtester import Backtester, BacktestResult
from gui.metrics import MetricDefinitions, RuleValidator

# Page configuration
st.set_page_config(page_title="AI Agent Builder", page_icon="🤖", layout="wide")


# Cache metric definitions for performance
@st.cache_data
def get_metric_definitions():
    """Cache metric definitions to avoid repeated calls."""
    return MetricDefinitions.get_all_metrics()


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
        
        **For production trading tools with proper risk management, see [thesis-app](https://thesisai.app)**
        """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ I Understand - Continue to Application", type="primary", use_container_width=True):
                st.session_state.disclaimer_accepted = True
                st.rerun()
        
        st.stop()


def show_code_viewer():
    """Display agent code in full screen."""
    viewing_file = st.session_state.get("current_viewing_file")
    
    if not viewing_file:
        st.error("No file selected")
        return
    
    st.title(f"👁️ Viewing: {viewing_file}")
    
    # Back button at top
    if st.button("← Back to Browse", type="primary"):
        st.session_state.current_viewing_file = None
        st.rerun()
    
    st.markdown("---")
    
    # Load and display code
    loader = st.session_state.agent_loader
    code = loader.get_agent_code(viewing_file)
    
    # Display in full-width container
    st.code(code, language="python", line_numbers=True)
    
    # Action buttons at bottom
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Back to Browse", use_container_width=True):
            st.session_state.current_viewing_file = None
            st.rerun()
    
    with col2:
        st.download_button(
            "⬇️ Download",
            data=code,
            file_name=viewing_file,
            mime="text/x-python",
            use_container_width=True
        )
    
    with col3:
        # Copy to clipboard (show code snippet)
        if st.button("📋 Copy Path", use_container_width=True):
            st.code(f"examples/{viewing_file}", language="bash")


def show_license_modal():
    """Display full MIT License."""
    st.title("📄 MIT License")
    
    # Back button at top
    if st.button("← Back to Application", type="primary"):
        st.session_state.show_license = False
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    ### AI-Agent-Builder Framework
    
    **Copyright (c) 2025 ThesisAI LLC**
    
    ---
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    **THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.**
    
    ---
    
    ### What This Means
    
    The MIT License is one of the most permissive open source licenses. You can:
    
    - ✅ Use this software for any purpose (personal, academic, commercial)
    - ✅ Modify the code however you want
    - ✅ Distribute your modified or unmodified versions
    - ✅ Sublicense or sell copies
    
    **Your only obligations:**
    
    - Include the copyright notice and license text in any copies
    - Accept that the software comes with no warranties
    
    ### Additional Legal Terms
    
    While the MIT License covers software usage, please also review:
    
    - **[DISCLAIMER.md](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/DISCLAIMER.md)** - Educational use and financial advice disclaimers
    - **[CONTRIBUTING.md](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/CONTRIBUTING.md)** - Guidelines for contributing
    
    ### Questions?
    
    For questions about licensing or usage, please:
    - Open an issue on [GitHub](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
    - Email: support@thesisai.app
    """)


def main():
    """Main application entry point."""
    # Show disclaimer first
    show_disclaimer()
    
    st.title("🤖 AI Agent Builder")
    st.markdown("Create and manage AI investment agents")
    
    # Show reminder banner
    st.warning("📚 **Educational Tool** | Not for real trading | [Read Full Disclaimer](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/DISCLAIMER.md)")

    # Initialize session state
    if "agent_loader" not in st.session_state:
        # Get absolute path to examples directory
        examples_dir = Path(__file__).parent.parent / "examples"
        examples_dir = examples_dir.resolve()
        st.session_state.agent_loader = AgentLoader(examples_dir)
        st.session_state.examples_dir = examples_dir

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["📋 Browse Agents", "➕ Create Agent", "🧪 Test Agent", "📈 Backtest Agent"])

    # Show quick stats
    loader = st.session_state.agent_loader
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Statistics")
    st.sidebar.metric("Total Agents", len(loader.list_agents()))

    # Show save location
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Save Location")
    st.sidebar.caption(f"`{st.session_state.examples_dir}`")
    
    # Disclaimer reminder in sidebar
    st.sidebar.markdown("---")
    st.sidebar.error("⚠️ **Educational Use Only**")
    st.sidebar.caption("""
    Not financial advice.
    Do not use for real trading.
    [Full Disclaimer](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/DISCLAIMER.md)
    """)
    
    # Link to thesis-app
    st.sidebar.markdown("---")
    st.sidebar.info("""
    🚀 **Ready for Production?**
    
    Check out [thesis-app](https://thesisai.app) for:
    - Real-time market data
    - Multi-agent orchestration
    - Risk management
    - Production support
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("**AI-Agent-Builder v1.0.0**  \nMIT License | [GitHub](https://github.com/thesisai-hq/AI-Agent-Builder)")
    
    # License link
    if st.sidebar.button("📄 View License", use_container_width=True):
        st.session_state.show_license = True

    # License modal
    if st.session_state.get("show_license", False):
        show_license_modal()
        return
    
    # Code viewer modal
    if st.session_state.get("current_viewing_file"):
        show_code_viewer()
        return
    
    # Page routing
    if page == "📋 Browse Agents":
        show_browse_page()
    elif page == "➕ Create Agent":
        show_create_page()
    elif page == "🧪 Test Agent":
        show_test_page()
    elif page == "📈 Backtest Agent":
        show_backtest_page()


def show_browse_page():
    """Display agent browsing interface."""
    st.header("Browse Existing Agents")
    
    # Check if we need to show the View button click handler
    loader = st.session_state.agent_loader
    
    # Handle file viewing
    for key in list(st.session_state.keys()):
        if key.startswith("viewing_") and st.session_state[key]:
            filename = key.replace("viewing_", "")
            st.session_state.current_viewing_file = filename
            del st.session_state[key]  # Clean up the trigger
            st.rerun()
    
    agents = loader.list_agents()

    if not agents:
        st.info("No agents found in examples/ directory")
        return

    # Summary stats
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

    # Search/Filter
    search = st.text_input("🔍 Search agents", placeholder="Type to filter...")

    if search:
        agents = [
            a
            for a in agents
            if search.lower() in a["name"].lower() or search.lower() in a["filename"].lower()
        ]

    st.caption(f"Showing {len(agents)} agent(s)")

    # Display agents in a grid
    cols = st.columns(2)
    for idx, agent_info in enumerate(agents):
        with cols[idx % 2]:
            # Check if framework example (can't delete)
            is_framework_example = agent_info["filename"].startswith("0")

            with st.expander(f"**{agent_info['name']}**", expanded=False):
                st.markdown(f"**File:** `{agent_info['filename']}`")
                st.markdown(f"**Type:** {agent_info['type']}")

                # Action buttons
                col_a, col_b, col_c, col_d = st.columns(4)

                with col_a:
                    if st.button(
                        "👁️ View", key=f"view_{agent_info['filename']}", use_container_width=True
                    ):
                        st.session_state[f"viewing_{agent_info['filename']}"] = True
                        st.rerun()

                with col_b:
                    if st.button(
                        "📋 Copy", key=f"dup_{agent_info['filename']}", use_container_width=True
                    ):
                        st.session_state[f"duplicating_{agent_info['filename']}"] = True

                with col_c:
                    code = loader.get_agent_code(agent_info["filename"])
                    st.download_button(
                        "⬇️ Export",
                        data=code,
                        file_name=agent_info["filename"],
                        mime="text/x-python",
                        key=f"export_{agent_info['filename']}",
                        use_container_width=True,
                    )

                with col_d:
                    if is_framework_example:
                        st.button(
                            "🔒 Protected",
                            disabled=True,
                            key=f"del_{agent_info['filename']}",
                            use_container_width=True,
                        )
                    else:
                        if st.button(
                            "🗑️ Delete",
                            key=f"del_{agent_info['filename']}",
                            type="secondary",
                            use_container_width=True,
                        ):
                            st.session_state[f"deleting_{agent_info['filename']}"] = True

                # Handle duplicate dialog
                if st.session_state.get(f"duplicating_{agent_info['filename']}"):
                    st.markdown("---")
                    st.markdown("**Duplicate Agent**")

                    base_name = agent_info["filename"][:-3]
                    suggested_name = f"{base_name}_copy.py"

                    new_name = st.text_input(
                        "New filename:",
                        value=suggested_name,
                        key=f"new_name_{agent_info['filename']}",
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Duplicate", key=f"confirm_dup_{agent_info['filename']}"):
                            success, message = loader.duplicate_agent(
                                agent_info["filename"], new_name
                            )
                            if success:
                                st.success(message)
                                del st.session_state[f"duplicating_{agent_info['filename']}"]
                                st.rerun()
                            else:
                                st.error(message)

                    with col2:
                        if st.button("Cancel", key=f"cancel_dup_{agent_info['filename']}"):
                            del st.session_state[f"duplicating_{agent_info['filename']}"]
                            st.rerun()

                # Handle delete confirmation
                if st.session_state.get(f"deleting_{agent_info['filename']}"):
                    st.markdown("---")
                    st.warning(f"⚠️ **Confirm Deletion**")
                    st.markdown(f"Are you sure you want to delete `{agent_info['filename']}`?")
                    st.caption("This action cannot be undone.")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "🗑️ Confirm Delete",
                            key=f"confirm_del_{agent_info['filename']}",
                            type="primary",
                        ):
                            success, message = loader.delete_agent(agent_info["filename"])
                            if success:
                                st.success(message)
                                del st.session_state[f"deleting_{agent_info['filename']}"]
                                st.rerun()
                            else:
                                st.error(message)

                    with col2:
                        if st.button("Cancel", key=f"cancel_del_{agent_info['filename']}"):
                            del st.session_state[f"deleting_{agent_info['filename']}"]
                            st.rerun()


def show_create_page():
    """Display agent creation interface."""
    st.header("Create New Agent")

    st.info(
        "💡 **Tip:** Browse the examples directory to see strategy templates (Buffett, Lynch, Graham, etc.). Duplicate them to create variations!"
    )

    # Initialize session state for generated code
    if "generated_code" not in st.session_state:
        st.session_state.generated_code = None
    if "current_filename" not in st.session_state:
        st.session_state.current_filename = None

    creator = AgentCreator()
    loader = st.session_state.agent_loader  # ✅ Get loader for validation

    # Agent configuration
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Basic Information")
        agent_name = st.text_input(
            "Agent Class Name",
            value="MyAgent",
            help="Python class name (e.g., ValueAgent, GrowthAgent)",
        )

        description = st.text_area("Description", help="What does this agent do?")

        filename = st.text_input(
            "Filename",
            value=f"{agent_name.lower() if agent_name else 'my_agent'}.py",
            help="File will be saved in examples/ directory",
        )

        # Real-time filename validation
        if filename:
            save_path = st.session_state.examples_dir / filename
            
            # Validate filename
            if not filename.endswith(".py"):
                st.error("❌ Filename must end with .py")
            elif not loader._is_valid_filename(filename):
                st.error("❌ Invalid filename. Use only letters, numbers, and underscores (e.g., my_agent.py, value_strategy_v2.py)")
                st.caption("Valid: `my_agent.py`, `value_v2.py` | Invalid: `my-agent.py`, `my agent.py`, `1agent.py`")
            elif (st.session_state.examples_dir / filename).exists():
                st.warning(f"⚠️ File `{filename}` already exists. Choose a different name or delete the existing file first.")
            else:
                st.success(f"✅ Valid filename: will save to `examples/{filename}`")
                st.caption(f"Full path: `{save_path}`")

    with col2:
        st.subheader("Agent Type")
        agent_type = st.selectbox(
            "Template", ["Rule-Based", "LLM-Powered", "Hybrid", "RAG-Powered"]
        )
        
        # Show explanation of Hybrid
        if agent_type == "Hybrid":
            st.info("""
            🧑‍💻 **What is a Hybrid Agent?**
            
            Combines rules + LLM:
            1. **Rules:** Fast screening (filter stocks)
            2. **LLM:** Deep analysis (only on filtered stocks)
            
            **Use when:** You want to screen thousands of stocks quickly,
            then use AI for detailed analysis on candidates.
            """)

        if agent_type in ["LLM-Powered", "Hybrid", "RAG-Powered"]:
            st.markdown("**LLM Configuration**")
            
            # Provider selection
            llm_provider = st.selectbox(
                "Provider", 
                ["ollama", "openai", "anthropic"],
                help="LLM service provider. Ollama is free and local, OpenAI and Anthropic require API keys."
            )
            
            # Model selection based on provider
            model_options = {
                "ollama": [
                    "llama3.2",
                    "llama3.1",
                    "llama3",
                    "llama2",
                    "mistral",
                    "mixtral",
                    "phi",
                    "gemma",
                    "qwen",
                    "custom (enter below)"
                ],
                "openai": [
                    "gpt-4o",
                    "gpt-4o-mini",
                    "gpt-4-turbo",
                    "gpt-4",
                    "gpt-3.5-turbo",
                    "custom (enter below)"
                ],
                "anthropic": [
                    "claude-3-5-sonnet-20241022",
                    "claude-3-5-haiku-20241022",
                    "claude-3-opus-20240229",
                    "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307",
                    "custom (enter below)"
                ]
            }
            
            selected_model = st.selectbox(
                "Model",
                model_options[llm_provider],
                help=f"Specific {llm_provider} model to use. Different models have different capabilities and costs."
            )
            
            # Custom model input if selected
            if selected_model == "custom (enter below)":
                custom_model = st.text_input(
                    "Custom Model Name",
                    placeholder=f"Enter exact model name for {llm_provider}",
                    help="Enter the exact model identifier (e.g., 'llama3.2:70b' for Ollama)"
                )
                final_model = custom_model if custom_model else model_options[llm_provider][0]
            else:
                final_model = selected_model
            
            # Show model info
            model_info = {
                "llama3.2": "💡 Latest Llama model, good balance of speed and quality",
                "gpt-4o": "💡 Latest GPT-4 with vision, fastest GPT-4 model",
                "gpt-4o-mini": "💡 Cost-effective GPT-4, 60% cheaper than GPT-4o",
                "claude-3-5-sonnet-20241022": "💡 Latest Claude, best for analysis and coding",
                "claude-3-5-haiku-20241022": "💡 Fastest Claude, good for simple tasks",
                "mistral": "💡 Good open-source alternative, fast inference",
                "gpt-4": "💡 Original GPT-4, very capable but slower",
                "gpt-3.5-turbo": "💡 Fast and cheap, good for simple analysis"
            }
            
            if selected_model in model_info:
                st.caption(model_info[selected_model])
            
            temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
            max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)
            system_prompt = st.text_area(
                "System Prompt", height=100, help="Define the agent's personality and approach"
            )
        else:
            llm_provider = None
            final_model = None
            temperature = None
            max_tokens = None
            system_prompt = None

        if agent_type == "RAG-Powered":
            st.markdown("**RAG Configuration**")
            chunk_size = st.number_input(
                "Chunk Size", 100, 1000, 300, 50, help="Size of text chunks for vector search"
            )
            chunk_overlap = st.number_input(
                "Chunk Overlap", 0, 200, 50, 10, help="Overlap between chunks"
            )
            top_k = st.number_input(
                "Top K Results", 1, 10, 3, 1, help="Number of relevant chunks to retrieve"
            )
        else:
            chunk_size = None
            chunk_overlap = None
            top_k = None

    # Analysis Logic
    st.subheader("Analysis Logic")

    if agent_type == "Rule-Based" or agent_type == "Hybrid":
        # Show different header for hybrid
        if agent_type == "Hybrid":
            st.markdown("🎯 **Screening Rules (Step 1: Filter Stocks)**")
            st.caption("Define rules to filter which stocks get LLM analysis")
        else:
            st.markdown("Define your investment strategy:")

        rule_style = st.radio(
            "Rule Style",
            ["Simple Rules", "Advanced Rules", "Score-Based"],
            help="Simple: Single conditions | Advanced: Multi-condition AND/OR | Score: Point accumulation",
        )

        if rule_style == "Simple Rules":
            num_rules = st.number_input("Number of Rules", 1, 5, 2)
            rules = []
            validation_warnings = []

            for i in range(num_rules):
                with st.expander(f"Rule {i+1}"):
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        metric = st.selectbox(
                            "Metric",
                            [
                                "pe_ratio",
                                "revenue_growth",
                                "profit_margin",
                                "roe",
                                "debt_to_equity",
                                "dividend_yield",
                                "pb_ratio",
                                "current_ratio",
                            ],
                            key=f"metric_{i}",
                            help="Hover over threshold field for metric details",
                        )

                    with col_b:
                        operator = st.selectbox(
                            "Operator", ["<", ">", "<=", ">=", "=="], key=f"op_{i}"
                        )

                    with col_c:
                        # Get metric definition for tooltip
                        metrics = get_metric_definitions()
                        metric_def = metrics.get(metric, {})

                        threshold = st.number_input(
                            "Threshold",
                            key=f"thresh_{i}",
                            help=metric_def.get("tooltip", "Enter threshold value"),
                        )

                        # Validate threshold
                        is_valid, error_msg = MetricDefinitions.validate_value(metric, threshold)
                        if not is_valid:
                            st.error(error_msg)
                            validation_warnings.append(f"Rule {i+1}: {error_msg}")

                        # Check threshold logic
                        logic_warning = RuleValidator.validate_threshold_logic(
                            metric, operator, threshold
                        )
                        if logic_warning:
                            st.warning(logic_warning)

                        # Get suggestion
                        suggestion = MetricDefinitions.get_suggestion(metric, threshold, operator)
                        if suggestion:
                            st.info(suggestion)

                    direction = st.selectbox(
                        "Signal", ["bullish", "bearish", "neutral"], key=f"dir_{i}"
                    )
                    confidence = st.slider("Confidence", 0.0, 1.0, 0.7, 0.1, key=f"conf_{i}")

                    rules.append(
                        {
                            "type": "simple",
                            "metric": metric,
                            "operator": operator,
                            "threshold": threshold,
                            "direction": direction,
                            "confidence": confidence,
                        }
                    )

            # Check for conflicts
            conflicts = RuleValidator.check_conflicts(rules)
            if conflicts:
                st.warning("**Rule Conflicts Detected:**")
                for conflict in conflicts:
                    st.warning(conflict)

        elif rule_style == "Advanced Rules":
            num_rules = st.number_input("Number of Rules", 1, 3, 1)
            rules = []

            for i in range(num_rules):
                with st.expander(f"Advanced Rule {i+1}"):
                    num_conditions = st.number_input(
                        "Number of Conditions", 1, 5, 2, key=f"num_cond_{i}"
                    )
                    logic_operator = st.selectbox(
                        "Combine conditions with", ["AND", "OR"], key=f"logic_{i}"
                    )

                    conditions = []
                    for j in range(num_conditions):
                        col_a, col_b, col_c = st.columns(3)

                        with col_a:
                            metric = st.selectbox(
                                "Metric",
                                [
                                    "pe_ratio",
                                    "revenue_growth",
                                    "profit_margin",
                                    "roe",
                                    "debt_to_equity",
                                    "dividend_yield",
                                    "pb_ratio",
                                    "current_ratio",
                                    "peg_ratio",
                                    "quality_score",
                                ],
                                key=f"adv_metric_{i}_{j}",
                                help="Hover over Value field for details",
                            )

                        with col_b:
                            operator = st.selectbox(
                                "Op", ["<", ">", "<=", ">=", "=="], key=f"adv_op_{i}_{j}"
                            )

                        with col_c:
                            metrics = get_metric_definitions()
                            metric_def = metrics.get(metric, {})
                            threshold = st.number_input(
                                "Value",
                                key=f"adv_thresh_{i}_{j}",
                                help=metric_def.get("tooltip", "Enter value"),
                            )

                            # Validate
                            is_valid, error_msg = MetricDefinitions.validate_value(
                                metric, threshold
                            )
                            if not is_valid:
                                st.error(error_msg)

                        conditions.append(
                            {"metric": metric, "operator": operator, "threshold": threshold}
                        )

                    direction = st.selectbox(
                        "Signal", ["bullish", "bearish", "neutral"], key=f"adv_dir_{i}"
                    )
                    confidence = st.slider("Confidence", 0.0, 1.0, 0.7, 0.1, key=f"adv_conf_{i}")

                    rules.append(
                        {
                            "type": "advanced",
                            "conditions": conditions,
                            "logic": logic_operator,
                            "direction": direction,
                            "confidence": confidence,
                        }
                    )

        else:  # Score-Based
            st.markdown(
                "**Score-Based Strategy:** Accumulate points, decide signal based on total score."
            )

            num_criteria = st.number_input("Number of Scoring Criteria", 1, 10, 5)
            criteria = []

            for i in range(num_criteria):
                with st.expander(f"Criterion {i+1}"):
                    col_a, col_b, col_c, col_d = st.columns(4)

                    with col_a:
                        metric = st.selectbox(
                            "Metric",
                            [
                                "pe_ratio",
                                "revenue_growth",
                                "profit_margin",
                                "roe",
                                "debt_to_equity",
                                "dividend_yield",
                                "pb_ratio",
                                "current_ratio",
                            ],
                            key=f"score_metric_{i}",
                            help="Hover over Value for details",
                        )

                    with col_b:
                        operator = st.selectbox("Op", ["<", ">", "<=", ">="], key=f"score_op_{i}")

                    with col_c:
                        metrics = get_metric_definitions()
                        metric_def = metrics.get(metric, {})
                        threshold = st.number_input(
                            "Value",
                            key=f"score_thresh_{i}",
                            help=metric_def.get("tooltip", "Enter value"),
                        )

                        # Validate
                        is_valid, error_msg = MetricDefinitions.validate_value(metric, threshold)
                        if not is_valid:
                            st.error(error_msg)

                    with col_d:
                        points = st.number_input(
                            "Points",
                            -5,
                            5,
                            1,
                            key=f"score_pts_{i}",
                            help="Positive points for good, negative for bad. Typical: +1 or +2 for positive factors, -1 or -2 for red flags",
                        )

                    criteria.append(
                        {
                            "metric": metric,
                            "operator": operator,
                            "threshold": threshold,
                            "points": points,
                        }
                    )

            st.markdown("**Score Thresholds:**")
            col1, col2 = st.columns(2)
            with col1:
                bullish_threshold = st.number_input("Bullish if score >=", 0, 20, 3)
                bullish_confidence = st.slider(
                    "Bullish Confidence", 0.0, 1.0, 0.8, 0.1, key="bullish_conf"
                )
            with col2:
                bearish_threshold = st.number_input("Bearish if score <=", -20, 0, -2)
                bearish_confidence = st.slider(
                    "Bearish Confidence", 0.0, 1.0, 0.7, 0.1, key="bearish_conf"
                )

            rules = [
                {
                    "type": "score",
                    "criteria": criteria,
                    "bullish_threshold": bullish_threshold,
                    "bullish_confidence": bullish_confidence,
                    "bearish_threshold": bearish_threshold,
                    "bearish_confidence": bearish_confidence,
                }
            ]

    elif agent_type == "RAG-Powered":
        rules = None
        st.info("📄 RAG agents analyze documents/text using retrieval and embeddings")
    elif agent_type == "LLM-Powered":
        rules = None
        st.info("🤖 LLM-powered agents use natural language prompts instead of explicit rules")
    # Hybrid agents already have rules defined above

    # Generate and preview code
    st.markdown("---")
    st.subheader("Preview Generated Code")

    if st.button("Generate Code", type="primary"):
        code = creator.generate_agent_code(
            agent_name=agent_name,
            description=description,
            agent_type=agent_type,
            rules=rules,
            llm_provider=llm_provider,
            llm_model=final_model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            top_k=top_k,
        )

        st.session_state.generated_code = code
        st.session_state.current_filename = filename

    # Display generated code if available
    if st.session_state.generated_code:
        st.code(st.session_state.generated_code, language="python")

        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("💾 Save Agent"):
                # Use current filename from text input, not cached session state
                current_filename = filename  # This is from the text_input above
                
                loader = st.session_state.agent_loader
                success, message = loader.save_agent(
                    current_filename, st.session_state.generated_code
                )
                if success:
                    st.success(message)
                    st.balloons()
                    # Clear session state
                    st.session_state.generated_code = None
                    st.session_state.current_filename = None
                    st.rerun()
                else:
                    # Show error and keep code visible for editing filename
                    st.error(message)
                    st.info("💡 **Tip:** Change the filename above and try saving again. Valid filenames use only letters, numbers, and underscores.")

        with col2:
            if st.button("🗑️ Clear"):
                st.session_state.generated_code = None
                st.session_state.current_filename = None
                st.rerun()


def show_test_page():
    """Display agent testing interface."""
    st.header("Test Agent")

    loader = st.session_state.agent_loader
    agents = loader.list_agents()

    if not agents:
        st.info("No agents available to test. Create one first!")
        return

    agent_names = [a["name"] for a in agents]
    selected_agent = st.selectbox("Select Agent", agent_names)

    agent_info = next(a for a in agents if a["name"] == selected_agent)
    agent_filename = agent_info["filename"]
    agent_class_name = agent_info["name"]  # Store the class name
    agent_type = agent_info["type"]

    st.info(f"Agent Type: **{agent_type}**")

    ticker = st.text_input("Ticker Symbol", value="AAPL")

    if agent_type == "RAG-Powered":
        st.subheader("📄 Document Upload")
        st.markdown("RAG agents analyze documents. Upload a PDF to test:")

        uploaded_file = st.file_uploader(
            "Drag and drop PDF here",
            type=["pdf"],
            help="Upload SEC filing, earnings report, or any financial document",
        )

        if uploaded_file:
            st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")

            with st.expander("Preview Document Text"):
                from PyPDF2 import PdfReader

                try:
                    pdf_reader = PdfReader(uploaded_file)
                    preview_text = ""
                    for page_num, page in enumerate(pdf_reader.pages[:3]):
                        preview_text += f"\n--- Page {page_num + 1} ---\n"
                        preview_text += page.extract_text()

                    st.text_area(
                        "Document Preview (first 3 pages)",
                        preview_text[:2000] + "..." if len(preview_text) > 2000 else preview_text,
                        height=200,
                    )
                    st.caption(f"Total pages: {len(pdf_reader.pages)}")
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")

        use_mock = False
        mock_data = None

    else:
        st.subheader("Test Data")
        use_mock = st.checkbox("Use Mock Data", value=True)
        uploaded_file = None

        if use_mock:
            # Mock data inputs with tooltips
            st.subheader("Mock Financial Data")

            # Get metric definitions (cached)
            metrics = get_metric_definitions()

            mock_data = {}

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                pe_def = metrics["pe_ratio"]
                mock_data["pe_ratio"] = st.number_input(
                    "PE Ratio", 5.0, 100.0, 20.0, help=pe_def["tooltip"]
                )

                growth_def = metrics["revenue_growth"]
                mock_data["revenue_growth"] = st.number_input(
                    "Revenue Growth (%)", -20.0, 100.0, 15.0, help=growth_def["tooltip"]
                )

            with col_b:
                margin_def = metrics["profit_margin"]
                mock_data["profit_margin"] = st.number_input(
                    "Profit Margin (%)", -10.0, 50.0, 12.0, help=margin_def["tooltip"]
                )

                roe_def = metrics["roe"]
                mock_data["roe"] = st.number_input(
                    "ROE (%)", -20.0, 50.0, 15.0, help=roe_def["tooltip"]
                )

            with col_c:
                debt_def = metrics["debt_to_equity"]
                mock_data["debt_to_equity"] = st.number_input(
                    "Debt/Equity", 0.0, 5.0, 0.8, help=debt_def["tooltip"]
                )

                div_def = metrics["dividend_yield"]
                mock_data["dividend_yield"] = st.number_input(
                    "Dividend Yield (%)", 0.0, 10.0, 2.0, help=div_def["tooltip"]
                )
        else:
            mock_data = None

    # Show warning before running analysis
    st.markdown("---")
    st.warning("""
    ⚠️ **Testing Reminder:**
    - This is a theoretical test using mock data
    - Results are for educational purposes only
    - Do not use these signals for real trading
    - Always consult financial professionals for investment decisions
    """)
    
    if st.button("🚀 Run Analysis", type="primary"):
        tester = AgentTester()

        if agent_type == "RAG-Powered" and not uploaded_file:
            st.error("Please upload a PDF document to test RAG agent")
            return

        with st.spinner("Running analysis..."):
            result = tester.test_agent(
                agent_filename, 
                ticker, 
                mock_data, 
                uploaded_file,
                agent_class_name  # Pass the specific class name!
            )

        if result["success"]:
            # Check if LLM fallback occurred
            if result.get("is_fallback", False):
                st.warning("⚠️ **LLM Service Unavailable - Using Fallback Logic**")
                
                llm_error = result.get("llm_error_info", {})
                error_type = llm_error.get("error_type")
                
                # Show specific error message based on type
                if error_type == "missing_package":
                    st.error(f"""
                    ❌ **Missing LLM Package**
                    
                    **Problem:** {llm_error.get('description')}
                    
                    **Solution:** Install the required package:
                    ```bash
                    {llm_error.get('install_command')}
                    ```
                    
                    Or install all LLM providers:
                    ```bash
                    pip install 'ai-agent-framework[llm]'
                    ```
                    """)
                
                elif error_type == "model_not_found":
                    model_name = llm_error.get('model', 'llama3.2')
                    st.error(f"""
                    ❌ **Model Not Available**
                    
                    **Problem:** Model '{model_name}' not downloaded
                    
                    **Solution:** Download the model with Ollama:
                    ```bash
                    {llm_error.get('install_command')}
                    ```
                    
                    **Available Models:** Check with `ollama list`
                    
                    **Popular Models:**
                    - `ollama pull llama3.2` (recommended)
                    - `ollama pull mistral`
                    - `ollama pull phi`
                    """)
                
                elif error_type == "connection_error":
                    st.error("""
                    ❌ **Ollama Service Not Running**
                    
                    **Problem:** Can't connect to Ollama service
                    
                    **Solution:** Start Ollama in a terminal:
                    ```bash
                    ollama serve
                    ```
                    
                    Or if Ollama is not installed:
                    ```bash
                    # Install Ollama
                    curl https://ollama.ai/install.sh | sh
                    
                    # Download a model
                    ollama pull llama3.2
                    
                    # Start service
                    ollama serve
                    ```
                    """)
                
                elif error_type == "missing_api_key":
                    provider = llm_error.get('provider', 'unknown')
                    env_var = f"{provider.upper()}_API_KEY" if provider != 'unknown' else 'API_KEY'
                    
                    st.error(f"""
                    ❌ **API Key Not Configured**
                    
                    **Problem:** {llm_error.get('description')}
                    
                    **Solution:** Add your API key to the `.env` file:
                    ```bash
                    # Edit .env file
                    nano .env
                    
                    # Add this line:
                    {env_var}=your-api-key-here
                    ```
                    
                    **Get an API Key:**
                    - OpenAI: https://platform.openai.com/api-keys
                    - Anthropic: https://console.anthropic.com/
                    """)
                
                elif error_type == "rate_limit":
                    st.error("""
                    ❌ **Rate Limit Exceeded**
                    
                    **Problem:** Too many API requests
                    
                    **Solution:**
                    - Wait 1-2 minutes and try again
                    - Or use Ollama (free, no rate limits)
                    - Or upgrade your API plan
                    """)
                
                else:
                    st.error(f"""
                    ❌ **LLM Error Occurred**
                    
                    **Problem:** {llm_error.get('description', 'LLM service error')}
                    
                    **Using Fallback:** Agent used simple rules instead of LLM analysis
                    
                    **To Fix:**
                    - Check that LLM service is running
                    - Verify configuration in .env file
                    - Try a different provider or model
                    """)
                
                st.info("""
                🛠️ **Fallback Mode Active**
                
                The agent used simple rule-based logic instead of LLM analysis.
                Results shown below are from fallback logic, not AI reasoning.
                """)
            
            # Show results (even with fallback)
            st.success("Analysis Complete!" if not result.get("is_fallback") else "Fallback Analysis Complete")

            col1, col2, col3 = st.columns(3)

            with col1:
                direction = result["signal"]["direction"]
                color = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[direction]
                st.metric("Signal", f"{color} {direction.upper()}")

            with col2:
                st.metric("Confidence", f"{result['signal']['confidence']:.1%}")

            with col3:
                st.metric("Runtime", f"{result['execution_time']:.2f}s")

            st.markdown("**Reasoning:**")
            st.info(result["signal"]["reasoning"])

            if "insights" in result["signal"] and result["signal"]["insights"]:
                st.markdown("**Detailed Insights:**")
                for i, insight in enumerate(result["signal"]["insights"], 1):
                    with st.expander(f"Insight {i}"):
                        st.write(insight)

        else:
            st.error(f"Error: {result['error']}")


def show_backtest_page():
    """Display backtesting interface."""
    st.header("📈 Backtest Agent")
    
    st.info("""
    🎯 **What is Backtesting?**
    
    Backtesting shows how your agent would have performed on historical data.
    This helps you understand if your rules would have been profitable.
    
    **⚠️ Important:** Past performance does NOT guarantee future results!
    """)
    
    loader = st.session_state.agent_loader
    agents = loader.list_agents()
    
    if not agents:
        st.info("No agents available to backtest. Create one first!")
        return
    
    # Agent selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        agent_names = [a["name"] for a in agents]
        selected_agent = st.selectbox("🤖 Select Agent to Backtest", agent_names)
        
        agent_info = next(a for a in agents if a["name"] == selected_agent)
        agent_filename = agent_info["filename"]
        agent_class_name = agent_info["name"]  # Store the class name
        agent_type = agent_info["type"]
        
        st.caption(f"Type: **{agent_type}**")
    
    with col2:
        st.markdown("### Quick Info")
        st.caption("ℹ️ Backtesting runs your agent on multiple scenarios to see signal distribution.")
    
    # Data source selection
    st.markdown("---")
    st.subheader("📊 Data Source")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        use_database = st.radio(
            "Data Source",
            ["Mock Data (Scenarios)", "Database (Sample Stocks)"],
            help="Mock data tests various financial scenarios. Database uses actual sample data."
        )
    
    with col_b:
        if use_database == "Database (Sample Stocks)":
            st.info("📁 Uses: AAPL, MSFT, TSLA, JPM from database")
            tickers = ["AAPL", "MSFT", "TSLA", "JPM"]
        else:
            st.info("🎲 Tests 5 scenarios: undervalued, growth, overvalued, balanced, high-debt")
            tickers = ["SCENARIO_1", "SCENARIO_2", "SCENARIO_3", "SCENARIO_4", "SCENARIO_5"]
    
    # Educational disclaimer
    st.markdown("---")
    st.warning("""
    📚 **Educational Backtesting**
    
    This is a simplified backtest for learning purposes:
    
    **What it does:**
    - ✅ Shows signal distribution (bullish/bearish/neutral)
    - ✅ Calculates average confidence
    - ✅ Shows reasoning for each signal
    - ✅ Helps you understand your rules
    
    **What it does NOT do:**
    - ❌ No real price movements
    - ❌ No profit/loss calculation
    - ❌ No transaction costs
    - ❌ No market impact simulation
    
    For production backtesting, use:
    - Backtrader, Zipline, QuantConnect
    - Or thesis-app with real historical data
    """)
    
    # Run backtest button
    st.markdown("---")
    
    if st.button("🚀 Run Backtest", type="primary", use_container_width=True):
        with st.spinner("Running backtest..."):
            import asyncio
            
            backtester = Backtester()
            
            # Run async backtest
            success, result, error = asyncio.run(
                backtester.run_backtest(
                    agent_filename,
                    tickers,
                    use_database=(use_database == "Database (Sample Stocks)"),
                    agent_class_name=agent_class_name  # Pass specific class name!
                )
            )
        
        if success:
            st.success("✅ Backtest Complete!")
            
            # Display results
            st.markdown("---")
            st.subheader("📈 Backtest Results")
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Signals", result.total_signals)
            
            with col2:
                st.metric("Avg Confidence", f"{result.avg_confidence:.1%}")
            
            with col3:
                win_rate = result.get_win_rate()
                st.metric("Bullish Signals", f"{win_rate:.1%}")
                st.caption("(Simplified win rate)")
            
            with col4:
                st.metric("Execution Time", f"{result.execution_time:.2f}s")
            
            # Signal distribution
            st.markdown("---")
            st.subheader("📊 Signal Distribution")
            
            col_x, col_y = st.columns([2, 1])
            
            with col_x:
                # Create bar chart data
                import pandas as pd
                
                chart_data = pd.DataFrame({
                    'Signal': ['🟢 Bullish', '🔴 Bearish', '🟡 Neutral'],
                    'Count': [result.bullish_count, result.bearish_count, result.neutral_count]
                })
                
                st.bar_chart(chart_data.set_index('Signal'))
            
            with col_y:
                st.markdown("**Summary:**")
                st.write(f"🟢 Bullish: {result.bullish_count} ({result.bullish_count/result.total_signals*100:.1f}%)")
                st.write(f"🔴 Bearish: {result.bearish_count} ({result.bearish_count/result.total_signals*100:.1f}%)")
                st.write(f"🟡 Neutral: {result.neutral_count} ({result.neutral_count/result.total_signals*100:.1f}%)")
                
                st.markdown("---")
                
                # Interpretation
                if result.bullish_count > result.bearish_count + result.neutral_count:
                    st.success("📈 Very bullish strategy")
                elif result.bearish_count > result.bullish_count + result.neutral_count:
                    st.error("📉 Very bearish strategy")
                elif result.neutral_count > result.bullish_count + result.bearish_count:
                    st.info("🟡 Mostly neutral - conservative")
                else:
                    st.info("⚖️ Balanced strategy")
            
            # Detailed signals by ticker
            st.markdown("---")
            st.subheader("📝 Detailed Signals")
            
            for ticker, signals in result.signals_by_ticker.items():
                with st.expander(f"**{ticker}** ({len(signals)} signal(s))"):
                    for i, sig in enumerate(signals, 1):
                        direction_emoji = {
                            'bullish': '🟢',
                            'bearish': '🔴',
                            'neutral': '🟡'
                        }[sig['direction']]
                        
                        st.markdown(f"**Signal {i}:** {direction_emoji} {sig['direction'].upper()}")
                        st.write(f"Confidence: {sig['confidence']:.1%}")
                        st.caption(f"Reasoning: {sig['reasoning']}")
                        
                        if i < len(signals):
                            st.markdown("---")
            
            # Learning tips
            st.markdown("---")
            st.info("""
            💡 **How to Use These Results:**
            
            1. **High Bullish %:** Your rules favor buying - good for bull markets
            2. **High Bearish %:** Your rules favor selling - good for bear markets
            3. **High Neutral %:** Very conservative - may miss opportunities
            4. **Low Confidence:** Rules might be too vague - refine thresholds
            5. **High Confidence:** Rules are very specific - might miss edge cases
            
            **Next Steps:**
            - Adjust your rules based on these insights
            - Run backtest again to see improvements
            - Compare different agent strategies
            - Remember: This is for learning, not real trading!
            """)
            
        else:
            st.error(f"❌ Backtest Failed: {error}")
            st.info("🛈 **Troubleshooting:**\n- Make sure agent file exists\n- Check agent code for errors\n- Try with mock data first")


if __name__ == "__main__":
    main()
