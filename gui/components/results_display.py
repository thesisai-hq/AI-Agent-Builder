"""Test results display component.

Renders test results with metrics, reasoning, and error messages.
Handles both successful and failed test scenarios.
Uses centralized LLMErrorHandler for consistent error messages.
"""

from typing import Dict

import streamlit as st

from gui.core import LLMErrorHandler


def display_test_results(result: Dict) -> None:
    """Display successful test results.

    Args:
        result: Test result dictionary with signal and execution_time
    """
    # Check for fallback mode
    if result.get("is_fallback", False):
        _show_fallback_warning(result)

    st.success(
        "Analysis Complete!" if not result.get("is_fallback") else "Fallback Analysis Complete"
    )

    _show_result_metrics(result)
    _show_reasoning(result)
    _show_insights(result)


def _show_fallback_warning(result: Dict) -> None:
    """Display warning about LLM fallback mode.

    Args:
        result: Test result with LLM error info
    """
    st.warning("⚠️ **LLM Service Unavailable - Using Fallback Logic**")

    llm_error = result.get("llm_error_info", {})
    if llm_error:
        # Use centralized error handler for solution text
        error_handler = LLMErrorHandler()
        solution_text = error_handler.get_solution_text(llm_error)
        st.error(solution_text)

    st.info(
        """
    🛠️ **Fallback Mode Active**
    
    The agent used simple rule-based logic instead of LLM analysis.
    Results shown below are from fallback logic, not AI reasoning.
    """
    )


def _show_result_metrics(result: Dict) -> None:
    """Display three-column result metrics.

    Args:
        result: Test result with signal and execution_time
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        _show_signal_metric(result["signal"])

    with col2:
        _show_confidence_metric(result["signal"])

    with col3:
        _show_runtime_metric(result["execution_time"])


def _show_signal_metric(signal: Dict) -> None:
    """Display signal direction with emoji.

    Args:
        signal: Signal dict with direction
    """
    direction = signal["direction"]
    emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[direction]
    st.metric("Signal", f"{emoji} {direction.upper()}")


def _show_confidence_metric(signal: Dict) -> None:
    """Display confidence percentage.

    Args:
        signal: Signal dict with confidence
    """
    st.metric("Confidence", f"{signal['confidence']:.1%}")


def _show_runtime_metric(execution_time: float) -> None:
    """Display execution time.

    Args:
        execution_time: Time in seconds
    """
    st.metric("Runtime", f"{execution_time:.2f}s")


def _show_reasoning(result: Dict) -> None:
    """Display agent reasoning.

    Args:
        result: Test result with signal reasoning
    """
    st.markdown("**Reasoning:**")
    st.info(result["signal"]["reasoning"])


def _show_insights(result: Dict) -> None:
    """Display detailed insights if available.

    Args:
        result: Test result with optional insights
    """
    insights = result["signal"].get("insights", [])
    if not insights:
        return

    st.markdown("**Detailed Insights:**")
    for i, insight in enumerate(insights, 1):
        with st.expander(f"Insight {i}"):
            st.write(insight)


def display_error_with_solution(result: Dict) -> None:
    """Display error message with actionable solution.

    Uses centralized LLMErrorHandler for consistent error messages.

    Args:
        result: Test result with error and optional error_info
    """
    error_info = result.get("error_info")

    if error_info:
        # Use centralized error handler
        error_handler = LLMErrorHandler()
        solution_text = error_handler.get_solution_text(error_info)
        st.error(solution_text)
    else:
        # Fallback for non-LLM errors
        error_type = result.get("error_type", "unknown")

        if error_type == "timeout":
            st.error(
                """⚠️ **Request Timed Out**

**Problem:** Analysis took too long to complete

**Solutions to try:**
1. Try again (might be temporary slowness)
2. Use simpler test data
3. Check if LLM service is responsive"""
            )
        else:
            # Generic error
            st.error(f"❌ **Error**\n\n{result.get('error', 'Unknown error occurred')}")
            st.info(
                """💡 **Troubleshooting:**
- Check that all dependencies are installed
- Verify LLM service is running (for LLM agents)
- Check agent code for syntax errors
- Try with mock data first"""
            )
