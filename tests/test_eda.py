"""Tests for Day 4 EDA report generation."""

from __future__ import annotations

import json

import pytest
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from src.eda import ANALYST_REPORT_FILE, EDA_SUMMARY_FILE, NOTEBOOK_FILE, build_analyst_report
from src.ingest import database_url_from_env


def postgres_unreachable() -> bool:
    try:
        engine = sa.create_engine(database_url_from_env(), pool_pre_ping=True)
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        return False
    except SQLAlchemyError:
        return True


requires_postgres = pytest.mark.skipif(
    postgres_unreachable(),
    reason="Postgres is unreachable; start it with `make up` and load data with `make load`.",
)


@requires_postgres
def test_build_analyst_report_includes_required_sections() -> None:
    report = build_analyst_report()
    required_sections = [
        "# Analyst Report",
        "## Executive Readout",
        "## National Wait-Time Snapshot",
        "## BC vs Canada Gaps",
        "## Vancouver Coastal Operational View",
        "## Data Quality Caveats",
    ]
    for section in required_sections:
        assert section in report


def test_d4_output_paths_are_project_artifacts() -> None:
    assert EDA_SUMMARY_FILE.as_posix().endswith("data/processed/eda_summary.md")
    assert ANALYST_REPORT_FILE.as_posix().endswith("reports/analyst_report.md")
    assert NOTEBOOK_FILE.as_posix().endswith("notebooks/01_eda_wait_times.ipynb")


def test_notebook_is_valid_json() -> None:
    with NOTEBOOK_FILE.open(encoding="utf-8") as file:
        notebook = json.load(file)
    assert notebook["nbformat"] == 4
    assert notebook["nbformat_minor"] == 5
