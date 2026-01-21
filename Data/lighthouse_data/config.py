from pathlib import Path
from dataclasses import dataclass
import os

@dataclass
class DataConfig:
    base_dir: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = base_dir / "data"
    raw_dir: Path = data_dir / "raw"
    curated_dir: Path = data_dir / "curated"
    indicators_dir: Path = data_dir / "indicators"
    logs_dir: Path = base_dir / "logs"
    
    # API Keys (set these in your environment variables for security)
    fred_api_key: str | None = os.environ.get('FRED_API_KEY')
    santiment_api_key: str | None = os.environ.get('SANTIMENT_API_KEY')
    dune_api_key: str | None = os.environ.get('DUNE_API_KEY')
    coinglass_api_key: str | None = os.environ.get('COINGLASS_API_KEY')

    def ensure_dirs(self) -> None:
        for p in [self.data_dir, self.raw_dir, self.curated_dir, self.indicators_dir, self.logs_dir]:
            p.mkdir(parents=True, exist_ok=True)

CONFIG = DataConfig()
CONFIG.ensure_dirs()
