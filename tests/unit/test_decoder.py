import io
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from iscan.scanning.decoder import ImageDecoder, ImageDecodeError


class TestDecoder:
    def test_decode_rgb_jpeg(self, tmp_path: Path) -> None:
        image_path = tmp_path / "photo.jpg"

        with Image.new(
            mode="RGB",
            size=(10, 20),
            color=(255, 0, 0),
        ) as image:
            image.save(image_path, format="JPEG")

        decoder = ImageDecoder()
        pixels = decoder.decode(image_path)

        assert isinstance(pixels, np.ndarray)
        assert pixels.shape == (20, 10, 3)
        assert pixels.dtype == np.uint8

    def test_decode_grayscale_as_rgb(self, tmp_path: Path) -> None:
        image_path = tmp_path / "gray.jpg"

        with Image.new(
            mode="L",
            size=(8, 6),
            color=128,
        ) as image:
            image.save(image_path, format="JPEG")

        pixels = ImageDecoder().decode(image_path)

        assert pixels.shape == (6, 8, 3)
        assert pixels.dtype == np.uint8

    def test_decode_broken_file(self, tmp_path: Path) -> None:
        image_path = tmp_path / "broken.jpg"
        with Image.new(
            mode="RGB",
            size=(20, 20),
            color=(255, 0, 0),
        ) as image:
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            data = buf.getvalue()

            # Урезаем данные (например, оставляем только первую половину байтов)
        corrupted_data = data[: len(data) // 2]
        image_path.write_bytes(corrupted_data)
        with pytest.raises(
            ImageDecodeError,
            match="Cannot decode image",
        ):
            ImageDecoder().decode(image_path)
