import os
import shutil
from pathlib import Path
from typing import Union, List

class FileOrchestrator:
    def __init__(self, root: str = '.'):
        self.root = Path(root)

    def purge_by_extension(self, ext: str) -> int:
        count = 0
        for path in self.root.rglob(f'*{ext}'):
            if path.is_file():
                path.unlink()
                count += 1
        return count

    def reorganize_files(self, mapping: dict) -> List[str]:
        moved = []
        for file_path in self.root.iterdir():
            if file_path.is_file() and file_path.suffix in mapping:
                target_dir = self.root / mapping[file_path.suffix]
                target_dir.mkdir(exist_ok=True)
                dest = target_dir / file_path.name
                shutil.move(str(file_path), str(dest))
                moved.append(str(dest))
        return moved

def clean_temp_workspace(path: Union[str, Path]) -> None:
    target = Path(path)
    if target.exists():
        shutil.rmtree(target)
        target.mkdir()

def get_directory_stats(path: str) -> dict:
    return {
        'files': sum(1 for f in Path(path).rglob('*') if f.is_file()),
        'size_bytes': sum(f.stat().st_size for f in Path(path).rglob('*') if f.is_file())
    }