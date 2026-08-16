import mlx.core as mx

from iscan.search.exact_knn import exclude_self_matches, top_k_neighbor_indices
from iscan.search.grouping import group_similar_images, build_groups


class TestGroupSimilarImages:
    def test_group_similar_images(self):

        row_0 = mx.array([1.0, 0.95, 0.0, 0.1], dtype=mx.float32)
        row_1 = mx.array([0.95, 1.0, 0.0, 0.1], dtype=mx.float32)
        row_2 = mx.array([0.0, 0.0, 1.0, 0.92], dtype=mx.float32)
        row_3 = mx.array([0.1, 0.1, 0.92, 1.0], dtype=mx.float32)
        similarity_matrix = mx.stack([row_0, row_1, row_2, row_3])
        masked = exclude_self_matches(similarity_matrix)
        indices = top_k_neighbor_indices(masked, top_k=5)

        result = group_similar_images(masked, indices)
        assert result.parent == [1, 1, 3, 3]

    def test_group_similar_images_no_groups(self):
        row_0 = mx.array([1.0, 0.2, 0.3, 0.1], dtype=mx.float32)
        row_1 = mx.array([0.2, 1.0, 0.0, 0.1], dtype=mx.float32)
        row_2 = mx.array([0.3, 0.0, 1.0, 0.05], dtype=mx.float32)
        row_3 = mx.array([0.1, 0.1, 0.05, 1.0], dtype=mx.float32)
        similarity_matrix = mx.stack([row_0, row_1, row_2, row_3])
        masked = exclude_self_matches(similarity_matrix)
        indices = top_k_neighbor_indices(masked, top_k=5)

        result = group_similar_images(masked, indices)
        similar_groups = build_groups(result)
        assert similar_groups == []
