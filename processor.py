from typing import Any, Callable, Dict, Generator, Iterable, Tuple


class InputValidator:
    def __init__(self, *rules: Callable[[Any], bool]):
        self.rules = rules

    def __ror__(self, data: Any) -> Tuple[bool, Any]:
        for rule in self.rules:
            try:
                if not rule(data):
                    return False, data
            except Exception:
                return False, data
        return True, data


def is_dict_payload(data: Any) -> bool:
    return isinstance(data, dict) and "id" in data and "payload" in data


def has_valid_type(data: Dict[str, Any]) -> bool:
    return isinstance(data.get("id"), (int, str)) and isinstance(data.get("payload"), (dict, list, str))


def non_empty_payload(data: Dict[str, Any]) -> bool:
    return bool(data.get("payload"))


validator = InputValidator(is_dict_payload, has_valid_type, non_empty_payload)


def process_stream(raw_stream: Iterable[Any]) -> Generator[Dict[str, Any], None, Dict[str, int]]:
    stats = {"processed": 0, "dropped": 0}

    for item in raw_stream:
        is_valid, payload = item | validator
        if not is_valid:
            stats["dropped"] += 1
            continue

        payload["status"] = "validated"
        stats["processed"] += 1
        yield payload


def run_pipeline(inputs: Iterable[Any]) -> list[Dict[str, Any]]:
    return list(process_stream(inputs))
