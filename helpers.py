import os
import shutil
from pathlib import Path
from typing import Union, List

class WorkspaceCleaner:
    def __init__(self, target_dir: Union[str, Path] = '.tmp'):
        self.target = Path(target_dir)

    def purge_recursive(self, patterns: List[str] = None) -> int:
        count = 0
        if not self.target.exists():
            return count
        
        extensions = patterns or ['.log', '.tmp', '.bak']
        for path in self.target.rglob('*'):
            if path.suffix in extensions:
                try:
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
                    count += 1
                except OSError:
                    pass
        return count

def organize_imports(code_block: str) -> str:
    lines = code_block.splitlines()
    imports = sorted([l for l in lines if l.startswith('import ') or l.startswith('from ')])
    others = [l for l in lines if not (l.startswith('import ') or l.startswith('from '))]
    return '\n'.join(imports + [''] + others).strip()

def format_path_structure(base_path: str) -> dict:
    tree = {path.name: path.is_dir() for path in Path(base_path).iterdir()}
    return dict(sorted(tree.items(), key=lambda item: item[1]))