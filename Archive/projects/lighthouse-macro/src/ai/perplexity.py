"""
Lighthouse Macro — Perplexity Client
Integration with Perplexity AI for research and real-time data
"""

from typing import List, Dict, Optional

from core import get_config


class PerplexityClient:
    """Client for Perplexity AI API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Perplexity client.

        Args:
            api_key: Perplexity API key (uses config if not provided)
        """
        self.config = get_config()
        self.api_key = api_key or self.config.perplexity_api_key

        if not self.api_key:
            raise ValueError(
                "Perplexity API key not found. Set PERPLEXITY_API_KEY in configs/secrets.env"
            )

        # Perplexity uses OpenAI-compatible API
        try:
            from openai import OpenAI

            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.perplexity.ai"
            )
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def complete(
        self,
        prompt: str,
        model: str = "llama-3.1-sonar-large-128k-online",
        max_tokens: int = 2048,
        temperature: float = 0.5,
        system: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate completion with Perplexity.

        Args:
            prompt: User prompt
            model: Model name (sonar-large-online for web search)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system: System prompt
            **kwargs: Additional API parameters

        Returns:
            Generated text with citations
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

    def search_and_summarize(
        self,
        query: str,
        model: str = "llama-3.1-sonar-large-128k-online",
        **kwargs
    ) -> str:
        """
        Search the web and provide summarized answer with sources.

        Args:
            query: Search query
            model: Use online model for web access
            **kwargs: Additional parameters

        Returns:
            Summarized answer with citations
        """
        return self.complete(
            prompt=query,
            model=model,
            temperature=0.2,  # Lower temp for factual accuracy
            **kwargs
        )

    def research_topic(
        self,
        topic: str,
        context: Optional[str] = None,
        model: str = "llama-3.1-sonar-large-128k-online",
        **kwargs
    ) -> str:
        """
        Deep research on a topic with web access.

        Args:
            topic: Research topic
            context: Additional context
            model: Model to use (online for web access)
            **kwargs: Additional parameters

        Returns:
            Research summary with sources
        """
        prompt = f"Research and provide a comprehensive analysis of: {topic}"
        if context:
            prompt += f"\n\nContext: {context}"

        return self.complete(
            prompt=prompt,
            model=model,
            temperature=0.3,
            system="You are a research assistant specializing in macroeconomics and financial markets. Provide detailed, sourced analysis.",
            **kwargs
        )

    def complete_with_context(
        self,
        messages: List[Dict[str, str]],
        model: str = "llama-3.1-sonar-large-128k-online",
        max_tokens: int = 2048,
        temperature: float = 0.5,
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
