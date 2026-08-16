from iscan.config import DUPLICATE_SIMILARITY_THRESHOLD

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))


    def find(self, i):
        while self.parent[i] != i:
            i = self.parent[i]
        return i


    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
        return self.parent[root_i]


def group_similar_images(similarity_matrix, top_k_indices, threshold=DUPLICATE_SIMILARITY_THRESHOLD):
    n = similarity_matrix.shape[0]

    dsj = DisjointSet(n)
    for i in range(n):
        for j in top_k_indices[i].tolist():
            similarity = similarity_matrix[i, j]
            if similarity >= threshold:
                dsj.union(i, j)
    return dsj


def build_groups(disjoint_set):
    n = len(disjoint_set.parent)
    my_dict = {}
    for i in range(n):
        root = disjoint_set.find(i)
        my_dict.setdefault(root, []).append(i)
    result = []
    for group in my_dict.values():
        if len(group) > 1:
            result.append(group)
    return result