"""
Lighthouse Macro — Gemini Client
Integration with Google's Gemini AI
"""

from typing import List, Dict, Optional

from core import get_config


class GeminiClient:
    """Client for Google Gemini API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client.

        Args:
            api_key: Google API key (uses config if not provided)
        """
        self.config = get_config()
        self.api_key = api_key or self.config.gemini_api_key

        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY in configs/secrets.env"
            )

        # Lazy import
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            self.genai = genai
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. Run: pip install google-generativeai"
            )

    def complete(
        self,
        prompt: str,
        model: str = "gemini-2.0-flash-exp",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate completion with Gemini.

        Args:
            prompt: User prompt
            model: Model name (gemini-2.0-flash-exp, gemini-pro)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system: System instruction
            **kwargs: Additional API parameters

        Returns:
            Generated text
        """
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        model_instance = self.genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config,
            system_instruction=system if system else None,
        )

        response = model_instance.generate_content(prompt)
        return response.text

    def complete_with_context(
        self,
        messages: List[Dict[str, str]],
        model: str = "gemini-2.0-flash-exp",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate completion with conversation context.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name
            max_tokens: Maximum tokens
            temperature: Sampling temperature
            system: System instruction
            **kwargs: Additional parameters

        Returns:
            Generated text
        """
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        model_instance = self.genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config,
            system_instruction=system if system else None,
        )

        # Convert messages to Gemini format
        chat = model_instance.start_chat(history=[])

        # Add previous messages
        for msg in messages[:-1]:
            if msg["role"] == "user":
                chat.send_message(msg["content"])

        # Send final message and get response
        response = chat.send_message(messages[-1]["content"])
        return response.text

    def analyze_chart(
        self,
        chart_path: str,
        prompt: str,
        model: str = "gemini-2.0-flash-exp",
        temperature: float = 0.4,
    ) -> str:
        """
        Analyze a chart image with Gemini vision.

        Args:
            chart_path: Path to chart image
            prompt: Analysis prompt
            model: Model name (must support vision)
            temperature: Sampling temperature

        Returns:
            Analysis text
        """
        import PIL.Image

        img = PIL.Image.open(chart_path)

        generation_config = {
            "temperature": temperature,
            "max_output_tokens": 2048,
        }

        model_instance = self.genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config,
        )

        response = model_instance.generate_content([prompt, img])
        return response.text

    def stream_complete(
        self,
        prompt: str,
        model: str = "gemini-2.0-flash-exp",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs,
    ):
        """
        Stream completion from Gemini.

        Args:
            prompt: User prompt
            model: Model name
            max_tokens: Maximum tokens
            temperature: Sampling temperature
            system: System instruction
            **kwargs: Additional parameters

        Yields:
            Text chunks
        """
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        model_instance = self.genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config,
            system_instruction=system if system else None,
        )

        response = model_instance.generate_content(prompt, stream=True)

        for chunk in response:
            yield chunk.text
