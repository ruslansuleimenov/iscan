from pathlib import Path

import pytest

from iscan.core import ScanConfig, SimilarityMetric


def test_scan_config_accepts_mvp_defaults() -> None:
    config = ScanConfig(input_paths=(Path("/photos"),))

    assert config.top_k == 5
    assert config.metric is SimilarityMetric.COSINE
    assert config.report_html == Path("report.html")
    assert config.open_report is False


def test_scan_config_rejects_empty_input_paths() -> None:
    with pytest.raises(ValueError, match="At least one input path"):
        ScanConfig(input_paths=())


def test_scan_config_rejects_non_positive_top_k() -> None:
    with pytest.raises(ValueError, match="top_k"):
        ScanConfig(input_paths=(Path("/photos"),), top_k=0)
