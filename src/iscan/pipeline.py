from dataclasses import dataclass
from pathlib import Path
import mlx.core as mx

from iscan.domain.models import ImageMetadata
from iscan.features.image_basic import BasicImageFeatureExtractor
from iscan.scanning.decoder import ImageDecoder, ImageDecodeError
from iscan.scanning.metadata import MetadataExtractor
from iscan.scanning.scanner import LocalDirectorySource
from iscan.search.exact_knn import pairwise_similarity, exclude_self_matches, top_k_neighbor_indices
from iscan.search.grouping import group_similar_images, build_groups
from iscan.config import DUPLICATE_SIMILARITY_THRESHOLD

@dataclass
class ScanResult:
    images: list[tuple[Path, ImageMetadata]]
    groups: list[list[int]]
    warnings: list[str]

def run_scan(root, top_k=5, threshold=DUPLICATE_SIMILARITY_THRESHOLD):
    local_directory_source = LocalDirectorySource(root)
    images = local_directory_source.find_images()
    warnings = []
    metadata_list = []
    feature_vector_list = []
    for image in images:
        image_decoder = ImageDecoder()
        try:
            pixels = image_decoder.decode(image)
        except ImageDecodeError as e:
            warnings.append(str(e))
            continue
        metadata_extractor = MetadataExtractor()
        metadata = metadata_extractor.extract(image, pixels)
        metadata_list.append((image, metadata))
        feature_extractor = BasicImageFeatureExtractor()
        feature_vector = feature_extractor.extract(pixels)
        feature_vector_list.append(feature_vector)
    if len(feature_vector_list) == 0:
        return ScanResult(images=[], groups=[], warnings=warnings)
    feature_matrix = mx.stack(feature_vector_list)
    similarity_matrix = pairwise_similarity(feature_matrix)
    masked_matrix = exclude_self_matches(similarity_matrix)
    top_k_n_indices = top_k_neighbor_indices(masked_matrix, top_k=top_k)
    grouped_similar_images = group_similar_images(masked_matrix, top_k_n_indices, threshold=threshold)
    groups = build_groups(grouped_similar_images)
    scan_result = ScanResult(images=metadata_list, groups=groups, warnings=warnings)
    return scan_result


