"""Streamlit entry point for the healthcare operations analytics briefing."""

from __future__ import annotations

import streamlit as st

from src.dashboard_data import dashboard_summary, load_dashboard_frames


st.set_page_config(
    page_title="Healthcare Ops Analytics Briefing",
    layout="wide",
)

st.title("Healthcare Ops Analytics Briefing")

st.write(
    "Public Canadian wait-time reporting demo for executive summaries, operational "
    "drilldowns, data quality monitoring, and responsible-use review."
)

try:
    frames = load_dashboard_frames()
    summary = dashboard_summary(frames)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Largest BC gap", summary["top_gap_procedure"], f"{summary['top_gap_days']:.1f} days")
    col2.metric(
        "Longest VCH median wait",
        summary["top_vch_wait_procedure"],
        f"{summary['top_vch_wait_days']:.1f} days",
    )
    col3.metric("BC null volume rows", f"{summary['bc_missing_case_volume_rows']:,}")
    col4.metric("Validity issues", summary["validity_issues"])
except Exception as exc:  # pragma: no cover - Streamlit runtime fallback
    st.error(f"Dashboard data is unavailable: {exc}")
    summary = None

if summary:
    st.caption(f"Data loaded: {summary['max_loaded_at']}")

st.warning(
    "Data-source boundary: all data is public and aggregate. This project does not use "
    "patient-level data or VCH internal data."
)
