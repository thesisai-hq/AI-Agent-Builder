"""Test results display component.

Renders test results with metrics, reasoning, and error messages.
Handles both successful and failed test scenarios.
"""

from typing import Dict, Optional

import streamlit as st


def display_test_results(result: Dict) -> None:
    """Display successful test results.
    
    Args:
        result: Test result dictionary with signal and execution_time
    """
    # Check for fallback mode
    if result.get("is_fallback", False):
        _show_fallback_warning(result)
    
    st.success("Analysis Complete!" if not result.get("is_fallback") else "Fallback Analysis Complete")
    
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
    _show_llm_error_solution(llm_error)
    
    st.info("""
    🛠️ **Fallback Mode Active**
    
    The agent used simple rule-based logic instead of LLM analysis.
    Results shown below are from fallback logic, not AI reasoning.
    """)


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
    
    Args:
        result: Test result with error and error_type
    """
    error_type = result.get("error_type", "unknown")
    
    if error_type == "missing_package":
        _show_missing_package_error(result)
    elif error_type == "model_not_found":
        _show_model_not_found_error(result)
    elif error_type == "connection_error":
        _show_connection_error(result)
    elif error_type == "missing_api_key":
        _show_missing_api_key_error(result)
    elif error_type == "rate_limit":
        _show_rate_limit_error(result)
    else:
        _show_generic_error(result)


def _show_llm_error_solution(llm_error: Dict) -> None:
    """Show specific solution for LLM error type.
    
    Args:
        llm_error: LLM error info dict
    """
    error_type = llm_error.get("error_type")
    
    if error_type == "missing_package":
        st.error(f"""
        ❌ **Missing LLM Package**
        
        **Problem:** {llm_error.get("description")}
        
        **Solution:** Install the required package:
        ```bash
        {llm_error.get("install_command")}
        ```
        
        Or install all LLM providers:
        ```bash
        pip install 'ai-agent-framework[llm]'
        ```
        """)
    
    elif error_type == "model_not_found":
        model_name = llm_error.get("model", "llama3.2")
        st.error(f"""
        ❌ **Model Not Available**
        
        **Problem:** Model '{model_name}' not downloaded
        
        **Solution:** Download the model with Ollama:
        ```bash
        {llm_error.get("install_command")}
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
        provider = llm_error.get("provider", "unknown")
        env_var = f"{provider.upper()}_API_KEY" if provider != "unknown" else "API_KEY"
        
        st.error(f"""
        ❌ **API Key Not Configured**
        
        **Problem:** {llm_error.get("description")}
        
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


def _show_missing_package_error(result: Dict) -> None:
    """Show missing package error."""
    st.error(f"❌ Error: {result['error']}")
    st.info("💡 Install required packages: `pip install 'ai-agent-framework[llm]'`")


def _show_model_not_found_error(result: Dict) -> None:
    """Show model not found error."""
    st.error(f"❌ Error: {result['error']}")
    st.info("💡 Download the model: `ollama pull llama3.2`")


def _show_connection_error(result: Dict) -> None:
    """Show connection error."""
    st.error(f"❌ Error: {result['error']}")
    st.info("💡 Start Ollama service: `ollama serve`")


def _show_missing_api_key_error(result: Dict) -> None:
    """Show missing API key error."""
    st.error(f"❌ Error: {result['error']}")
    st.info("💡 Add API key to .env file")


def _show_rate_limit_error(result: Dict) -> None:
    """Show rate limit error."""
    st.error(f"❌ Error: {result['error']}")
    st.info("💡 Wait a minute or use Ollama instead")


def _show_generic_error(result: Dict) -> None:
    """Show generic error message."""
    st.error(f"❌ Error: {result['error']}")
