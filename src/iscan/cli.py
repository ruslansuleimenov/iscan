import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from rich.console import Console

from iscan import __version__
from iscan.core import ScanConfig, SimilarityMetric
from iscan.core.scan import bootstrap_scan

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="iscan",
        description="Find duplicate and near-duplicate photos on local disk.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    add_scan_arguments(parser)

    return parser


def add_scan_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Photo files or directories to scan. Default: current directory.",
    )
    parser.add_argument(
        "--top-k",
        type=positive_int,
        default=5,
        help="Number of nearest candidates per image. Default: 5.",
    )
    parser.add_argument(
        "--metric",
        choices=[metric.value for metric in SimilarityMetric],
        default=SimilarityMetric.COSINE.value,
        help="Similarity metric to use. Default: cosine.",
    )
    parser.add_argument(
        "--report-html",
        type=Path,
        default=Path("report.html"),
        help="Path to the generated HTML report. Default: report.html.",
    )
    parser.add_argument(
        "--open-report",
        action="store_true",
        help="Open the HTML report after generation.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase log verbosity. Can be passed multiple times.",
    )


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        msg = "must be greater than zero"
        raise argparse.ArgumentTypeError(msg)
    return parsed


def run_scan_command(namespace: argparse.Namespace) -> int:
    # CLI остается тонким адаптером: парсит аргументы и передает typed config в core.
    input_paths = namespace.paths or [Path.cwd()]
    config = ScanConfig(
        input_paths=tuple(input_paths),
        top_k=namespace.top_k,
        metric=SimilarityMetric(namespace.metric),
        report_html=namespace.report_html,
        open_report=namespace.open_report,
        verbose=namespace.verbose,
    )
    run_scan(config)
    return 0


def run_scan(config: ScanConfig) -> None:
    result = bootstrap_scan(config)
    console.print("[yellow]Scan pipeline is not implemented yet.[/yellow]")
    console.print(f"metric: {result.metric}")
    console.print(f"top_k: {result.top_k}")
    console.print(f"report_html: {result.report_html}")
    console.print(f"open_report: {result.open_report}")
    console.print("input_paths:")
    for path in result.input_paths:
        console.print(f"- {path}")


def main(argv: Sequence[str] | None = None) -> int:
    raw_args = sys.argv[1:] if argv is None else list(argv)
    parser = build_parser()
    namespace = parser.parse_args(raw_args)
    return run_scan_command(namespace)


if __name__ == "__main__":
    raise SystemExit(main())
