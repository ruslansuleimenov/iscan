from pathlib import Path

import typer

from iscan.pipeline import run_scan
from iscan.config import DUPLICATE_SIMILARITY_THRESHOLD
app = typer.Typer()

@app.command()
def scan(
    path: Path = typer.Argument(Path(".")),
    top_k: int = typer.Option(5, "--top-k", "-k"),
    threshold: float = typer.Option(DUPLICATE_SIMILARITY_THRESHOLD, "--threshold", "-t"),
):
    result = run_scan(path, top_k, threshold)
    print(result)
