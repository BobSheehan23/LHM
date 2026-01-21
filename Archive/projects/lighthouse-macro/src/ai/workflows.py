"""
Lighthouse Macro — AI Workflows
Pre-built workflows for research cadence (Beacon, Beam, Chartbook, Horizon)
"""

from typing import Dict, List, Optional

from ai.router import AIRouter, TaskType
from ai.claude import ClaudeClient
from ai.openai import OpenAIClient


class ResearchWorkflow:
    """Base class for research workflows"""

    def __init__(self):
        self.router = AIRouter()
        self.claude = None
        self.openai = None

    def _get_client(self, provider: str):
        """Get appropriate AI client"""
        if provider == "anthropic":
            if self.claude is None:
                self.claude = ClaudeClient()
            return self.claude
        elif provider == "openai":
            if self.openai is None:
                self.openai = OpenAIClient()
            return self.openai
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _execute_stage(self, task: TaskType, prompt: str, **kwargs) -> str:
        """Execute a single workflow stage"""
        config = self.router.get_model_for_task(task)
        client = self._get_client(config["provider"])

        return client.complete(
            prompt=prompt,
            model=config["model"],
            temperature=config.get("temperature", 0.5),
            **kwargs,
        )


class BeaconWorkflow(ResearchWorkflow):
    """
    Sunday — The Beacon
    Long-form macro narrative (3k-4k words)
    """

    def generate(
        self, data_summary: str, recent_events: str, additional_context: str = ""
    ) -> Dict[str, str]:
        """
        Generate complete Beacon article.

        Args:
            data_summary: Summary of latest macro data
            recent_events: Recent market/economic events
            additional_context: Any additional context

        Returns:
            Dictionary with draft, fact_check, final
        """
        results = {}

        # Stage 1: Initial analysis
        analysis_prompt = f"""
        Analyze the following macro data and events for this week's Beacon article:

        DATA SUMMARY:
        {data_summary}

        RECENT EVENTS:
        {recent_events}

        {additional_context}

        Provide a structured analysis covering:
        1. Key macro developments
        2. Cross-pillar connections (Macro Dynamics, Monetary Mechanics, Market Technicals)
        3. Notable divergences or confirmations
        4. Forward-looking implications

        Be specific and data-driven.
        """

        results["analysis"] = self._execute_stage(TaskType.CHART_ANALYSIS, analysis_prompt)

        # Stage 2: Narrative draft
        draft_prompt = f"""
        Based on this analysis, write a complete Beacon article (3000-4000 words).

        ANALYSIS:
        {results['analysis']}

        Requirements:
        - Write in Bob's voice: quick humor, encouraging, precise, human
        - Integrate all three pillars (Macro Dynamics, Monetary Mechanics, Market Technicals)
        - Use specific data points and transformations
        - Include forward-looking insights
        - Avoid AI tells (em-dashes, redundancy, self-reference)
        - Structure: Opening, Macro Dynamics section, Monetary Mechanics section, Market Technicals section, Synthesis & Outlook

        Title format: "The Beacon: [Compelling Title]"
        """

        results["draft"] = self._execute_stage(TaskType.NARRATIVE_SYNTHESIS, draft_prompt)

        # Stage 3: Fact check
        fact_check_prompt = f"""
        Review this Beacon draft for factual accuracy and data consistency:

        {results['draft']}

        Check:
        - Data accuracy and sourcing
        - Logical consistency
        - Any unsupported claims
        - Transformation correctness

        Provide specific corrections needed.
        """

        results["fact_check"] = self._execute_stage(TaskType.FACT_CHECKING, fact_check_prompt)

        # Stage 4: Final polish
        polish_prompt = f"""
        Polish this Beacon draft incorporating fact-check feedback:

        DRAFT:
        {results['draft']}

        FACT CHECK FEEDBACK:
        {results['fact_check']}

        Refine for:
        - Voice consistency
        - Flow and readability
        - Precise language
        - Compelling narrative

        Maintain institutional rigor while being accessible.
        """

        results["final"] = self._execute_stage(TaskType.NARRATIVE_SYNTHESIS, polish_prompt)

        return results


class BeamWorkflow(ResearchWorkflow):
    """
    Tuesday/Thursday — The Beam
    One chart + one paragraph
    """

    def generate(self, series_id: str, chart_description: str) -> str:
        """
        Generate Beam content (chart + paragraph).

        Args:
            series_id: FRED series ID or data identifier
            chart_description: Description of what the chart shows

        Returns:
            Paragraph text
        """
        prompt = f"""
        Write a Beam paragraph for this chart:

        SERIES: {series_id}
        CHART: {chart_description}

        Requirements:
        - One paragraph (100-150 words)
        - Lead with the key insight
        - Provide context and implication
        - Bob's voice: sharp, accessible, forward-thinking
        - End with a question or forward-looking statement

        Format:
        "The Beam: [Brief Title]"
        [Paragraph]
        """

        return self._execute_stage(TaskType.QUICK_SUMMARY, prompt)


class ChartbookWorkflow(ResearchWorkflow):
    """
    Friday — The Chartbook
    50+ charts + dashboard
    """

    def generate_annotations(self, charts_metadata: List[Dict]) -> Dict[str, str]:
        """
        Generate annotations for multiple charts.

        Args:
            charts_metadata: List of dicts with series_id, title, pillar

        Returns:
            Dictionary mapping series_id to annotation
        """
        annotations = {}

        # Batch process for efficiency (use GPT for speed)
        for chart in charts_metadata:
            prompt = f"""
            Write a 1-2 sentence annotation for this Chartbook chart:

            Series: {chart['series_id']}
            Title: {chart['title']}
            Pillar: {chart['pillar']}

            Be concise and insightful. What's the key takeaway?
            """

            annotations[chart["series_id"]] = self._execute_stage(
                TaskType.QUICK_SUMMARY, prompt
            )

        return annotations


class HorizonWorkflow(ResearchWorkflow):
    """
    First Monday — The Horizon
    Forward-looking cross-asset outlook
    """

    def generate(
        self, macro_summary: str, positioning_data: str, scenario_inputs: str
    ) -> Dict[str, str]:
        """
        Generate Horizon outlook.

        Args:
            macro_summary: Current macro state
            positioning_data: Market positioning
            scenario_inputs: Scenario analysis inputs

        Returns:
            Dictionary with scenarios, outlook, recommendations
        """
        results = {}

        # Stage 1: Scenario analysis
        scenario_prompt = f"""
        Develop forward-looking scenarios for the Horizon:

        MACRO STATE:
        {macro_summary}

        POSITIONING:
        {positioning_data}

        INPUTS:
        {scenario_inputs}

        Create 2-3 scenarios (base case + alternatives) with:
        - Trigger conditions
        - Probability assessments
        - Asset implications
        - Key signposts to watch

        Be specific and falsifiable.
        """

        results["scenarios"] = self._execute_stage(TaskType.RESEARCH_IDEATION, scenario_prompt)

        # Stage 2: Cross-asset outlook
        outlook_prompt = f"""
        Based on these scenarios, write a cross-asset outlook:

        SCENARIOS:
        {results['scenarios']}

        Cover:
        - Equities
        - Rates
        - Credit
        - Commodities
        - FX
        - Crypto

        For each: directional view, key drivers, risk/reward, tactical considerations.

        Bob's voice: confident but humble, data-driven, actionable.
        """

        results["outlook"] = self._execute_stage(TaskType.NARRATIVE_SYNTHESIS, outlook_prompt)

        return results
