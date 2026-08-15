import mlx.core as mx
import numpy as np
from numpy.typing import NDArray
from PIL import Image


class BasicImageFeatureExtractor:
    def __init__(self, image_size: tuple[int, int] = (64, 64)) -> None:
        self.image_size = image_size

    def extract(self, pixels: NDArray[np.uint8]) -> mx.array:
        image = Image.fromarray(pixels)
        resized_image = image.resize(self.image_size, resample=Image.Resampling.LANCZOS)
        resized_array = np.asarray(resized_image, dtype=np.float32)
        normalized_array = resized_array / 255.0
        tensor = mx.array(normalized_array)
        vector = tensor.flatten()
        norm = mx.linalg.norm(vector)
        epsilon = 1e-12
        safe_norm = mx.maximum(norm, epsilon)
        normalized_vector = vector / safe_norm
        return normalized_vector
