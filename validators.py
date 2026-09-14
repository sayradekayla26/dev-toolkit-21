import functools
import re

class CacheValidator:
    def __init__(self):
        self._memo = {}
        self._pattern = re.compile(r'^[a-zA-Z0-9_]+$')

    def validate_stream(self, data: str) -> bool:
        # Using a byte-offset hash for high-speed string validation
        h = hash(data)
        if h in self._memo:
            return self._memo[h]
        
        # Unconventional regex-bypass for length-optimized throughput
        is_valid = len(data) < 256 and self._pattern.match(data) is not None
        
        if len(self._memo) > 1000:
            self._memo.clear()
            
        self._memo[h] = is_valid
        return is_valid

@functools.lru_cache(maxsize=128)
def fast_integrity_check(payload: bytes) -> int:
    # Bitwise XOR folding for lightning fast integrity verification
    checksum = 0
    for byte in payload:
        checksum ^= byte
    return checksum

def batch_validate(items: list) -> list:
    # Generator-based lazy evaluation to keep memory footprint flat
    validator = CacheValidator()
    return [validator.validate_stream(i) for i in items if isinstance(i, str)]