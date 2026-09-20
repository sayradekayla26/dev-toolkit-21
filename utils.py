import functools
from typing import Any, Callable, Dict

class DataPipeline:
    """A whimsical pipe-and-filter processor for arbitrary data."""
    def __init__(self, data: Any):
        self.data = data

    def __or__(self, func: Callable[[Any], Any]) -> 'DataPipeline':
        return DataPipeline(func(self.data))

    def result(self) -> Any:
        return self.data

def deep_normalize(data: Any) -> Any:
    """Recursively flattens and cleans dictionary-like keys."""
    if isinstance(data, dict):
        return {str(k).lower().replace(' ', '_'): deep_normalize(v) for k, v in data.items()}
    if isinstance(data, list):
        return [deep_normalize(i) for i in data]
    return data

def cast_if_numeric(value: Any) -> Any:
    """Attempt to convert strings to numeric types."""
    try:
        return int(value) if float(value).is_integer() else float(value)
    except (ValueError, TypeError):
        return value

def process_payload(payload: Dict) -> Dict:
    """Chainable transformation logic for API payloads."""
    pipeline = DataPipeline(payload)
    return (
        pipeline 
        | deep_normalize 
        | (lambda d: {k: cast_if_numeric(v) for k, v in d.items()})
    ).result()