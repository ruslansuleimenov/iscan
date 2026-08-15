from pathlib import Path

from iscan.config import SUPPORTED_EXTENSIONS


class LocalDirectorySource:
    def __init__(self, root: Path):
        if not root.exists():
            raise FileNotFoundError(f'"{root}" does not exist')
        if not root.is_dir():
            raise NotADirectoryError(f'"{root}" is not a directory')
        self.root = root

    def find_images(self) -> list[Path]:
        images = []
        for path in self.root.rglob("*"):
            try:
                if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    images.append(path)
            except OSError:
                continue
        return sorted(images)
