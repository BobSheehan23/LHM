"""
Lighthouse Macro — App-Based Workflow Helpers
For AI models you access via apps (not API)
"""

import pyperclip
from typing import Optional


class AppWorkflowHelper:
    """
    Helper for working with AI models via apps instead of APIs.
    Generates optimized prompts and manages copy/paste workflows.
    """

    def __init__(self):
        self.prompt_templates = {
            "perplexity": self._perplexity_template,
            "grok": self._grok_template,
        }

    def _perplexity_template(self, query: str, context: str = "", focus: str = "") -> str:
        """Generate optimized Perplexity prompt"""
        prompt = f"{query}"

        if context:
            prompt += f"\n\nContext: {context}"

        if focus:
            prompt += f"\n\nFocus specifically on: {focus}"

        prompt += "\n\nProvide cited sources and focus on recent developments."

        return prompt

    def _grok_template(self, query: str, timeframe: str = "today") -> str:
        """Generate optimized Grok prompt"""
        prompt = f"{query}"

        if timeframe:
            prompt += f"\n\nTimeframe: {timeframe}"

        prompt += "\n\nFocus on X/Twitter discussions and real-time sentiment."

        return prompt

    def generate_prompt(
        self, app: str, query: str, context: str = "", focus: str = ""
    ) -> str:
        """
        Generate optimized prompt for specific app.

        Args:
            app: App name (perplexity, grok)
            query: Main query
            context: Additional context
            focus: Specific focus area

        Returns:
            Formatted prompt
        """
        if app not in self.prompt_templates:
            raise ValueError(f"Unknown app: {app}. Supported: {list(self.prompt_templates.keys())}")

        template_func = self.prompt_templates[app]

        if app == "perplexity":
            return template_func(query, context, focus)
        elif app == "grok":
            return template_func(query, context)

        return template_func(query)

    def copy_to_clipboard(self, text: str) -> None:
        """Copy text to clipboard"""
        try:
            pyperclip.copy(text)
            print("✓ Copied to clipboard!")
        except Exception as e:
            print(f"⚠ Could not copy to clipboard: {e}")
            print("\n=== MANUAL COPY ===")
            print(text)
            print("===================\n")

    def prompt_and_copy(
        self, app: str, query: str, context: str = "", focus: str = ""
    ) -> str:
        """
        Generate prompt and copy to clipboard.

        Args:
            app: App name
            query: Main query
            context: Additional context
            focus: Specific focus

        Returns:
            Generated prompt
        """
        prompt = self.generate_prompt(app, query, context, focus)

        print(f"\n{'='*60}")
        print(f"PROMPT FOR {app.upper()}")
        print('='*60)
        print(prompt)
        print('='*60)

        self.copy_to_clipboard(prompt)

        print(f"\n1. Paste into {app.title()} app")
        print("2. Copy the response")
        print("3. Come back here and paste it\n")

        return prompt

    def get_response(self) -> str:
        """
        Get response from user after they've used the app.

        Returns:
            User's pasted response
        """
        print("\n=== PASTE RESPONSE FROM APP ===")
        print("(Paste response and press Enter, then Ctrl+D or Ctrl+Z when done)")
        print()

        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        response = "\n".join(lines)
        print("\n✓ Response captured!")

        return response

    def workflow(
        self, app: str, query: str, context: str = "", focus: str = ""
    ) -> str:
        """
        Complete workflow: generate prompt → copy → get response.

        Args:
            app: App name
            query: Main query
            context: Additional context
            focus: Specific focus

        Returns:
            User's response from app
        """
        self.prompt_and_copy(app, query, context, focus)
        return self.get_response()


# Convenience functions
def perplexity_research(query: str, context: str = "", focus: str = "") -> str:
    """
    Research workflow with Perplexity app.

    Args:
        query: Research query
        context: Additional context
        focus: Specific focus area

    Returns:
        Response from Perplexity
    """
    helper = AppWorkflowHelper()
    return helper.workflow("perplexity", query, context, focus)


def grok_sentiment(query: str, timeframe: str = "today") -> str:
    """
    Sentiment analysis workflow with Grok app.

    Args:
        query: Sentiment query
        timeframe: Time period

    Returns:
        Response from Grok
    """
    helper = AppWorkflowHelper()
    return helper.workflow("grok", query, context=timeframe)


# Multi-app workflow helper
def multi_app_workflow(tasks: list) -> dict:
    """
    Run multiple app workflows in sequence.

    Args:
        tasks: List of (app, query, context, focus) tuples

    Returns:
        Dictionary mapping app name to response

    Example:
        tasks = [
            ("perplexity", "Latest Fed policy", "", "Rate decisions"),
            ("grok", "Market sentiment on Fed", "today", ""),
        ]
        results = multi_app_workflow(tasks)
    """
    helper = AppWorkflowHelper()
    results = {}

    for task in tasks:
        app = task[0]
        query = task[1]
        context = task[2] if len(task) > 2 else ""
        focus = task[3] if len(task) > 3 else ""

        print(f"\n{'='*60}")
        print(f"TASK {len(results) + 1}/{len(tasks)}: {app.upper()}")
        print('='*60)

        response = helper.workflow(app, query, context, focus)
        results[app] = response

    print(f"\n{'='*60}")
    print("ALL TASKS COMPLETE")
    print('='*60)

    return results
