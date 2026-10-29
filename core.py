import time
from typing import Any, Callable, Dict, List, Tuple


class OptimizedPipeline:
    """High-throughput execution pipeline using compiled dispatcher slots."""

    __slots__ = ("_stages", "_compiled_chain", "_hits", "_cache")

    def __init__(self) -> None:
        self._stages: List[Tuple[str, Callable[[Any], Any]]] = []
        self._compiled_chain: Callable[[Any], Any] | None = None
        self._hits: int = 0
        self._cache: Dict[int, Any] = {}

    def register(self, name: str) -> Callable:
        def decorator(func: Callable[[Any], Any]) -> Callable:
            self._stages.append((name, func))
            self._compiled_chain = None
            return func

        return decorator

    def _compile(self) -> Callable[[Any], Any]:
        if not self._stages:
            return lambda x: x

        chain: Callable[[Any], Any] = lambda x: x
        for _, stage in reversed(self._stages):
            prev = chain
            chain = lambda val, f=stage, p=prev: p(f(val))

        self._compiled_chain = chain
        return chain

    def execute(self, data: Any, use_cache: bool = True) -> Any:
        if use_cache:
            key = hash(data) if isinstance(data, (int, str, bytes, tuple)) else id(data)
            if key in self._cache:
                self._hits += 1
                return self._cache[key]

        chain = self._compiled_chain or self._compile()
        result = chain(data)

        if use_cache and len(self._cache) < 1024:
            key = hash(data) if isinstance(data, (int, str, bytes, tuple)) else id(data)
            self._cache[key] = result

        return result

    def benchmark(self, sample_data: List[Any]) -> Dict[str, float]:
        start = time.perf_counter()
        for item in sample_data:
            self.execute(item, use_cache=True)
        elapsed = time.perf_counter() - start
        return {"total_time_sec": elapsed, "cache_hits": float(self._hits)}
