from iscan.search.exact_knn import cosine_similarity, pairwise_similarity, exclude_self_matches
import mlx.core as mx
import pytest


class TestCosineSimilarity:
    def test_cosine_similarity_equal_one(self):
        vector_a = mx.array([1.0, 0.0, 0.0], dtype=mx.float32)
        vector_b = mx.array([1.0, 0.0, 0.0], dtype=mx.float32)
        score = cosine_similarity(vector_a, vector_b).item()
        assert score == pytest.approx(1.0)


    def test_cosine_similarity_equal_zero(self):
        vector_a = mx.array([1.0, 0.0, 0.0], dtype=mx.float32)
        vector_b = mx.array([0.0, 1.0, 0.0], dtype=mx.float32)
        score = cosine_similarity(vector_a, vector_b).item()
        assert score == pytest.approx(0.0)

    def test_cosine_similarity_returns_intermediate_score(self):
        vector_a = mx.array([1.0, 0.0], dtype=mx.float32)
        vector_b = mx.array([0.6, 0.8], dtype=mx.float32)
        score = cosine_similarity(vector_a, vector_b).item()
        assert score == pytest.approx(0.6)


class TestPairwiseSimilarity:
    def test_pairwise_similarity(self):
        vector_a = mx.array([1.0, 0.0], dtype=mx.float32)
        vector_b = mx.array([0.0, 1.0], dtype=mx.float32)
        vector_c = mx.array([0.6, 0.8], dtype=mx.float32)
        feature_matrix = mx.stack([vector_a, vector_b, vector_c])
        assert feature_matrix.shape == (3, 2)
        matrix = pairwise_similarity(feature_matrix)
        assert matrix.shape == (3, 3)
        assert matrix[0, 0].item() == pytest.approx(1.0)
        assert matrix[0, 1].item() == pytest.approx(0.0)
        assert matrix[0, 2].item() == pytest.approx(0.6)
        assert matrix[0, 2].item() == pytest.approx(
            matrix[2, 0].item()
        )

class TestExcludeSelfMatches:
    def test_exclude_self_matches(self):
        row_0 = mx.array([1.0, 0.6, 0.0], dtype=mx.float32)
        row_1 = mx.array([0.6, 1.0, 0.8], dtype=mx.float32)
        row_2 = mx.array([0.0, 0.8, 1.0], dtype=mx.float32)
        similarity_matrix = mx.stack([row_0, row_1, row_2])
        masked_matrix = exclude_self_matches(similarity_matrix)
        assert mx.isneginf(masked_matrix[0, 0]).item()
        assert mx.isneginf(masked_matrix[1, 1]).item()
        assert mx.isneginf(masked_matrix[2, 2]).item()
        assert masked_matrix[0, 1].item() == pytest.approx(0.6)
        assert masked_matrix[1, 2].item() == pytest.approx(0.8)
