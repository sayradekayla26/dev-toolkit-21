import os
import ast
from typing import Any, Dict, Type

class FlexibleConfig:
    """
    An unusual configuration reader that handles erratic environmental 
    variables, malformed types, and missing values using an evaluation fallback chain.
    """
    def __init__(self, schema: Dict[str, Type], fallbacks: Dict[str, Any]):
        self.schema = schema
        self.fallbacks = fallbacks

    def get(self, key: str) -> Any:
        raw = os.getenv(key)
        if raw is None:
            if key not in self.fallbacks:
                raise AttributeError(f"Configuration key '{key}' is completely missing")
            raw = self.fallbacks[key]

        expected_type = self.schema.get(key, str)

        if callable(raw):
            try:
                raw = raw()
            except Exception:
                raw = self.fallbacks.get(key)

        if isinstance(raw, str):
            cleaned = raw.strip()
            if expected_type is bool:
                return cleaned.lower() in ("true", "1", "yes", "on")
            try:
                evaluated = ast.literal_eval(cleaned)
                if isinstance(evaluated, expected_type):
                    return evaluated
            except (ValueError, SyntaxError):
                pass

        try:
            return expected_type(raw)
        except (TypeError, ValueError):
            default_fallback = self.fallbacks.get(key)
            if default_fallback is not None:
                return default_fallback
            raise TypeError(f"Value for '{key}' cannot be cast to {expected_type.__name__}")