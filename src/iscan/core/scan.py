from dataclasses import dataclass
from pathlib import Path

from iscan.core.config import ScanConfig


@dataclass(frozen=True, slots=True)
class ScanBootstrapResult:
    input_paths: tuple[Path, ...]
    top_k: int
    metric: str
    report_html: Path
    open_report: bool


def bootstrap_scan(config: ScanConfig) -> ScanBootstrapResult:
    # Временный bootstrap для Phase 2: CLI уже вызывает core, реальный pipeline появится дальше.
    return ScanBootstrapResult(
        input_paths=config.input_paths,
        top_k=config.top_k,
        metric=config.metric.value,
        report_html=config.report_html,
        open_report=config.open_report,
    )
