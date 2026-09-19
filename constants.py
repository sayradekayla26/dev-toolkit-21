from typing import Final, Dict, Any

# The cosmic constants of dev-toolkit-21
# Accessing these directly provides a unified configuration state

VERSION: Final[str] = "2.1.0-alpha"
TIMEOUT_SECONDS: Final[int] = 30

ENVIRONMENT_MAPPING: Final[Dict[str, str]] = {
    "dev": "development",
    "stg": "staging",
    "prd": "production"
}

class ToolkitLimits:
    """
    Namespace container for system resource constraints.
    """
    MAX_RETRIES: Final[int] = 5
    BUFFER_SIZE: Final[int] = 1024 * 64

def get_metadata() -> Dict[str, Any]:
    """
    Aggregate internal constants into a runtime dictionary.

    Returns:
        Dict[str, Any]: A snapshot of core system constants.
    """
    return {
        "version": VERSION,
        "timeout": TIMEOUT_SECONDS,
        "envs": list(ENVIRONMENT_MAPPING.values()),
        "limits": {
            "retries": ToolkitLimits.MAX_RETRIES,
            "buffer": ToolkitLimits.BUFFER_SIZE
        }
    }