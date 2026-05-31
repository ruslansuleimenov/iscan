import argparse
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import cast

from rich.console import Console

from iscan import __version__
from iscan.core import ScanConfig, SimilarityMetric
from iscan.core.scan import bootstrap_scan

console = Console()


def normalize_cli_args(args: Sequence[str]) -> list[str]:
    normalized = list(args)
    # Короткая форма `iscan /path` должна вести себя как `iscan scan /path`.
    if normalized and not normalized[0].startswith("-") and normalized[0] != "scan":
        return ["scan", *normalized]
    return normalized


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="iscan",
        description="Find duplicate and near-duplicate photos on local disk.",
    )
    parser.add_argument("--version", action="version", version=__version__)

    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan local photo files or directories.",
        description="Scan local photo files or directories.",
    )
    add_scan_arguments(scan_parser)
    scan_parser.set_defaults(handler=run_scan_command)

    return parser


def add_scan_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Photo files or directories to scan.",
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
    config = ScanConfig(
        input_paths=tuple(namespace.paths),
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
    namespace = parser.parse_args(normalize_cli_args(raw_args))
    raw_handler = getattr(namespace, "handler", None)
    if raw_handler is None:
        parser.print_help()
        return 0
    # argparse хранит handler динамически в Namespace, поэтому тип уточняем явно.
    handler = cast(Callable[[argparse.Namespace], int], raw_handler)
    return handler(namespace)


if __name__ == "__main__":
    raise SystemExit(main())
