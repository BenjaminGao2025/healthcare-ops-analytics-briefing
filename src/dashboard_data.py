"""Shared data access helpers for Streamlit dashboard pages."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from src.eda import create_db_engine
from src.kpi import KpiQuery, load_kpi_queries, run_query as run_kpi_query
from src.quality import QualityQuery, load_quality_queries, run_query as run_quality_query


KPI_FRAME_MAP = {
    "K01": "executive_national",
    "K03": "bc_gaps",
    "K04": "national_trend",
    "K06": "tail_risk",
    "K07": "ha_comparison",
    "K08": "vch_long_waits",
    "K09": "vch_vs_other",
    "K10": "vch_hospital_p90",
    "K11": "ha_volume_trend",
}

QUALITY_FRAME_MAP = {
    "DQ02": "quality_missingness",
    "DQ03": "quality_duplicates",
    "DQ04": "quality_validity",
    "DQ06": "quality_freshness",
    "DQ08": "suppressed_counts",
}


def _queries_by_id(queries: Iterable[KpiQuery | QualityQuery]) -> dict[str, KpiQuery | QualityQuery]:
    """Return parsed query objects keyed by check/KPI id."""
    keyed = {}
    for query in queries:
        key = getattr(query, "kpi_id", None) or getattr(query, "check_id")
        keyed[key] = query
    return keyed


def load_dashboard_frames() -> dict[str, pd.DataFrame]:
    """Load all datasets needed by the Streamlit dashboard."""
    engine = create_db_engine()
    kpi_queries = _queries_by_id(load_kpi_queries())
    quality_queries = _queries_by_id(load_quality_queries())

    frames: dict[str, pd.DataFrame] = {}
    for query_id, frame_name in KPI_FRAME_MAP.items():
        frames[frame_name] = run_kpi_query(engine, kpi_queries[query_id])
    for query_id, frame_name in QUALITY_FRAME_MAP.items():
        frames[frame_name] = run_quality_query(engine, quality_queries[query_id])
    return frames


def dashboard_summary(frames: dict[str, pd.DataFrame]) -> dict[str, object]:
    """Return headline dashboard metrics from loaded frames."""
    top_gap = frames["bc_gaps"].iloc[0]
    top_vch = frames["vch_long_waits"].iloc[0]
    bc_missing = frames["quality_missingness"].query("source_name == 'BC_MoH'").iloc[0]
    validity_issues = int(frames["quality_validity"]["bad_row_count"].sum())
    duplicate_rows = int(frames["quality_duplicates"]["duplicate_row_count"].sum())
    freshness_statuses = sorted(set(frames["quality_freshness"]["freshness_status"].astype(str)))
    return {
        "top_gap_procedure": str(top_gap.procedure_name),
        "top_gap_days": float(top_gap.gap_days),
        "top_vch_wait_procedure": str(top_vch.procedure_name),
        "top_vch_wait_days": float(top_vch.median_wait_days),
        "bc_missing_case_volume_rows": int(bc_missing.missing_case_volume),
        "bc_missing_case_volume_pct": float(bc_missing.missing_case_volume_pct),
        "validity_issues": validity_issues,
        "duplicate_rows": duplicate_rows,
        "freshness_status": ", ".join(freshness_statuses),
    }
