import io
from pathlib import Path

import numpy as np
import rawpy
from numpy.typing import NDArray
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

from iscan.config import RAW_EXTENSIONS

register_heif_opener()


class ImageDecodeError(Exception):
    pass



class ImageDecoder:
    def decode(self, path: Path) -> NDArray[np.uint8]:
        try:
            if path.suffix.lower() in RAW_EXTENSIONS:
                image = self._decode_raw(path)
            else:
                image = self._decode_with_pillow(path)

            return image
        except Exception as error:
            raise ImageDecodeError(
                f'Cannot decode image "{path}"'
            ) from error

    def _decode_with_pillow(
        self,
        path: Path,
    ) -> NDArray[np.uint8]:
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image)
            image = image.convert("RGB")
            return np.array(image, dtype=np.uint8)

    def _decode_raw(
        self,
        path: Path,
    ) -> NDArray[np.uint8]:
        with rawpy.imread(path) as raw:
            try:
                thumb = raw.extract_thumb()
            except (
                rawpy.LibRawNoThumbnailError,
                rawpy.LibRawUnsupportedThumbnailError
            ):
                return np.array(raw.postprocess(), dtype=np.uint8)
            if thumb.format == rawpy.ThumbFormat.JPEG:
                with Image.open(io.BytesIO(thumb.data)) as image:
                    image = ImageOps.exif_transpose(image)
                    image = image.convert("RGB")
                    return np.array(image, dtype=np.uint8)
            elif thumb.format == rawpy.ThumbFormat.BITMAP:
                return np.array(thumb.data, dtype=np.uint8)
            else:
                raise ImageDecodeError(
                    f"Unsupported image format: {thumb.format}"
                )



