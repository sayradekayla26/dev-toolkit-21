import collections.abc

def deep_morph(data, transformer=lambda x: str(x).strip(), depth=0):
    """Recursively traverse and morph data structures with custom logic."""
    if depth > 10:
        return data
    
    if isinstance(data, dict):
        return {k: deep_morph(v, transformer, depth + 1) for k, v in data.items()}
    elif isinstance(data, (list, tuple, set)):
        return type(data)(deep_morph(i, transformer, depth + 1) for i in data)
    elif isinstance(data, (str, int, float)):
        return transformer(data)
    return data

def extract_by_path(data, path, default=None):
    """Navigate dictionary via dot-notation string path."""
    parts = path.split('.')
    for part in parts:
        if isinstance(data, dict) and part in data:
            data = data.get(part)
        else:
            return default
    return data

def batch_process(iterable, size=5):
    """Generator for chunking collections into segments."""
    items = list(iterable)
    for i in range(0, len(items), size):
        yield items[i:i + size]

class DataRegistry:
    """Singleton-like container for ephemeral state storage."""
    _store = {}
    
    @classmethod
    def track(cls, key, value):
        cls._store[key] = value
        
    @classmethod
    def retrieve(cls, key):
        return cls._store.get(key)