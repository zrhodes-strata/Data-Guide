from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from connectors.csv_connector import CSVConnector
from core.models import SchemaContract
from outputs.static_report import StaticReportRenderer
from profilers.univariate import profile as run_profile

app = typer.Typer(help="Data Guide — general-purpose EDA tool.")

_VERSION = "0.1.0"


@app.command()
def version() -> None:
    """Show the current version."""
    typer.echo(f"data-guide {_VERSION}")


@app.command()
def validate(
    file: Path = typer.Argument(..., help="Path to data file to validate."),
    metric_col: str = typer.Option("metric", help="Name of the metric column."),
    value_col: str = typer.Option("value", help="Name of the value column."),
    type_col: Optional[str] = typer.Option(None, help="Name of the data_type column (optional)."),
) -> None:
    """Validate that a file matches the expected schema contract."""
    import pandas as pd
    df = pd.read_csv(file)
    errors = []
    if metric_col not in df.columns:
        errors.append(f"metric column '{metric_col}' not found in {list(df.columns)}")
    if value_col not in df.columns:
        errors.append(f"value column '{value_col}' not found in {list(df.columns)}")
    if type_col and type_col not in df.columns:
        errors.append(f"type column '{type_col}' not found in {list(df.columns)}")

    if errors:
        for err in errors:
            typer.echo(f"ERROR: {err}", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Valid: schema contract satisfied for '{file.name}'.")


@app.command()
def profile(
    file: Path = typer.Argument(..., help="Path to data file to profile."),
    output: Path = typer.Option(Path("reports/report.html"), help="Output HTML report path."),
    metric_col: str = typer.Option("metric", help="Name of the metric column."),
    value_col: str = typer.Option("value", help="Name of the value column."),
    type_col: Optional[str] = typer.Option(None, help="Name of the data_type column (optional)."),
    mode: str = typer.Option("unknown", help="Schema mode: long, wide, or unknown."),
) -> None:
    """Profile a data file and generate a static HTML report."""
    sc = SchemaContract(
        metric_col=metric_col,
        value_col=value_col,
        type_col=type_col,
        mode=mode,  # type: ignore[arg-type]
    )
    connector = CSVConnector(path=str(file), schema=sc)
    connector.connect()
    gdf = connector.load()

    result = run_profile(gdf, output_dir=str(output.parent))

    renderer = StaticReportRenderer()
    renderer.render(result, output_path=str(output))
    typer.echo(f"Report written to {output}")


if __name__ == "__main__":
    app()
