"""Enhanced 'How To' page with comprehensive LLM and RAG agent guides

This provides complete step-by-step workflows for all agent types,
designed for finance students learning investment analysis with AI.
"""

import streamlit as st


def show_how_to_page():
    """Display comprehensive guide for all agent types."""
    st.header("📚 How to Use Agents for Investment Analysis")

    st.markdown("""
    This guide teaches you how to use all types of AI agents to analyze stocks and learn investment strategies.
    """)

    # Navigation tabs for different agent types and workflows
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        [
            "🎯 Getting Started",
            "📊 Rule-Based Agents",
            "🤖 LLM Agents",
            "📄 RAG Agents",
            "🔀 Hybrid Agents",
            "💾 Using Real Data",
            "🎨 Customizing Prompts",
            "⚖️ Understanding Signals",
        ]
    )

    with tab1:
        st.markdown("""
        ## 🎯 Getting Started: Choose Your Agent Type

        ### What is an Investment Agent?

        An agent is like a **virtual analyst** that follows rules or uses AI to analyze stocks automatically.

        Think of it as:
        - A **checklist** that screens stocks (Rule-Based)
        - A **smart analyst** that reasons about companies (LLM-Powered)
        - A **document reader** that extracts insights from filings (RAG-Powered)
        - A **combination** of screening + deep analysis (Hybrid)

        ---

        ### Four Types of Agents

        #### 1. 📊 **Rule-Based Agent** (Recommended for Beginners)

        **What it does:**
        - Follows clear, specific rules you define
        - Example: "Buy if PE < 15 AND ROE > 15%"

        **When to use:**
        - ✅ You have clear investment criteria
        - ✅ Need fast analysis (thousands of stocks)
        - ✅ Want predictable, consistent results
        - ✅ No AI dependencies or costs

        **Speed:** ⚡⚡⚡⚡⚡ (instant)
        **Cost:** Free
        **Setup:** None - works immediately
        **Depth:** Basic

        **Example:**
        ```
        IF pe_ratio < 15:
            Signal: BULLISH (undervalued)
        ```

        ---

        #### 2. 🤖 **LLM-Powered Agent** (AI Intelligence)

        **What it does:**
        - Uses large language models (like ChatGPT, Claude, LLaMA)
        - Provides nuanced, contextual analysis
        - Explains reasoning in natural language

        **When to use:**
        - ✅ Need intelligent, nuanced analysis
        - ✅ Analyzing small numbers of stocks (< 20)
        - ✅ Want natural language explanations
        - ✅ Complex or subjective criteria

        **Speed:** ⚡⚡☆☆☆ (2-5 seconds per stock)
        **Cost:** Free (Ollama) or API fees (OpenAI/Anthropic)
        **Setup:** Install Ollama + download model
        **Depth:** Very Deep

        **Example:**
        ```
        "Apple demonstrates exceptional business quality with
        ROE of 28% and margins of 25%. The premium valuation
        reflects strong competitive advantages in the smartphone
        ecosystem. Consider for long-term portfolio."
        ```

        ---

        #### 3. 📄 **RAG-Powered Agent** (Document Analysis)

        **What it does:**
        - Analyzes long documents (SEC filings, reports)
        - Extracts specific information using semantic search
        - Combines retrieval with AI reasoning

        **When to use:**
        - ✅ Analyzing documents (10-K, 10-Q filings)
        - ✅ Documents too long for normal AI (50+ pages)
        - ✅ Need to extract specific information
        - ✅ Processing PDFs or unstructured text

        **Speed:** ⚡☆☆☆☆ (5-10 seconds per document)
        **Cost:** Free (Ollama) or API fees (OpenAI/Anthropic)
        **Setup:** Install Ollama + download model
        **Depth:** Very Deep (Document-specific)

        **Example:**
        ```
        "From the 10-K filing:
        - Revenue grew 8% YoY to $394.3B
        - Services revenue up 16% (key growth driver)
        - Primary risk: China supply chain concentration
        - Strategy: Expanding into India market"
        ```

        ---

        #### 4. 🔀 **Hybrid Agent** (Best of Both Worlds)

        **What it does:**
        - Uses rules for fast screening
        - Uses AI for deep analysis on filtered stocks
        - 95% cost reduction vs. pure AI

        **When to use:**
        - ✅ Analyzing large numbers of stocks (100-1000+)
        - ✅ Need both speed and intelligence
        - ✅ Want to optimize AI API costs
        - ✅ Production workflows at scale

        **Speed:** ⚡⚡⚡⚡☆ (Fast screening + selective AI)
        **Cost:** Very low (only AI on filtered stocks)
        **Setup:** Install Ollama + download model
        **Depth:** Deep (on candidates)

        **Example:**
        ```
        Stage 1 (Rules): Filter 1000 stocks → 50 pass
        Stage 2 (AI): Deep analysis on those 50
        Result: Save 95% on AI costs, same depth on good picks
        ```

        ---

        ### Quick Decision Guide

        | Your Goal | Best Agent Type |
        |-----------|----------------|
        | Screen 1000s of stocks quickly | Rule-Based |
        | Deep analysis of a few stocks | LLM-Powered |
        | Analyze SEC filings or reports | RAG-Powered |
        | Balance speed + intelligence | Hybrid |
        | Learning how agents work | Rule-Based → LLM → RAG |
        | No AI setup wanted | Rule-Based |

        ---

        ### Setup Requirements

        | Agent Type | What You Need |
        |------------|---------------|
        | Rule-Based | ✅ Nothing - works immediately! |
        | LLM-Powered | ⚙️ Ollama installed + model downloaded |
        | RAG-Powered | ⚙️ Ollama installed + model downloaded |
        | Hybrid | ⚙️ Ollama installed + model downloaded |

        **For LLM/RAG/Hybrid agents:**
        ```bash
        # Install Ollama (one-time)
        curl https://ollama.ai/install.sh | sh

        # Download a model (one-time)
        ollama pull llama3.2

        # Start Ollama (each time you use it)
        ollama serve  # Keep running in separate terminal
        ```

        ---

        ### Next Steps

        **👉 Click through the tabs above to learn:**
        - **Rule-Based Agents**: Define clear investment rules
        - **LLM Agents**: Use AI for intelligent analysis
        - **RAG Agents**: Analyze documents with AI
        - **Hybrid Agents**: Combine rules + AI efficiently
        - **Using Real Data**: Integrate yfinance data
        - **Customizing Prompts**: Control how AI thinks
        - **Understanding Signals**: Interpret results

        ---

        ### 📚 Learning Path

        **Beginner (Week 1):**
        1. Start with Rule-Based agents
        2. Create a simple value investor (PE < 15)
        3. Test with mock data
        4. Understand signals and confidence

        **Intermediate (Week 2-3):**
        1. Install Ollama (see LLM Agents tab)
        2. Create your first LLM agent
        3. Try different "personalities" (conservative, aggressive)
        4. Compare LLM vs Rules on same stock

        **Advanced (Week 4+):**
        1. Create a Hybrid agent for efficiency
        2. Try RAG agent with PDF documents
        3. Build multi-agent systems
        4. Compare different strategies

        **Remember:**
        - ⚠️ This is for learning only
        - ⚠️ Not financial advice
        - ⚠️ Don't use for real trading without professional guidance
        """)

    with tab2:
        st.markdown("""
        ## 📊 Rule-Based Agents: Fast and Deterministic

        ### What Are Rule-Based Agents?

        Rule-based agents follow **explicit conditions** you define. They're fast, predictable, and require no AI.

        **Think of it like:**
        - A checklist you'd use manually
        - But automated to check thousands of stocks instantly

        **No AI needed** - Works immediately after GUI setup!

        ---

        ### Example 1: Simple Value Screener

        **Goal:** Find undervalued stocks like Warren Buffett

        #### Step 1: Define Your Criteria

        Ask yourself: "What makes a stock attractive to me?"

        **Example criteria:**
        ```
        IF pe_ratio < 15 THEN bullish (undervalued)
        IF roe > 20 THEN bullish (high quality)
        IF dividend_yield > 3 THEN bullish (income)
        OTHERWISE neutral
        ```

        #### Step 2: Create the Agent in GUI

        1. Go to **➕ Create Agent** tab
        2. Fill in:
           - **Agent Name:** ValueHunter
           - **Type:** Rule-Based
           - **Description:** Finds undervalued quality stocks

        3. Add rules:
           - **Rule 1:** pe_ratio < 15 → bullish (80% confidence)
           - **Rule 2:** roe > 20 → bullish (75% confidence)
           - **Rule 3:** dividend_yield > 3 → bullish (70% confidence)

        4. Click **Generate Code** → **Save Agent**

        ✅ Done! Your agent is created and saved to `examples/valuehunter.py`

        #### Step 3: View the Generated Code

        Click **👁️ View** button to see the Python code:

        ```python
        class ValueHunter(Agent):
            async def analyze(self, ticker: str, data: dict) -> Signal:
                pe_ratio = data.get('pe_ratio', 0)

                if pe_ratio < 15:
                    return Signal(
                        direction='bullish',
                        confidence=0.8,
                        reasoning=f"PE ratio {pe_ratio:.1f} is bullish"
                    )

                # ... more rules
        ```

        **💡 Learning Tip:** Read the generated code to understand:
        - How rules become Python if/else statements
        - How signals are created
        - How confidence levels work

        #### Step 4: Test Your Agent

        1. Go to **🧪 Test Agent** tab
        2. Select: "ValueHunter"
        3. Choose: "Mock Data"
        4. Set PE Ratio: 12 (undervalued)
        5. Click **Run Analysis**

        **Result:**
        ```
        Signal: 🟢 BULLISH
        Confidence: 80%
        Reasoning: "PE ratio 12.0 is bullish"
        ```

        **Why bullish?** Because 12 < 15 (meets your rule!)

        ---

        ### Example 2: Score-Based Strategy (More Sophisticated)

        **Goal:** Accumulate points for multiple criteria

        Instead of simple yes/no rules, give points for each positive factor.

        #### Point System

        | Criterion | Points |
        |-----------|--------|
        | PE < 15 | +2 |
        | ROE > 15% | +2 |
        | Debt < 1.0 | +1 |
        | Margin > 12% | +1 |

        **Thresholds:**
        - Score ≥ 5: BULLISH (high quality value)
        - Score ≤ 1: BEARISH (avoid)
        - Otherwise: NEUTRAL (wait)

        #### Test Cases to Understand the Logic

        **Company A (Strong Value):**
        ```
        PE: 12 → +2 points ✅
        ROE: 18% → +2 points ✅
        Debt: 0.5 → +1 point ✅
        Margin: 15% → +1 point ✅
        ───────────────────────
        Total: 6 points → 🟢 BULLISH

        Why? Cheap (low PE), high quality (high ROE),
        safe (low debt), profitable (good margins)
        ```

        **Company B (Value Trap):**
        ```
        PE: 8 → +2 points ✅ (very cheap!)
        ROE: 5% → 0 points ❌ (poor returns)
        Debt: 2.5 → 0 points ❌ (high debt)
        Margin: 3% → 0 points ❌ (low margins)
        ───────────────────────
        Total: 2 points → 🔴 BEARISH or 🟡 NEUTRAL

        Why? Cheap PE but terrible fundamentals! This is
        called a "value trap" - avoid!
        ```

        **Company C (Fairly Valued):**
        ```
        PE: 18 → 0 points ❌ (not cheap)
        ROE: 16% → +2 points ✅
        Debt: 0.8 → +1 point ✅
        Margin: 14% → +1 point ✅
        ───────────────────────
        Total: 4 points → 🟡 NEUTRAL

        Why? Good company but not undervalued. Wait for
        better price or look elsewhere.
        ```

        **💡 Key Lesson:** Score-based agents are smarter than simple rules because they consider multiple factors together!

        ---

        ### When to Use Rule-Based Agents

        ✅ **Perfect for:**
        - Quick screening of large stock universes (1000s)
        - Clear, quantitative criteria
        - Consistent, repeatable analysis
        - When you know exactly what you want
        - Learning investment concepts
        - No AI setup wanted

        ❌ **Not ideal for:**
        - Subjective or nuanced analysis
        - Analyzing qualitative information
        - Reading documents or reports
        - Complex context-dependent decisions

        ---

        ### Pro Tips for Creating Good Rules

        💡 **Keep rules simple:** Complex rules are hard to maintain and understand

        💡 **Test with edge cases:** Try extreme values (PE=0, PE=1000) to see what happens

        💡 **Use score-based for multi-factor:** Better than many IF statements

        💡 **Learn from examples:** Browse examples/ folder for famous investor strategies (Buffett, Lynch, Graham)

        💡 **Iterate:** Create agent → Test → Adjust rules → Test again

        💡 **Document your reasoning:** Write down WHY you chose each threshold

        ---

        ### Common Mistakes to Avoid

        ❌ **Mistake 1: Only using one rule**
        ```
        IF pe_ratio < 15 THEN buy

        Problem: Might buy value traps (cheap for a reason)
        Solution: Add quality checks (ROE, margins, debt)
        ```

        ❌ **Mistake 2: Thresholds too strict**
        ```
        IF pe_ratio < 8 AND roe > 25% THEN buy

        Problem: Almost nothing passes - too selective
        Solution: Use realistic thresholds based on market conditions
        ```

        ❌ **Mistake 3: Ignoring debt**
        ```
        Only looking at PE and growth

        Problem: High debt = high risk
        Solution: Always include debt-to-equity in criteria
        ```

        ❌ **Mistake 4: Not testing various scenarios**
        ```
        Only testing with "normal" values

        Problem: Rules might fail in extreme conditions
        Solution: Test with undervalued, overvalued, growth, value trap scenarios
        ```

        ---

        ### Learning Exercise

        **Try This:** Create three different rule-based agents:

        1. **Conservative Value Agent**
           - Very strict rules (PE < 12, Debt < 0.5)
           - High thresholds for quality (ROE > 20%)
           - Test: Should reject most stocks

        2. **Balanced Agent**
           - Moderate rules (PE < 20, Debt < 1.5)
           - Reasonable quality (ROE > 12%)
           - Test: Should find good mix

        3. **Aggressive Growth Agent**
           - Loose valuation (PE < 40)
           - High growth focus (Revenue Growth > 20%)
           - Test: Should find growth stocks even if expensive

        **Compare:** Run the same stock through all three and see how they differ!

        ---

        **Next:** Ready for AI intelligence? See the **🤖 LLM Agents** tab!
        """)

    with tab3:
        st.markdown("""
        ## 🤖 LLM-Powered Agents: AI Intelligence

        ### What Are LLM Agents?

        LLM (Large Language Model) agents use AI models like ChatGPT, Claude, or LLaMA to analyze stocks with human-like reasoning.

        **Think of it like:**
        - Having a smart analyst who reads all the data
        - Provides nuanced, context-aware insights
        - Explains reasoning in natural language

        **Unlike rules:** AI can understand context, make connections, and provide sophisticated analysis.

        ---

        ### 🔧 Setup Required (One-Time)

        LLM agents need an AI model to work. **Easiest option: Ollama (free, local)**

        #### Install Ollama

        ```bash
        # 1. Install Ollama service (one-time)
        curl https://ollama.ai/install.sh | sh

        # 2. Download a model (one-time, ~4GB)
        ollama pull llama3.2

        # 3. Start Ollama (each time you want to use LLM agents)
        ollama serve
        ```

        **Keep `ollama serve` running** in a separate terminal while using LLM agents!

        #### Verify Setup

        ```bash
        # Check if Ollama is running
        curl http://localhost:11434/api/tags

        # Should show installed models including llama3.2
        ```

        ✅ **Setup complete!** You can now create LLM agents.

        ---

        ### Alternative: Use Cloud AI (OpenAI/Anthropic)

        If you don't want to install Ollama, use cloud AI:

        **OpenAI (ChatGPT):**
        ```bash
        # Add to .env file
        OPENAI_API_KEY=sk-your-key-here

        # Get key at: https://platform.openai.com/api-keys
        # Cost: ~$0.01-0.02 per analysis
        ```

        **Anthropic (Claude):**
        ```bash
        # Add to .env file
        ANTHROPIC_API_KEY=sk-ant-your-key-here

        # Get key at: https://console.anthropic.com/
        # Cost: ~$0.01-0.03 per analysis
        ```

        **Ollama vs Cloud:**
        - Ollama: Free, private, but needs good computer
        - Cloud: Fast, no install, but costs money per use

        **For learning:** Use Ollama (free!)

        ---

        ### Example 1: Value Investor with AI

        #### Step 1: Create LLM Agent in GUI

        1. Go to **➕ Create Agent**
        2. Fill in:
           - **Agent Name:** AIValueInvestor
           - **Type:** LLM-Powered
           - **Description:** AI-powered value analysis like Buffett

        3. **LLM Configuration:**
           - **Provider:** ollama
           - **Model:** llama3.2
           - **Temperature:** 0.3 (conservative analysis)
           - **Max Tokens:** 1200 (detailed reasoning)

        4. **System Prompt (Agent Personality):**
           ```
           You are a value investment analyst inspired by Warren Buffett.

           Your philosophy:
           - Focus on business quality over price
           - Look for competitive advantages ("moats")
           - Prefer high ROE (>15%) and strong margins (>15%)
           - Favor companies with low debt (< 1.0)
           - Value consistent growth over explosive growth

           Analyze companies systematically:
           1. Quality of business
           2. Financial health
           3. Growth prospects
           4. Valuation

           Be thorough but concise.
           ```

        5. Click **Generate Code** → **Save Agent**

        #### Step 2: View the Code (Learning!)

        Click **👁️ View** to see the Python code:

        ```python
        class AIValueInvestor(Agent):
            def __init__(self):
                config = AgentConfig(
                    name="AIValueInvestor",
                    llm=LLMConfig(
                        provider='ollama',
                        model='llama3.2',
                        temperature=0.3,
                        max_tokens=1200,
                        system_prompt="You are a value investment analyst..."
                    )
                )
                super().__init__(config)

            async def analyze(self, ticker: str, data: dict) -> Signal:
                # Format data for AI
                fundamentals_text = format_fundamentals(data)

                # Build prompt
                prompt = f"Analyze {ticker}: {fundamentals_text}"

                # Query AI
                response = self.llm.chat(prompt)
                return parse_llm_signal(response)
        ```

        **💡 Learning Points:**
        - `system_prompt` defines AI personality
        - `temperature` controls creativity (low = focused)
        - `max_tokens` controls response length
        - AI response is parsed into a Signal

        #### Step 3: Test Your AI Agent

        1. **Make sure Ollama is running:**
           ```bash
           # In separate terminal
           ollama serve
           ```

        2. Go to **🧪 Test Agent**
        3. Select: "AIValueInvestor"
        4. Choose: "Mock Data" or "YFinance (Real)"
        5. Set data (if mock):
           - PE Ratio: 12
           - ROE: 28%
           - Profit Margin: 25%
           - Debt/Equity: 0.8

        6. Click **Run Analysis**

        **AI Response (Example):**
        ```
        Signal: 🟢 BULLISH
        Confidence: 75%

        Reasoning: The company demonstrates strong business quality
        with ROE of 28% and profit margins of 25%, indicating efficient
        management and competitive advantages. The PE ratio of 12
        suggests the stock is undervalued relative to its quality.

        However, debt-to-equity of 0.8, while manageable, is slightly
        elevated. Overall, this represents a quality business trading
        at attractive valuation - a good value investment opportunity
        for long-term investors.
        ```

        **Notice the difference from rules:**
        - AI considers multiple factors together
        - Explains reasoning naturally
        - Identifies tradeoffs (high ROE but some debt)
        - Provides nuanced conclusion

        ---

        ### Controlling AI Behavior: Temperature

        **Temperature controls how creative vs focused the AI is.**

        #### Low Temperature (0.0 - 0.3): The Conservative Analyst

        **Use when:** You want consistent, focused analysis

        **What happens:**
        - Very consistent answers (run 5 times → similar results)
        - Sticks to facts and clear patterns
        - Conservative, risk-aware

        **Example (Temperature = 0.2):**
        ```
        "PE ratio of 12 indicates undervaluation. ROE of 28% is
        excellent. Debt-to-equity of 0.8 is acceptable.
        Recommendation: Buy with moderate allocation."

        [Run it 5 times → Get nearly identical analysis]
        ```

        **Good for:**
        - Risk analysis
        - Consistent signals for trading systems
        - Conservative portfolio management

        #### Medium Temperature (0.4 - 0.7): The Balanced Analyst (DEFAULT)

        **Use when:** You want natural, professional analysis

        **What happens:**
        - Balanced creativity and focus
        - Natural language reasoning
        - Considers different angles

        **Example (Temperature = 0.5):**
        ```
        "This company presents a compelling value opportunity. The
        combination of strong ROE (28%) and attractive valuation
        (PE=12) suggests the market is underappreciating its quality.

        While debt levels are moderate, the robust cash generation
        implied by high ROE should provide adequate coverage. Consider
        for value-focused portfolios with 3-5% allocation."

        [Run it 5 times → Similar conclusions, different phrasing]
        ```

        **Good for:**
        - General stock analysis
        - Learning and exploration
        - Most use cases

        #### High Temperature (0.8 - 1.0): The Creative Strategist

        **Use when:** You want diverse perspectives and novel insights

        **What happens:**
        - Each analysis explores different angles
        - More creative, less predictable
        - Finds non-obvious connections

        **Example (Temperature = 0.9):**
        ```
        Run 1: "The company's moat appears durable based on
                consistently high margins..."

        Run 2: "Consider this through the lens of capital allocation
                efficiency - ROE of 28% means..."

        Run 3: "The valuation discount may reflect market concerns
                about sector headwinds, but..."

        Run 4: "From a risk-adjusted return perspective, the
                combination of..."

        Run 5: "Historical precedents suggest companies with similar
                fundamentals have..."

        [Each analysis takes completely different approach!]
        ```

        **Good for:**
        - Brainstorming investment ideas
        - Finding non-obvious opportunities
        - Research and exploration
        - Getting multiple perspectives

        **⚠️ Warning:** Very high temperature can sometimes produce less reliable analysis!

        ---

        ### Controlling Response Length: Max Tokens

        **Max tokens controls how detailed the AI's response is.**

        **Rule of thumb:** ~750 words per 1000 tokens

        | Tokens | ~Words | ~Paragraphs | Use Case |
        |--------|--------|-------------|----------|
        | 500 | 375 | 2-3 | Quick signals |
        | 1000 | 750 | 3-4 | Standard analysis |
        | 2000 | 1500 | 6-8 | Detailed reports |
        | 4000 | 3000 | 12-15 | Comprehensive research |

        #### Brief (500 tokens):
        ```
        "Strong fundamentals with ROE of 28% and attractive PE of 12.
        Debt is manageable. Recommend buy for value portfolios."

        [Fast, to the point]
        ```

        #### Standard (1000-1500 tokens):
        ```
        "Analysis of Company XYZ:

        The company demonstrates exceptional business quality with ROE
        of 28%, well above industry average of 15%. This indicates...

        [2-3 more paragraphs covering valuation, risks, conclusion]

        Recommendation: Buy with 3-5% portfolio allocation."

        [Good balance of detail and readability]
        ```

        #### Detailed (2000+ tokens):
        ```
        "Comprehensive Analysis of Company XYZ:

        Business Quality Assessment:
        The company's ROE of 28% significantly exceeds the industry...
        [Multiple paragraphs]

        Financial Health:
        Balance sheet analysis reveals...
        [Multiple paragraphs]

        Valuation Analysis:
        Trading at PE of 12 vs industry average of 18...
        [Multiple paragraphs]

        Risk Factors:
        1. Debt levels at 0.8x equity...
        2. Industry competitive pressures...
        3. Macroeconomic sensitivities...

        Investment Thesis:
        [Detailed conclusion]

        [Comprehensive report for serious research]
        ```

        **💰 Cost Note:** More tokens = higher API costs (if using OpenAI/Anthropic)

        ---

        ### Comparing AI Providers

        #### Ollama (Local, Free) ⭐ Recommended for Learning

        **Pros:**
        - ✅ Completely free (no API costs)
        - ✅ Private (runs on your computer)
        - ✅ No rate limits
        - ✅ Works offline
        - ✅ Full control over models

        **Cons:**
        - ❌ Requires installation and setup
        - ❌ Slower than cloud (2-5 seconds)
        - ❌ Needs decent computer (8GB+ RAM recommended)
        - ❌ Need to download models (~4GB each)

        **Best for:** Students, learning, testing, privacy-sensitive use

        **Setup:**
        ```bash
        # Install
        curl https://ollama.ai/install.sh | sh

        # Download model
        ollama pull llama3.2  # Recommended
        # or
        ollama pull mistral   # Alternative

        # Start service
        ollama serve  # Keep running
        ```

        #### OpenAI (Cloud, Paid)

        **Pros:**
        - ✅ Very fast (< 1 second)
        - ✅ Very capable (GPT-4)
        - ✅ No local setup needed
        - ✅ Consistent quality
        - ✅ Best for complex analysis

        **Cons:**
        - ❌ Costs money per use (~$0.01-0.02/analysis)
        - ❌ Requires internet
        - ❌ API rate limits
        - ❌ Less private (data sent to OpenAI)

        **Cost for students:**
        - Analyzing 10 stocks/day: ~$3/month
        - Analyzing 50 stocks/day: ~$15/month

        **Best for:** Production use, accuracy-critical, when speed matters

        #### Anthropic Claude (Cloud, Paid)

        **Pros:**
        - ✅ Excellent reasoning ability
        - ✅ Good at structured analysis
        - ✅ Handles nuance well
        - ✅ Good for document analysis (with RAG)

        **Cons:**
        - ❌ Similar costs to OpenAI
        - ❌ Requires API key
        - ❌ Rate limits

        **Cost:** ~$0.01-0.03 per analysis

        **Best for:** Complex analysis, regulatory documents, detailed reasoning

        ---

        ### When to Use LLM Agents

        ✅ **Perfect for:**
        - Deep analysis of individual stocks (< 20)
        - Nuanced, context-aware reasoning
        - Explaining investment thesis
        - Complex, subjective criteria
        - Natural language insights
        - Learning investment analysis
        - When quality matters more than speed

        ❌ **Not ideal for:**
        - Screening thousands of stocks (expensive!)
        - When you need deterministic results
        - Real-time trading signals (too slow)
        - When cost is a major concern
        - When AI setup is not possible

        **💡 Pro Tip:** Use Hybrid agents (next tab) to get LLM intelligence at 5% of the cost!

        ---

        ### Troubleshooting LLM Agents

        #### ❌ "Can't connect to Ollama"

        **Problem:** Ollama service not running

        **Solution:**
        ```bash
        # Start Ollama in separate terminal
        ollama serve

        # Keep it running while using agents
        ```

        #### ❌ "Model 'llama3.2' not found"

        **Problem:** Model not downloaded

        **Solution:**
        ```bash
        # Download the model (one-time, ~4GB)
        ollama pull llama3.2

        # Verify
        ollama list
        ```

        #### ❌ "API key not found" (OpenAI/Anthropic)

        **Problem:** API key not configured

        **Solution:**
        ```bash
        # Edit .env file
        nano .env

        # Add your key:
        OPENAI_API_KEY=sk-your-key-here
        # or
        ANTHROPIC_API_KEY=sk-ant-your-key-here
        ```

        #### ❌ Agent returns neutral with low confidence

        **Problem:** LLM not working, using fallback logic

        **Check:**
        1. Is Ollama running? (`ollama serve`)
        2. Is model downloaded? (`ollama list`)
        3. Is .env file configured? (for OpenAI/Anthropic)

        ---

        ### Learning Exercise

        **Try This:** Create three LLM agents with different personalities:

        1. **Conservative Value Agent**
           - Temperature: 0.2 (very focused)
           - Max Tokens: 800
           - Prompt: "You are extremely conservative. Focus on safety."

        2. **Balanced Quality Agent**
           - Temperature: 0.5 (balanced)
           - Max Tokens: 1200
           - Prompt: "Balance growth and value. Consider quality."

        3. **Aggressive Growth Agent**
           - Temperature: 0.8 (creative)
           - Max Tokens: 1500
           - Prompt: "Find high-growth opportunities. Be bold."

        **Compare:** Run the same stock through all three and see how their analysis differs!

        ---

        **Next:** Want to analyze documents? See the **📄 RAG Agents** tab!
        **Or:** Want efficiency at scale? See the **🔀 Hybrid Agents** tab!
        """)

    with tab4:
        st.markdown("""
        ## 📄 RAG-Powered Agents: Document Analysis

        ### What Are RAG Agents?

        RAG (Retrieval-Augmented Generation) agents analyze **long documents** like SEC filings, earnings reports, or research papers.

        **The Problem:**
        - SEC 10-K filings are 50-100+ pages
        - AI models have context limits (~4000-32000 words)
        - Can't just paste entire filing into AI

        **The Solution (RAG):**
        1. **Chunk:** Break document into small pieces (300 chars each)
        2. **Embed:** Convert text to numbers for similarity search
        3. **Search:** Find relevant chunks using your question
        4. **Analyze:** Use AI only on relevant chunks

        **Result:** Can analyze 100-page documents by finding relevant sections!

        ---

        ### 🔧 Setup Required (Same as LLM)

        RAG agents need the same setup as LLM agents:

        ```bash
        # 1. Install Ollama (one-time)
        curl https://ollama.ai/install.sh | sh

        # 2. Download model (one-time)
        ollama pull llama3.2

        # 3. Start service (each time)
        ollama serve  # Keep running
        ```

        ✅ If you set up LLM agents, you're ready for RAG!

        ---

        ### How RAG Works (Simple Explanation)

        **Traditional approach (doesn't work):**
        ```
        [50-page document] → AI model → ❌ "Error: Too long!"
        ```

        **RAG approach (works):**
        ```
        [50-page document]
          ↓ Step 1: Break into chunks
        [300 small chunks of 300 chars each]
          ↓ Step 2: Find relevant ones
        Query: "What are the risk factors?"
        Semantic search finds: Chunks #45, #46, #47 (risk section)
          ↓ Step 3: Analyze only relevant chunks
        [Top 3 relevant chunks] → AI model → ✅ Analysis!
        ```

        **Example:**
        ```
        You ask: "What are the company's growth strategies?"

        RAG process:
        1. Searches all 300 chunks
        2. Finds chunks #88, #89, #120 mention growth
        3. AI analyzes only those 3 chunks
        4. Returns: "Company focuses on international expansion,
           particularly India and Southeast Asia markets, plus
           increasing R&D in AI/ML by 25%"
        ```

        **Magic:** You get precise answers from 100-page documents in seconds!

        ---

        ### Example: SEC Filing Analyst

        #### Step 1: Create RAG Agent in GUI

        1. Go to **➕ Create Agent**
        2. Fill in:
           - **Agent Name:** SEC10KAnalyst
           - **Type:** RAG-Powered
           - **Description:** Analyzes SEC 10-K filings

        3. **LLM Configuration:**
           - **Provider:** ollama
           - **Model:** llama3.2
           - **Temperature:** 0.4 (focused on facts)
           - **Max Tokens:** 2000 (detailed analysis)

        4. **System Prompt:**
           ```
           You are an expert SEC filing analyst with 20 years of experience.

           Your expertise:
           - Reading and interpreting 10-K, 10-Q filings
           - Identifying key financial trends
           - Spotting risk factors and red flags
           - Evaluating management strategy
           - Assessing competitive positioning

           When analyzing document excerpts:
           1. Focus on factual information from the filing
           2. Identify specific numbers, metrics, and trends
           3. Highlight both opportunities and risks
           4. Be precise and cite specific details
           5. Provide actionable investment insights

           Be thorough but concise. Extract what matters most.
           ```

        5. **RAG Configuration:**
           - **Chunk Size:** 300 (good balance)
           - **Chunk Overlap:** 50 (prevents cutting sentences)
           - **Top K:** 3 (retrieve top 3 most relevant chunks)

        6. Click **Generate Code** → **Save Agent**

        #### Step 2: Test with a PDF Document

        1. **Make sure Ollama is running:**
           ```bash
           ollama serve
           ```

        2. Go to **🧪 Test Agent**
        3. Select: "SEC10KAnalyst"
        4. **Upload a PDF:**
           - Drag and drop a SEC 10-K filing
           - Or any financial document (earnings report, annual report)
           - Or even a research paper

        5. Click **Run Analysis**

        #### Step 3: Understanding the Results

        The RAG agent automatically queries multiple aspects:

        **Query 1: Financial Performance**
        ```
        Question: "What are the key financial metrics and trends?"

        Chunks Found:
        - Chunk #34: "Revenue increased 8% YoY to $394.3B..."
        - Chunk #35: "iPhone revenue remained flat at $200B..."
        - Chunk #36: "Services revenue grew 16% to $85B..."

        AI Analysis:
        "Financial performance shows continued growth with 8% revenue
        increase driven primarily by Services segment (16% growth).
        iPhone revenue plateauing at $200B indicates market maturity,
        but Services diversification provides growth runway. Gross
        margin expansion to 43.3% demonstrates pricing power and
        operational efficiency improvements."
        ```

        **Query 2: Risk Factors**
        ```
        Question: "What are the main risk factors?"

        Chunks Found:
        - Chunk #67: "Supply chain concentration in China..."
        - Chunk #68: "Regulatory scrutiny in EU regarding DMA..."
        - Chunk #69: "Antitrust investigations into App Store..."

        AI Analysis:
        "Primary risks center on geographic concentration and
        regulatory pressure. China exposure creates both growth
        opportunity and geopolitical risk. EU Digital Markets Act
        may impact App Store margins. Antitrust scrutiny could force
        changes to business model. Foreign exchange headwinds from
        strong dollar affect international sales."
        ```

        **Query 3: Growth Strategies**
        ```
        Question: "What are the growth opportunities?"

        Chunks Found:
        - Chunk #103: "Expanding retail presence in India..."
        - Chunk #105: "Vision Pro launch planned for 2024..."
        - Chunk #107: "Increased R&D investment in AI/ML..."

        AI Analysis:
        "Company pursuing geographic diversification (India expansion)
        and product innovation (Vision Pro spatial computing).
        Significant R&D increase in AI/ML (14% higher spending)
        suggests future product differentiation. Services ecosystem
        expansion into healthcare and financial services represents
        TAM expansion opportunity."
        ```

        **Final Signal:**
        ```
        Direction: 🟢 BULLISH
        Confidence: 70%

        Summary: Strong Services growth and margin expansion demonstrate
        business model evolution. Geographic diversification reduces China
        dependency. Regulatory headwinds are near-term challenges but
        don't invalidate long-term thesis. Vision Pro represents significant
        TAM expansion into new category.

        Recommendation: Buy for long-term growth, 3-5% portfolio allocation.
        ```

        ---

        ### RAG Configuration Guide

        #### Chunk Size Selection

        **Small Chunks (200-300 chars):**

        **Pros:**
        - ✅ Very precise search (finds exact info)
        - ✅ Better for specific questions
        - ✅ Less noise in results

        **Cons:**
        - ❌ Less context per chunk
        - ❌ Might miss connections

        **Use for:**
        - Extracting specific numbers or facts
        - Finding key statements
        - Precise information retrieval

        **Example:** "What was Q3 revenue?" → Finds exact number

        ---

        **Large Chunks (400-600 chars):**

        **Pros:**
        - ✅ More context preserved
        - ✅ Better for understanding themes
        - ✅ Captures relationships

        **Cons:**
        - ❌ Less precise search
        - ❌ More irrelevant info might be included

        **Use for:**
        - Understanding overall strategy
        - Grasping narrative themes
        - Connecting related concepts

        **Example:** "What's the strategic vision?" → Gets broader context

        ---

        #### Top K Selection

        **Top K = 1-3 (Focused):**
        - Fast analysis
        - Most relevant info only
        - Good for specific, targeted questions
        - Less comprehensive

        **Example:** "What was net income?" → One number needed

        ---

        **Top K = 5-7 (Comprehensive):**
        - More thorough analysis
        - Better for complex questions
        - Captures multiple perspectives
        - Slower but more complete

        **Example:** "Analyze competitive position" → Need multiple sections

        ---

        #### Overlap Selection

        **Low Overlap (20-30):**
        - More distinct chunks
        - Better for long documents
        - Faster processing

        **High Overlap (50-100):**
        - Better context preservation
        - Won't cut sentences mid-way
        - Slightly slower

        **Recommended:** 50 (good balance)

        ---

        ### Document Types RAG Can Handle

        #### SEC Filings ✅
        - 10-K (Annual Report)
        - 10-Q (Quarterly Report)
        - 8-K (Current Events)
        - Proxy Statement (DEF 14A)
        - S-1 (IPO Registration)

        **What to analyze:**
        - Financial trends
        - Risk factors
        - Management discussion (MD&A)
        - Business strategy
        - Competitive landscape

        ---

        #### Financial Reports ✅
        - Annual reports
        - Earnings call transcripts
        - Investor presentations
        - Analyst reports
        - Credit rating reports

        **What to analyze:**
        - Revenue drivers
        - Margin trends
        - Management guidance
        - Capital allocation
        - Growth initiatives

        ---

        #### News and Research ✅
        - News articles (long-form)
        - Industry reports
        - Research papers
        - Conference proceedings
        - Market commentary

        **What to analyze:**
        - Sentiment and tone
        - Key events and catalysts
        - Industry trends
        - Competitive dynamics
        - Expert opinions

        ---

        ### When to Use RAG Agents

        ✅ **Perfect for:**
        - Analyzing long documents (50+ pages)
        - SEC filings and regulatory documents
        - Extracting specific information
        - Document comparison over time
        - Research and due diligence
        - Reading earnings transcripts
        - Processing research reports

        ❌ **Not ideal for:**
        - Quick numerical screening
        - Real-time analysis
        - When you only have summary data
        - Simple questions about current price
        - When documents aren't available

        ---

        ### Pro Tips for RAG

        💡 **Specific queries work best:**
        - Good: "What are supply chain risks?"
        - Bad: "Tell me about risks"

        💡 **Multiple queries for comprehensive analysis:**
        - Query 1: Financial performance
        - Query 2: Risk factors
        - Query 3: Growth strategy
        - Query 4: Competitive position

        💡 **Compare over time:**
        - Analyze Q1 filing: "What are growth drivers?"
        - Analyze Q2 filing: "What are growth drivers?"
        - Compare: Are they consistent? Improving? Declining?

        💡 **Verify numbers:**
        - AI might misread numbers from PDFs
        - Double-check important figures against source

        💡 **Use for discovery:**
        - Ask exploratory questions
        - Find insights you might miss reading manually
        - Let AI surface hidden patterns

        ---

        ### Troubleshooting RAG Agents

        #### ❌ "Can't read PDF"

        **Problem:** PDF format issue

        **Solutions:**
        1. Try a different PDF
        2. Convert to text-based PDF (not scanned image)
        3. Use OCR if PDF is scanned

        ---

        #### ❌ "Analysis taking too long"

        **Problem:** Large document + high top_k

        **Solutions:**
        1. Reduce top_k from 5 to 3
        2. Use smaller document sections
        3. Increase chunk_size to reduce total chunks

        ---

        #### ❌ "Results not relevant"

        **Problem:** Search not finding right chunks

        **Solutions:**
        1. Make query more specific
        2. Adjust chunk_size (try smaller for precision)
        3. Increase top_k to get more context

        ---

        ### Learning Exercise

        **Try This:** Compare same company across quarters

        1. Download SEC 10-Q filings for Q1, Q2, Q3, Q4
        2. Create RAG agent
        3. Ask same question for each quarter:
           "What are the primary growth drivers?"
        4. Compare answers:
           - Are strategies consistent?
           - Are metrics improving?
           - Any new risks emerging?

        **What you'll learn:**
        - How company strategy evolves
        - Trend analysis over time
        - Risk factor changes
        - Management consistency

        ---

        **Next:** Want to combine rules + AI? See the **🔀 Hybrid Agents** tab!
        **Or:** Want to use real market data? See the **💾 Using Real Data** tab!
        """)

    with tab5:
        st.markdown("""
        ## 🔀 Hybrid Agents: Efficiency at Scale

        ### Why Hybrid Agents?

        **The Problem:**
        - Rule-based agents: Fast but not intelligent
        - LLM agents: Smart but expensive and slow for large datasets

        **The Solution: Hybrid = Rules (fast filter) + LLM (deep analysis)**

        **Result:** Get AI intelligence at 5% of the cost!

        ---

        ### How Hybrid Works: Two-Stage Process

        **Stage 1: Rules (Fast Screening)**
        ```
        [1000 stocks]
          ↓ Apply simple rules (milliseconds)
        [50 stocks pass rules] (95% filtered out!)
          ↓ Only 50 need deep analysis
        ```

        **Stage 2: LLM (Deep Analysis)**
        ```
        [50 filtered stocks]
          ↓ AI analyzes each one (2-3 seconds each)
        [10 top picks with detailed reasoning]
        ```

        **Total time:** ~2 minutes (vs 25 minutes for pure LLM!)
        **Total cost:** $0.50 (vs $10 for pure LLM!)
        **Same depth:** On the stocks that matter!

        ---

        ### Example: Growth + Quality Hybrid

        #### The Strategy

        **Stage 1 Rules (Fast Filter):**
        ```
        IF revenue_growth > 15% AND profit_margin > 10%
        THEN → Pass to Stage 2
        ELSE → Skip (neutral signal, no LLM needed)
        ```

        **Why these rules?**
        - Filters for growth stocks only
        - Ensures basic profitability
        - Removes 90-95% of stocks instantly
        - No AI cost for stocks that don't meet baseline

        **Stage 2 LLM (Quality Analysis):**
        ```
        System Prompt:
        "You are evaluating growth stocks for QUALITY.

        This stock passed growth screening (>15% revenue, >10% margin).
        Your job: Assess if this growth is SUSTAINABLE.

        Consider:
        1. Is growth sustainable or temporary?
        2. Does the company have competitive advantages?
        3. What are key risks to growth?
        4. Is management executing well?
        5. Are margins stable or improving?

        Be critical and thorough. Growth without quality is risky."
        ```

        ---

        #### Step 1: Create Hybrid Agent in GUI

        1. Go to **➕ Create Agent**
        2. Fill in:
           - **Agent Name:** GrowthQualityHybrid
           - **Type:** Hybrid
           - **Description:** Screens for growth, analyzes quality

        3. **Screening Rules (Stage 1):**
           - Rule 1: revenue_growth > 15 → pass to LLM
           - Rule 2: profit_margin > 10 → pass to LLM
           - Logic: AND (both must be true)

        4. **LLM Configuration (Stage 2):**
           - Provider: ollama
           - Model: llama3.2
           - Temperature: 0.6 (balanced creativity)
           - Max Tokens: 1500
           - System Prompt: (quality-focused as above)

        5. Click **Generate Code** → **Save Agent**

        #### Step 2: Understanding the Process

        **Test Case 1: Passes Stage 1**
        ```
        Stock: SHOP (Shopify)
        Revenue Growth: 25% ✅ (> 15%)
        Profit Margin: 12% ✅ (> 10%)

        Stage 1 Result: PASS → Send to LLM

        Stage 2 (LLM Analysis):
        "Shopify demonstrates sustainable growth driven by:

        1. SMB market shift to e-commerce (secular trend)
        2. Increasing take rate from payments (6.2% → 7.1%)
        3. International expansion (35% of revenue, growing)
        4. Platform network effects strengthen competitive moat

        However, competitive pressure from Amazon and BigCommerce
        may compress margins over time. Management's pivot to
        profitability is positive but execution risk remains.

        Quality Assessment: Above-average quality growth

        Signal: 🟢 BULLISH
        Confidence: 65%"
        ```

        **Test Case 2: Fails Stage 1**
        ```
        Stock: XYZ Corp
        Revenue Growth: 8% ❌ (< 15%)
        Profit Margin: 5% ❌ (< 10%)

        Stage 1 Result: FAIL → Skip LLM

        Final Signal: 🟡 NEUTRAL
        Confidence: 50%
        Reasoning: "Did not pass growth screening (8% growth, 5% margin).
                   Criteria: Growth >15% AND Margin >10%"

        [No LLM cost! Instant result!]
        ```

        ---

        ### Cost & Time Comparison

        #### Scenario: Daily Market Scan of S&P 500

        **Pure LLM Approach:**
        ```
        500 stocks × $0.01 per analysis = $5.00 per day
        500 stocks × 3 seconds = 25 minutes

        Annual Cost: $5 × 250 trading days = $1,250/year
        Daily Time: 25 minutes
        ```

        **Hybrid Approach:**
        ```
        Stage 1 (Rules):
        500 stocks × 0.001 seconds = 0.5 seconds
        Cost: $0 (no AI)

        Stage 2 (LLM):
        ~25 stocks pass (5%)
        25 stocks × $0.01 = $0.25 per day
        25 stocks × 3 seconds = 75 seconds

        Annual Cost: $0.25 × 250 = $62.50/year
        Daily Time: 76 seconds (1.3 minutes)
        ```

        **Savings:**
        - Cost: $1,187.50/year (95% reduction!)
        - Time: 23.7 minutes/day (94% faster!)
        - Quality: Same depth on the 25 stocks that matter!

        ---

        ### Threshold Tuning (Critical!)

        The success of hybrid agents depends on good thresholds.

        #### Too Strict (< 5% pass)

        **Rules:**
        ```
        IF revenue_growth > 30% AND margin > 20%
        ```

        **Problem:**
        - Only 2-3% of stocks pass
        - Miss good opportunities
        - Too selective

        **Result:** Few LLM calls but also few good picks

        ---

        #### Too Loose (> 20% pass)

        **Rules:**
        ```
        IF revenue_growth > 5% OR margin > 5%
        ```

        **Problem:**
        - 30-40% of stocks pass
        - Too many LLM calls
        - Defeats purpose of hybrid

        **Result:** High costs, slow, not much better than pure LLM

        ---

        #### Just Right (5-15% pass) ✅

        **Rules:**
        ```
        IF revenue_growth > 15% AND margin > 10%
        ```

        **Result:**
        - ~10% of stocks pass (50 out of 500)
        - Good candidates for deep analysis
        - Manageable LLM costs
        - Fast screening

        **This is the sweet spot!**

        ---

        ### When to Use Hybrid Agents

        ✅ **Perfect for:**
        - Large stock universes (S&P 500, Russell 2000, etc.)
        - Production workflows and systematic investing
        - Cost-sensitive applications
        - Need both speed and depth
        - Screening + selective analysis
        - Daily/weekly market scans

        ❌ **Not ideal for:**
        - Small stock lists (< 50) - just use LLM directly
        - When rules can't filter effectively
        - Highly subjective criteria that rules can't capture
        - When you need deep analysis on everything

        ---

        ### Real-World Example: Portfolio Construction

        **Goal:** Build a portfolio of 10 growth stocks from universe of 1000

        **Step 1: Initial Screening (Rules)**
        ```
        [1000 stocks]
          ↓ Revenue Growth > 20%
        [150 stocks remain]
          ↓ Profit Margin > 12%
        [50 stocks remain]
          ↓ Debt/Equity < 1.5
        [30 stocks remain]

        Time: < 1 second
        Cost: $0
        ```

        **Step 2: Quality Analysis (LLM)**
        ```
        [30 candidates]
          ↓ AI analyzes each for quality, moat, risks
        [30 detailed analyses]

        Time: 90 seconds (3 sec × 30)
        Cost: $0.30 ($0.01 × 30)
        ```

        **Step 3: Final Selection (You)**
        ```
        Review 30 AI analyses
        Pick top 10 based on:
        - Highest quality scores
        - Best risk/reward
        - Portfolio diversification

        Result: 10-stock growth portfolio
        ```

        **Total:** 90 seconds, $0.30, high-quality picks!

        **vs Pure LLM:** Would cost $10 and take 25 minutes for same quality on final picks.

        ---

        ### Pro Tips for Hybrid Agents

        💡 **Use rules for objective criteria:**
        - Growth rates, margins, ratios
        - Things that are clearly measurable
        - Binary filters (pass/fail)

        💡 **Use LLM for subjective assessment:**
        - Quality evaluation
        - Competitive advantage assessment
        - Risk analysis
        - Strategic positioning

        💡 **Tune thresholds based on results:**
        - Too many passing? Tighten rules
        - Too few passing? Loosen rules
        - Target: 5-15% pass rate

        💡 **Monitor performance:**
        - Track how many stocks pass Stage 1
        - Measure LLM cost per day/week
        - Adjust rules seasonally (bull vs bear market)

        ---

        ### Troubleshooting Hybrid Agents

        #### ❌ "All stocks getting neutral signals"

        **Problem:** Rules too strict, nothing passing to LLM

        **Check:**
        1. How many stocks pass Stage 1? (should be 5-15%)
        2. Are thresholds realistic?

        **Solution:**
        - Loosen one rule slightly
        - Or change AND to OR for some conditions

        ---

        #### ❌ "Taking too long and costing too much"

        **Problem:** Too many stocks passing to Stage 2

        **Check:**
        1. What % of stocks pass Stage 1? (should be < 15%)
        2. Are rules too loose?

        **Solution:**
        - Tighten thresholds
        - Add another rule to filter more
        - Change OR to AND

        ---

        #### ❌ "Hybrid slower than pure rules"

        **Problem:** LLM service slow or not responding

        **Check:**
        1. Is Ollama running? (`ollama serve`)
        2. Is model downloaded?

        **Solution:**
        - Make sure Ollama service is running
        - Or switch to cloud provider (faster)

        ---

        ### Learning Exercise

        **Experiment:** Compare three approaches on S&P 500

        **1. Pure Rules:**
        - Create simple rule-based agent
        - Count bullish/bearish/neutral
        - Time: < 1 second
        - Note: Fast but simplistic

        **2. Pure LLM:**
        - Create LLM agent
        - Run on 10 sample stocks (not all 500!)
        - Extrapolate time/cost for 500
        - Note: Very detailed but expensive

        **3. Hybrid:**
        - Create hybrid agent
        - Run on all 500 stocks
        - Count how many pass Stage 1
        - Note: Best balance

        **Compare:**
        - Speed: Rules > Hybrid >> LLM
        - Cost: Rules = $0, Hybrid = $0.30, LLM = $5
        - Depth: LLM = Hybrid > Rules
        - Scalability: Hybrid is the winner!

        ---

        **Next:** Want to use real market data? See the **💾 Using Real Data** tab!
        **Or:** Want to customize AI prompts? See the **🎨 Customizing Prompts** tab!
        """)

    with tab6:
        st.markdown("""
        ## 💾 Using Real Financial Data

        ### Data Sources Overview

        The GUI supports three data sources:

        | Source | When to Use | Setup |
        |--------|-------------|-------|
        | **Mock Data** | Testing, learning | None - works immediately |
        | **Database** | Sample stocks (AAPL, MSFT, etc.) | Already set up |
        | **YFinance** | Real current market data | Install yfinance |

        ---

        ### Option 1: Mock Data (Best for Learning)

        **What it is:** Fictional data you create for testing

        **When to use:**
        - Testing agent logic
        - Learning how agents work
        - Experimenting with different scenarios
        - No internet needed
        - Instant results

        **How to use:**

        1. Go to **🧪 Test Agent**
        2. Select your agent
        3. Choose: **"Mock Data"**
        4. Enter values:
           - PE Ratio: 12
           - Revenue Growth: 15%
           - Profit Margin: 12%
           - ROE: 18%
           - Debt/Equity: 0.5
           - Dividend Yield: 2%
        5. Click **Run Analysis**

        **Advantages:**
        - ✅ Full control over values
        - ✅ Test edge cases easily
        - ✅ No API limits or costs
        - ✅ Works offline
        - ✅ Instant results

        **Use for:**
        - "What if PE was 50?"
        - "What if debt was 5.0?"
        - Testing your rules
        - Learning

        ---

        ### Option 2: YFinance (Real Market Data)

        **What it is:** Real-time stock data from Yahoo Finance

        **When to use:**
        - Analyzing real companies
        - Getting current market data
        - Testing with actual metrics
        - Research and analysis

        #### Setup YFinance

        ```bash
        # Install yfinance package
        pip install yfinance

        # Verify installation
        python3 -c "import yfinance; print('✅ YFinance installed')"
        ```

        **Already done!** If you ran `./gui/setup.sh`, yfinance is installed.

        #### How to Use YFinance in GUI

        1. Go to **🧪 Test Agent**
        2. Select your agent
        3. Choose: **"YFinance (Real Market Data)"**
        4. Enter ticker: **AAPL** (or MSFT, GOOGL, etc.)
        5. Click **Run Analysis**

        **What happens:**
        - GUI fetches current data from Yahoo Finance
        - Displays the data so you can see it
        - Runs your agent on real metrics
        - Shows result

        **Example Output:**
        ```
        ✅ Real data fetched successfully!

        📊 View Fetched Data:
        PE Ratio: 28.5
        Revenue Growth: 8.2%
        Profit Margin: 25.7%
        ROE: 147.4%
        Debt/Equity: 1.98
        Dividend Yield: 0.48%

        [Agent analyzes real data]

        Signal: 🟢 BULLISH
        Confidence: 72%
        Reasoning: Strong profitability with 25.7% margins and
        exceptional ROE of 147%. Growth steady at 8%. Valuation
        reasonable at PE 28.5 for this quality.
        ```

        #### YFinance Available Metrics

        **Valuation:**
        - Market Cap
        - PE Ratio (trailing and forward)
        - Price to Book
        - PEG Ratio
        - Price to Sales
        - Enterprise Value

        **Profitability:**
        - Profit Margin
        - Operating Margin
        - Gross Margin
        - ROE (Return on Equity)
        - ROA (Return on Assets)

        **Growth:**
        - Revenue Growth (YoY)
        - Earnings Growth (YoY)
        - Quarterly Revenue Growth
        - Quarterly Earnings Growth

        **Financial Health:**
        - Total Cash
        - Total Debt
        - Debt to Equity
        - Current Ratio
        - Quick Ratio

        **Dividends:**
        - Dividend Yield
        - Dividend Rate
        - Payout Ratio
        - 5-Year Average Dividend Yield

        **Price Data:**
        - Current Price
        - 52-Week High
        - 52-Week Low
        - Average Volume
        - Beta

        ---

        #### Error Handling

        **❌ "No data for ticker"**

        **Problem:** Ticker not found or invalid

        **Solutions:**
        1. Check ticker spelling (AAPL not Apple)
        2. Try a different ticker
        3. Check if ticker exists on Yahoo Finance

        **Common mistakes:**
        - ❌ "Apple" → ✅ "AAPL"
        - ❌ "Microsoft" → ✅ "MSFT"
        - ❌ "Google" → ✅ "GOOGL" or "GOOG"

        ---

        **❌ "Connection timeout"**

        **Problem:** Can't reach Yahoo Finance servers

        **Solutions:**
        1. Check internet connection
        2. Try again (temporary server issue)
        3. Use Mock Data instead

        ---

        **❌ "Missing some metrics"**

        **Problem:** Some data not available for this company

        **Solution:**
        - YFinance might not have all data for all companies
        - Missing values will show as 0 or N/A
        - Agent should handle this gracefully

        ---

        ### Comparing Data Sources

        #### Test the Same Agent with Different Data

        **Exercise:** See how data source affects results

        **1. Create a value agent:**
        ```
        Rule: IF pe_ratio < 15 THEN bullish
        ```

        **2. Test with Mock Data:**
        ```
        PE Ratio: 12 (you set this)
        Result: BULLISH (obviously, since you designed it to pass)
        ```

        **3. Test with YFinance:**
        ```
        Ticker: AAPL
        PE Ratio: 28.5 (actual current value)
        Result: NEUTRAL (doesn't meet your criteria)
        ```

        **4. Insight:**
        - Mock data is for testing logic
        - Real data shows if your rules actually work in market
        - Your "PE < 15" rule might be too strict!

        ---

        ### When to Use Each Source

        **Mock Data:**
        - ✅ Developing and testing agents
        - ✅ Learning how rules work
        - ✅ Testing edge cases
        - ✅ No internet available
        - ✅ Quick experiments

        **YFinance:**
        - ✅ Analyzing real companies
        - ✅ Research and due diligence
        - ✅ Checking if your rules work in reality
        - ✅ Getting current market data
        - ✅ Comparing multiple real stocks

        **Database:**
        - ✅ Quick tests with sample data
        - ✅ When examples are sufficient
        - ✅ Consistent test data (doesn't change)

        ---

        ### Pro Tips

        💡 **Develop with Mock, Validate with Real:**
        1. Create agent with mock data
        2. Test logic works as expected
        3. Then test with real YFinance data
        4. See if your thresholds are realistic

        💡 **Use YFinance for Research:**
        - Quickly check fundamentals of any company
        - Compare metrics across competitors
        - Track changes over time (re-fetch periodically)

        💡 **Mock Data for Edge Cases:**
        ```
        Test with extreme values:
        - PE = 0 (what happens?)
        - PE = 1000 (what happens?)
        - Debt = 10.0 (highly leveraged)
        - Negative growth (recession scenario)
        ```

        💡 **Verify Important Decisions:**
        - If agent says BULLISH on high confidence
        - Verify the numbers make sense
        - Check YFinance data is recent
        - Look up the company to confirm

        ---

        ### Real vs Mock Data Example

        **Scenario:** Testing a growth agent

        **Your Rule:**
        ```
        IF revenue_growth > 20% AND profit_margin > 15% THEN bullish
        ```

        **Mock Data Test (Optimistic):**
        ```
        Revenue Growth: 25% ✅
        Profit Margin: 18% ✅

        Result: BULLISH
        Thinking: "Great! My rule works!"
        ```

        **Real Data Test (Reality Check):**
        ```
        Test 10 actual growth stocks with YFinance:

        1. NVDA: Growth 50%, Margin 20% → BULLISH ✅
        2. AMD: Growth 18%, Margin 3% → NEUTRAL ❌
        3. SHOP: Growth 22%, Margin 12% → NEUTRAL ❌
        4. SQ: Growth 15%, Margin 25% → NEUTRAL ❌
        5. ... and so on

        Result: Only 2/10 pass!

        Insight: "My thresholds might be too strict. Maybe I should
        lower them to growth > 15% OR adjust margin requirement."
        ```

        **Lesson:** Real data helps you calibrate your rules to reality!

        ---

        ### Troubleshooting

        #### ❌ YFinance not installed

        ```bash
        pip install yfinance

        # Or reinstall everything:
        ./gui/setup.sh
        ```

        #### ❌ Data fetch very slow

        **Problem:** Internet slow or YFinance servers busy

        **Solution:**
        - Use Mock Data for testing
        - Try again later
        - Check internet connection

        #### ❌ Agent works with mock but fails with real data

        **Problem:** Real data has None/null values

        **Solution:**
        - Agents should handle missing data gracefully
        - Check generated code handles `get('metric', 0)` properly
        - Missing data defaults to 0

        ---

        **Next:** Want to customize how AI thinks? See the **🎨 Customizing Prompts** tab!
        **Or:** Want to understand signals better? See the **⚖️ Understanding Signals** tab!
        """)

    with tab7:
        st.markdown("""
        ## 🎨 Customizing AI Prompts

        ### What Are Prompts?

        Prompts are instructions you give to the AI. They control:
        - **What** the AI focuses on
        - **How** it analyzes
        - **What** personality it has

        Think of prompts like giving instructions to a human analyst!

        ---

        ### Two Types of Prompts

        #### 1. System Prompt (Agent Personality)

        **What it does:** Defines who the AI "is"

        **Example - Conservative Analyst:**
        ```
        You are a conservative investment analyst.

        Your approach:
        - Focus on capital preservation over growth
        - Require margin of safety (30% discount to value)
        - Prefer established, profitable companies
        - Avoid speculative stocks
        - Be extremely cautious

        Always explain risks clearly.
        ```

        **Result:** AI will be very cautious, conservative, risk-aware

        ---

        **Example - Aggressive Growth Hunter:**
        ```
        You are an aggressive growth investor.

        Your approach:
        - Focus on disruption and innovation
        - Accept higher valuations for superior growth
        - Look for 10x potential
        - Embrace calculated risks
        - Think 5-10 years out

        Be bold and forward-thinking.
        ```

        **Result:** AI will be bullish on growth, less concerned about current valuation

        ---

        #### 2. User Prompt (Analysis Instructions)

        **What it does:** Specific question or request

        **In the GUI:** This is automatically generated when you create the agent.

        **Example:**
        ```
        Analyze AAPL with these metrics:
        PE Ratio: 28
        ROE: 147%
        Profit Margin: 25%

        Provide investment recommendation.
        Format: DIRECTION|CONFIDENCE|REASONING
        ```

        ---

        ### Creating Effective System Prompts

        #### Template Structure

        ```
        You are a [ROLE].

        Your philosophy:
        - [Core belief 1]
        - [Core belief 2]
        - [Core belief 3]

        Your approach:
        - [Method 1]
        - [Method 2]
        - [Method 3]

        When analyzing:
        1. [Step 1]
        2. [Step 2]
        3. [Step 3]

        [Any special instructions]
        ```

        ---

        #### Example 1: Value Investor

        ```
        You are a value investor inspired by Benjamin Graham.

        Your philosophy:
        - Buy stocks trading below intrinsic value
        - Require 30% margin of safety
        - Focus on established, profitable businesses
        - Prefer low debt (< 50% of equity)
        - Patient, long-term approach

        Your approach:
        - Calculate intrinsic value from fundamentals
        - Compare price to value for margin of safety
        - Assess business quality (ROE, margins, stability)
        - Evaluate financial safety (debt, liquidity)
        - Identify risks that could impair value

        When analyzing:
        1. Determine if stock is undervalued (price < intrinsic value)
        2. Check if margin of safety exists (at least 30% discount)
        3. Verify business quality (profitable, stable, low debt)
        4. Assess downside risks
        5. Provide conservative recommendation

        Be thorough and skeptical. Err on the side of caution.
        ```

        ---

        #### Example 2: Momentum Trader

        ```
        You are a momentum trader focused on price action.

        Your philosophy:
        - Follow the trend
        - Buy strength, sell weakness
        - Price tells the story
        - Volume confirms moves
        - Cut losses quickly, let winners run

        Your approach:
        - Identify trend direction (up, down, sideways)
        - Check volume confirmation
        - Find key support and resistance levels
        - Assess momentum strength
        - Determine entry and exit points

        When analyzing:
        1. Determine primary trend
        2. Check if volume supports the trend
        3. Identify key price levels
        4. Assess momentum indicators
        5. Provide actionable trade setup

        Focus on price action over fundamentals.
        ```

        ---

        #### Example 3: Dividend Income Investor

        ```
        You are a dividend income investor seeking reliable cash flow.

        Your philosophy:
        - Dividend safety is paramount
        - Look for sustainable, growing dividends
        - Prefer dividend aristocrats (25+ years of increases)
        - Payout ratio should be sustainable (< 70%)
        - Free cash flow must cover dividends

        Your approach:
        - Evaluate current dividend yield (target > 3%)
        - Check dividend growth history (prefer 10+ years)
        - Assess payout ratio sustainability
        - Verify free cash flow coverage
        - Identify risks to dividend

        When analyzing:
        1. Is current yield attractive?
        2. Does company have dividend growth history?
        3. Is payout ratio sustainable?
        4. Is free cash flow sufficient to cover dividend?
        5. What risks could force a dividend cut?

        Prioritize dividend safety above all else.
        ```

        ---

        ### How to Customize Prompts in GUI

        #### Creating Agent with Custom Prompt

        1. Go to **➕ Create Agent**
        2. Select **LLM-Powered** type
        3. In **System Prompt** field, write your custom prompt
        4. Use one of the templates above as starting point
        5. Or create your own!

        **Tips for writing good prompts:**
        - Be specific about what you want
        - Define the role/personality clearly
        - List core principles or beliefs
        - Explain the approach step-by-step
        - Give examples if helpful

        ---

        ### Prompt Engineering Tips

        #### Tip 1: Be Specific

        ❌ **Vague:**
        ```
        You are an analyst. Analyze stocks.
        ```

        ✅ **Specific:**
        ```
        You are a quality-focused analyst.

        Focus on:
        - ROE above 15% (efficiency)
        - Profit margins above 12% (pricing power)
        - Debt-to-equity below 1.0 (safety)
        - Consistent earnings growth (reliability)

        Prioritize sustainable competitive advantages.
        ```

        ---

        #### Tip 2: Provide Context

        ❌ **No Context:**
        ```
        Is this stock a buy?
        ```

        ✅ **With Context:**
        ```
        For a conservative retirement portfolio seeking dividend
        income with low volatility:

        - Is the dividend safe and sustainable?
        - Is the business stable with low cyclicality?
        - Are there growth risks that could hurt dividends?

        Prioritize safety over growth.
        ```

        ---

        #### Tip 3: Define Output Format

        ❌ **Unstructured:**
        ```
        Tell me about this stock.
        ```

        ✅ **Structured:**
        ```
        Provide analysis in this format:

        1. Business Quality (ROE, margins, competitive position)
        2. Financial Health (debt, liquidity, cash flow)
        3. Valuation (fair value vs current price)
        4. Key Risks (what could go wrong)
        5. Recommendation (buy/hold/sell with conviction level)

        Format final answer as: DIRECTION|CONFIDENCE|REASONING
        ```

        ---

        #### Tip 4: Use Examples

        ```
        When providing reasoning, be specific:

        Good: "ROE of 18% exceeds cost of capital at 10%, creating
               value. Margins of 15% demonstrate pricing power."

        Bad: "Good company with strong financials."

        Always use specific numbers and explain what they mean.
        ```

        ---

        ### Testing Your Prompts

        **Always test with multiple scenarios:**

        #### Test Case 1: Strong Bull Case
        ```
        PE: 10, ROE: 25%, Margin: 20%, Debt: 0.3

        Expected: Should be clearly BULLISH with high confidence

        If not: Prompt might be too conservative
        ```

        #### Test Case 2: Strong Bear Case
        ```
        PE: 50, ROE: 3%, Margin: 2%, Debt: 5.0

        Expected: Should be clearly BEARISH with high confidence

        If not: Prompt might be too lenient
        ```

        #### Test Case 3: Mixed Signals
        ```
        PE: 20, ROE: 15%, Margin: 12%, Debt: 1.0

        Expected: Should be NEUTRAL or low-confidence signal

        If not: Prompt might be too opinionated
        ```

        #### Test Case 4: Edge Case
        ```
        PE: 8, ROE: 5%, Margin: 3%, Debt: 3.0

        This is a "value trap" - cheap for a reason

        Expected: Should be NEUTRAL or BEARISH despite low PE

        If not: Prompt doesn't check quality enough
        ```

        ---

        ### Common Prompt Patterns

        #### Pattern 1: Multi-Factor Analysis

        ```
        Analyze using these factors:

        1. Valuation (30% weight)
           - Is PE ratio reasonable?
           - Compare to industry average

        2. Quality (40% weight)
           - ROE above 15%?
           - Margins above 12%?
           - Consistent growth?

        3. Safety (30% weight)
           - Debt manageable?
           - Cash flow positive?
           - Business cyclical?

        Weight factors and provide overall score.
        ```

        ---

        #### Pattern 2: Risk-Focused

        ```
        Focus on risks first:

        1. What could go wrong?
           - Business risks
           - Financial risks
           - Market risks

        2. How likely are these risks?
        3. What's the potential impact?
        4. Does reward outweigh risk?

        Only recommend BUY if risks are acceptable.
        ```

        ---

        #### Pattern 3: Comparative

        ```
        Compare this stock to:
        - Industry average
        - Historical performance
        - Peer companies

        Is it better, worse, or similar?

        Only recommend if meaningfully better than alternatives.
        ```

        ---

        ### Advanced: Combining Prompts with Temperature

        **Same prompt, different temperature = different behavior!**

        **Prompt:** "You are a growth investor"

        **Temperature 0.2 (Conservative):**
        ```
        Result: "Growth is good at 25% but valuation at PE 40 is
                concerning. Recommend NEUTRAL until valuation improves."

        [Focused, cautious even as growth investor]
        ```

        **Temperature 0.8 (Aggressive):**
        ```
        Result: "Exceptional growth at 25%! This is exactly the kind
                of compounding machine we seek. PE of 40 is justified
                by growth trajectory. Strong BUY."

        [Bold, optimistic, embraces high valuation]
        ```

        **Lesson:** Temperature + Prompt work together to shape behavior!

        ---

        ### Troubleshooting Prompts

        #### ❌ Agent always says NEUTRAL

        **Problem:** Prompt too cautious or unclear criteria

        **Solution:**
        - Make criteria more specific
        - Reduce required conditions
        - Lower temperature (more decisive)

        ---

        #### ❌ Agent too bullish on everything

        **Problem:** Prompt lacks critical analysis

        **Solution:**
        - Add "be critical and skeptical"
        - Require higher standards
        - Add risk assessment requirement

        ---

        #### ❌ Reasoning too vague

        **Problem:** Prompt doesn't ask for specifics

        **Solution:**
        ```
        Add to prompt:
        "Always cite specific numbers. Explain what each metric means.
        Compare to industry standards."
        ```

        ---

        ### Learning Exercise

        **Try This:** Create 3 versions of same agent with different prompts

        **Agent 1 - Conservative:**
        ```
        "You are extremely conservative. Only recommend stocks with
        exceptional safety. Require PE < 12, Debt < 0.5, ROE > 20%"
        ```

        **Agent 2 - Balanced:**
        ```
        "You balance growth and value. Look for reasonable valuations
        with good fundamentals. Flexible on criteria based on context."
        ```

        **Agent 3 - Aggressive:**
        ```
        "You seek maximum growth. Accept high valuations if growth
        justifies it. Focus on potential, not current metrics."
        ```

        **Compare:** Run same stock (e.g., NVDA) through all three

        **Learn:** How prompts shape AI behavior!

        ---

        **Next:** Want to understand what signals mean? See the **⚖️ Understanding Signals** tab!
        """)

    with tab8:
        st.markdown("""
        ## ⚖️ Understanding Agent Signals
        
        ### Signal Components
        
        Every agent returns three key pieces:
        
        1. **Direction**: Bullish, Bearish, or Neutral
        2. **Confidence**: 0-100% (calculated, not hardcoded!)
        3. **Reasoning**: Why it made this decision
        
        ---
        
        ### 🎯 How Confidence is Calculated (NEW!)
        
        **Confidence is now calculated based on signal strength, not hardcoded!**
        
        #### For Rule-Based Agents
        
        Confidence depends on **how far the value is from the threshold:**
        
        **Example: PE Ratio rule (Buy if PE < 15)**
        
        | PE Value | Distance | Strength | Confidence |
        |----------|----------|----------|------------|
        | 14.5 | 3% below | Barely met | ~60% |
        | 13.0 | 13% below | Moderately met | ~70% |
        | 11.0 | 27% below | Strongly met | ~80% |
        | 8.0 | 47% below | Very strongly met | ~90% |
        
        **Why this matters:**
        - PE of 5 is much more compelling than PE of 14.9
        - Confidence now reflects signal strength
        - Better for position sizing decisions
        
        **The Algorithm:**
        ```
        If barely met (< 5% from threshold):
            confidence = base × 0.85 ≈ 60%
        
        If moderately met (5-15%):
            confidence = base ≈ 70%
        
        If strongly met (15-30%):
            confidence = base × 1.15 ≈ 80%
        
        If very strongly met (> 30%):
            confidence = base × 1.3 ≈ 90%
        ```
        
        ---
        
        #### For Multi-Rule Agents
        
        **Combines individual rule confidence with consensus:**
        
        **Example: 3 rules, all met**
        ```
        Rule 1 (PE < 15): PE = 10 → 85% confidence (strong)
        Rule 2 (ROE > 15%): ROE = 28% → 90% confidence (very strong)
        Rule 3 (Debt < 1.0): Debt = 0.3 → 85% confidence (strong)
        
        Step 1: Average = (85% + 90% + 85%) / 3 = 87%
        Step 2: Consensus boost = +10% (all 3 of 3 rules met)
        Step 3: Final = min(95%, 87% + 10%) = 95%
        
        Result: 95% confidence - "Strong consensus, very strong signals"
        ```
        
        **Example: Mixed signals**
        ```
        Rule 1 (PE < 15): PE = 14.8 → 62% confidence (barely)
        Rule 2 (ROE > 15%): Not met → Skipped
        Rule 3 (Debt < 1.0): Debt = 0.9 → 65% confidence (barely)
        
        Step 1: Average = (62% + 65%) / 2 = 64%
        Step 2: Consensus = 2 of 3 met (67%) → +0% boost
        Step 3: Final = 64%
        
        Result: 64% confidence - "Weak signal, barely met criteria"
        ```
        
        ---
        
        #### For Score-Based Agents
        
        **Confidence based on score margin:**
        
        **Example: Bullish threshold = 5 points**
        
        | Score | Margin | Margin % | Confidence | Description |
        |-------|--------|----------|------------|-------------|
        | 5 | 0 | 0% | 60% | At threshold |
        | 6 | 1 | 20% | 65% | Barely past |
        | 7 | 2 | 40% | 75% | Moderately past |
        | 9 | 4 | 80% | 90% | Strongly past |
        
        **Why this is better:**
        - Score of 9 (strongly bullish) gets higher confidence than score of 5 (barely bullish)
        - Reflects conviction in the signal
        - Helps with position sizing
        
        ---
        
        #### For LLM Agents
        
        **AI-provided confidence is validated and adjusted:**
        
        **LLM says 85% confidence:**
        ```
        Check reasoning quality:
        - Length: 250 characters ✓
        - Has specific numbers: Yes ✓
        - Cites metrics: Yes ✓
        
        Quality adjustment: ×1.0 (no reduction)
        Final: 85% confidence
        ```
        
        **LLM says 80% but reasoning is vague:**
        ```
        Check reasoning:
        - Length: 45 characters ✗ (too short)
        - Has specific numbers: No ✗
        - Cites metrics: No ✗
        
        Quality adjustment: ×0.85 × 0.90 = ×0.77
        Final: 62% confidence (adjusted down)
        Reason appended: "[Confidence adjusted down due to vague reasoning]"
        ```
        
        **Why this matters:**
        - Some AI responses are more confident than they should be
        - We validate by checking reasoning quality
        - Protects against overconfident AI
        
        ---
        
        #### Data Quality Factor
        
        **All confidence scores are adjusted for data quality:**
        
        | Missing Values | Extreme Values | Multiplier | Impact |
        |----------------|----------------|------------|--------|
        | 0 | 0 | ×1.0 | No reduction |
        | 1 | 0 | ×0.95 | -5% |
        | 2 | 0 | ×0.85 | -15% |
        | 3+ | Any | ×0.70 | -30% |
        
        **Example:**
        ```
        Signal: Bullish, 85% confidence
        Data check: Missing ROE and Revenue Growth
        
        Adjustment: 85% × 0.85 = 72%
        Final: 72% confidence
        Reasoning: "...original reasoning... | Data: some missing data"
        ```
        
        **Why this matters:**
        - Incomplete data = Less reliable signal
        - Confidence reflects data quality
        - Protects against decisions on bad data
        
        ---

        ### Confidence Levels Explained

        Confidence shows **how certain** the agent is about its recommendation.

        #### Confidence Scale Guide

        | Range | Level | What It Means | How to Use It |
        |-------|-------|---------------|---------------|
        | **90-100%** | Very High | All criteria strongly met, very certain | High conviction - larger position (5-10%) |
        | **70-89%** | High | Most criteria met well | Good signal - normal position (3-5%) |
        | **50-69%** | Moderate | Some criteria met | Proceed cautiously - small position (1-2%) |
        | **30-49%** | Low | Few criteria met | Avoid or minimal allocation (<1%) |
        | **0-29%** | Very Low | Error or no clear signal | Skip entirely |

        ---

        ### Interpreting Different Agent Types

        #### Rule-Based Agent Confidence

        **High Confidence (80-100%):**
        - Multiple rules matched strongly
        - Clear, unambiguous signal
        - Values far from thresholds

        **Example:**
        ```
        Company: MSFT
        Rules:
        - PE < 15 → MSFT has PE=10 ✅ (well below threshold)
        - ROE > 15% → MSFT has ROE=28% ✅ (well above threshold)
        - Debt < 1.0 → MSFT has Debt=0.3 ✅ (well below threshold)

        Result: 🟢 BULLISH (90% confidence)
        Reason: "All criteria strongly met - clear value opportunity"

        Interpretation: This is a STRONG signal - rules decisively met!
        ```

        ---

        **Low Confidence (30-50%):**
        - Rules barely met or borderline
        - Mixed signals from different rules
        - Values close to thresholds

        **Example:**
        ```
        Company: XYZ
        Rules:
        - PE < 15 → XYZ has PE=14.9 ⚠️ (barely passes)
        - ROE > 15% → XYZ has ROE=14.5% ❌ (barely fails)
        - Debt < 1.0 → XYZ has Debt=0.95 ⚠️ (barely passes)

        Result: 🟡 NEUTRAL (45% confidence)
        Reason: "Borderline case - some criteria barely met"

        Interpretation: Not a strong signal - values are marginal.
        Probably skip this one.
        ```

        ---

        #### LLM Agent Confidence

        **High Confidence (70-90%):**
        - Clear fundamental story
        - Multiple supporting factors
        - Few significant concerns
        - Strong conviction in reasoning

        **Example:**
        ```
        Company: AAPL

        AI Analysis:
        "Apple demonstrates exceptional business quality:
        - ROE of 147% (far above 15% threshold)
        - Profit margins of 25% (excellent pricing power)
        - Services revenue growing 16% (diversification)
        - Brand moat is durable and strengthening
        - Balance sheet fortress with $100B+ cash

        Valuation at PE 28 is reasonable given quality and growth.
        Limited near-term risks.

        High conviction BUY recommendation."

        Result: 🟢 BULLISH (85% confidence)

        Interpretation: AI is very confident - multiple strong factors
        align with no major concerns.
        ```

        ---

        **Low Confidence (40-60%):**
        - Mixed signals
        - Significant uncertainties
        - Competing factors (e.g., good growth but high debt)
        - Ambiguous outlook

        **Example:**
        ```
        Company: SNAP

        AI Analysis:
        "Snapchat presents a mixed picture:

        Positives:
        - Strong user growth (20% YoY)
        - Engagement metrics improving
        - AR technology leadership

        Concerns:
        - Monetization remains challenging
        - Competition from TikTok intensifying
        - High valuation (8x sales) assumes continued growth
        - Management execution has been inconsistent
        - Advertising market facing headwinds

        Multiple uncertainties make conviction difficult."

        Result: 🟡 NEUTRAL (50% confidence)

        Interpretation: AI sees both sides - no clear answer.
        Too uncertain to recommend strongly either way.
        ```

        ---

        ### Using Confidence for Position Sizing

        **Investment Rule:** Confidence Level → Position Size

        | Confidence | Position Size | Example |
        |------------|---------------|---------|
        | 90-100% | 5-10% | Very strong pick - larger allocation |
        | 70-89% | 3-5% | Good pick - normal allocation |
        | 50-69% | 1-2% | Speculative - small position |
        | < 50% | 0% | Skip - not confident enough |

        **Example Portfolio:**
        ```
        Total Portfolio: $100,000

        Agent signals:
        1. AAPL - BULLISH (85%) → Allocate $4,000 (4%)
        2. MSFT - BULLISH (90%) → Allocate $6,000 (6%)
        3. GOOGL - BULLISH (70%) → Allocate $3,000 (3%)
        4. META - NEUTRAL (55%) → Allocate $1,000 (1%) or skip
        5. SNAP - BEARISH (40%) → Allocate $0 (skip)

        Total Allocation: $13,000-14,000 (13-14%)
        Remaining: Cash or other opportunities
        ```

        **Why this works:**
        - More confident = more capital
        - Less confident = less capital or skip
        - Diversification across multiple picks
        - Risk management built-in

        ---

        ### Combining Multiple Agent Signals

        **Technique:** Run same stock through different agents

        #### Example: Analyzing "AAPL"

        | Agent | Strategy | Signal | Confidence | Key Point |
        |-------|----------|--------|------------|-----------|
        | **Value Agent** | Low PE, High ROE | 🟡 Neutral | 55% | "Fairly valued, not cheap" |
        | **Growth Agent** | Revenue growth | 🟢 Bullish | 65% | "Steady 8% growth" |
        | **Quality Agent** | Margins, moat | 🟢 Bullish | 90% | "Exceptional quality" |
        | **Momentum Agent** | Price action | 🟢 Bullish | 75% | "Strong uptrend" |

        #### Consensus Analysis

        **Count:**
        - 3 out of 4 agents bullish (75%)
        - Average confidence: 71%
        - Value agent is neutral (not bearish!)

        **Interpretation:**
        - **Strong consensus for BULLISH**
        - Not a value stock (fairly valued)
        - But growth, quality, momentum all positive
        - Quality agent very confident (90%)

        **Investment Decision:**
        ```
        This is a QUALITY/GROWTH stock, not VALUE:

        ✅ Good for: Growth portfolios, quality focus
        ❌ Not for: Deep value hunters

        Action: Buy for growth/quality portfolio
        Position: Moderate-High (4-6% based on 71% avg confidence)
        Timeframe: Long-term (quality compounds over time)
        ```

        ---

        ### When Agents Disagree (This is Valuable!)

        **Disagreement shows different perspectives - don't ignore it!**

        #### Scenario 1: Value vs Growth Conflict

        ```
        Value Agent: 🟢 BULLISH (85%)
        "PE of 8, trading below book value"

        Growth Agent: 🔴 BEARISH (70%)
        "Revenue declining 5% annually, margins compressing"

        ═══════════════════════════════════════════════════════

        Interpretation: CLASSIC VALUE TRAP

        - Cheap for a reason (declining business)
        - Value agent sees low price
        - Growth agent sees deteriorating fundamentals

        Action: ❌ AVOID - Respect the growth agent's warning

        Lesson: Cheap ≠ Good Investment
        ```

        ---

        #### Scenario 2: Fundamentals vs Momentum Conflict

        ```
        Quality Agent: 🟢 BULLISH (80%)
        "ROE 25%, margins expanding, low debt - excellent fundamentals"

        Momentum Agent: 🔴 BEARISH (75%)
        "Breaking below 200-day MA, volume declining - downtrend"

        ═══════════════════════════════════════════════════════

        Interpretation: GOOD BUSINESS, BAD TIMING

        - Strong fundamentals (quality agent)
        - But market currently pessimistic (momentum bearish)
        - Potential contrarian buy opportunity
        - OR wait for technical confirmation

        Action:
        Option A: Buy now (contrarian, value opportunity)
        Option B: Wait for momentum to turn positive

        Lesson: Timing matters! Even good companies can decline.
        ```

        ---

        #### Scenario 3: All Agents Neutral (Common!)

        ```
        Value Agent: 🟡 NEUTRAL (50%)
        "Not particularly cheap or expensive"

        Growth Agent: 🟡 NEUTRAL (55%)
        "Average growth, nothing special"

        Quality Agent: 🟡 NEUTRAL (45%)
        "Decent fundamentals, nothing exceptional"

        ═══════════════════════════════════════════════════════

        Interpretation: NO CLEAR SIGNAL

        - Nothing compelling about this stock
        - No strong reason to buy OR sell
        - Probably many better opportunities elsewhere

        Action: ❌ SKIP - Look for higher conviction ideas

        Lesson: Sometimes the answer is "nothing interesting here"
        ```

        ---

        ### Common Mistakes to Avoid

        #### ❌ Mistake 1: Following Low Confidence Signals

        ```
        Agent: 🟢 Bullish (35% confidence)
        You: "But it says bullish, so I'll buy!"

        Problem: 35% confidence is LOW - agent is uncertain
        Reality: This signal is weak, probably skip

        Rule: Only act on confidence > 60%
        ```

        ---

        #### ❌ Mistake 2: Ignoring Reasoning

        ```
        Agent: 🟢 Bullish (80%)
        Reasoning: "Bullish due to temporary accounting boost"
        You: Bought without reading reasoning

        Problem: "Temporary" = not sustainable!
        Reality: Agent is warning you in the reasoning

        Rule: ALWAYS read the reasoning carefully
        ```

        ---

        #### ❌ Mistake 3: Only Using One Agent Type

        ```
        Using only value agents → Miss growth opportunities
        Using only growth agents → Miss value opportunities
        Using only technical → Miss fundamental issues

        Problem: One perspective is limited
        Reality: Different agents see different things

        Rule: Use multiple agent types for complete picture
        ```

        ---

        #### ❌ Mistake 4: Treating Agents as Oracles

        ```
        Agent: 🟢 Bullish (90%)
        You: "Agent says buy, so I'm going all-in!"

        Problem: Agents are TOOLS, not crystal balls
        Reality: Even 90% confidence isn't 100% certainty

        Rule: Agents screen → You research → You decide
        ```

        ---

        ### Real-World Decision Framework

        #### Step 1: Get Signals from Multiple Agents

        ```
        Run target stock through 2-3 different agent types:
        - Value agent (is it cheap?)
        - Quality agent (is it good?)
        - Growth agent (is it growing?)

        Record: Direction, Confidence, Reasoning for each
        ```

        #### Step 2: Calculate Consensus

        ```
        Example: Analyzing stock XYZ

        Agent 1 (Value): Bullish 80%
        Agent 2 (Quality): Bullish 75%
        Agent 3 (Growth): Neutral 50%

        Bullish votes: 2/3 (67%)
        Average confidence: (80 + 75 + 50) / 3 = 68%

        Consensus: Lean BULLISH but not overwhelmingly
        ```

        #### Step 3: Read ALL Reasoning Carefully

        ```
        Look for:
        ✓ Common themes (what do all agents see?)
        ✓ Unique insights (what did only one agent catch?)
        ✓ Red flags (what concerns are mentioned?)
        ✓ Catalysts (what could drive price?)
        ✓ Risks (what could go wrong?)
        ```

        #### Step 4: Do Your Own Research

        ```
        Agents found candidates, now YOU research:

        - Read company reports
        - Check recent news
        - Compare to competitors
        - Understand the business
        - Verify key numbers
        - Assess management

        Agents HELP but don't REPLACE research!
        ```

        #### Step 5: Make Decision with Position Sizing

        ```
        If confidence + research both positive:

        High confidence (>75%) + Good research = 4-6% position
        Medium confidence (60-75%) + Good research = 2-4% position
        Lower confidence (<60%) + Good research = 1-2% position
        Any doubts from research = Reduce or skip

        NEVER exceed position size limits based on confidence alone!
        ```

        #### Step 6: Monitor and Adjust

        ```
        Re-run agents periodically:
        - After earnings (quarterly)
        - On major news
        - When price moves significantly (>20%)

        If confidence drops:
        - From 80% to 50% → Consider selling
        - From 80% to 90% → Consider adding
        - From 70% to 70% → No change

        Agents help you stay disciplined!
        ```

        ---

        ### Summary: Using Signals Effectively

        #### ✅ Do:

        1. **Use multiple agent types** - Get different perspectives
        2. **Weight by confidence** - More confident = more capital
        3. **Read all reasoning** - Details matter!
        4. **Do your own research** - Agents are starting points
        5. **Position size by conviction** - Match size to confidence
        6. **Monitor regularly** - Re-check signals periodically
        7. **Stay disciplined** - Follow your rules and limits

        #### ❌ Don't:

        1. **Follow signals blindly** - Always think critically
        2. **Ignore low confidence** - <60% usually means skip
        3. **Skip reading reasoning** - This is where insights are!
        4. **Treat agents as oracles** - They're tools, not crystal balls
        5. **Risk more than you can afford** - Use position sizing
        6. **Make emotional decisions** - Stick to your system
        7. **Forget the disclaimers** - This is for learning, not real trading advice!

        ---

        ### Final Reminders

        ⚠️ **This is Educational Software**
        - Agents are for learning investment concepts
        - Not financial advice
        - Not real trading recommendations
        - Always consult professionals before real investing

        📚 **Learning Focus**
        - Understand how signals work
        - Practice interpreting confidence levels
        - Learn to combine multiple perspectives
        - Develop critical thinking about investments

        🎯 **Best Practice**
        - Agents screen → You research → You decide
        - Use confidence for position sizing
        - Read reasoning carefully
        - Think critically, always

        ---

        **Congratulations!** You now understand how to use all agent types, interpret signals, and make informed decisions. Keep learning and experimenting!
        """)

    # Educational footer
    st.markdown("---")
    st.info("""
    ### 🎓 Practice Recommendations

    **Beginner Path (Week 1-2):**
    1. Create a simple rule-based agent (PE < 15)
    2. Test with mock data
    3. Try different thresholds and see results
    4. Browse examples (Buffett, Lynch strategies)
    5. Compare rule-based vs LLM agents

    **Intermediate Path (Week 3-4):**
    1. Install Ollama and set up LLM agents
    2. Create LLM agent with custom personality
    3. Test with YFinance real data
    4. Create hybrid agent for efficiency
    5. Compare multiple agents on same stock

    **Advanced Path (Week 5+):**
    1. Create RAG agent for document analysis
    2. Build custom prompt templates
    3. Develop multi-agent systems
    4. Practice interpreting conflicting signals
    5. Build your own investment strategy

    **Remember:**
    - ⚠️ Educational use only
    - ⚠️ Not financial advice
    - ⚠️ Always consult professionals before real investing
    - ⚠️ Past performance doesn't guarantee future results

    **Need Help?**
    - Check [Documentation](https://github.com/thesisai-hq/AI-Agent-Builder/tree/main/docs)
    - View example agents in `examples/` folder
    - Read generated code to learn Python
    - Experiment with different scenarios
    """)


if __name__ == "__main__":
    import streamlit as st

    show_how_to_page()
