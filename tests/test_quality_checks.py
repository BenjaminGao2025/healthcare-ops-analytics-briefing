"""Database-backed checks for Day 3 data quality queries."""

from __future__ import annotations

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.quality import QualityQuery, create_db_engine, load_quality_queries, run_query


def postgres_unreachable() -> bool:
    """Return True when the local Postgres container is not reachable."""
    try:
        engine = create_db_engine()
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        return False
    except SQLAlchemyError:
        return True


requires_postgres = pytest.mark.skipif(
    postgres_unreachable(),
    reason="Postgres is unreachable; start it with `make up` and load data with `make load`.",
)


def query_by_id(check_id: str) -> QualityQuery:
    """Return one parsed quality query by ID."""
    queries = {query.check_id: query for query in load_quality_queries()}
    return queries[check_id]


def assert_quality_result_shape(check_id: str, expected_columns: set[str]) -> None:
    """Run one quality query and assert it returns the expected columns."""
    engine = create_db_engine()
    df = run_query(engine, query_by_id(check_id))
    assert expected_columns.issubset(set(df.columns))


@requires_postgres
def test_dq01_row_counts_per_source_year() -> None:
    assert_quality_result_shape("DQ01", {"source_name", "reporting_year", "row_count"})


@requires_postgres
def test_dq02_missing_values_per_source() -> None:
    assert_quality_result_shape(
        "DQ02",
        {
            "source_name",
            "total_rows",
            "missing_median_wait_days",
            "missing_median_wait_days_pct",
            "missing_case_volume",
            "missing_case_volume_pct",
        },
    )


@requires_postgres
def test_dq03_duplicate_fact_keys() -> None:
    assert_quality_result_shape("DQ03", {"source_name", "duplicate_key_count", "duplicate_row_count"})


@requires_postgres
def test_dq04_out_of_range_values() -> None:
    assert_quality_result_shape("DQ04", {"issue_type", "bad_row_count"})


@requires_postgres
def test_dq05_category_drift() -> None:
    assert_quality_result_shape("DQ05", {"issue_type", "bad_row_count"})


@requires_postgres
def test_dq06_freshness_by_source() -> None:
    assert_quality_result_shape("DQ06", {"source_name", "max_loaded_at", "freshness_status"})


@requires_postgres
def test_dq07_reporting_coverage() -> None:
    assert_quality_result_shape(
        "DQ07",
        {"source_name", "geo_type", "reporting_year", "n_procedures", "n_rows"},
    )


@requires_postgres
def test_dq08_suppressed_count_summary() -> None:
    assert_quality_result_shape(
        "DQ08",
        {"source_name", "total_rows", "suppressed_case_volume_rows", "suppressed_case_volume_pct"},
    )
