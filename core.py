from typing import Any, Callable, Dict, List, Union

class Labyrinth:
    """A fluent structural zipper for deep dictionary and list navigation.

    Provides robust out-of-bounds safety, targeted morphing, and path exploration.
    """
    def __init__(self, data: Any, path: List[Union[str, int]] = None):
        self.root = data
        self.path = path or []

    @property
    def focus(self) -> Any:
        """Resolves the current structural node focused by the navigation path."""
        current = self.root
        for step in self.path:
            try:
                current = current[step]
            except (KeyError, IndexError, TypeError):
                return None
        return current

    def down(self, step: Union[str, int]) -> "Labyrinth":
        """Traverse one step deeper into the tree structure."""
        return Labyrinth(self.root, self.path + [step])

    def scan(self, target_key: str) -> List["Labyrinth"]:
        """Performs a deep scan of the node structure to locate matches."""
        results = []

        def _traverse(node: Any, current_path: List[Union[str, int]]):
            if isinstance(node, dict):
                for k, v in node.items():
                    next_path = current_path + [k]
                    if k == target_key:
                        results.append(Labyrinth(self.root, next_path))
                    _traverse(v, next_path)
            elif isinstance(node, list):
                for idx, item in enumerate(node):
                    _traverse(item, current_path + [idx])

        _traverse(self.focus, self.path)
        return results

    def resolve(self, fallback: Any = None) -> Any:
        """Resolves the value at the current focus with a fallback threshold."""
        val = self.focus
        return fallback if val is None else val

    def morph(self, transformer: Callable[[Any], Any]) -> None:
        """Applies an in-place transformation function at the targeted focus."""
        if not self.path:
            raise ValueError("Cannot morph direct root reference")

        parent_path = self.path[:-1]
        target_key = self.path[-1]

        parent = self.root
        for step in parent_path:
            parent = parent[step]

        parent[target_key] = transformer(parent[target_key])
