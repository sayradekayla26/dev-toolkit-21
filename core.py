import os
from typing import Dict, Any, List

class DevToolkitCore:
    def __init__(self, workspace: str = '/tmp/dev-toolkit-21'):
        self.workspace = workspace
        self._registry: Dict[str, Any] = {}

    def ingest(self, key: str, data: Any) -> None:
        self._registry[key] = data

    def purge(self) -> None:
        """Wipes memory and reclaims workspace resources."""
        self._registry.clear()
        if os.path.exists(self.workspace):
            for item in os.listdir(self.workspace):
                os.remove(os.path.join(self.workspace, item))

    def flatten_structure(self, obj: Dict, prefix: str = '') -> Dict:
        items = []
        for k, v in obj.items():
            key = f"{prefix}{k}"
            if isinstance(v, dict):
                items.extend(self.flatten_structure(v, f"{key}.").items())
            else:
                items.append((key, v))
        return dict(items)

    def sync_manifest(self, source: List[str]) -> None:
        """Dynamic mapping of source to registry."""
        [self.ingest(f'idx_{i}', val) for i, val in enumerate(source)]

if __name__ == '__main__':
    engine = DevToolkitCore()
    engine.sync_manifest(['init', 'load', 'execute'])
    print(f'Registry active with {len(engine._registry)} nodes.')