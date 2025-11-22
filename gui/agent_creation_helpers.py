"""Helper functions for agent creation UI.

Extracted from app.py to improve maintainability and testability.
Each function handles a specific UI section or logic.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st

from gui.metrics import MetricDefinitions, RuleValidator


# ============================================================================
# Session State Management
# ============================================================================


class AgentCreationState:
    """Manages session state for agent creation."""

    @staticmethod
    def get_generated_code() -> Optional[str]:
        """Get currently generated code."""
        return st.session_state.get("generated_code")

    @staticmethod
    def set_generated_code(code: str):
        """Set generated code in session state."""
        st.session_state.generated_code = code

    @staticmethod
    def clear_generated_code():
        """Clear generated code from session state."""
        st.session_state.generated_code = None
        st.session_state.current_filename = None

    @staticmethod
    def get_filename() -> Optional[str]:
        """Get current filename."""
        return st.session_state.get("current_filename")

    @staticmethod
    def set_filename(filename: str):
        """Set current filename in session state."""
        st.session_state.current_filename = filename


# ============================================================================
# Validation Helpers
# ============================================================================


def validate_and_show_filename_status(filename: str, examples_dir: Path) -> bool:
    """Validate filename and show appropriate status message.

    Args:
        filename: Filename to validate
        examples_dir: Examples directory path

    Returns:
        True if filename is valid and available
    """
    if not filename:
        return False

    if not filename.endswith(".py"):
        st.error("❌ Filename must end with .py")
        return False

    # Import here to avoid circular dependency
    from gui.agent_loader import AgentLoader

    # Check valid Python identifier
    if not AgentLoader._is_valid_filename(filename):
        st.error("❌ Invalid filename. Use only letters, numbers, and underscores")
        st.caption("Valid: `my_agent.py` | Invalid: `my-agent.py`, `1agent.py`")
        return False

    # Check if exists
    if (examples_dir / filename).exists():
        st.warning(f"⚠️ File `{filename}` already exists. Choose a different name.")
        return False

    # All good!
    st.success(f"✅ Valid filename: will save to `examples/{filename}`")
    return True


def handle_agent_save(filename: str, code: str, loader) -> Tuple[bool, str]:
    """Handle saving agent with validation.

    Args:
        filename: Filename to save as
        code: Agent code to save
        loader: AgentLoader instance

    Returns:
        Tuple of (success, message)
    """
    if not filename or not code:
        return False, "Missing filename or code"

    # Validate filename one more time
    if not filename.endswith(".py"):
        return False, "Filename must end with .py"

    # Attempt save
    success, message = loader.save_agent(filename, code)

    return success, message


# ============================================================================
# UI Section Builders
# ============================================================================


def show_basic_info_section() -> Dict[str, str]:
    """Show basic info section and return user inputs.

    Returns:
        Dict with 'agent_name', 'description', 'filename'
    """
    st.subheader("Basic Information")

    agent_name = st.text_input(
        "Agent Class Name",
        value="MyAgent",
        help="Python class name (e.g., ValueAgent, GrowthAgent)",
    )

    description = st.text_area("Description", help="What does this agent do?")

    # Auto-generate filename from agent name
    default_filename = f"{agent_name.lower() if agent_name else 'my_agent'}.py"
    filename = st.text_input(
        "Filename",
        value=default_filename,
        help="File will be saved in examples/ directory",
    )

    # Validate and show status
    if filename:
        examples_dir = st.session_state.examples_dir
        validate_and_show_filename_status(filename, examples_dir)

    return {"agent_name": agent_name, "description": description, "filename": filename}


def show_agent_type_section() -> Dict[str, str]:
    """Show agent type selection and return configuration.

    Returns:
        Dict with 'agent_type'
    """
    st.subheader("Agent Type")

    agent_type = st.selectbox("Template", ["Rule-Based", "LLM-Powered", "Hybrid", "RAG-Powered"])

    # Show type-specific info
    if agent_type == "Hybrid":
        st.info(
            """
        🧑‍💻 **What is a Hybrid Agent?**

        Combines rules + LLM:
        1. **Rules:** Fast screening (filter stocks)
        2. **LLM:** Deep analysis (only on filtered stocks)

        **Use when:** You want to screen thousands of stocks quickly,
        then use AI for detailed analysis on candidates.
        """
        )

    return {"agent_type": agent_type}


def show_llm_configuration() -> Dict:
    """Show LLM configuration UI.

    Returns:
        Dict with LLM config: provider, model, temperature, max_tokens, prompts
    """
    st.markdown("**LLM Configuration**")

    # Provider selection
    llm_provider = st.selectbox(
        "Provider",
        ["ollama", "openai", "anthropic"],
        help="LLM service provider. Ollama is free and local.",
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
            "custom (enter below)",
        ],
        "openai": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
            "custom (enter below)",
        ],
        "anthropic": [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "custom (enter below)",
        ],
    }

    selected_model = st.selectbox("Model", model_options[llm_provider])

    # Handle custom model
    if selected_model == "custom (enter below)":
        custom_model = st.text_input(
            "Custom Model Name", placeholder=f"Enter exact model name for {llm_provider}"
        )
        final_model = custom_model if custom_model else model_options[llm_provider][0]
    else:
        final_model = selected_model

    # Show model info
    model_info = {
        "llama3.2": "💡 Latest Llama model, good balance of speed and quality",
        "gpt-4o": "💡 Latest GPT-4 with vision, fastest GPT-4 model",
        "gpt-4o-mini": "💡 Cost-effective GPT-4, 60% cheaper than GPT-4o",
        "claude-3-5-sonnet-20241022": "💡 Latest Claude, best for analysis",
        "claude-3-5-haiku-20241022": "💡 Fastest Claude, good for simple tasks",
        "mistral": "💡 Good open-source alternative, fast inference",
        "gpt-4": "💡 Original GPT-4, very capable but slower",
        "gpt-3.5-turbo": "💡 Fast and cheap, good for simple analysis",
    }

    if selected_model in model_info:
        st.caption(model_info[selected_model])

    # Settings
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)

    # Prompts
    st.markdown("**Prompts (AI Instructions)**")

    system_prompt = st.text_area(
        "System Prompt (Agent Personality)",
        height=120,
        help="Defines who the AI is and its overall approach.",
        placeholder="Example: You are a value investor inspired by Warren Buffett...",
    )

    # Optional custom instructions
    user_prompt_instructions = None
    with st.expander("➕ Add Custom Analysis Instructions (Optional)", expanded=False):
        st.info(
            """
        **What are User Prompt Instructions?**

        Add specific questions or analysis requirements beyond the standard.

        **Examples:**
        - "Focus specifically on dividend safety"
        - "Assess the competitive moat"
        - "Evaluate management decisions"
        """
        )

        user_prompt_instructions = st.text_area(
            "Custom Analysis Instructions",
            height=80,
            placeholder="Example: Focus on dividend safety...",
        )

        if user_prompt_instructions:
            st.success(f"✅ Custom instructions added ({len(user_prompt_instructions)} chars)")

    return {
        "provider": llm_provider,
        "model": final_model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "system_prompt": system_prompt,
        "user_instructions": user_prompt_instructions,
    }


def show_rag_configuration() -> Dict:
    """Show RAG configuration UI.

    Returns:
        Dict with RAG config: chunk_size, chunk_overlap, top_k
    """
    st.markdown("**RAG Configuration**")

    chunk_size = st.number_input(
        "Chunk Size", 100, 1000, 300, 50, help="Size of text chunks for vector search"
    )
    chunk_overlap = st.number_input("Chunk Overlap", 0, 200, 50, 10, help="Overlap between chunks")
    top_k = st.number_input(
        "Top K Results", 1, 10, 3, 1, help="Number of relevant chunks to retrieve"
    )

    return {"chunk_size": chunk_size, "chunk_overlap": chunk_overlap, "top_k": top_k}


# ============================================================================
# Rules UI Sections
# ============================================================================


def show_simple_rules_ui(num_rules: int) -> List[Dict]:
    """Show simple rules UI and return rule configurations.

    Args:
        num_rules: Number of rules to create

    Returns:
        List of rule dictionaries
    """
    rules = []
    metrics = MetricDefinitions.get_all_metrics()

    for i in range(num_rules):
        with st.expander(f"Rule {i + 1}"):
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
                    help="Hover over threshold for details",
                )

            with col_b:
                operator = st.selectbox("Operator", ["<", ">", "<=", ">=", "=="], key=f"op_{i}")

            with col_c:
                metric_def = metrics.get(metric, {})
                threshold = st.number_input(
                    "Threshold", key=f"thresh_{i}", help=metric_def.get("tooltip", "")
                )

                # Validate
                is_valid, error_msg = MetricDefinitions.validate_value(metric, threshold)
                if not is_valid:
                    st.error(error_msg)

                # Check logic
                logic_warning = RuleValidator.validate_threshold_logic(metric, operator, threshold)
                if logic_warning:
                    st.warning(logic_warning)

                # Get suggestion
                suggestion = MetricDefinitions.get_suggestion(metric, threshold, operator)
                if suggestion:
                    st.info(suggestion)

            direction = st.selectbox("Signal", ["bullish", "bearish", "neutral"], key=f"dir_{i}")
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

    # Check conflicts
    conflicts = RuleValidator.check_conflicts(rules)
    if conflicts:
        st.warning("**Rule Conflicts Detected:**")
        for conflict in conflicts:
            st.warning(conflict)

    return rules


def show_advanced_rules_ui(num_rules: int) -> List[Dict]:
    """Show advanced rules UI with multi-condition logic.

    Args:
        num_rules: Number of advanced rules to create

    Returns:
        List of advanced rule dictionaries
    """
    rules = []
    metrics = MetricDefinitions.get_all_metrics()

    for i in range(num_rules):
        with st.expander(f"Advanced Rule {i + 1}"):
            num_conditions = st.number_input("Number of Conditions", 1, 5, 2, key=f"num_cond_{i}")
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
                    )

                with col_b:
                    operator = st.selectbox(
                        "Op", ["<", ">", "<=", ">=", "=="], key=f"adv_op_{i}_{j}"
                    )

                with col_c:
                    metric_def = metrics.get(metric, {})
                    threshold = st.number_input(
                        "Value", key=f"adv_thresh_{i}_{j}", help=metric_def.get("tooltip", "")
                    )

                    # Validate
                    is_valid, error_msg = MetricDefinitions.validate_value(metric, threshold)
                    if not is_valid:
                        st.error(error_msg)

                conditions.append({"metric": metric, "operator": operator, "threshold": threshold})

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

    return rules


def show_score_based_ui(num_criteria: int) -> List[Dict]:
    """Show score-based strategy UI.

    Args:
        num_criteria: Number of scoring criteria

    Returns:
        List with single score-based rule config
    """
    st.markdown("**Score-Based Strategy:** Accumulate points, decide signal based on total score.")

    criteria = []
    metrics = MetricDefinitions.get_all_metrics()

    for i in range(num_criteria):
        with st.expander(f"Criterion {i + 1}"):
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
                )

            with col_b:
                operator = st.selectbox("Op", ["<", ">", "<=", ">="], key=f"score_op_{i}")

            with col_c:
                metric_def = metrics.get(metric, {})
                threshold = st.number_input(
                    "Value", key=f"score_thresh_{i}", help=metric_def.get("tooltip", "")
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
                    help="Positive for good, negative for bad",
                )

            criteria.append(
                {"metric": metric, "operator": operator, "threshold": threshold, "points": points}
            )

    st.markdown("**Score Thresholds:**")
    col1, col2 = st.columns(2)
    with col1:
        bullish_threshold = st.number_input("Bullish if score >=", 0, 20, 3)
        bullish_confidence = st.slider("Bullish Confidence", 0.0, 1.0, 0.8, 0.1, key="bullish_conf")
    with col2:
        bearish_threshold = st.number_input("Bearish if score <=", -20, 0, -2)
        bearish_confidence = st.slider("Bearish Confidence", 0.0, 1.0, 0.7, 0.1, key="bearish_conf")

    return [
        {
            "type": "score",
            "criteria": criteria,
            "bullish_threshold": bullish_threshold,
            "bullish_confidence": bullish_confidence,
            "bearish_threshold": bearish_threshold,
            "bearish_confidence": bearish_confidence,
        }
    ]


def show_analysis_logic_section(agent_type: str) -> Optional[List[Dict]]:
    """Show analysis logic section based on agent type.

    Args:
        agent_type: Type of agent (Rule-Based, LLM-Powered, etc.)

    Returns:
        List of rules or None
    """
    st.subheader("Analysis Logic")

    # Show confidence explanation
    with st.expander("📊 How Confidence Levels Are Calculated", expanded=False):
        st.markdown(
            """
        **Enhanced Confidence System:**
        
        Confidence is calculated based on signal strength!
        
        **For Rule-Based Agents:**
        - **Barely met** (within 5% of threshold): ~60% confidence
        - **Moderately met** (5-15% from threshold): ~70% confidence
        - **Strongly met** (15-30% from threshold): ~80% confidence
        - **Very strongly met** (>30% from threshold): ~90% confidence
        
        **For Score-Based Agents:**
        - Confidence based on how far past the threshold
        - Margin percentage affects final confidence
        
        **For LLM Agents:**
        - AI provides base confidence
        - Adjusted if reasoning is vague or lacks specifics
        """
        )

    # Only show rules for Rule-Based or Hybrid
    if agent_type not in ["Rule-Based", "Hybrid"]:
        if agent_type == "RAG-Powered":
            st.info("📄 RAG agents analyze documents using retrieval and embeddings")
        else:  # LLM-Powered
            st.info("🤖 LLM-powered agents use natural language prompts")
        return None

    # Show appropriate header
    if agent_type == "Hybrid":
        st.markdown("🎯 **Screening Rules (Step 1: Filter Stocks)**")
        st.caption("Define rules to filter which stocks get LLM analysis")
    else:
        st.markdown("Define your investment strategy:")

    # Rule style selection
    rule_style = st.radio(
        "Rule Style",
        ["Simple Rules", "Advanced Rules", "Score-Based"],
        help="Simple: Single conditions | Advanced: Multi-condition | Score: Point accumulation",
    )

    # Show appropriate UI
    if rule_style == "Simple Rules":
        num_rules = st.number_input("Number of Rules", 1, 5, 2)
        return show_simple_rules_ui(num_rules)
    elif rule_style == "Advanced Rules":
        num_rules = st.number_input("Number of Rules", 1, 3, 1)
        return show_advanced_rules_ui(num_rules)
    else:  # Score-Based
        num_criteria = st.number_input("Number of Scoring Criteria", 1, 10, 5)
        return show_score_based_ui(num_criteria)


# ============================================================================
# Code Display and Actions
# ============================================================================


def show_save_action_buttons(code: str, filename: str, loader, key_suffix: str = ""):
    """Show save, clear, and download buttons.

    This function is reused for both top and bottom button sets.

    Args:
        code: Generated agent code
        filename: Filename to save as
        loader: AgentLoader instance
        key_suffix: Suffix for button keys to avoid duplicates
    """
    col1, col2, col3 = st.columns([2, 2, 3])

    with col1:
        if st.button(
            "💾 Save Agent",
            type="primary",
            use_container_width=True,
            key=f"save_{key_suffix}",
        ):
            with st.spinner(f"Saving {filename}..."):
                success, message = handle_agent_save(filename, code, loader)

            if success:
                st.success(f"✅ {message}")
                st.info("🎉 Your agent is ready! Test it in the '🧪 Test Agent' tab.")
                st.balloons()
                AgentCreationState.clear_generated_code()
                st.rerun()
            else:
                st.error(f"❌ {message}")
                if key_suffix == "bottom":
                    st.info("💡 Scroll up to change the filename, then regenerate.")
                else:
                    st.info("💡 Change the filename above and regenerate.")

    with col2:
        if st.button("🗑️ Clear & Start Over", use_container_width=True, key=f"clear_{key_suffix}"):
            AgentCreationState.clear_generated_code()
            st.rerun()

    with col3:
        st.download_button(
            "⬇️ Download Code",
            data=code,
            file_name=filename,
            mime="text/x-python",
            use_container_width=True,
            key=f"download_{key_suffix}",
        )


def show_generated_code_section(code: str, filename: str, loader):
    """Display generated code with action buttons.

    Args:
        code: Generated agent code
        filename: Filename to save as
        loader: AgentLoader instance
    """
    # Action buttons at top
    st.markdown("### 💾 Save Your Agent")
    show_save_action_buttons(code, filename, loader, key_suffix="top")

    st.markdown("---")

    # Code stats
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Lines of Code", len(code.split("\n")))
    with col_info2:
        st.metric("Characters", len(code))
    with col_info3:
        st.metric("Status", "✅ Ready to Save")

    st.markdown("---")

    # Display code
    st.code(code, language="python")

    # Action buttons at bottom (reusing same function!)
    st.markdown("---")
    st.markdown("### 💾 Quick Actions")
    show_save_action_buttons(code, filename, loader, key_suffix="bottom")
