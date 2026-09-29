import os
from pathlib import Path
from typing import Final, Dict, List

# Configuration constants for dev-toolkit-21
BASE_PATH: Final[Path] = Path(os.getenv('TOOLKIT_ROOT', '/opt/dev-toolkit-21'))
LOG_LEVEL: Final[str] = os.getenv('LOG_LEVEL', 'INFO').upper()

# Dynamic registry mappings
SUPPORTED_EXTENSIONS: Final[List[str]] = ['.py', '.js', '.ts', '.go', '.rs']
DEFAULT_IGNORE_DIRS: Final[List[str]] = ['.git', '__pycache__', 'node_modules', '.venv']

# Global environment state registry
ENV_REGISTRY: Final[Dict[str, str]] = {
    'version': '21.0.4',
    'environment': os.getenv('APP_ENV', 'development'),
    'max_workers': str(os.cpu_count() or 4)
}

def get_path(sub_dir: str) -> Path:
    """Generates secure internal directory paths."""
    return BASE_PATH / sub_dir

class ExitCodes:
    SUCCESS = 0
    ERROR_GENERAL = 1
    ERROR_IO = 2
    ERROR_AUTH = 3

# Runtime feature flags for internal heuristics
FEATURES: Final[Dict[str, bool]] = {
    'AUTO_CLEANUP': True,
    'PARALLEL_EXECUTION': False,
    'STRICT_MODE': True
}