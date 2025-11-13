"""Educational 'How To' page for GUI - replaces backtesting

This provides step-by-step workflows for finance students.
"""

import streamlit as st


def show_how_to_page():
    """Display educational guide for financial students."""
    st.header("📚 How to Use Agents for Investment Analysis")
    
    st.markdown("""
    This guide teaches you how to use AI agents to analyze stocks, even if you've never programmed before.
    """)
    
    # Navigation tabs for different workflows
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Getting Started",
        "📊 Value Investing",
        "🚀 Growth Investing",
        "🤖 Using AI Agents",
        "📄 Analyzing Documents",
        "⚖️ Understanding Signals"
    ])
    
    with tab1:
        st.markdown("""
        ## 🎯 Getting Started: Your First Analysis
        
        ### What is an Investment Agent?
        
        Think of an agent as a **virtual analyst** that follows specific rules or uses AI to analyze stocks.
        Just like a human analyst might say "I only buy stocks with PE < 15", an agent can follow the same rule automatically.
        
        ---
        
        ### Step-by-Step: Analyze Your First Stock
        
        #### Step 1: Choose an Agent Type
        
        **Rule-Based Agent** (Recommended for beginners)
        - Follows clear rules (like "buy if PE < 15")
        - Fast and predictable
        - No AI needed
        
        **Example:** A value investor who only buys undervalued stocks
        
        ---
        
        #### Step 2: Define Your Investment Criteria
        
        Ask yourself: *What makes a stock attractive to me?*
        
        **Example criteria:**
        - Low price relative to earnings (PE Ratio < 15)
        - Strong profitability (Profit Margin > 15%)
        - Low debt (Debt-to-Equity < 1.0)
        
        ---
        
        #### Step 3: Create the Agent
        
        1. Go to **➕ Create Agent** tab
        2. Fill in:
           - **Agent Name:** "ValueHunter"
           - **Type:** Rule-Based
        3. Add your rule:
           - **Metric:** pe_ratio
           - **Operator:** <
           - **Threshold:** 15
           - **Signal:** bullish
        4. Click **Generate Code**
        5. Click **Save Agent**
        
        ✅ Done! Your agent is created.
        
        ---
        
        #### Step 4: Test Your Agent
        
        1. Go to **🧪 Test Agent** tab
        2. Select your agent: "ValueHunter"
        3. Enter a stock ticker: "AAPL"
        4. Use mock data:
           - PE Ratio: 12
        5. Click **Run Analysis**
        
        **Result:**
        ```
        Signal: 🟢 BULLISH
        Confidence: 80%
        Reasoning: PE ratio 12.0 is bullish
        ```
        
        ---
        
        #### Step 5: Understand the Result
        
        **Signal = BULLISH** means the agent thinks you should **buy** this stock.
        
        **Confidence = 80%** means the agent is **fairly confident** (scale: 0% = no confidence, 100% = very confident).
        
        **Reasoning** explains **why** the agent made this decision.
        
        ---
        
        ### What Each Signal Means
        
        | Signal | Meaning | Action |
        |--------|---------|--------|
        | 🟢 **BULLISH** | Positive outlook | Consider buying |
        | 🔴 **BEARISH** | Negative outlook | Consider selling or avoiding |
        | 🟡 **NEUTRAL** | No strong opinion | Hold or wait for better opportunity |
        
        ⚠️ **Important:** Signals are suggestions, not guarantees. Always do your own research!
        """)
    
    with tab2:
        st.markdown("""
        ## 📊 Workflow: Value Investing Strategy
        
        ### The Warren Buffett Approach
        
        Value investing means buying stocks that are **cheap relative to their true worth**.
        
        ---
        
        ### Step-by-Step Workflow
        
        #### Step 1: Define Your Value Criteria
        
        A value investor typically looks for:
        
        1. **Low PE Ratio** (< 15) - Stock is cheap relative to earnings
        2. **High ROE** (> 15%) - Company earns good returns
        3. **Low Debt** (< 1.0) - Company isn't over-leveraged
        4. **Good Margins** (> 12%) - Company is profitable
        
        ---
        
        #### Step 2: Create Your Value Agent
        
        **In the Create Agent tab:**
        
        **Basic Info:**
        - Agent Name: `ValueInvestor`
        - Description: "Finds undervalued quality stocks"
        - Type: **Score-Based** (accumulate points for each criterion)
        
        **Add Scoring Criteria:**
        
        | Criterion | Threshold | Points if Met |
        |-----------|-----------|---------------|
        | PE Ratio < 15 | < 15 | +2 points |
        | ROE > 15% | > 15 | +2 points |
        | Debt < 1.0 | < 1.0 | +1 point |
        | Profit Margin > 12% | > 12 | +1 point |
        
        **Set Thresholds:**
        - Bullish if score ≥ **5 points**
        - Bearish if score ≤ **1 point**
        
        ---
        
        #### Step 3: Test with Example Companies
        
        **Company A (Strong Value):**
        ```
        PE Ratio: 12
        ROE: 18%
        Debt-to-Equity: 0.5
        Profit Margin: 15%
        ```
        
        **Scoring:**
        - PE < 15 → +2 points ✅
        - ROE > 15% → +2 points ✅
        - Debt < 1.0 → +1 point ✅
        - Margin > 12% → +1 point ✅
        - **Total: 6 points**
        
        **Result:** 🟢 BULLISH (Strong value!)
        
        **Why?** Meets all criteria - cheap, profitable, safe, high returns
        
        ---
        
        **Company B (Value Trap):**
        ```
        PE Ratio: 8 (very low!)
        ROE: 5% (poor returns)
        Debt-to-Equity: 2.5 (high debt)
        Profit Margin: 3% (low margins)
        ```
        
        **Scoring:**
        - PE < 15 → +2 points ✅
        - ROE > 15% → 0 points ❌
        - Debt < 1.0 → 0 points ❌
        - Margin > 12% → 0 points ❌
        - **Total: 2 points**
        
        **Result:** 🟡 NEUTRAL or 🔴 BEARISH
        
        **Why?** Cheap PE but **terrible fundamentals** - this is called a "value trap"!
        
        ---
        
        **Company C (Fairly Valued):**
        ```
        PE Ratio: 18 (not cheap)
        ROE: 16%
        Debt-to-Equity: 0.8
        Profit Margin: 14%
        ```
        
        **Scoring:**
        - PE < 15 → 0 points ❌
        - ROE > 15% → +2 points ✅
        - Debt < 1.0 → +1 point ✅
        - Margin > 12% → +1 point ✅
        - **Total: 4 points**
        
        **Result:** 🟡 NEUTRAL
        
        **Why?** Good company but **not undervalued** - wait for better price
        
        ---
        
        #### Step 4: What You Learned
        
        **Key Insights:**
        
        1. **Low PE alone ≠ Good investment**
           - Company B had PE=8 but was a value trap
           - Need to check quality metrics too!
        
        2. **Multiple criteria protect you**
           - Requiring 5+ points filters for quality + value
           - Avoids cheap stocks with problems
        
        3. **Score-based is more nuanced**
           - Not just YES/NO
           - Weighs multiple factors
           - More like how analysts actually think
        
        ---
        
        ### Common Mistakes to Avoid
        
        ❌ **Mistake 1:** Only using PE ratio
        - **Problem:** Finds value traps (cheap for a reason)
        - **Solution:** Add ROE, debt, margins
        
        ❌ **Mistake 2:** Setting thresholds too strict
        - **Problem:** PE < 8, ROE > 25% → Never find anything
        - **Solution:** Use realistic thresholds based on market conditions
        
        ❌ **Mistake 3:** Ignoring debt
        - **Problem:** High debt = high risk
        - **Solution:** Always include debt-to-equity in criteria
        
        ❌ **Mistake 4:** Not testing with different scenarios
        - **Problem:** Rules might only work in specific conditions
        - **Solution:** Test with various example companies
        
        💡 **Pro Tip:** Start with proven strategies (Buffett, Lynch) and modify them for your style!
        """)
    
    with tab3:
        st.markdown("""
        ## 🚀 Workflow: Growth Investing Strategy
        
        ### The Peter Lynch Approach
        
        Growth investing means buying stocks with **strong revenue and earnings growth**.
        
        ---
        
        ### Step-by-Step Workflow
        
        #### Step 1: Define Growth Criteria
        
        A growth investor typically looks for:
        
        1. **High Revenue Growth** (> 20%) - Sales increasing rapidly
        2. **Expanding Margins** (> 15%) - Getting more profitable
        3. **Strong ROE** (> 20%) - Efficient use of capital
        4. **Reasonable Valuation** (PE < 40) - Not too expensive for growth
        
        ---
        
        #### Step 2: Create Your Growth Agent
        
        **In the Create Agent tab:**
        
        **Basic Info:**
        - Agent Name: `GrowthScout`
        - Description: "Finds high-growth companies"
        - Type: **Score-Based**
        
        **Scoring Criteria:**
        
        | Criterion | Threshold | Points |
        |-----------|-----------|--------|
        | Revenue Growth > 20% | > 20 | +3 points (most important!) |
        | Profit Margin > 15% | > 15 | +2 points |
        | ROE > 20% | > 20 | +2 points |
        | PE < 40 | < 40 | +1 point |
        
        **Thresholds:**
        - Bullish if score ≥ **6 points**
        - Bearish if score ≤ **2 points**
        
        ---
        
        #### Step 3: Test with Growth Scenarios
        
        **Company A (High-Quality Growth):**
        ```
        Revenue Growth: 35%
        Profit Margin: 22%
        ROE: 28%
        PE Ratio: 32
        ```
        
        **Score: 8 points** → 🟢 BULLISH
        
        **Why invest?** Strong growth, high margins, great returns, reasonable price
        
        ---
        
        **Company B (Unsustainable Growth):**
        ```
        Revenue Growth: 40% (impressive!)
        Profit Margin: 5% (losing money on sales!)
        ROE: 8%
        PE Ratio: 60 (very expensive!)
        ```
        
        **Score: 3 points** → 🟡 NEUTRAL
        
        **Why cautious?** Growth is there but **not profitable** - burning cash to grow
        
        ---
        
        **Company C (Overvalued Growth):**
        ```
        Revenue Growth: 15%
        Profit Margin: 18%
        ROE: 22%
        PE Ratio: 55 (very expensive!)
        ```
        
        **Score: 4 points** → 🟡 NEUTRAL
        
        **Why neutral?** Good fundamentals but **paying too much** for the growth
        
        ---
        
        #### Step 4: Interpreting Growth Signals
        
        **When agent says BULLISH on growth stock:**
        
        ✅ **What it means:**
        - Strong revenue growth AND
        - Maintaining or improving profitability AND
        - Valuation is not extreme
        
        ⚠️ **What to check next:**
        - Is growth sustainable? (not one-time event)
        - What's driving growth? (new product, market expansion, etc.)
        - Any competitive threats?
        
        ---
        
        **When agent says NEUTRAL:**
        
        **Common reasons:**
        - Growth is slowing down
        - Margins are shrinking (competition?)
        - Valuation is too high for the growth rate
        
        **Action:** Wait for better entry point or look elsewhere
        
        ---
        
        ### Key Lesson: Growth + Quality
        
        **Just growth ≠ Good investment**
        - Company B had 40% growth but terrible margins
        - Might be burning cash unsustainably
        \n        **Growth + Profitability = Quality growth**
        - Company A had growth AND margins
        - Sustainable, profitable expansion
        
        💡 **Remember:** Peter Lynch said \"Growth at a Reasonable Price\" - not growth at any price!
        """)
    
    with tab4:
        st.markdown("""
        ## ⚖️ Understanding Agent Signals
        
        ### Confidence Levels Explained
        
        Confidence shows **how sure** the agent is about its recommendation.
        
        ---
        
        #### Confidence Scale Guide
        
        | Range | Level | What It Means | How to Use It |
        |-------|-------|---------------|---------------|
        | **80-100%** | Very High | All criteria strongly met | High conviction - larger position |
        | **60-79%** | High | Most criteria met | Good signal - normal position |
        | **40-59%** | Moderate | Some criteria met | Proceed cautiously - small position |
        | **20-39%** | Low | Few criteria met | Avoid or minimal allocation |
        | **0-19%** | Very Low | Error or no criteria | Skip entirely |
        
        ---
        
        #### Real-World Examples
        
        **Example 1: High Confidence = Strong Conviction**
        ```
        Company: Tech Growth Inc.
        
        Revenue Growth: 45% ✅
        Profit Margin: 25% ✅
        ROE: 30% ✅
        PE Ratio: 28 ✅
        Debt: 0.3 ✅
        \n        Agent Signal: 🟢 BULLISH
        Confidence: 90%
        
        Interpretation:
        - ALL growth criteria strongly met
        - High quality growth at reasonable price
        - This is a STRONG BUY signal
        ```
        
        **What to do:**
        - Do deeper research on this company
        - If research confirms, consider larger position (5-10% of portfolio)
        - High confidence signals are rare - take them seriously!
        
        ---
        
        **Example 2: Low Confidence = Proceed with Caution**
        ```
        Company: Retail Corp.
        
        Revenue Growth: 18% ⚠️ (just below 20% threshold)
        Profit Margin: 14% ⚠️ (just below 15%)
        ROE: 19% ⚠️ (just below 20%)
        PE Ratio: 35 ✅
        \n        Agent Signal: 🟡 NEUTRAL
        Confidence: 45%
        \n        Interpretation:
        - Metrics are CLOSE but don't quite meet thresholds
        - Borderline case
        - Agent is unsure - you should be too
        ```
        
        **What to do:**
        - This is a **marginal opportunity**
        - If you invest, use small position (1-2%)
        - Or wait for metrics to improve
        - Low confidence = low conviction
        
        ---
        
        #### Combining Signals from Multiple Agents
        
        **Advanced Technique:** Run the same stock through different agents
        
        **Example: Analyzing "Company XYZ"**
        
        | Agent | Strategy | Signal | Confidence |
        |-------|----------|--------|------------|
        | ValueAgent | Low PE, high ROE | 🟢 Bullish | 85% |
        | GrowthAgent | Revenue growth | 🟡 Neutral | 50% |
        | QualityAgent | Margins, debt | 🟢 Bullish | 80% |
        
        **Consensus Analysis:**
        - **2 out of 3** agents are bullish
        - **Value + Quality** strong, **Growth** moderate
        - Average confidence: ~72%
        
        **Investment Decision:**
        - This is a **VALUE STOCK** (not growth)
        - Good for conservative value portfolio
        - Probably not for aggressive growth portfolio
        - Consider moderate position size (3-5%)
        
        ---
        
        ### How Professional Analysts Use Agents
        
        **Step 1: Screen Universe**
        - Run value agent on 500 stocks
        - Get 50 bullish signals
        \n        **Step 2: Filter by Confidence**
        - Keep only signals with confidence > 70%
        - Now have 20 high-quality candidates
        \n        **Step 3: Manual Research**
        - Research these 20 companies deeply
        - Read reports, understand business
        - Check management, competition, risks
        \n        **Step 4: Portfolio Construction**
        - Select best 10 after research
        - Allocate based on confidence + research
        - High confidence + good research = larger position
        \n        **Step 5: Monitor**
        - Run agents monthly to check if thesis still holds
        - Sell if agent signal changes significantly
        
        ---
        
        ### Key Takeaways
        
        1. **Agents are screening tools**, not final decisions
        2. **Confidence matters** - high confidence signals deserve more attention
        3. **Multiple agents** give you different perspectives
        4. **Always research** the companies agents recommend
        5. **Use agents to save time**, not replace thinking
        
        💡 **Best Practice:** Agent finds candidates → You do deep research → You make final decision
        """)
    
    # Educational footer
    st.markdown("---")
    st.info("""
    ### 🎓 Want to Learn More?
    
    **Try these workflows:**
    1. Create a value agent and test with 5 different mock companies
    2. Create a growth agent with different point weights
    3. Compare value vs growth signals on the same company
    4. Adjust thresholds and see how signals change
    
    **Resources:**
    - Browse example agents (Buffett, Lynch, Graham strategies)
    - Duplicate and modify them for your needs
    - Test with various scenarios to understand patterns
    
    ⚠️ **Educational Use Only:** Practice here, consult professionals before real investing!
    """)


# For testing
if __name__ == "__main__":
    import streamlit as st
    show_how_to_page()
