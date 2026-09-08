from typing import Any, Callable, Dict, List, Union
import re

def create_pipeline(*validators: Callable[[Any], bool]) -> Callable[[Any], bool]:
    def pipeline(value: Any) -> bool:
        return all(v(value) for v in validators)
    return pipeline

def regex_match(pattern: str) -> Callable[[str], bool]:
    return lambda x: bool(re.match(pattern, str(x)))

def range_check(min_val: float, max_val: float) -> Callable[[Union[int, float]], bool]:
    return lambda x: min_val <= float(x) <= max_val

def compose_data_processor(mapping: Dict[str, Callable]) -> Callable[[Dict], Dict]:
    def processor(data: Dict) -> Dict:
        return {k: (mapping[k](v) if k in mapping else v) for k, v in data.items()}
    return processor

class DataValidator:
    def __init__(self, schema: Dict[str, List[Callable]]):
        self.schema = schema

    def validate(self, data: Dict) -> bool:
        try:
            return all(
                all(validator(data.get(field)) for validator in validators)
                for field, validators in self.schema.items()
            )
        except (TypeError, ValueError):
            return False

    @staticmethod
    def soft_clean(data: Dict, default_val: Any = None) -> Dict:
        return {k: (v if v is not None else default_val) for k, v in data.items()}