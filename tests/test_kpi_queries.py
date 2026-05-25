"""Database-backed checks for Day 2 KPI queries."""

from __future__ import annotations

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.kpi import KpiQuery, create_db_engine, load_kpi_queries, run_query


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


def query_by_id(kpi_id: str) -> KpiQuery:
    """Return one parsed KPI query by ID."""
    queries = {query.kpi_id: query for query in load_kpi_queries()}
    return queries[kpi_id]


def assert_kpi_result_is_plausible(kpi_id: str) -> None:
    """Run one KPI query and assert basic data quality expectations."""
    engine = create_db_engine()
    df = run_query(engine, query_by_id(kpi_id))
    assert not df.empty

    identifier_columns = [
        column
        for column in df.columns
        if column in {"procedure_name", "province", "health_authority", "hospital", "source_name", "geo_type"}
    ]
    for column in identifier_columns:
        assert df[column].notna().all(), f"{kpi_id} has null identifier values in {column}"

    for column in df.columns:
        values = df[column].dropna()
        if column in {"median_wait_days", "bc_median", "canada_median", "vch_median", "bc_other_avg_median"}:
            assert ((0 <= values) & (values <= 1000)).all(), f"{kpi_id} has implausible {column}"
        elif column == "p90_wait_days":
            assert ((0 <= values) & (values <= 2000)).all(), f"{kpi_id} has implausible {column}"
        elif column == "pct_meeting_benchmark":
            assert ((0 <= values) & (values <= 100)).all(), f"{kpi_id} has implausible {column}"
        elif column in {"case_volume", "total_case_volume", "n_procedures", "n_rows"}:
            assert (values >= 0).all(), f"{kpi_id} has negative {column}"


@requires_postgres
def test_k01_national_median_wait() -> None:
    assert_kpi_result_is_plausible("K01")


@requires_postgres
def test_k02_provincial_median_wait_top_volume() -> None:
    assert_kpi_result_is_plausible("K02")


@requires_postgres
def test_k03_bc_vs_canada_gap() -> None:
    assert_kpi_result_is_plausible("K03")


@requires_postgres
def test_k04_five_year_median_wait_trend() -> None:
    assert_kpi_result_is_plausible("K04")


@requires_postgres
def test_k05_benchmark_by_procedure_province() -> None:
    assert_kpi_result_is_plausible("K05")


@requires_postgres
def test_k06_p90_tail_risk_by_procedure_province() -> None:
    assert_kpi_result_is_plausible("K06")


@requires_postgres
def test_k07_bc_health_authority_comparison() -> None:
    assert_kpi_result_is_plausible("K07")


@requires_postgres
def test_k08_vch_top_long_wait_procedures() -> None:
    assert_kpi_result_is_plausible("K08")


@requires_postgres
def test_k09_vch_vs_other_ha_gap() -> None:
    assert_kpi_result_is_plausible("K09")


@requires_postgres
def test_k10_vch_hospital_p90() -> None:
    assert_kpi_result_is_plausible("K10")


@requires_postgres
def test_k11_case_volume_trend_by_ha() -> None:
    assert_kpi_result_is_plausible("K11")


@requires_postgres
def test_k12_reporting_coverage_by_source_geo_level() -> None:
    assert_kpi_result_is_plausible("K12")
