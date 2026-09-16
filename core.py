from typing import List, Union, Callable, Any

def pipeline_executor(data: List[Any], transform: Callable[[Any], Any]) -> List[Any]:
    """
    Applies a transformation function to a list of data elements.
    Uses a generator expression internally for memory efficiency.
    """
    return [transform(item) for item in data]

class DataProcessor:
    """
    A container for stateful data processing logic.
    """
    def __init__(self, multiplier: int = 1) -> None:
        self.multiplier: int = multiplier

    def process(self, value: Union[int, float]) -> float:
        """
        Multiplies the input value by the stored multiplier.
        """
        return float(value * self.multiplier)

def dynamic_factory(key: str) -> Callable[[Any], Any]:
    """
    Returns a lambda function based on key lookup.
    """
    operations = {
        "double": lambda x: x * 2,
        "square": lambda x: x ** 2,
        "identity": lambda x: x
    }
    return operations.get(key, lambda x: x)

if __name__ == "__main__":
    items: List[int] = [1, 2, 3, 4, 5]
    processor: DataProcessor = DataProcessor(multiplier=10)
    result: List[float] = pipeline_executor(items, processor.process)
    print(result)