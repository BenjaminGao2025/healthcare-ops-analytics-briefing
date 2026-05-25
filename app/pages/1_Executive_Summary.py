"""Executive summary dashboard page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.dashboard_data import dashboard_summary, load_dashboard_frames


@st.cache_data(ttl=600, show_spinner=False)
def frames_for_page():
    """Load cached dashboard frames for this page."""
    return load_dashboard_frames()


st.title("Executive Summary")

try:
    frames = frames_for_page()
    summary = dashboard_summary(frames)
except Exception as exc:  # pragma: no cover - Streamlit runtime fallback
    st.error(f"Dashboard data is unavailable: {exc}")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Largest BC vs Canada gap", summary["top_gap_procedure"], f"{summary['top_gap_days']:.1f} days")
col2.metric("Longest VCH wait", summary["top_vch_wait_procedure"], f"{summary['top_vch_wait_days']:.1f} days")
col3.metric("Null BC volume rows", f"{summary['bc_missing_case_volume_rows']:,}")
col4.metric("Validity issues", summary["validity_issues"])

st.subheader("BC vs Canada median-wait gaps")
gap_chart = frames["bc_gaps"].head(8).sort_values("gap_days")
st.plotly_chart(
    px.bar(
        gap_chart,
        x="gap_days",
        y="procedure_name",
        orientation="h",
        labels={"gap_days": "Gap days", "procedure_name": "Procedure"},
        color="gap_days",
        color_continuous_scale="Teal",
    ),
    use_container_width=True,
)

st.subheader("National latest-year access snapshot")
st.dataframe(frames["executive_national"], use_container_width=True, hide_index=True)
st.caption(
    "Unit note: CIHI Hip Fracture Repair source values are reported in hours and "
    "converted to days for table consistency."
)

st.subheader("Vancouver Coastal long-wait procedures")
st.dataframe(frames["vch_long_waits"], use_container_width=True, hide_index=True)
