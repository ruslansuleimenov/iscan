import numpy as np
import pytest
import mlx.core as mx


from iscan.features.image_basic import BasicImageFeatureExtractor


class TestBasicImageFeatureExtractor:
    def test_exact_returns_expected_vector_shape(self):
        extractor = BasicImageFeatureExtractor()
        test_array = np.full((100, 200, 3), 128, dtype=np.uint8)
        vector = extractor.extract(test_array)
        mx.eval(vector)
        assert vector.shape == (64 * 64 * 3,)

    def test_extract_returns_unit_vector(self):
        extractor = BasicImageFeatureExtractor()
        normalized_vector = extractor.extract(
            np.full((100, 200, 3), 128, dtype=np.uint8)
        )
        actual_norm = mx.linalg.norm(normalized_vector).item()
        assert actual_norm == pytest.approx(1.0, abs=1e-6)

    def test_extract_black_image_contains_only_finite_values(self):
        black_array = np.zeros((100, 200, 3), dtype=np.uint8)
        extractor = BasicImageFeatureExtractor()
        black_vector = extractor.extract(black_array)
        all_values_are_finite = mx.all(mx.isfinite(black_vector)).item()
        assert all_values_are_finite

    def test_extract_returns_float32(self):
        extractor = BasicImageFeatureExtractor()
        test_array = np.full((100, 200, 3), 128, dtype=np.uint8)
        vector = extractor.extract(test_array)
        mx.eval(vector)
        assert vector.dtype == mx.float32
