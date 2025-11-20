"""LLM Setup - Configure AI providers for intelligent agents.

Step-by-step wizard for setting up OpenAI, Anthropic, or Ollama.
"""

import sys
from pathlib import Path
import os

import streamlit as st

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Page config
st.set_page_config(page_title="LLM Setup", page_icon="⚙️", layout="wide")


def show_llm_setup_wizard():
    """LLM setup wizard - step by step configuration guide."""
    st.title("⚙️ LLM Setup Wizard")
    
    st.markdown("""
    Configure AI providers to enable LLM-powered and RAG agents.
    Choose your provider based on your needs and budget.
    """)
    
    # Provider comparison
    st.subheader("Choose Your Provider")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("""
        ### 🟢 Ollama (Recommended)
        
        **Best for beginners**
        
        ✅ **Free** - No API costs
        ✅ **Local** - Runs on your computer
        ✅ **Private** - Data stays local
        ✅ **Fast** - No network latency
        
        **Requirements:**
        - 8GB RAM minimum
        - 10GB disk space
        - 5 minutes setup
        
        **Models:**
        - LLaMA 3.2 (recommended)
        - Mistral
        - Phi
        """)
        
        if st.button("📖 Ollama Setup Guide", use_container_width=True):
            st.session_state.setup_provider = "ollama"
    
    with col2:
        st.info("""
        ### 🔵 OpenAI
        
        **Best for power users**
        
        ✅ **Powerful** - GPT-4 quality
        ✅ **Reliable** - 99.9% uptime
        ✅ **Fast** - Cloud-based
        
        **Requirements:**
        - API key ($5-20/month)
        - Internet connection
        - Credit card
        
        **Models:**
        - GPT-4 (best quality)
        - GPT-3.5 (faster, cheaper)
        """)
        
        if st.button("📖 OpenAI Setup Guide", use_container_width=True):
            st.session_state.setup_provider = "openai"
    
    with col3:
        st.info("""
        ### 🟣 Anthropic
        
        **Best for advanced analysis**
        
        ✅ **Intelligent** - Claude quality
        ✅ **Detailed** - Long responses
        ✅ **Thoughtful** - Nuanced reasoning
        
        **Requirements:**
        - API key ($5-20/month)
        - Internet connection
        - Credit card
        
        **Models:**
        - Claude 3.5 Sonnet
        - Claude 3 Opus
        """)
        
        if st.button("📖 Anthropic Setup Guide", use_container_width=True):
            st.session_state.setup_provider = "anthropic"
    
    st.markdown("---")
    
    # Show setup guide based on selection
    provider = st.session_state.get("setup_provider")
    
    if provider == "ollama":
        show_ollama_setup()
    elif provider == "openai":
        show_openai_setup()
    elif provider == "anthropic":
        show_anthropic_setup()
    else:
        st.info("👆 Select a provider above to see setup instructions")


def show_ollama_setup():
    """Ollama setup guide."""
    st.subheader("🟢 Ollama Setup Guide")
    
    st.markdown("""
    Ollama runs AI models locally on your computer - completely free!
    """)
    
    # Step-by-step tabs
    step1, step2, step3, step4 = st.tabs([
        "1️⃣ Install Ollama",
        "2️⃣ Download Model",
        "3️⃣ Start Service",
        "4️⃣ Test Connection"
    ])
    
    with step1:
        st.markdown("""
        ### Install Ollama
        
        **Linux / WSL2:**
        ```bash
        curl https://ollama.ai/install.sh | sh
        ```
        
        **macOS:**
        ```bash
        brew install ollama
        ```
        
        **Windows:**
        1. Download from https://ollama.ai/download
        2. Run the installer
        3. Follow the prompts
        
        **Verify installation:**
        ```bash
        ollama --version
        ```
        
        Should show version number (e.g., `ollama version 0.1.17`)
        """)
    
    with step2:
        st.markdown("""
        ### Download a Model
        
        **Recommended: LLaMA 3.2** (3.2GB, good balance)
        ```bash
        ollama pull llama3.2
        ```
        
        **Alternatives:**
        
        **Smaller models** (faster, less RAM):
        ```bash
        ollama pull phi          # 1.6GB - lightweight
        ```
        
        **Larger models** (better quality):
        ```bash
        ollama pull mistral      # 4.1GB - very capable
        ollama pull llama3.1     # 4.7GB - latest
        ```
        
        **Check downloaded models:**
        ```bash
        ollama list
        ```
        
        Should show your downloaded models with sizes.
        """)
    
    with step3:
        st.markdown("""
        ### Start Ollama Service
        
        **Option 1: Terminal** (recommended for learning)
        ```bash
        ollama serve
        ```
        
        Leave this terminal open - Ollama runs here.
        
        **Option 2: Background** (macOS/Linux)
        ```bash
        ollama serve > /dev/null 2>&1 &
        ```
        
        Runs in background, terminal can be closed.
        
        **Verify service is running:**
        
        Open browser to: http://localhost:11434
        
        Should see: "Ollama is running"
        
        **Stop service:**
        ```bash
        # If running in terminal: Ctrl+C
        # If in background: 
        killall ollama
        ```
        """)
    
    with step4:
        st.markdown("""
        ### Test Connection
        
        **Test in terminal:**
        ```bash
        ollama run llama3.2 "What is 2+2?"
        ```
        
        Should respond: "The answer is 4."
        
        **Test in this GUI:**
        
        1. Go to "➕ Create Agent"
        2. Select "LLM-Powered" type
        3. Choose provider: Ollama
        4. Model: llama3.2
        5. Generate and save agent
        6. Go to "🧪 Test Agent"
        7. Run the agent
        8. Should see AI-generated reasoning!
        
        **Troubleshooting:**
        
        ❌ "Connection refused"
        → Solution: Start ollama service (`ollama serve`)
        
        ❌ "Model not found"
        → Solution: Download model (`ollama pull llama3.2`)
        
        ❌ "Out of memory"
        → Solution: Use smaller model (`ollama pull phi`)
        """)


def show_openai_setup():
    """OpenAI setup guide."""
    st.subheader("🔵 OpenAI Setup Guide")
    
    st.markdown("""
    OpenAI provides powerful cloud-based AI models (GPT-4, GPT-3.5).
    """)
    
    step1, step2, step3 = st.tabs([
        "1️⃣ Get API Key",
        "2️⃣ Configure",
        "3️⃣ Test"
    ])
    
    with step1:
        st.markdown("""
        ### Get OpenAI API Key
        
        **Steps:**
        
        1. Go to https://platform.openai.com/api-keys
        2. Sign up or log in
        3. Click "Create new secret key"
        4. Copy the key (starts with `sk-...`)
        5. **Important:** Save it somewhere safe - you can't see it again!
        
        **Pricing:**
        - GPT-4: ~$0.03 per 1000 tokens (~$0.10 per agent test)
        - GPT-3.5: ~$0.002 per 1000 tokens (~$0.01 per agent test)
        
        **Free tier:** $5 credit for new accounts
        
        **Recommended:** Start with GPT-3.5 Turbo (cheaper, fast)
        """)
    
    with step2:
        st.markdown("""
        ### Configure API Key
        
        **Add to .env file:**
        
        ```bash
        # Navigate to project root
        cd ~/AI-Agent-Builder
        
        # Edit .env file
        nano .env
        
        # Add this line:
        OPENAI_API_KEY=sk-your-key-here
        
        # Save and exit (Ctrl+X, then Y, then Enter)
        ```
        
        **Verify .env file:**
        ```bash
        cat .env | grep OPENAI
        ```
        
        Should show: `OPENAI_API_KEY=sk-...`
        
        **Security:**
        - ✅ Never commit .env to git
        - ✅ Keep API key secret
        - ✅ Don't share in screenshots
        - ✅ Rotate if exposed
        """)
    
    with step3:
        st.markdown("""
        ### Test Connection
        
        **In this GUI:**
        
        1. Go to "➕ Create Agent"
        2. Select "LLM-Powered" type
        3. Choose provider: OpenAI
        4. Model: gpt-3.5-turbo (cheaper) or gpt-4 (better)
        5. Generate and save agent
        6. Go to "🧪 Test Agent"
        7. Run the agent
        8. Should see GPT-generated analysis!
        
        **Monitor usage:**
        
        Check usage at: https://platform.openai.com/usage
        
        **Troubleshooting:**
        
        ❌ "Invalid API key"
        → Solution: Check .env file has correct key
        
        ❌ "Rate limit exceeded"
        → Solution: Wait 1 minute or upgrade plan
        
        ❌ "Insufficient credits"
        → Solution: Add payment method to account
        """)


def show_anthropic_setup():
    """Anthropic setup guide."""
    st.subheader("🟣 Anthropic Setup Guide")
    
    st.markdown("""
    Anthropic provides Claude - excellent for detailed investment analysis.
    """)
    
    step1, step2, step3 = st.tabs([
        "1️⃣ Get API Key",
        "2️⃣ Configure",
        "3️⃣ Test"
    ])
    
    with step1:
        st.markdown("""
        ### Get Anthropic API Key
        
        **Steps:**
        
        1. Go to https://console.anthropic.com
        2. Sign up or log in
        3. Navigate to API Keys section
        4. Click "Create Key"
        5. Copy the key (starts with `sk-ant-...`)
        6. Save it securely!
        
        **Pricing:**
        - Claude 3.5 Sonnet: ~$0.015 per 1000 tokens
        - Claude 3 Opus: ~$0.075 per 1000 tokens
        
        **Free tier:** $5 credit for new accounts
        
        **Recommended:** Start with Claude 3.5 Sonnet
        """)
    
    with step2:
        st.markdown("""
        ### Configure API Key
        
        **Add to .env file:**
        
        ```bash
        # Navigate to project root
        cd ~/AI-Agent-Builder
        
        # Edit .env file
        nano .env
        
        # Add this line:
        ANTHROPIC_API_KEY=sk-ant-your-key-here
        
        # Save and exit
        ```
        
        **Verify:**
        ```bash
        cat .env | grep ANTHROPIC
        ```
        
        Should show: `ANTHROPIC_API_KEY=sk-ant-...`
        """)
    
    with step3:
        st.markdown("""
        ### Test Connection
        
        **In this GUI:**
        
        1. Go to "➕ Create Agent"
        2. Select "LLM-Powered" type
        3. Choose provider: Anthropic
        4. Model: claude-3-5-sonnet-20241022
        5. Generate and save agent
        6. Go to "🧪 Test Agent"
        7. Run the agent
        8. Should see Claude's detailed analysis!
        
        **Monitor usage:**
        
        Check at: https://console.anthropic.com/usage
        
        **Troubleshooting:**
        
        ❌ "Authentication failed"
        → Solution: Check API key in .env file
        
        ❌ "Rate limit"
        → Solution: Wait or contact support for increase
        """)
    
    st.markdown("---")
    st.info("""
    **💡 Which Provider Should You Choose?**
    
    **For Learning (Free):** Use Ollama
    - No cost, runs locally
    - Good enough for learning concepts
    - Can experiment unlimited
    
    **For Best Quality:** Use OpenAI GPT-4 or Anthropic Claude
    - Better reasoning and insights
    - More nuanced analysis
    - Worth it for serious research
    
    **For Production:** Use thesis-app
    - Optimized for trading
    - Professional risk management
    - Real-time data integration
    """)


# Run the page
show_llm_setup_wizard()
