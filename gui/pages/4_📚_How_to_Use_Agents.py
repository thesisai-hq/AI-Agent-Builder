"""How to Use Agents - Complete guide for learning investment analysis with AI.

Comprehensive guide covering all agent types, testing strategies, and best practices.
"""

import sys
from pathlib import Path

import streamlit as st

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gui.sidebar_info import show_sidebar_info

# Page config
st.set_page_config(page_title="How to Use Agents", page_icon="📚", layout="wide")


def show_how_to_page():
    """Display comprehensive guide for all agent types."""
    # Show sidebar info on all pages
    show_sidebar_info()
    
    st.title("📚 How to Use Agents for Investment Analysis")

    st.markdown(
        """
    This guide teaches you how to use AI agents to analyze stocks and learn investment strategies.
    Choose a topic below to get started!
    """
    )

    # Navigation tabs for different topics
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🎯 Getting Started",
            "📊 Agent Types",
            "🧪 Testing Agents",
            "💡 Best Practices",
            "🎓 Learning Resources",
        ]
    )

    with tab1:
        show_getting_started()

    with tab2:
        show_agent_types()

    with tab3:
        show_testing_guide()

    with tab4:
        show_best_practices()

    with tab5:
        show_learning_resources()


def show_getting_started():
    """Getting started guide."""
    st.markdown(
        """
    ## 🎯 Getting Started with AI Agent Builder
    
    ### Quick Start (5 minutes)
    
    **Step 1: Browse Example Agents**
    1. Click "📋 Browse Agents" in the sidebar
    2. Explore the pre-built strategies (Buffett, Lynch, Graham)
    3. Click "👁️ View" to see the code
    4. Click "📋 Copy" to duplicate and modify
    
    **Step 2: Test an Agent**
    1. Click "🧪 Test Agent" in the sidebar
    2. Select an agent (e.g., ValueAgent)
    3. Choose "Mock Data" to start
    4. Click "🚀 Run Analysis"
    5. See the signal, confidence, and reasoning
    
    **Step 3: Create Your First Agent**
    1. Click "➕ Create Agent" in the sidebar
    2. Enter a name (e.g., "MyValueAgent")
    3. Select "Rule-Based" type
    4. Add a simple rule: "PE Ratio < 15 → Bullish"
    5. Click "Generate Code"
    6. Click "Save Agent"
    
    **Step 4: Experiment!**
    - Modify the rule thresholds
    - Add more rules
    - Try different agent types
    - Test on real data (YFinance)
    
    ### 🎓 Learning Path
    
    **Week 1: Rule-Based Agents**
    - Understand simple if/then rules
    - Learn key financial metrics (PE, ROE, etc.)
    - Build 2-3 rule-based agents
    - Test with mock data
    
    **Week 2: LLM-Powered Agents**
    - Set up Ollama (free local AI)
    - Create AI-powered agent
    - Compare AI vs rule-based results
    - Learn prompt engineering basics
    
    **Week 3: Advanced Features**
    - Build hybrid agents (rules + AI)
    - Analyze SEC filings with RAG agents
    - Test on real market data
    - Compare multiple strategies
    
    ### 💡 Key Concepts
    
    **Signal**: The agent's recommendation (Bullish/Bearish/Neutral)
    
    **Confidence**: How confident the agent is (0-100%)
    
    **Reasoning**: Why the agent made this decision
    
    **Mock Data**: Fictional data for testing
    
    **Real Data**: Live market data from Yahoo Finance
    """
    )


def show_agent_types():
    """Explain different agent types."""
    st.markdown(
        """
    ## 📊 Agent Types Explained
    
    Choose the right agent type for your learning goals.
    """
    )

    # Rule-Based
    st.markdown("### 1. Rule-Based Agents 📊")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.success(
            """
        **Best for:**
        - Beginners
        - Learning fundamentals
        - Clear investment criteria
        
        **Speed:** ⚡ Very fast (<1ms)
        
        **Setup:** ✅ None needed
        
        **Cost:** 💚 Free
        """
        )

    with col2:
        st.markdown(
            """
        **What are they?**
        
        Rule-based agents use simple if/then logic you define:
        
        ```python
        if pe_ratio < 15:
            return Signal("bullish", 0.8, "Undervalued")
        elif pe_ratio > 30:
            return Signal("bearish", 0.7, "Overvalued")
        else:
            return Signal("neutral", 0.6, "Fair value")
        ```
        
        **Example strategies:**
        - Value investing: Buy if PE < 15 AND ROE > 15%
        - Growth investing: Buy if revenue growth > 20%
        - Quality investing: Buy if profit margin > 15% AND debt < 0.5
        
        **When to use:**
        - You have clear investment rules
        - You want deterministic results
        - You're learning basic concepts
        - You want fast execution
        """
        )

    st.markdown("---")

    # LLM-Powered
    st.markdown("### 2. LLM-Powered Agents 🤖")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.info(
            """
        **Best for:**
        - Nuanced analysis
        - Learning AI integration
        - Complex decisions
        
        **Speed:** 🕐 Slower (2-5s)
        
        **Setup:** ⚙️ Ollama/OpenAI/Anthropic
        
        **Cost:** 💛 Free (Ollama) or Paid (APIs)
        """
        )

    with col2:
        st.markdown(
            """
        **What are they?**
        
        LLM agents use AI (ChatGPT, Claude, LLaMA) for intelligent analysis:
        
        ```python
        prompt = f"Analyze {ticker}: PE={pe}, Growth={growth}%"
        response = llm.chat(prompt)
        # AI provides nuanced reasoning
        ```
        
        **Example insights:**
        - "Strong competitive moat with durable brand equity"
        - "Management has proven capital allocation skills"
        - "Cyclical headwinds may pressure near-term earnings"
        
        **When to use:**
        - You want AI-powered insights
        - Rules alone aren't enough
        - You need qualitative analysis
        - You're learning prompt engineering
        
        **Setup required:**
        - Ollama (free, local AI) - Recommended for learning
        - OpenAI API (paid, powerful)
        - Anthropic Claude (paid, advanced)
        """
        )

    st.markdown("---")

    # RAG-Powered
    st.markdown("### 3. RAG Agents 📄")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.warning(
            """
        **Best for:**
        - Document analysis
        - SEC filing research
        - Learning RAG concepts
        
        **Speed:** 🕐 Slower (5-30s)
        
        **Setup:** ⚙️ Same as LLM
        
        **Cost:** 💛 Free (Ollama) or Paid (APIs)
        """
        )

    with col2:
        st.markdown(
            """
        **What are they?**
        
        RAG (Retrieval-Augmented Generation) agents analyze long documents:
        
        ```python
        # Upload 100-page SEC 10-K filing
        chunks = rag.chunk_document(filing_text)
        relevant = rag.query("What are the risk factors?")
        insight = llm.analyze(relevant)
        ```
        
        **Example use cases:**
        - Extract risk factors from 10-K filings
        - Analyze earnings call transcripts
        - Review management discussion sections
        - Find competitive advantages in annual reports
        
        **When to use:**
        - You want to analyze long documents (50+ pages)
        - You need specific information extraction
        - You're learning document AI
        - You have PDFs to analyze
        
        **Limitation:**
        - Requires PDF upload (not for live market data)
        - Best for qualitative research, not quantitative screening
        """
        )

    st.markdown("---")

    # Hybrid
    st.markdown("### 4. Hybrid Agents 🔀")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.success(
            """
        **Best for:**
        - Advanced users
        - Efficient screening
        - Best of both worlds
        
        **Speed:** 🕐 Medium (fast filter + AI)
        
        **Setup:** ⚙️ Same as LLM
        
        **Cost:** 💛 Optimized (fewer LLM calls)
        """
        )

    with col2:
        st.markdown(
            """
        **What are they?**
        
        Hybrid agents combine rules and AI for efficient analysis:
        
        ```python
        # Step 1: Fast rule-based filter
        if pe_ratio < 15 and roe > 15:
            # Step 2: AI analyzes only promising stocks
            analysis = llm.analyze(data)
            return analysis
        else:
            # Quick reject without using AI
            return Signal("neutral", 0.5, "Doesn't meet criteria")
        ```
        
        **Example workflow:**
        - Filter 1000 stocks with rules (fast)
        - AI analyzes top 50 (selective)
        - Get best of both: speed + intelligence
        
        **When to use:**
        - You want efficiency (don't waste AI calls)
        - You have clear filters + need nuance
        - You're screening large lists
        - You want to optimize costs
        
        **Best practice:**
        - Use rules for quantitative filtering (PE, ROE, debt)
        - Use AI for qualitative analysis (moat, management, risks)
        """
        )


def show_testing_guide():
    """Testing guide."""
    st.markdown(
        """
    ## 🧪 Testing Your Agents
    
    ### Test Data Options
    
    **1. Mock Data** (Recommended for beginners)
    - Fictional data you control
    - Test edge cases easily
    - Fast and free
    - No internet needed
    
    **Use when:**
    - Learning how agents work
    - Testing rule logic
    - Experimenting with thresholds
    
    **Example:**
    ```
    PE Ratio: 10  (undervalued)
    ROE: 25%      (high quality)
    Debt: 0.3     (low debt)
    
    Expected: Bullish signal
    ```
    
    ---
    
    **2. Database** (Sample stocks)
    - Pre-loaded sample data (AAPL, MSFT, TSLA, JPM)
    - Realistic but limited
    - Snapshot data (not live)
    
    **Use when:**
    - Testing with realistic data
    - Comparing agents on same stocks
    - No internet connection
    
    ---
    
    **3. YFinance** (Real market data)
    - Live current market data
    - Any public stock
    - Free but requires internet
    
    **Use when:**
    - Testing with real data
    - Want current valuations
    - Researching specific stocks
    
    **Note:** Data is snapshot, not real-time
    
    ---
    
    **4. PDF Upload** (RAG agents only)
    - Upload SEC filings, earnings reports
    - AI extracts insights
    - Best for qualitative research
    
    **Use when:**
    - Analyzing specific documents
    - Extracting risk factors
    - Learning document AI
    
    ### How to Interpret Results
    
    **Signal: Bullish 🟢**
    - Agent recommends buying
    - Found positive indicators
    - Check reasoning for details
    
    **Signal: Bearish 🔴**
    - Agent recommends selling/avoiding
    - Found negative indicators
    - Review concerns carefully
    
    **Signal: Neutral 🟡**
    - No strong conviction either way
    - Criteria not met
    - Could mean "fair value" or "insufficient data"
    
    **Confidence Level:**
    - 80-100%: Strong conviction
    - 60-80%: Moderate confidence
    - 40-60%: Weak signal
    - <40%: Very uncertain
    
    ### Common Testing Scenarios
    
    **Scenario 1: Testing Rule Thresholds**
    ```
    Your rule: Buy if PE < 15
    
    Test with Mock Data:
    - PE = 10 → Should be Bullish
    - PE = 14.9 → Should be Bullish (edge case)
    - PE = 15.1 → Should be Neutral/Bearish
    - PE = 25 → Should be Bearish
    ```
    
    **Scenario 2: Comparing Strategies**
    ```
    Test same stock (AAPL) with:
    - ValueAgent → Result 1
    - GrowthAgent → Result 2
    - QualityAgent → Result 3
    
    Compare: Which strategy identifies AAPL as opportunity?
    Learn: Different strategies see different things!
    ```
    
    **Scenario 3: Validating LLM Agent**
    ```
    Test on known cases:
    - Undervalued stock → Should find value
    - Overpriced stock → Should warn
    - Compare AI reasoning with your analysis
    ```
    """
    )


def show_best_practices():
    """Best practices guide."""
    st.markdown(
        """
    ## 💡 Best Practices
    
    ### For Rule-Based Agents
    
    **✅ Do:**
    - Start with 1-2 simple rules
    - Use realistic thresholds (PE < 15, not PE < 1)
    - Test edge cases (what if PE = 14.9?)
    - Add rules gradually
    - Document your reasoning
    
    **❌ Don't:**
    - Use too many rules (start simple)
    - Set impossible thresholds (PE < 0)
    - Ignore data quality issues
    - Make contradictory rules
    
    **Example Good Rule Set:**
    ```
    1. PE Ratio < 15 (undervalued)
    2. ROE > 15% (profitable)
    3. Debt-to-Equity < 0.5 (safe)
    
    → If all 3 met: Strong Buy
    → If 2 met: Moderate Buy
    → If <2 met: Pass
    ```
    
    ### For LLM-Powered Agents
    
    **✅ Do:**
    - Write clear, specific prompts
    - Ask for structured output
    - Include relevant data in prompt
    - Test prompt variations
    - Use system prompts for persona
    
    **❌ Don't:**
    - Use vague prompts
    - Forget to include data
    - Trust AI blindly
    - Skip validation
    
    **Example Good Prompt:**
    ```
    You are a conservative value investor.
    
    Analyze this stock:
    - Ticker: AAPL
    - PE Ratio: 28.5
    - ROE: 147%
    - Debt-to-Equity: 2.1
    
    Respond in format:
    DIRECTION|CONFIDENCE|REASONING
    
    Example: bullish|75|Strong fundamentals with...
    ```
    
    ### For RAG Agents
    
    **✅ Do:**
    - Upload text-based PDFs (not scanned images)
    - Use specific questions
    - Review extracted chunks
    - Validate AI findings
    
    **❌ Don't:**
    - Upload huge documents (>200 pages) initially
    - Ask vague questions
    - Trust extracted data without verification
    
    **Example Good Workflow:**
    ```
    1. Upload: Apple 10-K filing
    2. Ask specific question: "What are the top 3 risk factors?"
    3. Review: Check AI extracted correct sections
    4. Validate: Read original document sections
    5. Use insights: Incorporate into analysis
    ```
    
    ### General Best Practices
    
    **⚠️ Remember:**
    - This is educational - not for real trading
    - Always validate agent logic
    - Understand why agent made decision
    - Don't over-fit to historical data
    - Consult professionals for real investments
    
    **📊 Good Habits:**
    - Test agents on multiple stocks
    - Compare different strategies
    - Understand each metric's meaning
    - Document your learning
    - Start simple, add complexity gradually
    """
    )


def show_learning_resources():
    """Learning resources and references."""
    st.markdown(
        """
    ## 🎓 Learning Resources
    
    ### Investment Strategies (What Agents Implement)
    
    **Warren Buffett - Quality Investing**
    - Focus: High-quality businesses at fair prices
    - Key metrics: ROE > 15%, Profit Margin > 15%, Low Debt
    - Agent: `BuffettQualityAgent` (examples/05_buffett_quality.py)
    - Learn more: "The Essays of Warren Buffett"
    
    **Peter Lynch - GARP (Growth at Reasonable Price)**
    - Focus: Growing companies at reasonable valuations
    - Key metric: PEG ratio < 1.0
    - Agent: `LynchGARPAgent` (examples/06_lynch_garp.py)
    - Learn more: "One Up on Wall Street"
    
    **Benjamin Graham - Deep Value**
    - Focus: Undervalued stocks with margin of safety
    - Key metrics: PE < 15, PB < 1.5, Current Ratio > 1.5
    - Agent: `GrahamValueAgent` (examples/07_graham_value.py)
    - Learn more: "The Intelligent Investor"
    
    ### Financial Metrics Explained
    
    **Valuation Metrics:**
    - **PE Ratio**: Price ÷ Earnings (how expensive is the stock?)
    - **PB Ratio**: Price ÷ Book Value (price vs asset value)
    - **PEG Ratio**: PE ÷ Growth (growth-adjusted valuation)
    
    **Profitability Metrics:**
    - **ROE**: Return on Equity (efficiency of capital use)
    - **Profit Margin**: Net Income ÷ Revenue (operational efficiency)
    - **Revenue Growth**: Year-over-year sales increase
    
    **Safety Metrics:**
    - **Debt-to-Equity**: Total Debt ÷ Equity (leverage risk)
    - **Current Ratio**: Current Assets ÷ Liabilities (liquidity)
    - **Dividend Yield**: Annual Dividend ÷ Price (income)
    
    ### Python & AI Learning
    
    **If you're new to Python:**
    1. View generated agent code (click 👁️ View)
    2. Read the comments explaining each line
    3. Try modifying values
    4. Download and run locally
    5. Gradually learn by doing
    
    **If you're new to AI:**
    1. Start with rule-based agents (no AI needed)
    2. Set up Ollama (free local AI)
    3. Create simple LLM agent
    4. Experiment with prompts
    5. Learn prompt engineering basics
    
    ### External Resources
    
    **Documentation:**
    - [GitHub Repository](https://github.com/thesisai-hq/AI-Agent-Builder)
    - [API Reference](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/docs/API_REFERENCE.md)
    - [Framework Quickstart](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/docs/FRAMEWORK_QUICKSTART.md)
    
    **AI Tools:**
    - [Ollama Installation](https://ollama.ai) - Free local AI
    - [OpenAI Platform](https://platform.openai.com) - ChatGPT API
    - [Anthropic Claude](https://console.anthropic.com) - Claude API
    
    **Investment Education:**
    - Investopedia - Financial metrics explained
    - Yahoo Finance - Free market data
    - SEC.gov - Company filings
    
    ### Support
    
    **Having issues?**
    - Check [Troubleshooting Guide](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/docs/TROUBLESHOOTING.md)
    - Review [LLM Setup Guide](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/docs/OLLAMA_SETUP.md)
    - Open [GitHub Issue](https://github.com/thesisai-hq/AI-Agent-Builder/issues)
    
    **Want to contribute?**
    - Read [Contributing Guide](https://github.com/thesisai-hq/AI-Agent-Builder/blob/main/CONTRIBUTING.md)
    - Share your agents
    - Improve documentation
    - Report bugs
    """
    )


# Run the page
show_how_to_page()
