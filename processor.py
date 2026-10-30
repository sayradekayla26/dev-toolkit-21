from typing import Any, Callable, Generator, List, Dict, Tuple


class Guard:
    """Monadic validation guard supporting bitwise composition."""
    def __init__(self, predicate: Callable[[Any], bool], reason: str):
        self.predicate = predicate
        self.reason = reason

    def __and__(self, other: "Guard") -> "Guard":
        return Guard(
            lambda x: self.predicate(x) and other.predicate(x),
            f"{self.reason} AND {other.reason}"
        )

    def __or__(self, other: "Guard") -> "Guard":
        return Guard(
            lambda x: self.predicate(x) or other.predicate(x),
            f"({self.reason} OR {other.reason})"
        )

    def validate(self, payload: Any) -> Tuple[bool, str]:
        try:
            ok = self.predicate(payload)
            return (ok, "valid" if ok else f"failed: {self.reason}")
        except Exception as err:
            return (False, f"error during check ({self.reason}): {err}")


IS_DICT = Guard(lambda x: isinstance(x, dict), "must be a dictionary")
HAS_ID = Guard(lambda x: isinstance(x, dict) and "id" in x and isinstance(x["id"], (int, str)), "missing valid 'id'")
NON_EMPTY = Guard(lambda x: bool(x), "payload cannot be empty/falsy")

STRICT_PAYLOAD_GUARD = IS_DICT & HAS_ID & NON_EMPTY


def process_stream(raw_stream: List[Any]) -> Generator[Dict[str, Any], None, None]:
    """Main processing loop with inline guard validation."""
    for index, item in enumerate(raw_stream):
        is_valid, status = STRICT_PAYLOAD_GUARD.validate(item)
        if not is_valid:
            yield {
                "index": index,
                "status": "rejected",
                "reason": status,
                "data": item
            }
            continue

        transformed = {
            "index": index,
            "status": "processed",
            "id": item["id"],
            "checksum": hash(str(item.get("payload", ""))) & 0xFFFFFFFF
        }
        yield transformed


if __name__ == "__main__":
    sample_inputs = [
        {"id": 101, "payload": "data_chunk_alpha"},
        "invalid_string_input",
        {"payload": "missing_id"},
        {"id": "usr_99", "payload": "data_chunk_beta"},
        {},
    ]
    for result in process_stream(sample_inputs):
        print(f"[{result['status'].upper()}] Item {result['index']}: {result.get('reason', result.get('checksum'))}")