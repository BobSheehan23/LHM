"""
Lighthouse Macro — Hybrid Workflow Example
Shows how to combine API-based models with app-based models
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai import ClaudeClient, OpenAIClient, GeminiClient
from ai.app_workflows import AppWorkflowHelper, perplexity_research


def example_1_fully_automated():
    """
    Example using only API-based models (Claude, GPT, Gemini).
    Fully automated, no manual steps.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Fully Automated (API Models Only)")
    print("="*60)

    # Step 1: Extract data with GPT (fast)
    gpt = OpenAIClient()
    data_summary = gpt.complete(
        "Summarize key economic data points from this week: "
        "GDP +3.2%, CPI +3.1%, Unemployment 3.7%, 10Y yield 4.5%"
    )
    print("\n1. GPT Data Summary:")
    print(data_summary)

    # Step 2: Analyze with Claude (deep reasoning)
    claude = ClaudeClient()
    analysis = claude.complete(
        f"Analyze these economic indicators and provide macro insights:\n\n{data_summary}"
    )
    print("\n2. Claude Analysis:")
    print(analysis[:300] + "...")

    print("\n✓ Fully automated workflow complete!")


def example_2_hybrid_with_perplexity_app():
    """
    Example combining API models with Perplexity app.
    Semi-automated: system generates prompts, you use app, system continues.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Hybrid (API + Perplexity App)")
    print("="*60)

    # Step 1: Use Perplexity app for current research
    print("\n1. Researching with Perplexity app...")
    perplexity_response = perplexity_research(
        query="Latest Federal Reserve policy changes and FOMC meeting outcomes",
        context="Focus on 2025 rate decisions",
        focus="Impact on asset markets"
    )
    # This will:
    # - Generate optimized prompt
    # - Copy to clipboard
    # - Wait for you to paste response

    # Step 2: Analyze with Claude (automated)
    print("\n2. Analyzing with Claude...")
    claude = ClaudeClient()
    analysis = claude.complete(
        f"Analyze this Fed policy research:\n\n{perplexity_response}"
    )
    print(analysis[:300] + "...")

    # Step 3: Fact-check with GPT (automated)
    print("\n3. Fact-checking with GPT...")
    gpt = OpenAIClient()
    verified = gpt.complete(
        f"Extract and verify key facts from this analysis:\n\n{analysis}",
        temperature=0.1
    )
    print(verified[:200] + "...")

    print("\n✓ Hybrid workflow complete!")


def example_3_multi_app_workflow():
    """
    Example using multiple apps in sequence.
    Good when you need both Perplexity research AND Grok sentiment.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Multi-App Workflow")
    print("="*60)

    helper = AppWorkflowHelper()

    # Step 1: Perplexity research
    print("\n1. Perplexity Research...")
    perplexity_prompt = helper.prompt_and_copy(
        "perplexity",
        query="Latest inflation trends and Fed response",
        focus="Core PCE and policy implications"
    )

    print("Waiting for Perplexity response...")
    perplexity_response = helper.get_response()

    # Step 2: Grok sentiment
    print("\n2. Grok Sentiment...")
    grok_prompt = helper.prompt_and_copy(
        "grok",
        query="What is market sentiment on X regarding Fed policy and inflation?"
    )

    print("Waiting for Grok response...")
    grok_response = helper.get_response()

    # Step 3: Synthesize with Claude
    print("\n3. Synthesizing with Claude...")
    claude = ClaudeClient()
    synthesis = claude.complete(
        f"""Synthesize these inputs into a coherent macro brief:

RESEARCH (Perplexity):
{perplexity_response}

SENTIMENT (Grok):
{grok_response}

Write a brief that integrates data and sentiment."""
    )

    print("\nFinal Synthesis:")
    print(synthesis[:400] + "...")

    print("\n✓ Multi-app workflow complete!")


def example_4_chart_analysis_pipeline():
    """
    Example: Chart analysis → Research → Narrative
    Uses Gemini API + Perplexity app + Claude API
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Chart Analysis Pipeline")
    print("="*60)

    # Step 1: Analyze chart with Gemini (automated)
    print("\n1. Analyzing chart with Gemini...")
    gemini = GeminiClient()

    # Assuming you have a chart file
    chart_path = "charts/yield_curve.png"

    try:
        chart_insights = gemini.analyze_chart(
            chart_path,
            "Analyze this yield curve chart. Identify key patterns, "
            "inversions, and what they signal about economic conditions."
        )
        print(chart_insights[:300] + "...")
    except Exception as e:
        print(f"Chart analysis skipped (no chart file): {e}")
        chart_insights = "Yield curve showing inversion at 2Y-10Y spread"

    # Step 2: Research context with Perplexity app
    print("\n2. Researching context with Perplexity...")
    helper = AppWorkflowHelper()
    context_response = helper.workflow(
        "perplexity",
        query="Yield curve inversions and recession predictions 2025",
        context=f"Chart shows: {chart_insights[:200]}"
    )

    # Step 3: Write analysis with Claude (automated)
    print("\n3. Writing analysis with Claude...")
    claude = ClaudeClient()
    article = claude.complete(
        f"""Write a Beam-style analysis (150 words) combining:

CHART ANALYSIS:
{chart_insights}

RESEARCH CONTEXT:
{context_response}

Write in Bob's voice: sharp, accessible, forward-thinking."""
    )

    print("\nFinal Article:")
    print(article)

    print("\n✓ Chart analysis pipeline complete!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("LIGHTHOUSE MACRO — HYBRID WORKFLOW EXAMPLES")
    print("="*60)

    print("\nAvailable examples:")
    print("1. Fully automated (API models only)")
    print("2. Hybrid (API + Perplexity app)")
    print("3. Multi-app workflow (Perplexity + Grok apps)")
    print("4. Chart analysis pipeline (Gemini + Perplexity + Claude)")

    choice = input("\nChoose example (1-4) or 'all': ")

    if choice == "1":
        example_1_fully_automated()
    elif choice == "2":
        example_2_hybrid_with_perplexity_app()
    elif choice == "3":
        example_3_multi_app_workflow()
    elif choice == "4":
        example_4_chart_analysis_pipeline()
    elif choice.lower() == "all":
        example_1_fully_automated()
        input("\nPress Enter to continue to Example 2...")
        example_2_hybrid_with_perplexity_app()
        input("\nPress Enter to continue to Example 3...")
        example_3_multi_app_workflow()
        input("\nPress Enter to continue to Example 4...")
        example_4_chart_analysis_pipeline()
    else:
        print("Invalid choice. Run script again with 1-4 or 'all'")

    print("\n" + "="*60)
    print("EXAMPLES COMPLETE")
    print("="*60)
