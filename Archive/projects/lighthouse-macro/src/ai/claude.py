"""
Lighthouse Macro — Claude API Client
Anthropic Claude integration
"""

from typing import Any, Dict, List, Optional

from core import get_config


class ClaudeClient:
    """Client for Anthropic Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client.

        Args:
            api_key: Anthropic API key (uses config if not provided)
        """
        self.config = get_config()
        self.api_key = api_key or self.config.anthropic_api_key

        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY in configs/secrets.env"
            )

        # Lazy import to avoid dependency if not using Claude
        try:
            from anthropic import Anthropic

            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

    def complete(
        self,
        prompt: str,
        model: str = "claude-sonnet-4",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate completion with Claude.

        Args:
            prompt: User prompt
            model: Model name
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system: System prompt
            **kwargs: Additional API parameters

        Returns:
            Generated text
        """
        # Use LHM system prompt if not provided
        if system is None:
            model_config = self.config.ai_routing_config.get("models", {}).get(model, {})
            system = model_config.get("system_prompt", "")

        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )

        return response.content[0].text

    def complete_with_context(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-sonnet-4",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate completion with conversation context.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system: System prompt
            **kwargs: Additional API parameters

        Returns:
            Generated text
        """
        if system is None:
            model_config = self.config.ai_routing_config.get("models", {}).get(model, {})
            system = model_config.get("system_prompt", "")

        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages,
            **kwargs,
        )

        return response.content[0].text

    def analyze_chart(
        self, chart_path: str, prompt: str, temperature: float = 0.4
    ) -> str:
        """
        Analyze a chart image with Claude.

        Args:
            chart_path: Path to chart image
            prompt: Analysis prompt
            temperature: Sampling temperature

        Returns:
            Analysis text
        """
        import base64

        with open(chart_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        # Determine image type
        if chart_path.endswith(".png"):
            media_type = "image/png"
        elif chart_path.endswith(".jpg") or chart_path.endswith(".jpeg"):
            media_type = "image/jpeg"
        else:
            media_type = "image/png"

        response = self.client.messages.create(
            model="claude-sonnet-4",
            max_tokens=4096,
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )

        return response.content[0].text

    def stream_complete(
        self,
        prompt: str,
        model: str = "claude-sonnet-4",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs,
    ):
        """
        Stream completion from Claude.

        Args:
            prompt: User prompt
            model: Model name
            max_tokens: Maximum tokens
            temperature: Sampling temperature
            system: System prompt
            **kwargs: Additional parameters

        Yields:
            Text chunks as they arrive
        """
        if system is None:
            model_config = self.config.ai_routing_config.get("models", {}).get(model, {})
            system = model_config.get("system_prompt", "")

        with self.client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        ) as stream:
            for text in stream.text_stream:
                yield text
