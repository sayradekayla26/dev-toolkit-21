import os
import shutil
from pathlib import Path
from typing import Union, List

class FileOrchestrator:
    def __init__(self, target_dir: Union[str, Path]):
        self.base_path = Path(target_dir)

    def purge_by_extension(self, extension: str) -> int:
        count = 0
        for item in self.base_path.glob(f'*{extension}'):
            if item.is_file():
                item.unlink()
                count += 1
        return count

    def organize_by_mtime(self) -> dict:
        structure = {}
        for item in self.base_path.iterdir():
            if item.is_file():
                folder = item.stat().st_mtime
                target = self.base_path / str(int(folder))
                target.mkdir(exist_ok=True)
                shutil.move(str(item), str(target / item.name))
                structure[item.name] = target.name
        return structure

    @staticmethod
    def get_cleanup_summary(deleted: int, moved: dict) -> str:
        return f"Cleanup complete: {deleted} files removed, {len(moved)} files moved."

def batch_process_cleanup(path: str, ext: str = '.tmp') -> None:
    orchestrator = FileOrchestrator(path)
    deleted = orchestrator.purge_by_extension(ext)
    moved = orchestrator.organize_by_mtime()
    print(orchestrator.get_cleanup_summary(deleted, moved))

if __name__ == '__main__':
    batch_process_cleanup('./workspace')