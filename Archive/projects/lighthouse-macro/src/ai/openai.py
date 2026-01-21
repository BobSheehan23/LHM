"""
Lighthouse Macro — OpenAI API Client
GPT integration
"""

from typing import Any, Dict, List, Optional

from core import get_config


class OpenAIClient:
    """Client for OpenAI GPT API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key (uses config if not provided)
        """
        self.config = get_config()
        self.api_key = api_key or self.config.openai_api_key

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY in configs/secrets.env"
            )

        # Lazy import to avoid dependency if not using OpenAI
        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def complete(
        self,
        prompt: str,
        model: str = "gpt-4-turbo",
        max_tokens: int = 2048,
        temperature: float = 0.5,
        system: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate completion with GPT.

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

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=model, max_tokens=max_tokens, temperature=temperature, messages=messages, **kwargs
        )

        return response.choices[0].message.content

    def complete_with_context(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4-turbo",
        max_tokens: int = 2048,
        temperature: float = 0.5,
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
        if system and messages[0].get("role") != "system":
            model_config = self.config.ai_routing_config.get("models", {}).get(model, {})
            system_prompt = system or model_config.get("system_prompt", "")
            if system_prompt:
                messages = [{"role": "system", "content": system_prompt}] + messages

        response = self.client.chat.completions.create(
            model=model, max_tokens=max_tokens, temperature=temperature, messages=messages, **kwargs
        )

        return response.choices[0].message.content

    def extract_structured(
        self, prompt: str, model: str = "gpt-4-turbo", temperature: float = 0.1, **kwargs
    ) -> str:
        """
        Extract structured data (optimized settings for GPT).

        Args:
            prompt: Extraction prompt
            model: Model name
            temperature: Low temperature for consistency
            **kwargs: Additional parameters

        Returns:
            Extracted text
        """
        return self.complete(prompt, model=model, temperature=temperature, **kwargs)

    def stream_complete(
        self,
        prompt: str,
        model: str = "gpt-4-turbo",
        max_tokens: int = 2048,
        temperature: float = 0.5,
        system: Optional[str] = None,
        **kwargs,
    ):
        """
        Stream completion from GPT.

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
            **kwargs,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
