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

# Page configuration
st.set_page_config(
    page_title="AI Agent Builder",
    page_icon="🤖",
    layout="wide"
)

def main():
    """Main application entry point."""
    st.title("🤖 AI Agent Builder")
    st.markdown("Create and manage AI investment agents")
    
    # Initialize session state
    if 'agent_loader' not in st.session_state:
        # Get absolute path to examples directory
        examples_dir = Path(__file__).parent.parent / "examples"
        examples_dir = examples_dir.resolve()  # Convert to absolute path
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
    
    # Display agents in a grid
    cols = st.columns(2)
    for idx, agent_info in enumerate(agents):
        with cols[idx % 2]:
            with st.expander(f"**{agent_info['name']}**"):
                st.markdown(f"**File:** `{agent_info['filename']}`")
                st.markdown(f"**Type:** {agent_info['type']}")
                
                # Show code preview
                if st.button("View Code", key=f"view_{agent_info['filename']}"):
                    code = loader.get_agent_code(agent_info['filename'])
                    st.code(code, language="python")

def show_create_page():
    """Display agent creation interface."""
    st.header("Create New Agent")
    
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
        
        # Show where file will be saved
        if filename:
            save_path = st.session_state.examples_dir / filename
            st.caption(f"Will save to: `{save_path}`")
    
    with col2:
        st.subheader("Agent Type")
        agent_type = st.selectbox(
            "Template",
            ["Rule-Based", "LLM-Powered", "Hybrid", "RAG-Powered"]
        )
        
        # LLM Configuration (for LLM, Hybrid, and RAG types)
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
        
        # RAG-specific configuration
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
        st.markdown("Define your rule-based logic:")
        
        # Simple rule builder
        num_rules = st.number_input("Number of Rules", 1, 5, 2)
        rules = []
        
        for i in range(num_rules):
            with st.expander(f"Rule {i+1}"):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    metric = st.selectbox(
                        "Metric",
                        ["pe_ratio", "revenue_growth", "profit_margin", "roe"],
                        key=f"metric_{i}"
                    )
                with col_b:
                    operator = st.selectbox("Operator", ["<", ">", "=="], key=f"op_{i}")
                with col_c:
                    threshold = st.number_input("Threshold", key=f"thresh_{i}")
                
                direction = st.selectbox(
                    "Signal",
                    ["bullish", "bearish", "neutral"],
                    key=f"dir_{i}"
                )
                confidence = st.slider(
                    "Confidence",
                    0.0, 1.0, 0.7, 0.1,
                    key=f"conf_{i}"
                )
                
                rules.append({
                    "metric": metric,
                    "operator": operator,
                    "threshold": threshold,
                    "direction": direction,
                    "confidence": confidence
                })
    elif agent_type == "RAG-Powered":
        rules = None
        st.info("📄 RAG agents analyze documents/text using retrieval and embeddings")
        st.markdown("""
        **RAG agents are best for:**
        - Analyzing SEC filings, earnings calls, news articles
        - Extracting insights from long documents
        - Sentiment analysis from text data
        
        **Requires:** `pip install 'ai-agent-framework[llm,rag]'`
        """)
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
        
        # Store in session state
        st.session_state.generated_code = code
        st.session_state.current_filename = filename
    
    # Display generated code if available
    if st.session_state.generated_code:
        st.code(st.session_state.generated_code, language="python")
        
        # Save button
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
                    # Clear session state after successful save
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
    
    # Select agent
    agent_names = [a['name'] for a in agents]
    selected_agent = st.selectbox("Select Agent", agent_names)
    
    # Get agent info
    agent_info = next(a for a in agents if a['name'] == selected_agent)
    agent_filename = agent_info['filename']
    agent_type = agent_info['type']
    
    # Show agent type
    st.info(f"Agent Type: **{agent_type}**")
    
    # Test configuration
    ticker = st.text_input("Ticker Symbol", value="AAPL")
    
    # Different UI for RAG agents vs traditional agents
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
            
            # Extract text preview
            with st.expander("Preview Document Text"):
                from PyPDF2 import PdfReader
                
                try:
                    pdf_reader = PdfReader(uploaded_file)
                    preview_text = ""
                    for page_num, page in enumerate(pdf_reader.pages[:3]):  # First 3 pages
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
        
        use_mock = False  # RAG agents don't use mock data
        mock_data = None
        
    else:
        # Traditional agents - use mock data
        st.subheader("Test Data")
        use_mock = st.checkbox("Use Mock Data", value=True)
        uploaded_file = None
        
        if use_mock:
            # Mock data inputs
            st.subheader("Mock Financial Data")
            mock_data = {}
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                mock_data['pe_ratio'] = st.number_input("PE Ratio", 5.0, 100.0, 20.0)
                mock_data['revenue_growth'] = st.number_input("Revenue Growth (%)", -20.0, 100.0, 15.0)
            with col_b:
                mock_data['profit_margin'] = st.number_input("Profit Margin (%)", -10.0, 50.0, 12.0)
                mock_data['roe'] = st.number_input("ROE (%)", -20.0, 50.0, 15.0)
            with col_c:
                mock_data['debt_to_equity'] = st.number_input("Debt/Equity", 0.0, 5.0, 0.8)
                mock_data['dividend_yield'] = st.number_input("Dividend Yield (%)", 0.0, 10.0, 2.0)
        else:
            mock_data = None
    
    # Run test
    if st.button("🚀 Run Analysis", type="primary"):
        tester = AgentTester()
        
        # Check if RAG agent has document
        if agent_type == "RAG-Powered" and not uploaded_file:
            st.error("Please upload a PDF document to test RAG agent")
            return
        
        with st.spinner("Running analysis..."):
            result = tester.test_agent(
                agent_filename,
                ticker,
                mock_data,
                uploaded_file  # Pass PDF file for RAG agents
            )
        
        if result['success']:
            st.success("Analysis Complete!")
            
            # Display results
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
            
            # Show insights for RAG agents
            if 'insights' in result['signal'] and result['signal']['insights']:
                st.markdown("**Detailed Insights:**")
                for i, insight in enumerate(result['signal']['insights'], 1):
                    with st.expander(f"Insight {i}"):
                        st.write(insight)
            
        else:
            st.error(f"Error: {result['error']}")

if __name__ == "__main__":
    main()
