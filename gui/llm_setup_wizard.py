"""Interactive LLM setup wizard for students.

This wizard helps users set up AI providers (Ollama, OpenAI, Anthropic)
with step-by-step instructions and connection testing.
"""

import subprocess
from pathlib import Path

import requests
import streamlit as st


def show_llm_setup_wizard():
    """Main wizard interface."""

    st.title("🔧 LLM Setup Wizard")

    st.markdown("""
    This wizard helps you set up AI providers for LLM-powered agents.

    **Choose your path:**
    """)

    # Provider selection
    provider = st.radio(
        "Which AI provider do you want to set up?",
        [
            "🆓 Ollama (Free, Local) - Recommended for students",
            "☁️ OpenAI (Paid, Cloud) - ChatGPT",
            "☁️ Anthropic (Paid, Cloud) - Claude",
        ],
        help="Ollama runs on your computer for free. OpenAI and Anthropic are cloud services that charge per use.",
    )

    st.markdown("---")

    if "Ollama" in provider:
        show_ollama_setup()
    elif "OpenAI" in provider:
        show_openai_setup()
    elif "Anthropic" in provider:
        show_anthropic_setup()


def show_ollama_setup():
    """Step-by-step Ollama setup with testing."""

    st.subheader("🆓 Setting Up Ollama (Free AI)")

    st.info("""
    **Why Ollama?**
    - ✅ Completely free (no API costs)
    - ✅ Runs on your computer (private)
    - ✅ No rate limits
    - ✅ Perfect for learning

    **Requirements:**
    - 8GB+ RAM (16GB recommended)
    - 10GB+ free disk space
    - Internet (for downloading models)
    """)

    # Initialize session state
    if "ollama_installed" not in st.session_state:
        st.session_state.ollama_installed = False
    if "model_downloaded" not in st.session_state:
        st.session_state.model_downloaded = False

    # Step 1: Check if already installed
    st.markdown("### Step 1: Install Ollama")

    # Try to detect if Ollama is already installed
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            st.success(f"✅ Ollama is already installed! Version: {result.stdout.strip()}")
            st.session_state.ollama_installed = True
        else:
            st.warning("⚠️ Ollama command found but not working properly")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        st.warning("⚠️ Ollama not detected on your system")

    if not st.session_state.ollama_installed:
        # Show installation instructions
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown("**Installation commands:**")

            # Platform-specific instructions
            platform_tab1, platform_tab2, platform_tab3 = st.tabs(
                ["🐧 Linux/WSL", "🍎 macOS", "🪟 Windows"]
            )

            with platform_tab1:
                st.code(
                    """
# Copy and paste this in your terminal:
curl https://ollama.ai/install.sh | sh

# Or if you prefer manual download:
# Visit: https://ollama.ai/download/linux
                """,
                    language="bash",
                )

            with platform_tab2:
                st.code(
                    """
# Copy and paste this in your terminal:
curl https://ollama.ai/install.sh | sh

# Or download the app from:
# https://ollama.ai/download/mac
                """,
                    language="bash",
                )

            with platform_tab3:
                st.markdown("""
                Download the Windows installer from:

                **https://ollama.ai/download/windows**

                Run the installer and follow the prompts.
                """)

        with col2:
            if st.button("✅ I installed it", type="primary", use_container_width=True):
                st.session_state.ollama_installed = True
                st.rerun()

        st.info("👆 Click the button after you've installed Ollama")
        st.stop()

    # Step 2: Download model
    st.markdown("---")
    st.markdown("### Step 2: Download AI Model")

    if not st.session_state.model_downloaded:
        st.markdown("**Choose a model size:**")

        model_choice = st.radio(
            "Model selection:",
            [
                "llama3.2 (7B) - Balanced quality and speed ⭐ Recommended",
                "mistral (7B) - Fast with good quality",
                "phi (3B) - Lightweight, good for older computers",
                "llama3.1 (8B) - Slightly larger, better quality",
            ],
            help="Larger models are smarter but slower and need more RAM",
        )

        # Extract model name
        model_name = model_choice.split()[0]

        st.code(
            f"""
# Copy and paste this in your terminal:
ollama pull {model_name}

# This downloads the model (one-time, ~4-8GB)
# May take 5-15 minutes depending on internet speed
        """,
            language="bash",
        )

        # Model size info
        model_sizes = {"llama3.2": "~4GB", "mistral": "~4GB", "phi": "~2GB", "llama3.1": "~5GB"}

        st.info(f"💾 Download size: approximately {model_sizes.get(model_name, '4GB')}")

        col_a, col_b = st.columns([3, 1])

        with col_a:
            st.caption("This downloads the AI model to your computer. It's a one-time download.")

        with col_b:
            if st.button("✅ Downloaded", type="primary", use_container_width=True):
                st.session_state.model_downloaded = True
                st.session_state.selected_model = model_name
                st.rerun()

        st.warning("👆 Click after the download completes (check your terminal)")
        st.stop()

    # Step 3: Start service
    st.markdown("---")
    st.markdown("### Step 3: Start Ollama Service")

    st.markdown("""
    **Every time you want to use LLM agents:**

    1. Open a **separate terminal** (keep it open)
    2. Run: `ollama serve`
    3. Leave that terminal running
    4. Come back to this GUI

    **Why?** The `ollama serve` command starts the AI service that agents connect to.
    """)

    st.code("ollama serve", language="bash")

    st.info("""
    💡 **Pro Tip:** Keep the terminal with `ollama serve` visible while using the GUI.
    If you see errors in the GUI, check that terminal for clues!
    """)

    # Step 4: Test connection
    st.markdown("---")
    st.markdown("### Step 4: Test Connection")

    if st.button("🧪 Test Ollama Connection", type="primary", use_container_width=True):
        with st.spinner("Testing connection to Ollama..."):
            try:
                # Test connection
                response = requests.get("http://localhost:11434/api/tags", timeout=3)

                if response.status_code == 200:
                    data = response.json()
                    models = data.get("models", [])

                    if models:
                        st.success("✅ **Ollama is running perfectly!**")

                        # Show available models
                        st.markdown("**Available models:**")
                        for model in models:
                            model_name = model.get("name", "unknown")
                            model_size = model.get("size", 0) / (1024**3)  # Convert to GB
                            st.write(f"- `{model_name}` ({model_size:.1f} GB)")

                        st.balloons()

                        st.markdown("---")
                        st.success("""
                        🎉 **Setup Complete!**

                        You're ready to create LLM-powered agents:

                        1. Go to **➕ Create Agent** tab
                        2. Choose **LLM-Powered** type
                        3. Select **ollama** as provider
                        4. Pick your model (e.g., llama3.2)
                        5. Start analyzing stocks with AI!

                        **Remember:** Keep `ollama serve` running in your terminal!
                        """)

                        # Add quick links with proper navigation
                        st.markdown("---")
                        st.markdown("### 🎯 What's Next?")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("""**Create Your First LLM Agent:**
                            1. Close this wizard (use sidebar)
                            2. Go to **➕ Create Agent**
                            3. Select **LLM-Powered** type
                            4. Choose **ollama** provider
                            5. Create and test!""")

                        with col2:
                            st.markdown("""**Learn More:**
                            1. Close this wizard (use sidebar)
                            2. Go to **📚 How to Use Agents**
                            3. Click **🤖 LLM Agents** tab
                            4. Read comprehensive guide""")

                        st.info("💡 Use the sidebar navigation to go to other pages")

                    else:
                        st.warning("""
                        ⚠️ **Ollama is running but no models found**

                        Did you download a model? Run this in your terminal:
                        ```bash
                        ollama pull llama3.2
                        ```

                        Then test again.
                        """)

                else:
                    st.error(f"❌ Ollama responded with error code: {response.status_code}")
                    show_connection_troubleshooting()

            except requests.exceptions.ConnectionError:
                st.error("""
                ❌ **Can't connect to Ollama**

                **Problem:** Ollama service is not running

                **Solution:**
                1. Open a terminal
                2. Run: `ollama serve`
                3. Keep that terminal open
                4. Come back here and test again
                """)
                show_connection_troubleshooting()

            except requests.exceptions.Timeout:
                st.error("""
                ❌ **Connection timeout**

                Ollama might be starting up. Wait 5 seconds and try again.
                """)

            except Exception as e:
                st.error(f"❌ **Unexpected error:** {str(e)}")
                show_connection_troubleshooting()


def show_connection_troubleshooting():
    """Show troubleshooting tips for connection issues."""

    with st.expander("🔧 Troubleshooting Help"):
        st.markdown("""
        ### Common Issues

        #### 1. "Connection refused" or "Can't connect"

        **Cause:** Ollama service not running

        **Fix:**
        ```bash
        # In a separate terminal, run:
        ollama serve

        # You should see something like:
        # "Ollama server is running on http://127.0.0.1:11434"
        ```

        #### 2. "No models found"

        **Cause:** Haven't downloaded a model yet

        **Fix:**
        ```bash
        ollama pull llama3.2

        # Wait for download to complete, then test again
        ```

        #### 3. Command not found

        **Cause:** Ollama not installed or not in PATH

        **Fix:**
        - Reinstall Ollama following Step 1
        - On Windows, restart your terminal after installing
        - On Linux/Mac, try: `source ~/.bashrc` or restart terminal

        #### 4. Port already in use

        **Cause:** Another service using port 11434

        **Fix:**
        ```bash
        # Stop ollama
        pkill ollama

        # Start again
        ollama serve
        ```

        #### 5. Still not working?

        **Check Ollama docs:** https://github.com/ollama/ollama

        **Get help:**
        - Ollama Discord: https://discord.gg/ollama
        - GitHub Issues: https://github.com/ollama/ollama/issues
        """)


def show_openai_setup():
    """OpenAI (ChatGPT) setup guide."""

    st.subheader("☁️ Setting Up OpenAI (ChatGPT)")

    st.info("""
    **About OpenAI:**
    - ☁️ Cloud-based (runs on OpenAI's servers)
    - 💰 Costs money (~$0.01-0.02 per stock analysis)
    - ⚡ Very fast (< 1 second)
    - 🧠 Very capable (GPT-4)

    **Cost estimate for students:**
    - Analyzing 10 stocks/day: ~$3/month
    - Analyzing 50 stocks/day: ~$15/month
    """)

    st.warning("""
    💰 **Cost Reminder:**

    Unlike Ollama (free), OpenAI charges per API call. Monitor your usage at:
    https://platform.openai.com/usage

    Consider setting up spending limits in your OpenAI account!
    """)

    # Step 1: Get API key
    st.markdown("### Step 1: Get API Key")

    st.markdown("""
    1. Go to: **https://platform.openai.com/api-keys**
    2. Sign up or log in
    3. Click **"Create new secret key"**
    4. Give it a name (e.g., "AI Agent Builder")
    5. Copy the key (starts with `sk-...`)

    ⚠️ **Important:** The key is shown only once! Save it securely.
    """)

    st.info("🔐 **Security:** API keys are like passwords. Don't share them!")

    # Step 2: Enter API key
    st.markdown("### Step 2: Configure API Key")

    api_key = st.text_input(
        "Paste your OpenAI API key here:",
        type="password",
        placeholder="sk-...",
        help="Your API key is encrypted and only stored in your .env file",
    )

    if api_key:
        # Validate format
        if api_key.startswith("sk-"):
            st.success("✅ Valid format!")

            # Show how to add to .env
            st.markdown("**Add to your `.env` file:**")

            env_path = Path(__file__).parent.parent / ".env"

            st.code(
                f"""
# Open .env file:
nano .env

# Add this line:
OPENAI_API_KEY={api_key}

# Save and close (Ctrl+X, then Y, then Enter)
            """,
                language="bash",
            )

            # Offer to save automatically
            st.markdown("**Or let the wizard add it for you:**")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.caption("This will add the key to your .env file automatically")

            with col2:
                if st.button("💾 Save to .env", type="primary", use_container_width=True):
                    try:
                        # Read existing .env
                        existing_env = ""
                        if env_path.exists():
                            with open(env_path, "r") as f:
                                existing_env = f.read()

                        # Check if key already exists
                        if "OPENAI_API_KEY" in existing_env:
                            # Update existing key
                            lines = existing_env.split("\n")
                            new_lines = []
                            for line in lines:
                                if line.startswith("OPENAI_API_KEY"):
                                    new_lines.append(f"OPENAI_API_KEY={api_key}")
                                else:
                                    new_lines.append(line)
                            new_env = "\n".join(new_lines)
                        else:
                            # Add new key
                            new_env = existing_env.strip() + f"\n\nOPENAI_API_KEY={api_key}\n"

                        # Write to .env
                        with open(env_path, "w") as f:
                            f.write(new_env)

                        st.success("✅ API key saved to .env file!")
                        st.balloons()

                        st.markdown("---")
                        st.success("""
                        🎉 **OpenAI Setup Complete!**

                        You can now create LLM-powered agents:
                        1. Go to **➕ Create Agent**
                        2. Choose **LLM-Powered** type
                        3. Select **openai** as provider
                        4. Pick a model (gpt-4o recommended)
                        5. Start analyzing!

                        💰 **Remember:** Monitor your usage to control costs!
                        """)

                    except Exception as e:
                        st.error(f"❌ Error saving to .env: {str(e)}")
                        st.info("Please add the key manually to your .env file")

        else:
            st.error("❌ Invalid format. OpenAI keys start with 'sk-'")
            st.info("Example: sk-proj-abc123...")

    # Additional info
    st.markdown("---")
    st.markdown("### Additional Information")

    with st.expander("💰 Managing Costs"):
        st.markdown("""
        **Set spending limits:**
        1. Go to: https://platform.openai.com/account/billing/limits
        2. Set a monthly budget (e.g., $10/month)
        3. You'll get notified when reaching the limit

        **Cost-saving tips:**
        - Use Hybrid agents (rules + LLM) for 95% cost reduction
        - Use gpt-3.5-turbo instead of gpt-4 (10x cheaper)
        - Test with Ollama first, then switch to OpenAI
        - Set lower max_tokens to reduce response length
        """)

    with st.expander("🔐 Security Best Practices"):
        st.markdown("""
        **Protect your API key:**
        - Never commit .env file to git (it's in .gitignore)
        - Don't share your key with others
        - Rotate keys periodically
        - Use separate keys for different projects

        **If key is compromised:**
        1. Go to: https://platform.openai.com/api-keys
        2. Revoke the old key
        3. Create a new key
        4. Update your .env file
        """)


def show_anthropic_setup():
    """Anthropic (Claude) setup guide."""

    st.subheader("☁️ Setting Up Anthropic (Claude)")

    st.info("""
    **About Anthropic Claude:**
    - ☁️ Cloud-based (runs on Anthropic's servers)
    - 💰 Costs money (~$0.01-0.03 per analysis)
    - ⚡ Fast
    - 🧠 Excellent reasoning ability
    - 📄 Great for document analysis (RAG)

    **Cost estimate for students:**
    - Analyzing 10 stocks/day: ~$3-5/month
    - Analyzing 50 stocks/day: ~$15-25/month
    """)

    st.warning("""
    💰 **Cost Reminder:**

    Like OpenAI, Anthropic charges per API call. Monitor usage in your console:
    https://console.anthropic.com/
    """)

    # Step 1: Get API key
    st.markdown("### Step 1: Get API Key")

    st.markdown("""
    1. Go to: **https://console.anthropic.com/**
    2. Sign up or log in
    3. Navigate to **API Keys** section
    4. Click **Create Key**
    5. Give it a name (e.g., "AI Agent Builder")
    6. Copy the key (starts with `sk-ant-...`)
    """)

    st.info("🔐 **Security:** Keep your API key secret and secure!")

    # Step 2: Enter API key
    st.markdown("### Step 2: Configure API Key")

    api_key = st.text_input(
        "Paste your Anthropic API key here:",
        type="password",
        placeholder="sk-ant-...",
        help="Your API key is stored securely in .env file",
    )

    if api_key:
        # Validate format
        if api_key.startswith("sk-ant-"):
            st.success("✅ Valid format!")

            # Show how to add to .env
            st.markdown("**Add to your `.env` file:**")

            env_path = Path(__file__).parent.parent / ".env"

            st.code(
                f"""
# Open .env file:
nano .env

# Add this line:
ANTHROPIC_API_KEY={api_key}

# Save and close (Ctrl+X, then Y, then Enter)
            """,
                language="bash",
            )

            # Offer to save automatically
            st.markdown("**Or let the wizard add it for you:**")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.caption("This will add the key to your .env file automatically")

            with col2:
                if st.button("💾 Save to .env", type="primary", use_container_width=True):
                    try:
                        # Read existing .env
                        existing_env = ""
                        if env_path.exists():
                            with open(env_path, "r") as f:
                                existing_env = f.read()

                        # Check if key already exists
                        if "ANTHROPIC_API_KEY" in existing_env:
                            # Update existing key
                            lines = existing_env.split("\n")
                            new_lines = []
                            for line in lines:
                                if line.startswith("ANTHROPIC_API_KEY"):
                                    new_lines.append(f"ANTHROPIC_API_KEY={api_key}")
                                else:
                                    new_lines.append(line)
                            new_env = "\n".join(new_lines)
                        else:
                            # Add new key
                            new_env = existing_env.strip() + f"\n\nANTHROPIC_API_KEY={api_key}\n"

                        # Write to .env
                        with open(env_path, "w") as f:
                            f.write(new_env)

                        st.success("✅ API key saved to .env file!")
                        st.balloons()

                        st.markdown("---")
                        st.success("""
                        🎉 **Anthropic Setup Complete!**

                        You can now create LLM-powered agents:
                        1. Go to **➕ Create Agent**
                        2. Choose **LLM-Powered** or **RAG-Powered**
                        3. Select **anthropic** as provider
                        4. Pick a model (claude-3-5-sonnet recommended)
                        5. Start analyzing!

                        💰 **Remember:** Monitor your usage!
                        """)

                    except Exception as e:
                        st.error(f"❌ Error saving to .env: {str(e)}")
                        st.info("Please add the key manually to your .env file")

        else:
            st.error("❌ Invalid format. Anthropic keys start with 'sk-ant-'")
            st.info("Example: sk-ant-api03-...")

    # Additional info
    st.markdown("---")
    st.markdown("### Recommended Models")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Claude 3.5 Sonnet** (Recommended)
        - Best balance of quality and cost
        - Excellent reasoning
        - Good for most tasks
        - Model: `claude-3-5-sonnet-20241022`
        """)

    with col2:
        st.markdown("""
        **Claude 3.5 Haiku** (Budget-friendly)
        - Fastest and cheapest
        - Good for simple tasks
        - Good quality for price
        - Model: `claude-3-5-haiku-20241022`
        """)


# For testing standalone
if __name__ == "__main__":
    show_llm_setup_wizard()
