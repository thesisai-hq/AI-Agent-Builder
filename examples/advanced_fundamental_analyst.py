"""
Advanced Fundamental Analyst Agent
Combines quantitative analysis, RAG for SEC filings, and LLM for synthesis

This is a complete, production-ready example showing:
1. Traditional fundamental metrics analysis
2. RAG-powered SEC filing deep dive
3. LLM-powered synthesis and reasoning
4. Comprehensive scoring system
"""

from typing import Dict, Any, Tuple, List
import logging
from agent_builder import agent, get_registry
from agent_builder.llm import get_llm_provider, PromptTemplates
from agent_builder.rag import RAGEngine

logger = logging.getLogger(__name__)


# ============================================================================
# FUNDAMENTAL ANALYST AGENT
# ============================================================================


@agent("Advanced Fundamental Analyst", "Comprehensive fundamental analysis with AI")
def advanced_fundamental_analyst(ticker: str, context) -> Tuple[str, float, str]:
    """
    Multi-stage fundamental analysis:

    Stage 1: Quantitative Analysis (Traditional metrics)
    Stage 2: Qualitative Analysis (RAG on SEC filings)
    Stage 3: AI Synthesis (LLM combines all insights)
    Stage 4: Final Recommendation

    Returns: (signal, confidence, reasoning)
    """

    print(f"\n{'='*70}")
    print(f"ADVANCED FUNDAMENTAL ANALYSIS: {ticker}")
    print(f"{'='*70}\n")

    # ========================================================================
    # STAGE 1: QUANTITATIVE ANALYSIS
    # ========================================================================

    print("📊 Stage 1: Quantitative Analysis...")
    quant_result = analyze_quantitative_metrics(ticker, context)

    print(f"   Score: {quant_result['score']:.1f}/10")
    print(f"   Signal: {quant_result['signal']}")
    print(f"   Key metrics: {', '.join(quant_result['key_points'][:3])}")

    # ========================================================================
    # STAGE 2: QUALITATIVE ANALYSIS (RAG + LLM)
    # ========================================================================

    print("\n📄 Stage 2: SEC Filing Analysis (RAG + LLM)...")
    qual_result = analyze_sec_filings_with_rag(ticker, context)

    print(f"   Filings analyzed: {qual_result['filing_count']}")
    print(f"   Key insights found: {qual_result['insight_count']}")
    if qual_result.get("themes"):
        print(f"   LLM-extracted themes: {', '.join(qual_result['themes'][:3])}")
    if qual_result.get("reasoning"):
        print(
            f"   Qualitative signal: {qual_result['signal']} - {qual_result['reasoning'][:80]}..."
        )

    # ========================================================================
    # STAGE 3: AI SYNTHESIS (LLM)
    # ========================================================================

    print("\n🤖 Stage 3: AI Synthesis...")
    synthesis = synthesize_with_llm(ticker, quant_result, qual_result, context)

    if synthesis["success"]:
        print(f"   AI Signal: {synthesis['signal']}")
        print(f"   AI Confidence: {synthesis['confidence']:.0%}")
        print(f"   Reasoning: {synthesis['reasoning'][:100]}...")
    else:
        print(f"   AI synthesis unavailable: {synthesis['error']}")

    # ========================================================================
    # STAGE 4: FINAL RECOMMENDATION
    # ========================================================================

    print("\n🎯 Stage 4: Final Recommendation...")
    final_signal, final_confidence, final_reasoning = calculate_final_recommendation(
        quant_result, qual_result, synthesis
    )

    print(f"\n{'='*70}")
    print(f"FINAL RECOMMENDATION: {final_signal.upper()}")
    print(f"Confidence: {final_confidence:.0%}")
    print(f"{'='*70}\n")

    return final_signal, final_confidence, final_reasoning


# ============================================================================
# STAGE 1: QUANTITATIVE ANALYSIS
# ============================================================================


def analyze_quantitative_metrics(ticker: str, context) -> Dict[str, Any]:
    """
    Analyze traditional fundamental metrics

    Returns comprehensive scoring with detailed breakdown
    """
    fundamentals = context.get_fundamentals()

    if not fundamentals:
        return {
            "score": 5.0,
            "signal": "neutral",
            "key_points": ["No fundamental data available"],
            "detailed_scores": {},
            "strengths": [],
            "weaknesses": [],
        }

    # Extract metrics
    pe_ratio = fundamentals.get("pe_ratio", 25)
    roe = fundamentals.get("roe", 10)
    profit_margin = fundamentals.get("profit_margin", 10)
    revenue_growth = fundamentals.get("revenue_growth", 5)
    debt_to_equity = fundamentals.get("debt_to_equity", 1.0)
    dividend_yield = fundamentals.get("dividend_yield", 0)
    current_ratio = fundamentals.get("current_ratio", 1.0)

    # Scoring system (0-10 for each metric)
    scores = {}
    strengths = []
    weaknesses = []

    # 1. Valuation Score (P/E Ratio)
    if pe_ratio < 15:
        scores["valuation"] = 10
        strengths.append(f"Excellent valuation (P/E: {pe_ratio:.1f})")
    elif pe_ratio < 20:
        scores["valuation"] = 8
        strengths.append(f"Good valuation (P/E: {pe_ratio:.1f})")
    elif pe_ratio < 25:
        scores["valuation"] = 6
    elif pe_ratio < 35:
        scores["valuation"] = 4
        weaknesses.append(f"High P/E ratio: {pe_ratio:.1f}")
    else:
        scores["valuation"] = 2
        weaknesses.append(f"Very high P/E ratio: {pe_ratio:.1f}")

    # 2. Profitability Score (ROE + Margins)
    profitability_score = 0
    if roe > 20:
        profitability_score += 5
        strengths.append(f"Excellent ROE: {roe:.1f}%")
    elif roe > 15:
        profitability_score += 4
    elif roe > 10:
        profitability_score += 3
    else:
        weaknesses.append(f"Low ROE: {roe:.1f}%")
        profitability_score += 1

    if profit_margin > 20:
        profitability_score += 5
        strengths.append(f"High profit margin: {profit_margin:.1f}%")
    elif profit_margin > 15:
        profitability_score += 4
    elif profit_margin > 10:
        profitability_score += 3
    else:
        weaknesses.append(f"Low profit margin: {profit_margin:.1f}%")
        profitability_score += 1

    scores["profitability"] = profitability_score

    # 3. Growth Score
    if revenue_growth > 20:
        scores["growth"] = 10
        strengths.append(f"Exceptional growth: {revenue_growth:.1f}%")
    elif revenue_growth > 15:
        scores["growth"] = 8
        strengths.append(f"Strong growth: {revenue_growth:.1f}%")
    elif revenue_growth > 10:
        scores["growth"] = 7
    elif revenue_growth > 5:
        scores["growth"] = 5
    elif revenue_growth > 0:
        scores["growth"] = 3
    else:
        scores["growth"] = 1
        weaknesses.append(f"Negative growth: {revenue_growth:.1f}%")

    # 4. Financial Health Score (Debt + Liquidity)
    financial_health = 0
    if debt_to_equity < 0.5:
        financial_health += 5
        strengths.append(f"Low debt: {debt_to_equity:.2f}")
    elif debt_to_equity < 1.0:
        financial_health += 4
    elif debt_to_equity < 1.5:
        financial_health += 3
    else:
        financial_health += 1
        weaknesses.append(f"High debt: {debt_to_equity:.2f}")

    if current_ratio > 2.0:
        financial_health += 5
        strengths.append(f"Strong liquidity: {current_ratio:.2f}")
    elif current_ratio > 1.5:
        financial_health += 4
    elif current_ratio > 1.0:
        financial_health += 3
    else:
        financial_health += 1
        weaknesses.append(f"Low liquidity: {current_ratio:.2f}")

    scores["financial_health"] = financial_health

    # 5. Income Score (Dividend)
    if dividend_yield > 3:
        scores["income"] = 8
        strengths.append(f"Attractive dividend: {dividend_yield:.1f}%")
    elif dividend_yield > 2:
        scores["income"] = 6
    elif dividend_yield > 1:
        scores["income"] = 4
    else:
        scores["income"] = 2

    # Calculate overall score (weighted average)
    weights = {
        "valuation": 0.25,
        "profitability": 0.30,
        "growth": 0.25,
        "financial_health": 0.15,
        "income": 0.05,
    }

    overall_score = sum(scores[k] * weights[k] for k in scores)

    # Determine signal
    if overall_score >= 7.5:
        signal = "bullish"
    elif overall_score >= 5.5:
        signal = "neutral"
    else:
        signal = "bearish"

    # Create key points summary
    key_points = []
    key_points.extend(strengths[:3])  # Top 3 strengths
    if weaknesses:
        key_points.extend(weaknesses[:2])  # Top 2 weaknesses

    return {
        "score": overall_score,
        "signal": signal,
        "detailed_scores": scores,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "key_points": key_points,
        "metrics": {
            "pe_ratio": pe_ratio,
            "roe": roe,
            "profit_margin": profit_margin,
            "revenue_growth": revenue_growth,
            "debt_to_equity": debt_to_equity,
        },
    }


# ============================================================================
# STAGE 2: QUALITATIVE ANALYSIS (RAG)
# ============================================================================


def analyze_sec_filings_with_rag(ticker: str, context) -> Dict[str, Any]:
    """
    Use RAG + LLM to extract insights from SEC filings

    Process:
    1. RAG: Search SEC filings for relevant excerpts
    2. LLM: Analyze excerpts to extract themes and determine signal

    This combines the precision of RAG with the intelligence of LLM
    """

    try:
        # Initialize RAG engine
        rag = RAGEngine(
            db=context.db,
            embedding="sentence-transformers",
            vectorstore="faiss",  # Fast and working
        )

        # Index SEC filings
        rag.index_sec_filings(ticker)

        # Search for multiple aspects
        search_queries = [
            "revenue growth strategy and business expansion plans",
            "competitive advantages and market position",
            "key risks and challenges facing the business",
            "profitability trends and margin improvements",
        ]

        all_insights = []
        filing_count = 0

        for query in search_queries:
            results = rag.search_sec_filings(query=query, ticker=ticker, top_k=2)

            for result in results:
                if result["text"]:
                    all_insights.append(
                        {
                            "query": query,
                            "text": result["text"],
                            "similarity": result["similarity"],
                            "metadata": result["metadata"],
                        }
                    )

                    if result["metadata"].get("filing_type"):
                        filing_count += 1

        if not all_insights:
            return {
                "success": False,
                "filing_count": 0,
                "insight_count": 0,
                "insights": [],
                "themes": [],
                "signal": "neutral",
                "error": "No SEC filing data found",
            }

        # Use LLM to extract themes and determine signal
        llm_analysis = analyze_sec_insights_with_llm(ticker, all_insights)

        return {
            "success": llm_analysis["success"],
            "filing_count": min(filing_count, 5),  # Count unique filings
            "insight_count": len(all_insights),
            "insights": [i["text"] for i in all_insights],
            "themes": llm_analysis.get("themes", []),
            "signal": llm_analysis.get("signal", "neutral"),
            "confidence": llm_analysis.get("confidence", 0.5),
            "reasoning": llm_analysis.get("reasoning", ""),
            "raw_results": all_insights,
        }

    except Exception as e:
        logger.error(f"RAG analysis failed: {e}")
        return {
            "success": False,
            "filing_count": 0,
            "insight_count": 0,
            "insights": [],
            "themes": [],
            "signal": "neutral",
            "error": str(e),
        }


def analyze_sec_insights_with_llm(ticker: str, insights: List[Dict]) -> Dict[str, Any]:
    """
    Use LLM to analyze SEC filing excerpts

    This is much better than keyword matching because LLM can:
    - Understand context and nuance
    - Identify subtle themes
    - Connect related concepts
    - Provide sophisticated qualitative assessment
    """

    try:
        llm = get_llm_provider("ollama")

        if not llm or not llm.is_available():
            # Fallback to simple keyword-based analysis
            return fallback_theme_extraction(insights)

        # Build prompt with SEC excerpts
        excerpts_text = ""
        for i, insight in enumerate(
            insights[:6], 1
        ):  # Limit to 6 excerpts to fit in context
            query_type = insight["query"].split()[
                0
            ]  # e.g., "revenue", "competitive", "key"
            excerpts_text += (
                f"\n[Excerpt {i} - {query_type}]\n{insight['text'][:400]}...\n"
            )

        prompt = f"""Analyze these SEC filing excerpts for {ticker} and extract key investment themes.

{excerpts_text}

Based on these excerpts, provide:

1. KEY THEMES: List 3-5 major themes you identify (e.g., "Accelerating cloud growth", "Margin pressure from competition", "Strong R&D investment")

2. QUALITATIVE SIGNAL: Based on the overall tone and content, determine if this is:
   - BULLISH (positive outlook, strong positioning, growing opportunities)
   - BEARISH (significant risks, deteriorating position, headwinds)
   - NEUTRAL (mixed signals, stable but not exciting)

3. CONFIDENCE: Your confidence in this assessment (0.0-1.0)

4. REASONING: 2-3 sentences explaining your assessment

Focus on:
- Management's tone and outlook
- Competitive positioning
- Growth opportunities vs. risks
- Financial health indicators

Format your response as:
THEMES: [theme1], [theme2], [theme3]
SIGNAL: [BULLISH/BEARISH/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASONING: [Your explanation]"""

        # Get LLM analysis
        response = llm.generate(
            prompt=prompt,
            system_prompt="You are an expert at analyzing SEC filings for investment insights. Focus on what matters to investors.",
            temperature=0.3,
            max_tokens=500,
        )

        # Parse response
        parsed = parse_llm_sec_analysis(response.content)

        return {
            "success": True,
            "themes": parsed["themes"],
            "signal": parsed["signal"],
            "confidence": parsed["confidence"],
            "reasoning": parsed["reasoning"],
        }

    except Exception as e:
        logger.error(f"LLM SEC analysis failed: {e}")
        # Fallback to simple analysis
        return fallback_theme_extraction(insights)


def parse_llm_sec_analysis(response_text: str) -> Dict[str, Any]:
    """Parse LLM response for SEC analysis"""

    result = {"themes": [], "signal": "neutral", "confidence": 0.5, "reasoning": ""}

    lines = response_text.strip().split("\n")

    for line in lines:
        line = line.strip()

        if line.startswith("THEMES:"):
            # Extract themes (comma-separated)
            themes_text = line.split(":", 1)[1].strip()
            result["themes"] = [t.strip() for t in themes_text.split(",") if t.strip()]

        elif line.startswith("SIGNAL:"):
            signal = line.split(":", 1)[1].strip().lower()
            if signal in ["bullish", "bearish", "neutral"]:
                result["signal"] = signal

        elif line.startswith("CONFIDENCE:"):
            try:
                conf = float(line.split(":", 1)[1].strip())
                result["confidence"] = max(0.0, min(1.0, conf))
            except:
                pass

        elif line.startswith("REASONING:"):
            result["reasoning"] = line.split(":", 1)[1].strip()

    # If no themes extracted, use reasoning
    if not result["themes"] and result["reasoning"]:
        result["themes"] = ["See reasoning for details"]

    return result


def fallback_theme_extraction(insights: List[Dict]) -> Dict[str, Any]:
    """
    Fallback theme extraction when LLM is not available
    Simple keyword-based approach
    """

    themes = []
    positive_count = 0
    negative_count = 0

    # Keywords for analysis
    positive_keywords = [
        "growth",
        "expansion",
        "strong",
        "increased",
        "improved",
        "competitive advantage",
        "innovation",
        "market leader",
    ]
    negative_keywords = [
        "risk",
        "challenge",
        "decline",
        "decreased",
        "competition",
        "uncertainty",
        "headwind",
        "pressure",
    ]

    for insight in insights:
        text_lower = insight["text"].lower()

        if any(kw in text_lower for kw in positive_keywords):
            positive_count += 1
        if any(kw in text_lower for kw in negative_keywords):
            negative_count += 1

    # Determine themes
    if positive_count > negative_count * 1.5:
        themes = ["Strong growth indicators", "Positive management outlook"]
        signal = "bullish"
        confidence = 0.6
    elif negative_count > positive_count * 1.5:
        themes = ["Notable risks and challenges", "Headwinds mentioned"]
        signal = "bearish"
        confidence = 0.6
    else:
        themes = ["Balanced outlook", "Mixed signals"]
        signal = "neutral"
        confidence = 0.5

    return {
        "success": True,
        "themes": themes,
        "signal": signal,
        "confidence": confidence,
        "reasoning": "Simple keyword-based analysis (LLM unavailable)",
    }


# ============================================================================
# STAGE 3: AI SYNTHESIS (LLM)
# ============================================================================


def synthesize_with_llm(
    ticker: str, quant_result: Dict, qual_result: Dict, context
) -> Dict[str, Any]:
    """
    Use LLM to synthesize quantitative and qualitative analysis

    This is where AI adds real value - connecting dots humans might miss
    """

    try:
        llm = get_llm_provider("ollama")

        if not llm or not llm.is_available():
            return {
                "success": False,
                "error": "LLM not available",
                "signal": "neutral",
                "confidence": 0.5,
                "reasoning": "LLM synthesis unavailable",
            }

        # Build comprehensive prompt
        prompt = f"""You are a senior equity analyst. Provide a comprehensive investment recommendation for {ticker}.

QUANTITATIVE ANALYSIS:
Overall Score: {quant_result['score']:.1f}/10
Signal: {quant_result['signal']}

Detailed Scores:
- Valuation: {quant_result['detailed_scores'].get('valuation', 0):.1f}/10
- Profitability: {quant_result['detailed_scores'].get('profitability', 0):.1f}/10
- Growth: {quant_result['detailed_scores'].get('growth', 0):.1f}/10
- Financial Health: {quant_result['detailed_scores'].get('financial_health', 0):.1f}/10

Key Metrics:
- P/E Ratio: {quant_result['metrics'].get('pe_ratio', 0):.1f}
- ROE: {quant_result['metrics'].get('roe', 0):.1f}%
- Revenue Growth: {quant_result['metrics'].get('revenue_growth', 0):.1f}%
- Debt/Equity: {quant_result['metrics'].get('debt_to_equity', 0):.2f}

Strengths:
{chr(10).join('- ' + s for s in quant_result['strengths'][:5])}

Weaknesses:
{chr(10).join('- ' + w for w in quant_result['weaknesses'][:5])}

QUALITATIVE ANALYSIS (from SEC filings):
Themes: {', '.join(qual_result.get('themes', []))}

Key Insights:
{chr(10).join('- ' + insight[:150] + '...' for insight in qual_result.get('insights', [])[:3])}

TASK:
Synthesize the quantitative and qualitative data to provide:
1. Overall investment signal (BULLISH/BEARISH/NEUTRAL)
2. Confidence level (0.0-1.0)
3. 2-3 sentence reasoning explaining your recommendation

Focus on:
- How qualitative factors reinforce or contradict quantitative metrics
- Any red flags or strong positives
- Risk/reward balance

Format:
SIGNAL: [BULLISH/BEARISH/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASONING: [Your concise analysis]"""

        # Get LLM response
        response = llm.generate(
            prompt=prompt,
            system_prompt=PromptTemplates.ANALYST_SYSTEM,
            temperature=0.3,  # Lower for consistency
            max_tokens=600,
        )

        # Parse response
        parsed = PromptTemplates.parse_llm_response(response.content)

        return {
            "success": True,
            "signal": parsed["signal"],
            "confidence": parsed["confidence"],
            "reasoning": parsed["reasoning"],
            "raw_response": response.content,
        }

    except Exception as e:
        logger.error(f"LLM synthesis failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "signal": "neutral",
            "confidence": 0.5,
            "reasoning": f"LLM synthesis failed: {str(e)}",
        }


# ============================================================================
# STAGE 4: FINAL RECOMMENDATION
# ============================================================================


def calculate_final_recommendation(
    quant_result: Dict, qual_result: Dict, synthesis: Dict
) -> Tuple[str, float, str]:
    """
    Combine all analysis stages into final recommendation

    Weighting:
    - Quantitative: 40%
    - Qualitative (RAG+LLM): 30%
    - AI Synthesis: 30%
    """

    # Map signals to scores
    signal_to_score = {"bullish": 1.0, "neutral": 0.5, "bearish": 0.0}

    # Get scores
    quant_score = signal_to_score.get(quant_result["signal"], 0.5)
    qual_score = signal_to_score.get(qual_result["signal"], 0.5)
    ai_score = (
        signal_to_score.get(synthesis["signal"], 0.5) if synthesis["success"] else 0.5
    )

    # Calculate weighted average
    if synthesis["success"]:
        weights = {"quant": 0.40, "qual": 0.30, "ai": 0.30}
        final_score = (
            quant_score * weights["quant"]
            + qual_score * weights["qual"]
            + ai_score * weights["ai"]
        )

        # Use average of synthesis confidence and qualitative confidence
        qual_conf = qual_result.get("confidence", 0.6)
        confidence_base = (synthesis["confidence"] + qual_conf) / 2
    else:
        # If no AI synthesis, reweight
        weights = {"quant": 0.60, "qual": 0.40}
        final_score = quant_score * weights["quant"] + qual_score * weights["qual"]
        confidence_base = qual_result.get("confidence", 0.6)

    # Determine final signal
    if final_score >= 0.65:
        final_signal = "bullish"
    elif final_score <= 0.35:
        final_signal = "bearish"
    else:
        final_signal = "neutral"

    # Calculate confidence
    # Higher when all stages agree
    stage_signals = [quant_result["signal"], qual_result["signal"]]
    if synthesis["success"]:
        stage_signals.append(synthesis["signal"])

    agreement = len([s for s in stage_signals if s == final_signal]) / len(
        stage_signals
    )
    final_confidence = confidence_base * agreement

    # Build reasoning
    reasoning_parts = []

    # Add quantitative summary
    reasoning_parts.append(
        f"Quantitative: {quant_result['signal']} "
        f"(score: {quant_result['score']:.1f}/10)"
    )

    # Add key strengths/weaknesses
    if quant_result["strengths"]:
        reasoning_parts.append(f"Strengths: {quant_result['strengths'][0]}")
    if quant_result["weaknesses"]:
        reasoning_parts.append(f"Concerns: {quant_result['weaknesses'][0]}")

    # Add qualitative insights (now with LLM-extracted themes)
    if qual_result.get("themes") and qual_result["themes"]:
        themes_str = ", ".join(qual_result["themes"][:2])  # Top 2 themes
        reasoning_parts.append(f"SEC Themes: {themes_str}")

    if qual_result.get("reasoning"):
        reasoning_parts.append(f"SEC Signal: {qual_result['reasoning'][:80]}...")

    # Add AI synthesis if available
    if synthesis["success"]:
        reasoning_parts.append(f"AI View: {synthesis['reasoning'][:100]}...")

    final_reasoning = " | ".join(reasoning_parts)

    return final_signal, round(final_confidence, 2), final_reasoning


# ============================================================================
# HELPER: DETAILED REPORT GENERATOR
# ============================================================================


def generate_detailed_report(ticker: str, context) -> str:
    """
    Generate a detailed analysis report

    Usage:
        report = generate_detailed_report("AAPL", context)
        print(report)
    """

    quant_result = analyze_quantitative_metrics(ticker, context)
    qual_result = analyze_sec_filings_with_rag(ticker, context)
    synthesis = synthesize_with_llm(ticker, quant_result, qual_result, context)
    final_signal, final_confidence, final_reasoning = calculate_final_recommendation(
        quant_result, qual_result, synthesis
    )

    report = f"""
{'='*70}
FUNDAMENTAL ANALYSIS REPORT: {ticker}
{'='*70}

EXECUTIVE SUMMARY
-----------------
Final Recommendation: {final_signal.upper()}
Confidence Level: {final_confidence:.0%}

{final_reasoning}

QUANTITATIVE ANALYSIS
---------------------
Overall Score: {quant_result['score']:.1f}/10

Detailed Breakdown:
  • Valuation: {quant_result['detailed_scores'].get('valuation', 0):.1f}/10
  • Profitability: {quant_result['detailed_scores'].get('profitability', 0):.1f}/10
  • Growth: {quant_result['detailed_scores'].get('growth', 0):.1f}/10
  • Financial Health: {quant_result['detailed_scores'].get('financial_health', 0):.1f}/10
  • Income: {quant_result['detailed_scores'].get('income', 0):.1f}/10

Key Strengths:
{chr(10).join('  ✓ ' + s for s in quant_result['strengths'])}

Key Weaknesses:
{chr(10).join('  ✗ ' + w for w in quant_result['weaknesses'])}

QUALITATIVE ANALYSIS (SEC Filings with RAG + LLM)
---------------------------------------------------
Filings Analyzed: {qual_result['filing_count']}

LLM-Extracted Themes:
{chr(10).join('  • ' + theme for theme in qual_result.get('themes', []))}

Qualitative Signal: {qual_result['signal'].upper()}
Confidence: {qual_result.get('confidence', 0.5):.0%}

LLM Reasoning:
  {qual_result.get('reasoning', 'Not available')}

Sample Insights from RAG:
{chr(10).join('  • ' + insight[:200] + '...' for insight in qual_result.get('insights', [])[:2])}

AI SYNTHESIS
------------
{synthesis.get('reasoning', 'Not available') if synthesis['success'] else 'LLM not available'}

{'='*70}
END OF REPORT
{'='*70}
"""

    return report


# ============================================================================
# REGISTRATION
# ============================================================================


def register_advanced_fundamental_analyst():
    """Register the advanced fundamental analyst"""
    registry = get_registry()
    registry.register(
        advanced_fundamental_analyst.agent,
        weight=1.5,  # High weight - comprehensive analysis
        tags=["fundamental", "llm", "rag", "advanced"],
        enabled=True,
    )
    print("✅ Registered: Advanced Fundamental Analyst")


# ============================================================================
# STANDALONE TESTING
# ============================================================================

if __name__ == "__main__":
    """
    Test the advanced fundamental analyst
    """
    from agent_builder.core.config import Config
    from agent_builder.core.database import DatabasePool, Database
    from agent_builder.agents.context import AgentContext

    print("\n" + "=" * 70)
    print("TESTING ADVANCED FUNDAMENTAL ANALYST")
    print("=" * 70 + "\n")

    # Setup
    config = Config.from_env()
    pool = DatabasePool(config.database)
    db = Database(pool)

    # Test tickers
    test_tickers = ["AAPL", "TSLA", "MSFT"]

    for ticker in test_tickers:
        print(f"\n{'#'*70}")
        print(f"# Testing: {ticker}")
        print(f"{'#'*70}\n")

        context = AgentContext(ticker, db)

        try:
            # Run analysis
            signal, confidence, reasoning = advanced_fundamental_analyst(
                ticker, context
            )

            # Print summary
            print(f"\n{'='*70}")
            print(f"SUMMARY FOR {ticker}")
            print(f"{'='*70}")
            print(f"Signal: {signal.upper()}")
            print(f"Confidence: {confidence:.0%}")
            print(f"Reasoning: {reasoning}")
            print(f"{'='*70}\n")

            # Generate detailed report
            print("\nGenerating detailed report...")
            report = generate_detailed_report(ticker, context)
            print(report)

        except Exception as e:
            print(f"❌ Error analyzing {ticker}: {e}")
            import traceback

            traceback.print_exc()

        print("\n" + "=" * 70 + "\n")

    pool.close()

    print("\n✅ Testing complete!\n")
