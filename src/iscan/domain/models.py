from datetime import datetime
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ImageRecord:
    id: str
    path: Path
    extension: str
    size_bytes: int


@dataclass(frozen=True, slots=True)
class ImageMetadata:
    width: int
    height: int
    format: str
    size_bytes: int
    captured_at: datetime | None
    latitude: float | None
    longitude: float | None