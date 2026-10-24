from typing import Any, Callable, List


class Lens:
    """Creative functional lens for navigating and transforming nested structures."""

    def __init__(self, path: str) -> None:
        self.keys = [k for k in path.split(".") if k]

    def get(self, data: Any, default: Any = None) -> Any:
        curr = data
        for key in self.keys:
            if isinstance(curr, dict) and key in curr:
                curr = curr[key]
            elif isinstance(curr, (list, tuple)) and key.isdigit():
                idx = int(key)
                if 0 <= idx < len(curr):
                    curr = curr[idx]
                else:
                    return default
            else:
                return default
        return curr

    def mutate(self, data: Any, fn: Callable[[Any], Any]) -> Any:
        def _step(curr: Any, keys: List[str]) -> Any:
            if not keys:
                return fn(curr)
            head, *tail = keys
            if isinstance(curr, dict):
                res = dict(curr)
                res[head] = _step(curr.get(head), tail)
                return res
            if isinstance(curr, list) and head.isdigit():
                res = list(curr)
                idx = int(head)
                if 0 <= idx < len(res):
                    res[idx] = _step(res[idx], tail)
                return res
            return curr

        return _step(data, self.keys)

    def __matmul__(self, data: Any) -> Any:
        return self.get(data)

    def __rshift__(self, fn: Callable[[Any], Any]) -> "LensTransformer":
        return LensTransformer(self, fn)


class LensTransformer:

    def __init__(self, lens: Lens, fn: Callable[[Any], Any]) -> None:
        self.lens = lens
        self.fn = fn

    def __matmul__(self, data: Any) -> Any:
        return self.lens.mutate(data, self.fn)


def focus(path: str) -> Lens:
    return Lens(path)
