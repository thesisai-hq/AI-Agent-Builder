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
from gui.metrics import MetricDefinitions, RuleValidator

# Page configuration
st.set_page_config(
    page_title="AI Agent Builder",
    page_icon="🤖",
    layout="wide"
)

# Cache metric definitions for performance
@st.cache_data
def get_metric_definitions():
    """Cache metric definitions to avoid repeated calls."""
    return MetricDefinitions.get_all_metrics()

def main():
    """Main application entry point."""
    st.title("🤖 AI Agent Builder")
    st.markdown("Create and manage AI investment agents")
    
    # Initialize session state
    if 'agent_loader' not in st.session_state:
        # Get absolute path to examples directory
        examples_dir = Path(__file__).parent.parent / "examples"
        examples_dir = examples_dir.resolve()
        st.session_state.agent_loader = AgentLoader(examples_dir)
        st.session_state.examples_dir = examples_dir
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["📋 Browse Agents", "➕ Create Agent", "🧪 Test Agent"]
    )
    
    # Show quick stats
    loader = st.session_state.agent_loader
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Statistics")
    st.sidebar.metric("Total Agents", len(loader.list_agents()))
    
    # Show save location
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Save Location")
    st.sidebar.caption(f"`{st.session_state.examples_dir}`")
    
    # Page routing
    if page == "📋 Browse Agents":
        show_browse_page()
    elif page == "➕ Create Agent":
        show_create_page()
    elif page == "🧪 Test Agent":
        show_test_page()

def show_browse_page():
    """Display agent browsing interface."""
    st.header("Browse Existing Agents")
    
    loader = st.session_state.agent_loader
    agents = loader.list_agents()
    
    if not agents:
        st.info("No agents found in examples/ directory")
        return
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Agents", len(agents))
    with col2:
        rule_based = len([a for a in agents if a['type'] == 'Rule-Based'])
        st.metric("Rule-Based", rule_based)
    with col3:
        llm_powered = len([a for a in agents if 'LLM' in a['type'] or 'RAG' in a['type']])
        st.metric("LLM/RAG", llm_powered)
    with col4:
        custom = len([a for a in agents if not a['filename'].startswith('0')])
        st.metric("Your Agents", custom)
    
    st.markdown("---")
    
    # Search/Filter
    search = st.text_input("🔍 Search agents", placeholder="Type to filter...")
    
    if search:
        agents = [a for a in agents if search.lower() in a['name'].lower() or search.lower() in a['filename'].lower()]
    
    st.caption(f"Showing {len(agents)} agent(s)")
    
    # Display agents in a grid
    cols = st.columns(2)
    for idx, agent_info in enumerate(agents):
        with cols[idx % 2]:
            # Check if framework example (can't delete)
            is_framework_example = agent_info['filename'].startswith('0')
            
            with st.expander(f"**{agent_info['name']}**", expanded=False):
                st.markdown(f"**File:** `{agent_info['filename']}`")
                st.markdown(f"**Type:** {agent_info['type']}")
                
                # Action buttons
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    if st.button("👁️ View", key=f"view_{agent_info['filename']}", use_container_width=True):
                        code = loader.get_agent_code(agent_info['filename'])
                        st.code(code, language="python")
                
                with col_b:
                    if st.button("📋 Copy", key=f"dup_{agent_info['filename']}", use_container_width=True):
                        st.session_state[f"duplicating_{agent_info['filename']}"] = True
                
                with col_c:
                    code = loader.get_agent_code(agent_info['filename'])
                    st.download_button(
                        "⬇️ Export",
                        data=code,
                        file_name=agent_info['filename'],
                        mime="text/x-python",
                        key=f"export_{agent_info['filename']}",
                        use_container_width=True
                    )
                
                with col_d:
                    if is_framework_example:
                        st.button("🔒 Protected", disabled=True, key=f"del_{agent_info['filename']}", use_container_width=True)
                    else:
                        if st.button("🗑️ Delete", key=f"del_{agent_info['filename']}", type="secondary", use_container_width=True):
                            st.session_state[f"deleting_{agent_info['filename']}"] = True
                
                # Handle duplicate dialog
                if st.session_state.get(f"duplicating_{agent_info['filename']}"):
                    st.markdown("---")
                    st.markdown("**Duplicate Agent**")
                    
                    base_name = agent_info['filename'][:-3]
                    suggested_name = f"{base_name}_copy.py"
                    
                    new_name = st.text_input(
                        "New filename:",
                        value=suggested_name,
                        key=f"new_name_{agent_info['filename']}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Duplicate", key=f"confirm_dup_{agent_info['filename']}"):
                            success, message = loader.duplicate_agent(agent_info['filename'], new_name)
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
                        if st.button("🗑️ Confirm Delete", key=f"confirm_del_{agent_info['filename']}", type="primary"):
                            success, message = loader.delete_agent(agent_info['filename'])
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
    
    st.info("💡 **Tip:** Browse the examples directory to see strategy templates (Buffett, Lynch, Graham, etc.). Duplicate them to create variations!")
    
    # Initialize session state for generated code
    if 'generated_code' not in st.session_state:
        st.session_state.generated_code = None
    if 'current_filename' not in st.session_state:
        st.session_state.current_filename = None
    
    creator = AgentCreator()
    
    # Agent configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Information")
        agent_name = st.text_input(
            "Agent Class Name",
            value="MyAgent",
            help="Python class name (e.g., ValueAgent, GrowthAgent)"
        )
        
        description = st.text_area(
            "Description",
            help="What does this agent do?"
        )
        
        filename = st.text_input(
            "Filename",
            value=f"{agent_name.lower() if agent_name else 'my_agent'}.py",
            help="File will be saved in examples/ directory"
        )
        
        if filename:
            save_path = st.session_state.examples_dir / filename
            st.caption(f"Will save to: `{save_path}`")
    
    with col2:
        st.subheader("Agent Type")
        agent_type = st.selectbox(
            "Template",
            ["Rule-Based", "LLM-Powered", "Hybrid", "RAG-Powered"]
        )
        
        if agent_type in ["LLM-Powered", "Hybrid", "RAG-Powered"]:
            st.markdown("**LLM Configuration**")
            llm_provider = st.selectbox("Provider", ["ollama", "openai", "anthropic"])
            temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
            max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)
            system_prompt = st.text_area(
                "System Prompt",
                height=100,
                help="Define the agent's personality and approach"
            )
        else:
            llm_provider = None
            temperature = None
            max_tokens = None
            system_prompt = None
        
        if agent_type == "RAG-Powered":
            st.markdown("**RAG Configuration**")
            chunk_size = st.number_input("Chunk Size", 100, 1000, 300, 50,
                help="Size of text chunks for vector search")
            chunk_overlap = st.number_input("Chunk Overlap", 0, 200, 50, 10,
                help="Overlap between chunks")
            top_k = st.number_input("Top K Results", 1, 10, 3, 1,
                help="Number of relevant chunks to retrieve")
        else:
            chunk_size = None
            chunk_overlap = None
            top_k = None
    
    # Analysis Logic
    st.subheader("Analysis Logic")
    
    if agent_type == "Rule-Based":
        st.markdown("Define your investment strategy:")
        
        rule_style = st.radio(
            "Rule Style",
            ["Simple Rules", "Advanced Rules", "Score-Based"],
            help="Simple: Single conditions | Advanced: Multi-condition AND/OR | Score: Point accumulation"
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
                            ["pe_ratio", "revenue_growth", "profit_margin", "roe", 
                             "debt_to_equity", "dividend_yield", "pb_ratio", "current_ratio"],
                            key=f"metric_{i}",
                            help="Hover over threshold field for metric details"
                        )
                    
                    with col_b:
                        operator = st.selectbox("Operator", ["<", ">", "<=", ">=", "=="], key=f"op_{i}")
                    
                    with col_c:
                        # Get metric definition for tooltip
                        metrics = get_metric_definitions()
                        metric_def = metrics.get(metric, {})
                        
                        threshold = st.number_input(
                            "Threshold",
                            key=f"thresh_{i}",
                            help=metric_def.get('tooltip', 'Enter threshold value')
                        )
                        
                        # Validate threshold
                        is_valid, error_msg = MetricDefinitions.validate_value(metric, threshold)
                        if not is_valid:
                            st.error(error_msg)
                            validation_warnings.append(f"Rule {i+1}: {error_msg}")
                        
                        # Check threshold logic
                        logic_warning = RuleValidator.validate_threshold_logic(metric, operator, threshold)
                        if logic_warning:
                            st.warning(logic_warning)
                        
                        # Get suggestion
                        suggestion = MetricDefinitions.get_suggestion(metric, threshold, operator)
                        if suggestion:
                            st.info(suggestion)
                    
                    direction = st.selectbox("Signal", ["bullish", "bearish", "neutral"], key=f"dir_{i}")
                    confidence = st.slider("Confidence", 0.0, 1.0, 0.7, 0.1, key=f"conf_{i}")
                    
                    rules.append({
                        "type": "simple",
                        "metric": metric,
                        "operator": operator,
                        "threshold": threshold,
                        "direction": direction,
                        "confidence": confidence
                    })
            
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
                    num_conditions = st.number_input("Number of Conditions", 1, 5, 2, key=f"num_cond_{i}")
                    logic_operator = st.selectbox("Combine conditions with", ["AND", "OR"], key=f"logic_{i}")
                    
                    conditions = []
                    for j in range(num_conditions):
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            metric = st.selectbox(
                                "Metric",
                                ["pe_ratio", "revenue_growth", "profit_margin", "roe",
                                 "debt_to_equity", "dividend_yield", "pb_ratio", "current_ratio",
                                 "peg_ratio", "quality_score"],
                                key=f"adv_metric_{i}_{j}",
                                help="Hover over Value field for details"
                            )
                        
                        with col_b:
                            operator = st.selectbox("Op", ["<", ">", "<=", ">=", "=="], key=f"adv_op_{i}_{j}")
                        
                        with col_c:
                            metrics = get_metric_definitions()
                            metric_def = metrics.get(metric, {})
                            threshold = st.number_input(
                                "Value",
                                key=f"adv_thresh_{i}_{j}",
                                help=metric_def.get('tooltip', 'Enter value')
                            )
                            
                            # Validate
                            is_valid, error_msg = MetricDefinitions.validate_value(metric, threshold)
                            if not is_valid:
                                st.error(error_msg)
                        
                        conditions.append({"metric": metric, "operator": operator, "threshold": threshold})
                    
                    direction = st.selectbox("Signal", ["bullish", "bearish", "neutral"], key=f"adv_dir_{i}")
                    confidence = st.slider("Confidence", 0.0, 1.0, 0.7, 0.1, key=f"adv_conf_{i}")
                    
                    rules.append({
                        "type": "advanced",
                        "conditions": conditions,
                        "logic": logic_operator,
                        "direction": direction,
                        "confidence": confidence
                    })
        
        else:  # Score-Based
            st.markdown("**Score-Based Strategy:** Accumulate points, decide signal based on total score.")
            
            num_criteria = st.number_input("Number of Scoring Criteria", 1, 10, 5)
            criteria = []
            
            for i in range(num_criteria):
                with st.expander(f"Criterion {i+1}"):
                    col_a, col_b, col_c, col_d = st.columns(4)
                    
                    with col_a:
                        metric = st.selectbox(
                            "Metric",
                            ["pe_ratio", "revenue_growth", "profit_margin", "roe",
                             "debt_to_equity", "dividend_yield", "pb_ratio", "current_ratio"],
                            key=f"score_metric_{i}",
                            help="Hover over Value for details"
                        )
                    
                    with col_b:
                        operator = st.selectbox("Op", ["<", ">", "<=", ">="], key=f"score_op_{i}")
                    
                    with col_c:
                        metrics = get_metric_definitions()
                        metric_def = metrics.get(metric, {})
                        threshold = st.number_input(
                            "Value",
                            key=f"score_thresh_{i}",
                            help=metric_def.get('tooltip', 'Enter value')
                        )
                        
                        # Validate
                        is_valid, error_msg = MetricDefinitions.validate_value(metric, threshold)
                        if not is_valid:
                            st.error(error_msg)
                    
                    with col_d:
                        points = st.number_input(
                            "Points",
                            -5, 5, 1,
                            key=f"score_pts_{i}",
                            help="Positive points for good, negative for bad. Typical: +1 or +2 for positive factors, -1 or -2 for red flags"
                        )
                    
                    criteria.append({
                        "metric": metric,
                        "operator": operator,
                        "threshold": threshold,
                        "points": points
                    })
            
            st.markdown("**Score Thresholds:**")
            col1, col2 = st.columns(2)
            with col1:
                bullish_threshold = st.number_input("Bullish if score >=", 0, 20, 3)
                bullish_confidence = st.slider("Bullish Confidence", 0.0, 1.0, 0.8, 0.1, key="bullish_conf")
            with col2:
                bearish_threshold = st.number_input("Bearish if score <=", -20, 0, -2)
                bearish_confidence = st.slider("Bearish Confidence", 0.0, 1.0, 0.7, 0.1, key="bearish_conf")
            
            rules = [{
                "type": "score",
                "criteria": criteria,
                "bullish_threshold": bullish_threshold,
                "bullish_confidence": bullish_confidence,
                "bearish_threshold": bearish_threshold,
                "bearish_confidence": bearish_confidence
            }]
    
    elif agent_type == "RAG-Powered":
        rules = None
        st.info("📄 RAG agents analyze documents/text using retrieval and embeddings")
    else:
        rules = None
        st.info("LLM-powered agents use natural language prompts instead of explicit rules")
    
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
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            top_k=top_k
        )
        
        st.session_state.generated_code = code
        st.session_state.current_filename = filename
    
    # Display generated code if available
    if st.session_state.generated_code:
        st.code(st.session_state.generated_code, language="python")
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("💾 Save Agent"):
                loader = st.session_state.agent_loader
                success, message = loader.save_agent(
                    st.session_state.current_filename,
                    st.session_state.generated_code
                )
                if success:
                    st.success(message)
                    st.balloons()
                    st.session_state.generated_code = None
                    st.session_state.current_filename = None
                else:
                    st.error(message)
        
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
    
    agent_names = [a['name'] for a in agents]
    selected_agent = st.selectbox("Select Agent", agent_names)
    
    agent_info = next(a for a in agents if a['name'] == selected_agent)
    agent_filename = agent_info['filename']
    agent_type = agent_info['type']
    
    st.info(f"Agent Type: **{agent_type}**")
    
    ticker = st.text_input("Ticker Symbol", value="AAPL")
    
    if agent_type == "RAG-Powered":
        st.subheader("📄 Document Upload")
        st.markdown("RAG agents analyze documents. Upload a PDF to test:")
        
        uploaded_file = st.file_uploader(
            "Drag and drop PDF here",
            type=['pdf'],
            help="Upload SEC filing, earnings report, or any financial document"
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
                        height=200
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
                pe_def = metrics['pe_ratio']
                mock_data['pe_ratio'] = st.number_input(
                    "PE Ratio",
                    5.0, 100.0, 20.0,
                    help=pe_def['tooltip']
                )
                
                growth_def = metrics['revenue_growth']
                mock_data['revenue_growth'] = st.number_input(
                    "Revenue Growth (%)",
                    -20.0, 100.0, 15.0,
                    help=growth_def['tooltip']
                )
            
            with col_b:
                margin_def = metrics['profit_margin']
                mock_data['profit_margin'] = st.number_input(
                    "Profit Margin (%)",
                    -10.0, 50.0, 12.0,
                    help=margin_def['tooltip']
                )
                
                roe_def = metrics['roe']
                mock_data['roe'] = st.number_input(
                    "ROE (%)",
                    -20.0, 50.0, 15.0,
                    help=roe_def['tooltip']
                )
            
            with col_c:
                debt_def = metrics['debt_to_equity']
                mock_data['debt_to_equity'] = st.number_input(
                    "Debt/Equity",
                    0.0, 5.0, 0.8,
                    help=debt_def['tooltip']
                )
                
                div_def = metrics['dividend_yield']
                mock_data['dividend_yield'] = st.number_input(
                    "Dividend Yield (%)",
                    0.0, 10.0, 2.0,
                    help=div_def['tooltip']
                )
        else:
            mock_data = None
    
    if st.button("🚀 Run Analysis", type="primary"):
        tester = AgentTester()
        
        if agent_type == "RAG-Powered" and not uploaded_file:
            st.error("Please upload a PDF document to test RAG agent")
            return
        
        with st.spinner("Running analysis..."):
            result = tester.test_agent(agent_filename, ticker, mock_data, uploaded_file)
        
        if result['success']:
            st.success("Analysis Complete!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                direction = result['signal']['direction']
                color = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}[direction]
                st.metric("Signal", f"{color} {direction.upper()}")
            
            with col2:
                st.metric("Confidence", f"{result['signal']['confidence']:.1%}")
            
            with col3:
                st.metric("Runtime", f"{result['execution_time']:.2f}s")
            
            st.markdown("**Reasoning:**")
            st.info(result['signal']['reasoning'])
            
            if 'insights' in result['signal'] and result['signal']['insights']:
                st.markdown("**Detailed Insights:**")
                for i, insight in enumerate(result['signal']['insights'], 1):
                    with st.expander(f"Insight {i}"):
                        st.write(insight)
            
        else:
            st.error(f"Error: {result['error']}")

if __name__ == "__main__":
    main()
