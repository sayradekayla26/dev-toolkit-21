import sys
from collections import deque
from typing import Callable, Dict, List


class FastCorePipeline:
    """High-performance stream processor using memoryview slicing and interned dispatch keys."""
    __slots__ = ('_transforms', '_cache', '_ring_buffer', '_max_depth')

    def __init__(self, max_depth: int = 1024):
        self._transforms: Dict[str, Callable[[memoryview], memoryview]] = {}
        self._cache: Dict[int, memoryview] = {}
        self._ring_buffer: deque = deque(maxlen=max_depth)
        self._max_depth = max_depth

    def register_stage(self, stage_name: str, fn: Callable[[memoryview], memoryview]) -> None:
        key = sys.intern(stage_name)
        self._transforms[key] = fn

    def optimize_and_run(self, raw_data: bytes, pipeline_keys: List[str]) -> bytes:
        data_mv = memoryview(raw_data)
        cache_key = hash((bytes(data_mv[:16]), tuple(pipeline_keys)))

        if cache_key in self._cache:
            return bytes(self._cache[cache_key])

        curr = data_mv
        for key in pipeline_keys:
            interned_key = sys.intern(key)
            if interned_key in self._transforms:
                curr = self._transforms[interned_key](curr)

        self._ring_buffer.append(cache_key)
        if len(self._cache) >= self._max_depth:
            oldest = self._ring_buffer.popleft()
            self._cache.pop(oldest, None)

        self._cache[cache_key] = curr
        return bytes(curr)

    def clear_hot_spots(self) -> None:
        self._cache.clear()
        self._ring_buffer.clear()
