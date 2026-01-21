"""
Lighthouse Macro — AI Model Router
Intelligently route tasks to the optimal model (Claude vs GPT)
"""

from enum import Enum
from typing import Any, Dict, Optional

from core import get_config


class TaskType(Enum):
    """Task types for AI routing"""

    DATA_EXTRACTION = "data_extraction"
    NARRATIVE_SYNTHESIS = "narrative_synthesis"
    CODE_GENERATION = "code_generation"
    QUICK_SUMMARY = "quick_summary"
    CHART_ANALYSIS = "chart_analysis"
    RESEARCH_IDEATION = "research_ideation"
    FACT_CHECKING = "fact_checking"
    WEB_RESEARCH = "web_research"
    REAL_TIME_ANALYSIS = "real_time_analysis"
    MULTIMODAL_ANALYSIS = "multimodal_analysis"


class AIRouter:
    """
    Routes tasks to optimal AI model based on task type and requirements.
    """

    def __init__(self):
        self.config = get_config()
        self.routing_config = self.config.ai_routing_config.get("routing", {})

    def get_model_for_task(self, task: TaskType) -> Dict[str, Any]:
        """
        Get optimal model configuration for a task type.

        Args:
            task: TaskType enum

        Returns:
            Dictionary with model, provider, reason, temperature
        """
        task_key = task.value
        task_config = self.routing_config.get(task_key, {})

        if not task_config:
            # Default to Claude for unknown tasks
            return {
                "model": "claude-sonnet-4",
                "provider": "anthropic",
                "reason": "Default model for unspecified tasks",
                "temperature": 0.5,
            }

        return task_config

    def get_workflow_models(self, workflow_name: str) -> list:
        """
        Get model sequence for a research workflow.

        Args:
            workflow_name: Name of workflow (beacon, beam, chartbook, horizon)

        Returns:
            List of stage configurations
        """
        workflows = self.config.ai_routing_config.get("workflows", {})
        workflow = workflows.get(workflow_name, {})
        return workflow.get("stages", [])

    def should_use_claude(self, task: TaskType) -> bool:
        """
        Check if Claude should be used for a task.

        Args:
            task: TaskType enum

        Returns:
            True if Claude should be used
        """
        config = self.get_model_for_task(task)
        return config.get("provider") == "anthropic"

    def should_use_gpt(self, task: TaskType) -> bool:
        """
        Check if GPT should be used for a task.

        Args:
            task: TaskType enum

        Returns:
            True if GPT should be used
        """
        config = self.get_model_for_task(task)
        return config.get("provider") == "openai"

    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific model.

        Args:
            model_name: Model name (e.g., 'claude-sonnet-4', 'gpt-4-turbo')

        Returns:
            Model configuration dictionary
        """
        models = self.config.ai_routing_config.get("models", {})
        return models.get(model_name, {})

    def explain_routing(self, task: TaskType) -> str:
        """
        Get human-readable explanation of why a model was chosen.

        Args:
            task: TaskType enum

        Returns:
            Explanation string
        """
        config = self.get_model_for_task(task)
        model = config.get("model")
        reason = config.get("reason", "No reason provided")
        return f"Using {model} for {task.value}: {reason}"


# Convenience functions
def route_task(task: TaskType) -> Dict[str, Any]:
    """
    Route a task to optimal model.

    Args:
        task: TaskType enum

    Returns:
        Model configuration
    """
    router = AIRouter()
    return router.get_model_for_task(task)


def get_workflow(workflow_name: str) -> list:
    """
    Get workflow stages.

    Args:
        workflow_name: Workflow name

    Returns:
        List of stages
    """
    router = AIRouter()
    return router.get_workflow_models(workflow_name)
