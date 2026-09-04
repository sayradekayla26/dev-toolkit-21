from typing import Any, Callable, Dict, List, Optional, Union

def validate_schema(data: Dict[str, Any], schema: Dict[str, Callable[[Any], bool]]) -> bool:
    """
    Validates input dictionary against a schema of predicate functions.
    
    Args:
        data: The dictionary to inspect.
        schema: A mapping of keys to boolean-returning check functions.
        
    Returns:
        bool: True if all keys exist and predicates pass, otherwise False.
    """
    return all(key in data and validator(data[key]) for key, validator in schema.items())

def chain_validators(*validators: Callable[[Any], bool]) -> Callable[[Any], bool]:
    """
    Combines multiple validator functions into a single logical AND chain.
    
    Args:
        *validators: A variadic list of predicate functions.
        
    Returns:
        Callable: A single function that returns True only if all validators pass.
    """
    def composite(value: Any) -> bool:
        return all(v(value) for v in validators)
    return composite

def is_in_range(min_val: Union[int, float], max_val: Union[int, float]) -> Callable[[Union[int, float]], bool]:
    """
    Factory for creating numeric boundary checking predicates.
    
    Args:
        min_val: Lower inclusive bound.
        max_val: Upper inclusive bound.
        
    Returns:
        Callable: A validator function for the specified range.
    """
    return lambda x: min_val <= x <= max_val