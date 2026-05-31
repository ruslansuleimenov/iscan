from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class SimilarityMetric(StrEnum):
    COSINE = "cosine"
    L2 = "l2"


@dataclass(frozen=True, slots=True)
class ScanConfig:
    # Это core-level контракт запуска scan pipeline, а не argparse Namespace.
    input_paths: tuple[Path, ...]
    top_k: int = 5
    metric: SimilarityMetric = SimilarityMetric.COSINE
    report_html: Path = Path("report.html")
    open_report: bool = False
    verbose: int = 0

    def __post_init__(self) -> None:
        # Базовую валидацию держим в core, чтобы будущие CLI/worker/MCP получали одни правила.
        if not self.input_paths:
            msg = "At least one input path is required."
            raise ValueError(msg)

        if self.top_k < 1:
            msg = "top_k must be greater than zero."
            raise ValueError(msg)
