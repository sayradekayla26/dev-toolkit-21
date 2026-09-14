from typing import List, Callable, Any, TypeVar, Optional

T = TypeVar('T')

class Orchestrator:
    """Handles execution pipelines with dynamic functional injection."""
    
    def __init__(self, registry: Optional[List[Callable]] = None) -> None:
        self._tasks: List[Callable] = registry or []

    def pipeline(self, data: T) -> Any:
        """Sequentially process data through registered callable stack."""
        result: Any = data
        for task in self._tasks:
            result = task(result)
        return result

    def append_task(self, func: Callable[[Any], Any]) -> None:
        """Extension of internal task registry with type-checked callable."""
        self._tasks.append(func)

def transform_to_meta(payload: str) -> dict:
    """Factory for converting primitive input to annotated structure."""
    return {"value": payload, "status": "processed", "length": len(payload)}

if __name__ == "__main__":
    core = Orchestrator()
    core.append_task(str.upper)
    core.append_task(transform_to_meta)
    
    execution_result = core.pipeline("dev-toolkit-21 init")
    print(f"Result: {execution_result}")