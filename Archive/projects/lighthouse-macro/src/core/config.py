"""
Lighthouse Macro — Core Configuration Management
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration manager for Lighthouse Macro"""

    # Paths
    root_dir: Path = Field(default_factory=lambda: Path.home() / "lighthouse-macro")
    data_dir: Path = Field(default=None)
    config_dir: Path = Field(default=None)

    # API Keys
    fred_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    grok_api_key: Optional[str] = None
    perplexity_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    substack_api_key: Optional[str] = None
    twitter_api_key: Optional[str] = None

    # Configuration files
    series_config: Dict[str, Any] = Field(default_factory=dict)
    charting_config: Dict[str, Any] = Field(default_factory=dict)
    ai_routing_config: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)

        # Set default paths if not provided
        if self.data_dir is None:
            self.data_dir = self.root_dir / "data"
        if self.config_dir is None:
            self.config_dir = self.root_dir / "configs"

        # Load environment variables
        self._load_env()

        # Load configuration files
        self._load_configs()

    def _load_env(self) -> None:
        """Load environment variables from secrets.env"""
        env_file = self.config_dir / "secrets.env"
        if env_file.exists():
            load_dotenv(env_file)

        # Load API keys from environment
        self.fred_api_key = os.getenv("FRED_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.grok_api_key = os.getenv("GROK_API_KEY")
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.substack_api_key = os.getenv("SUBSTACK_API_KEY")
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")

    def _load_configs(self) -> None:
        """Load YAML configuration files"""
        # Load series taxonomy
        series_file = self.config_dir / "series.yaml"
        if series_file.exists():
            with open(series_file) as f:
                self.series_config = yaml.safe_load(f)

        # Load charting standards
        charting_file = self.config_dir / "charting.yaml"
        if charting_file.exists():
            with open(charting_file) as f:
                self.charting_config = yaml.safe_load(f)

        # Load AI routing
        ai_routing_file = self.config_dir / "ai_routing.yaml"
        if ai_routing_file.exists():
            with open(ai_routing_file) as f:
                self.ai_routing_config = yaml.safe_load(f)

    def get_series_by_pillar(self, pillar: str) -> Dict[str, list]:
        """Get all series for a given pillar"""
        return self.series_config.get(pillar, {})

    def get_all_series(self) -> list:
        """Get all series IDs across all pillars"""
        series = []
        for pillar in ["macro_dynamics", "monetary_mechanics", "market_technicals"]:
            pillar_data = self.series_config.get(pillar, {})
            for category_series in pillar_data.values():
                if isinstance(category_series, list):
                    series.extend(category_series)
        return series

    def get_chart_colors(self) -> Dict[str, str]:
        """Get LHM color palette"""
        return self.charting_config.get("colors", {})

    def get_ai_routing(self, task: str) -> Dict[str, Any]:
        """Get AI model routing for a specific task"""
        routing = self.ai_routing_config.get("routing", {})
        return routing.get(task, {})

    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate which API keys are configured"""
        return {
            "fred": bool(self.fred_api_key),
            "google": bool(self.google_api_key),
            "anthropic": bool(self.anthropic_api_key),
            "openai": bool(self.openai_api_key),
            "grok": bool(self.grok_api_key),
            "perplexity": bool(self.perplexity_api_key),
            "gemini": bool(self.gemini_api_key),
            "substack": bool(self.substack_api_key),
            "twitter": bool(self.twitter_api_key),
        }


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create global config instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config() -> Config:
    """Reload configuration from disk"""
    global _config
    _config = Config()
    return _config
