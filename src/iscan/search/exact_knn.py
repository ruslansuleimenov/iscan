def cosine_similarity(
    vector_a, vector_b
):  # Входные векторы должны быть L2-нормализованы.
    return vector_a @ vector_b


def pairwise_similarity(feature_matrix):
    return feature_matrix @ feature_matrix.T

