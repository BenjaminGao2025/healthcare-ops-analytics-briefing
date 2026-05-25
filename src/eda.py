"""Generate Day 4 exploratory analysis artifacts and analyst report."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.ingest import database_url_from_env


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EDA_SUMMARY_FILE = PROJECT_ROOT / "data" / "processed" / "eda_summary.md"
ANALYST_REPORT_FILE = PROJECT_ROOT / "reports" / "analyst_report.md"
NOTEBOOK_FILE = PROJECT_ROOT / "notebooks" / "01_eda_wait_times.ipynb"


def create_db_engine() -> Engine:
    """Create a SQLAlchemy engine using the same env pattern as ingest.py."""
    return create_engine(database_url_from_env(), pool_pre_ping=True)


def read_sql(engine: Engine, sql: str) -> pd.DataFrame:
    """Read one SQL query into a DataFrame."""
    with engine.connect() as conn:
        return pd.read_sql_query(text(sql), conn)


def format_value(value: object) -> str:
    """Format a value for Markdown output."""
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value).replace("|", "\\|")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Build a Markdown pipe table without optional dependencies."""
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


def load_eda_frames(engine: Engine) -> dict[str, pd.DataFrame]:
    """Load the Day 4 analysis frames from PostgreSQL."""
    return {
        "source_counts": read_sql(
            engine,
            """
            SELECT
              source_name,
              COUNT(*) AS row_count,
              MIN(reporting_year) AS min_year,
              MAX(reporting_year) AS max_year
            FROM fact_wait_time
            GROUP BY source_name
            ORDER BY source_name
            """,
        ),
        "national_snapshot": read_sql(
            engine,
            """
            WITH latest_year AS (
              SELECT MAX(reporting_year) AS reporting_year
              FROM fact_wait_time
              WHERE source_name = 'CIHI'
            )
            SELECT
              p.procedure_name,
              ROUND(f.median_wait_days::numeric, 1) AS median_wait_days,
              ROUND(f.p90_wait_days::numeric, 1) AS p90_wait_days,
              ROUND(f.pct_meeting_benchmark::numeric, 1) AS pct_meeting_benchmark,
              f.case_volume
            FROM fact_wait_time AS f
            JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
            JOIN dim_geography AS g ON g.geo_id = f.geo_id
            JOIN latest_year AS y ON y.reporting_year = f.reporting_year
            WHERE f.source_name = 'CIHI'
              AND g.geo_name = 'Canada'
            ORDER BY f.case_volume DESC NULLS LAST, p.procedure_name
            """,
        ),
        "bc_gaps": read_sql(
            engine,
            """
            WITH latest_year AS (
              SELECT MAX(reporting_year) AS reporting_year
              FROM fact_wait_time
              WHERE source_name = 'CIHI'
            ),
            comparison AS (
              SELECT
                f.procedure_id,
                MAX(CASE WHEN g.geo_name = 'British Columbia' THEN f.median_wait_days END) AS bc_median,
                MAX(CASE WHEN g.geo_name = 'Canada' THEN f.median_wait_days END) AS canada_median
              FROM fact_wait_time AS f
              JOIN dim_geography AS g ON g.geo_id = f.geo_id
              JOIN latest_year AS y ON y.reporting_year = f.reporting_year
              WHERE f.source_name = 'CIHI'
                AND g.geo_name IN ('British Columbia', 'Canada')
              GROUP BY f.procedure_id
            )
            SELECT
              p.procedure_name,
              ROUND(c.bc_median::numeric, 1) AS bc_median,
              ROUND(c.canada_median::numeric, 1) AS canada_median,
              ROUND((c.bc_median - c.canada_median)::numeric, 1) AS gap_days
            FROM comparison AS c
            JOIN dim_procedure AS p ON p.procedure_id = c.procedure_id
            WHERE c.bc_median IS NOT NULL
              AND c.canada_median IS NOT NULL
            ORDER BY gap_days DESC, p.procedure_name
            LIMIT 10
            """,
        ),
        "vch_long_waits": read_sql(
            engine,
            """
            WITH latest_year AS (
              SELECT MAX(reporting_year) AS reporting_year
              FROM fact_wait_time
              WHERE source_name = 'BC_MoH'
            )
            SELECT
              p.procedure_name,
              ROUND(f.median_wait_days::numeric, 1) AS median_wait_days,
              ROUND(f.p90_wait_days::numeric, 1) AS p90_wait_days,
              f.case_volume
            FROM fact_wait_time AS f
            JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
            JOIN dim_geography AS g ON g.geo_id = f.geo_id
            JOIN latest_year AS y ON y.reporting_year = f.reporting_year
            WHERE f.source_name = 'BC_MoH'
              AND g.geo_name = 'Vancouver Coastal'
              AND g.geo_type = 'health_authority'
              AND f.median_wait_days IS NOT NULL
            ORDER BY f.median_wait_days DESC, p.procedure_name
            LIMIT 10
            """,
        ),
        "quality_caveats": read_sql(
            engine,
            """
            SELECT
              source_name,
              COUNT(*) AS total_rows,
              COUNT(*) FILTER (WHERE median_wait_days IS NULL) AS missing_median_wait_days,
              ROUND(
                COUNT(*) FILTER (WHERE median_wait_days IS NULL)::numeric / NULLIF(COUNT(*), 0) * 100,
                1
              ) AS missing_median_wait_days_pct,
              COUNT(*) FILTER (WHERE case_volume IS NULL) AS missing_case_volume,
              ROUND(
                COUNT(*) FILTER (WHERE case_volume IS NULL)::numeric / NULLIF(COUNT(*), 0) * 100,
                1
              ) AS missing_case_volume_pct
            FROM fact_wait_time
            GROUP BY source_name
            ORDER BY source_name
            """,
        ),
    }


def build_eda_summary(frames: dict[str, pd.DataFrame] | None = None) -> str:
    """Build a compact EDA summary from loaded frames."""
    if frames is None:
        frames = load_eda_frames(create_db_engine())
    sections = [
        "# EDA Summary",
        "",
        "Generated from the loaded public aggregate wait-time warehouse.",
        "",
        "## Source Counts",
        "",
        dataframe_to_markdown(frames["source_counts"]),
        "",
        "## National Snapshot",
        "",
        dataframe_to_markdown(frames["national_snapshot"].head(10)),
        "",
        "## BC vs Canada Gaps",
        "",
        dataframe_to_markdown(frames["bc_gaps"].head(10)),
        "",
        "## Vancouver Coastal Long Waits",
        "",
        dataframe_to_markdown(frames["vch_long_waits"].head(10)),
        "",
        "## Quality Caveats",
        "",
        dataframe_to_markdown(frames["quality_caveats"]),
        "",
    ]
    return "\n".join(sections)


def build_analyst_report(frames: dict[str, pd.DataFrame] | None = None) -> str:
    """Build the Day 4 analyst-facing Markdown report."""
    if frames is None:
        frames = load_eda_frames(create_db_engine())

    top_gap = frames["bc_gaps"].iloc[0]
    top_vch = frames["vch_long_waits"].iloc[0]
    bc_quality = frames["quality_caveats"].query("source_name == 'BC_MoH'").iloc[0]

    sections = [
        "# Analyst Report",
        "",
        "## Executive Readout",
        "",
        (
            f"The largest latest-year BC vs Canada median-wait gap is {top_gap.procedure_name} "
            f"at {top_gap.gap_days:.1f} days. In Vancouver Coastal, the longest latest-fiscal-year "
            f"median wait is {top_vch.procedure_name} at {top_vch.median_wait_days:.1f} days."
        ),
        "",
        (
            f"Data quality is suitable for a portfolio dashboard, with no duplicate fact keys or impossible "
            f"wait values from Day 3 checks. The main caveat is BC_MoH case-volume suppression: "
            f"{int(bc_quality.missing_case_volume):,} rows ({bc_quality.missing_case_volume_pct:.1f}%) "
            "have null case volume and should stay visibly labeled rather than filled."
        ),
        "",
        "## National Wait-Time Snapshot",
        "",
        dataframe_to_markdown(frames["national_snapshot"].head(8)),
        "",
        "## BC vs Canada Gaps",
        "",
        dataframe_to_markdown(frames["bc_gaps"].head(8)),
        "",
        "## Vancouver Coastal Operational View",
        "",
        dataframe_to_markdown(frames["vch_long_waits"].head(10)),
        "",
        "## Data Quality Caveats",
        "",
        dataframe_to_markdown(frames["quality_caveats"]),
        "",
        "## Suggested Dashboard Implications",
        "",
        "- Put BC vs Canada gaps in the executive summary, because they translate directly into leadership-facing variance.",
        "- Put Vancouver Coastal procedure waits in the operational drilldown, because this is where managers can inspect local pressure points.",
        "- Put missingness and suppressed case-volume rates in the data quality tab, because these limits affect interpretation.",
        "",
    ]
    return "\n".join(sections)


def notebook_json() -> dict[str, object]:
    """Return a valid nbformat notebook for Day 4 EDA work."""
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# EDA: Wait Times\n",
                "\n",
                "Purpose: inspect loaded public aggregate wait-time data, review missingness, and produce analyst-ready tables for the portfolio dashboard.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from src.eda import create_db_engine, load_eda_frames\n",
                "\n",
                "engine = create_db_engine()\n",
                "frames = load_eda_frames(engine)\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["frames['source_counts']\n"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["frames['national_snapshot'].head(10)\n"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["frames['bc_gaps'].head(10)\n"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["frames['vch_long_waits'].head(10)\n"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["frames['quality_caveats']\n"],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Interpretation Notes\n",
                "\n",
                "- TODO: Confirm which national snapshot rows are most useful for the executive dashboard.\n",
                "- TODO: Decide whether Vancouver Coastal long-wait categories should be grouped for display.\n",
                "- TODO: Carry data quality caveats into the dashboard copy without overloading the first screen.\n",
            ],
        },
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_day4_artifacts() -> dict[str, Path]:
    """Write Day 4 summary, analyst report, and notebook artifacts."""
    frames = load_eda_frames(create_db_engine())
    EDA_SUMMARY_FILE.write_text(build_eda_summary(frames), encoding="utf-8")
    ANALYST_REPORT_FILE.write_text(build_analyst_report(frames), encoding="utf-8")
    NOTEBOOK_FILE.write_text(json.dumps(notebook_json(), indent=2) + "\n", encoding="utf-8")
    return {
        "eda_summary": EDA_SUMMARY_FILE,
        "analyst_report": ANALYST_REPORT_FILE,
        "notebook": NOTEBOOK_FILE,
    }


def main() -> None:
    """Generate Day 4 EDA artifacts and print written paths."""
    written = write_day4_artifacts()
    for name, path in written.items():
        print(f"{name}: {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
