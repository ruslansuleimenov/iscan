from datetime import datetime
from pathlib import Path
from typing import Any

import exifread
from numpy.typing import NDArray
import numpy as np

from iscan.domain.models import ImageMetadata


class MetadataExtractor:
    def extract(self, path: Path, pixels: NDArray[np.uint8]) -> ImageMetadata:
        height, width = pixels.shape[:2]
        image_format = path.suffix.lower()
        size_bytes = path.stat().st_size
        tags = self._read_exif_tags(path)
        metadata = ImageMetadata(
            height=height,
            width=width,
            format=image_format,
            size_bytes=size_bytes,
            captured_at= self._parse_captured_at(tags),
            latitude= self._parse_latitude(tags),
            longitude= self._parse_longitude(tags),
        )
        return metadata

    def _read_exif_tags(self, path: Path) -> dict:
        with open(path, "rb") as f:
            exif_tags = exifread.process_file(f)
        return exif_tags


    def _parse_captured_at(self, tags) -> datetime | None:
        captured_at_exif = tags.get("EXIF DateTimeOriginal")
        if captured_at_exif is None:
            return None
        return datetime.strptime(str(captured_at_exif), "%Y:%m:%d %H:%M:%S")


    def _parse_latitude(self, tags) -> float | None:
        latitude_exif = tags.get("GPS GPSLatitude")
        ref = tags.get("GPS GPSLatitudeRef")
        if latitude_exif is None or ref is None:
            return None
        return self._dms_to_decimal(latitude_exif, ref)

    def _parse_longitude(self, tags) -> float | None:
        longitude_exif = tags.get("GPS GPSLongitude")
        ref = tags.get("GPS GPSLongitudeRef")
        if longitude_exif is None or ref is None:
            return None
        return self._dms_to_decimal(longitude_exif, ref)


    def _dms_to_decimal(self, dms_tag, ref_tag):
        if dms_tag is None:
            return None
        degrees, minutes, seconds = dms_tag.values
        decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        if str(ref_tag) == "S" or str(ref_tag) == "W":
            decimal = -decimal
        return decimal
