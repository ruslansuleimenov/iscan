import mlx.core as mx

def cosine_similarity(
    vector_a, vector_b
):  # Input vectors must be L2-normalized
    return vector_a @ vector_b


def pairwise_similarity(feature_matrix):
    return feature_matrix @ feature_matrix.T

def exclude_self_matches(similarity_matrix):
    image_count = similarity_matrix.shape[0]
    self_match_mask = mx.eye(
        image_count,
        dtype=mx.bool_,
    )
    return mx.where(
        self_match_mask,
        float("-inf"),
        similarity_matrix
    )


