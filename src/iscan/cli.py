import sys
from pathlib import Path
from typing import Annotated

import typer

from iscan import __version__

app = typer.Typer(
    name="iscan",
    help="Find duplicate and near-duplicate photos on local disk.",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def root(
    version: Annotated[
        bool,
        typer.Option("--version", callback=_version_callback, help="Show version and exit."),
    ] = False,
) -> None:
    return None


@app.command()
def scan(
    paths: Annotated[list[Path], typer.Argument(help="Photo files or directories to scan.")],
) -> None:
    _scan(paths)


def _scan(paths: list[Path]) -> None:
    typer.echo("Scan pipeline is not implemented yet.")
    for path in paths:
        typer.echo(f"- {path}")


def main() -> None:
    args = sys.argv[1:]
    if args and not args[0].startswith("-") and args[0] != "scan":
        args = ["scan", *args]
    app(args=args)
