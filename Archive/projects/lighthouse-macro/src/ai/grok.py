"""
Lighthouse Macro — Grok (xAI) Client
Integration with xAI's Grok model
"""

from typing import List, Dict, Optional

from core import get_config


class GrokClient:
    """Client for xAI Grok API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Grok client.

        Args:
            api_key: xAI API key (uses config if not provided)
        """
        self.config = get_config()
        self.api_key = api_key or self.config.grok_api_key

        if not self.api_key:
            raise ValueError(
                "Grok API key not found. Set GROK_API_KEY in configs/secrets.env"
            )

        # Grok uses OpenAI-compatible API
        try:
            from openai import OpenAI

            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def complete(
        self,
        prompt: str,
        model: str = "grok-beta",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate completion with Grok.

        Args:
            prompt: User prompt
            model: Model name (grok-beta)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system: System prompt
            **kwargs: Additional API parameters

        Returns:
            Generated text
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
            **kwargs
        )

        return response.choices[0].message.content

    def complete_with_context(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-beta",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs,
    ) -> str:
        """
        Generate completion with conversation context.

        Args:
            messages: List of message dictionaries
            model: Model name
            max_tokens: Maximum tokens
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Returns:
            Generated text
        """
        response = self.client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
            **kwargs
        )

        return response.choices[0].message.content

    def stream_complete(
        self,
        prompt: str,
        model: str = "grok-beta",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs,
    ):
        """
        Stream completion from Grok.

        Args:
            prompt: User prompt
            model: Model name
            max_tokens: Maximum tokens
            temperature: Sampling temperature
            system: System prompt
            **kwargs: Additional parameters

        Yields:
            Text chunks
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        stream = self.client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
            stream=True,
            **kwargs
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
