import functools
import logging
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])

class ToolkitEngine:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.registry = {}

    def register(self, name: str):
        def decorator(func: F) -> F:
            self.registry[name] = func
            return func
        return decorator

    def execute(self, name: str, *args, **kwargs) -> Any:
        func = self.registry.get(name)
        if not func:
            raise ValueError(f"task {name} not found")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"execution error in {name}: {e}")
            raise

def async_safety_wrapper(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # unconventional trap for blocking calls in event loops
        import threading
        if threading.current_thread().name == 'MainThread':
            return func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper  # type: ignore

engine = ToolkitEngine()