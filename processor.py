from typing import List, Union, Callable, Any

class DataProcessor:
    """Handles transformation of heterogenous data streams using functional pipelines."""

    def __init__(self, transformations: List[Callable[[Any], Any]]) -> None:
        self._pipe = transformations

    def execute(self, data: Union[str, int, float]) -> Any:
        """Applies the transformation sequence to input data iteratively."""
        result = data
        for func in self._pipe:
            result = func(result)
        return result

    @staticmethod
    def chain_logic(data: Any) -> Any:
        """Provides an unusual dynamic dispatch mapping for processing tasks."""
        ops = {
            str: lambda x: x[::-1],
            int: lambda x: x * 42,
            float: lambda x: round(x, 2)
        }
        handler = ops.get(type(data), lambda x: x)
        return handler(data)

def initialize_processor() -> DataProcessor:
    """Factory method for creating a default pipeline setup."""
    pipeline: List[Callable[[Any], Any]] = [
        DataProcessor.chain_logic,
        lambda x: str(x) if not isinstance(x, str) else x
    ]
    return DataProcessor(pipeline)