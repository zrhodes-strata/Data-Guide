import json
from pathlib import Path
from typing import List, Optional

import pandas as pd
import typer
import yaml

from data_profiler import DataProfiler
from data_pipeline.bivariate_profiler import BivariateProfiler

app = typer.Typer(help="Run data profiling based on a configuration file.")


def load_config(path: Path) -> dict:
    """Load YAML or JSON configuration."""
    with open(path, "r") as f:
        if path.suffix in {".yaml", ".yml"}:
            return yaml.safe_load(f)
        return json.load(f)


@app.command()
def profile(
    config: Path = typer.Argument(..., help="Path to YAML/JSON configuration."),
) -> None:
    """Run profiling for datasets defined in the configuration."""
    cfg_path = config.resolve()
    cfg = load_config(cfg_path)

    api_key = cfg.get("api_key")  # Currently unused
    datasets = cfg.get("datasets", {})
    output_dir = Path(cfg.get("output_dir", "profiling_reports"))
    format = cfg.get("format", "markdown")
    analyses = cfg.get("analyses", ["dataset", "columns"])


    for name, ds in datasets.items():
        path = Path(ds["path"])
        if not path.is_absolute():
            path = (cfg_path.parent / path).resolve()
        df = pd.read_csv(path)

        fields: Optional[List[str]] = ds.get("fields")
        if fields:
            df = df[fields]

        types = ds.get("types", {})

        profiler = DataProfiler(df, custom_types=types)
        if "dataset" in analyses:
            profiler.profile_dataset()
        if "columns" in analyses:
            profiler.profile_columns()

        out_dir = (output_dir / name).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        ext = "md" if format == "markdown" else format

        report = profiler.generate_report(format, output_filename=f"{name}_report.{ext}")

        with open(out_dir / f"{name}_report.{ext}", "w") as f:
            f.write(report)

        if "bivariate" in analyses:
            pairs = ds.get("bivariate_pairs", [])
            bivariate = BivariateProfiler(df, output_dir=str(out_dir / "bivariate"))
            if pairs:
                for p in pairs:
                    if len(p) == 2:
                        bivariate.scatter_plot(p[0], p[1])
            bivariate.correlation_analysis()

    typer.echo("Profiling complete.")


if __name__ == "__main__":
    app()
