from __future__ import annotations

from pathlib import Path

import pandas as pd

from connectors.base import BaseConnector
from core.models import GuideDataFrame, SchemaContract


class SQLiteConnector(BaseConnector):
    def __init__(self, path: str, query: str, schema: SchemaContract) -> None:
        self._path = Path(path)
        self._query = query
        self._schema = schema

    def connect(self) -> None:
        if not self._path.exists():
            raise FileNotFoundError(f"SQLite file not found: {self._path}")

    def load(self) -> GuideDataFrame:
        import sqlite3
        conn = sqlite3.connect(self._path)
        df = pd.read_sql_query(self._query, conn)
        conn.close()
        return GuideDataFrame(
            df=df,
            schema=self._schema,
            source_type="sqlite",
            origin=str(self._path),
        )
