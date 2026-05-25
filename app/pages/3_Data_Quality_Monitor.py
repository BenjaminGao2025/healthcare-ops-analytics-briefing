"""Data quality monitor dashboard page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.dashboard_data import load_dashboard_frames


@st.cache_data(ttl=600, show_spinner=False)
def frames_for_page():
    """Load cached dashboard frames for this page."""
    return load_dashboard_frames()


st.title("Data Quality Monitor")

try:
    frames = frames_for_page()
except Exception as exc:  # pragma: no cover - Streamlit runtime fallback
    st.error(f"Dashboard data is unavailable: {exc}")
    st.stop()

missingness = frames["quality_missingness"]
validity = frames["quality_validity"]
freshness = frames["quality_freshness"]
suppressed = frames["suppressed_counts"]
duplicates = frames["quality_duplicates"]

col1, col2, col3 = st.columns(3)
col1.metric("Duplicate rows", int(duplicates["duplicate_row_count"].sum()))
col2.metric("Validity issues", int(validity["bad_row_count"].sum()))
col3.metric("Freshness", ", ".join(sorted(set(freshness["freshness_status"]))))

st.subheader("Missing core fields")
missing_chart = missingness.melt(
    id_vars=["source_name"],
    value_vars=["missing_median_wait_days_pct", "missing_case_volume_pct"],
    var_name="metric",
    value_name="missing_pct",
)
st.plotly_chart(
    px.bar(
        missing_chart,
        x="source_name",
        y="missing_pct",
        color="metric",
        barmode="group",
        labels={"source_name": "Source", "missing_pct": "Missing percent"},
    ),
    use_container_width=True,
)

left, right = st.columns(2)
with left:
    st.subheader("Validity checks")
    st.dataframe(validity, use_container_width=True, hide_index=True)

with right:
    st.subheader("Freshness")
    st.dataframe(freshness, use_container_width=True, hide_index=True)

st.subheader("Suppressed or unavailable case volume")
st.dataframe(suppressed, use_container_width=True, hide_index=True)
