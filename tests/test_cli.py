from pathlib import Path

import pytest

from iscan.cli import build_parser, main, normalize_cli_args, positive_int


def test_short_scan_form_is_rewritten_to_scan_command() -> None:
    assert normalize_cli_args(["/photos"]) == ["scan", "/photos"]


def test_explicit_scan_form_is_left_unchanged() -> None:
    assert normalize_cli_args(["scan", "/photos"]) == ["scan", "/photos"]


def test_option_first_args_are_left_unchanged() -> None:
    assert normalize_cli_args(["--help"]) == ["--help"]


def test_scan_parser_accepts_mvp_options() -> None:
    parser = build_parser()

    namespace = parser.parse_args(
        [
            "scan",
            "/photos",
            "--top-k",
            "3",
            "--metric",
            "l2",
            "--report-html",
            "out.html",
            "--open-report",
            "-vv",
        ]
    )

    assert namespace.paths == [Path("/photos")]
    assert namespace.top_k == 3
    assert namespace.metric == "l2"
    assert namespace.report_html == Path("out.html")
    assert namespace.open_report is True
    assert namespace.verbose == 2


def test_positive_int_rejects_zero() -> None:
    with pytest.raises(Exception, match="greater than zero"):
        positive_int("0")


def test_main_returns_zero_for_short_scan_form() -> None:
    assert main(["/photos"]) == 0
