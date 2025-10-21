from __future__ import annotations

"""Compatibility wrappers around the modern profiling toolkit.

This module previously contained the full implementation of the profiling
classes.  The canonical implementations now live in :mod:`data_profiler`.  The
symbols are re-exported here to avoid breaking legacy imports.
"""

from data_profiler import (  # noqa: F401 - re-exported symbols
    DataProfiler,
    DataProfilerPlots,
    NumericProfiler,
    StringProfiler,
    TemporalAnalyzer,
    TypeResolver,
)

__all__ = [
    "DataProfiler",
    "DataProfilerPlots",
    "NumericProfiler",
    "StringProfiler",
    "TemporalAnalyzer",
    "TypeResolver",
]


if __name__ == "__main__":  # pragma: no cover
    import pandas as pd

    df = pd.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie", "Bob", "Alice"],
            "Age": [25, 30, 35, 30, 25],
            "JoinDate": ["2022-01-01", "2022-02-15", "2022-03-10", "2022-02-15", "2022-01-01"],
            "Comments": ["#Hello", "@Bob", "Test123", "ZZZZ", "None"],
        }
    )

    profiler = DataProfiler(df, custom_types={"JoinDate": "date"}, output_dir="./profile_output")
    profiler.profile_dataset(include_bivariate=False)
    profiler.generate_report("markdown", "legacy_profile.md")
