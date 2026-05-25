"""Run Day 3 data quality checks and write a first-run Markdown report."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.ingest import database_url_from_env


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUERY_FILE = PROJECT_ROOT / "sql" / "04_data_quality_checks.sql"
REPORT_FILE = PROJECT_ROOT / "data" / "processed" / "data_quality_first_run.md"
QUALITY_HEADER_RE = re.compile(r"^-- (DQ\d{2}) \| ([^|]+) \| ([^\n]+)$", re.MULTILINE)


@dataclass(frozen=True)
class QualityQuery:
    """A parsed data quality SQL block."""

    check_id: str
    name: str
    audience: str
    sql: str


def load_quality_queries(path: Path = QUERY_FILE) -> list[QualityQuery]:
    """Parse data quality query blocks from the SQL file."""
    sql_text = path.read_text(encoding="utf-8")
    matches = list(QUALITY_HEADER_RE.finditer(sql_text))
    queries: list[QualityQuery] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(sql_text)
        queries.append(
            QualityQuery(
                check_id=match.group(1),
                name=match.group(2).strip(),
                audience=match.group(3).strip(),
                sql=sql_text[start:end].strip(),
            )
        )
    return queries


def create_db_engine() -> Engine:
    """Create a SQLAlchemy engine using the same env pattern as ingest.py."""
    return create_engine(database_url_from_env(), pool_pre_ping=True)


def run_query(engine: Engine, query: QualityQuery) -> pd.DataFrame:
    """Execute one data quality query and return the result as a DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql_query(text(query.sql), conn)


def format_value(value: object) -> str:
    """Format a cell for a Markdown pipe table."""
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return str(value).replace("|", "\\|")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Build a GitHub-flavored Markdown table without optional dependencies."""
    if df.empty:
        return "_No rows returned._"
    headers = [str(column) for column in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in df.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(format_value(value) for value in row) + " |")
    return "\n".join(lines)


def write_report(
    results: Iterable[tuple[QualityQuery, pd.DataFrame]],
    output_path: Path = REPORT_FILE,
) -> None:
    """Write the data quality first-run report."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sections = [
        "# Data Quality First Run",
        "",
        "Generated from public aggregate CIHI and BC_MoH wait-time data.",
        "",
    ]
    for query, df in results:
        sections.extend(
            [
                f"## {query.check_id} — {query.name}",
                "",
                f"Audience: {query.audience}",
                "",
                f"Rows returned: {len(df)}",
                "",
                dataframe_to_markdown(df),
                "",
            ]
        )
    output_path.write_text("\n".join(sections), encoding="utf-8")


def run_all_quality_checks() -> list[tuple[QualityQuery, pd.DataFrame]]:
    """Run all checks in sql/04_data_quality_checks.sql."""
    engine = create_db_engine()
    return [(query, run_query(engine, query)) for query in load_quality_queries()]


def main() -> None:
    """Run quality checks, write the report, and print row-count summary."""
    results = run_all_quality_checks()
    write_report(results)
    for query, df in results:
        print(f"{query.check_id}: {len(df)} rows")


if __name__ == "__main__":
    main()
