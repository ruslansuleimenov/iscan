from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from iscan.config import DUPLICATE_SIMILARITY_THRESHOLD
from iscan.pipeline import ScanResult, run_scan

app = typer.Typer()


@app.command()
def scan(
    path: Path = typer.Argument(Path(".")),
    top_k: int = typer.Option(5, "--top-k", "-k"),
    threshold: float = typer.Option(DUPLICATE_SIMILARITY_THRESHOLD, "--threshold", "-t"),
):
    result = run_scan(path, top_k, threshold)
    render_report(result)


def render_report(result: ScanResult) -> None:
    console = Console()

    if not result.groups:
        console.print("No duplicate or near-duplicate photos found.")
    else:
        for group_number, group in enumerate(result.groups, start=1):
            table = Table(title=f"Group {group_number} ({len(group)} photos)")
            table.add_column("Path")
            table.add_column("Resolution")
            table.add_column("Format")
            table.add_column("Size")
            table.add_column("Captured At")
            for index in group:
                path, metadata = result.images[index]
                table.add_row(
                    str(path),
                    f"{metadata.width}x{metadata.height}",
                    metadata.format,
                    f"{metadata.size_bytes / 1024:.1f} KB",
                    str(metadata.captured_at) if metadata.captured_at else "-",
                )
            console.print(table)

    console.print(
        f"\nScanned {len(result.images)} photo(s), found {len(result.groups)} group(s)."
    )

    if result.warnings:
        console.print("\n[yellow]Warnings:[/yellow]")
        for warning in result.warnings:
            console.print(f"[yellow]- {warning}[/yellow]")
