from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ImageRecord:
    id: str
    path: Path
    extension: str
    size_bytes: int