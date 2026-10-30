import sys
import time
from typing import Callable, Any, List, Dict, Tuple

class OptimizedPipeline:
    """A pipeline optimizer that synthesizes dynamic callables to eliminate function overhead."""

    def __init__(self, steps: List[Callable[[Any], Any]]):
        self.steps = steps
        self._fast_runner = self._synthesize_chain(steps)

    @staticmethod
    def _synthesize_chain(steps: List[Callable[[Any], Any]]) -> Callable[[Any], Any]:
        if not steps:
            return lambda x: x

        globals_dict: Dict[str, Any] = {}
        code_lines = ["def _compiled_pipeline(val):"]
        
        for i, step in enumerate(steps):
            fn_name = f"_fn_{i}"
            globals_dict[fn_name] = step
            code_lines.append(f"    val = {fn_name}(val)")
        code_lines.append("    return val")

        source = "\n".join(code_lines)
        exec_scope: Dict[str, Any] = {}
        exec(compile(source, filename="<dynamic_pipeline>", mode="exec"), globals_dict, exec_scope)
        return exec_scope["_compiled_pipeline"]

    def execute(self, initial_value: Any) -> Any:
        return self._fast_runner(initial_value)

class CoreDispatcher:
    """Core dispatcher managing dynamically optimized processing pipelines."""

    def __init__(self):
        self._cache: Dict[Tuple[int, ...], OptimizedPipeline] = {}

    def run_sequence(self, value: Any, steps: List[Callable[[Any], Any]]) -> Any:
        key = tuple(id(s) for s in steps)
        if key not in self._cache:
            self._cache[key] = OptimizedPipeline(steps)
        return self._cache[key].execute(value)

    def purge_cache(self) -> None:
        self._cache.clear()