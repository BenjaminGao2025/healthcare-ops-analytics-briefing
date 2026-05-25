"""Operational drilldown dashboard page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.dashboard_data import load_dashboard_frames


@st.cache_data(ttl=600, show_spinner=False)
def frames_for_page():
    """Load cached dashboard frames for this page."""
    return load_dashboard_frames()


st.title("Operational Drilldown")

try:
    frames = frames_for_page()
except Exception as exc:  # pragma: no cover - Streamlit runtime fallback
    st.error(f"Dashboard data is unavailable: {exc}")
    st.stop()

st.subheader("Five-year national median-wait trend")
st.plotly_chart(
    px.line(
        frames["national_trend"],
        x="reporting_year",
        y="median_wait_days",
        color="procedure_name",
        markers=True,
        labels={"reporting_year": "Year", "median_wait_days": "Median wait days"},
    ),
    use_container_width=True,
)

left, right = st.columns(2)
with left:
    st.subheader("VCH vs other BC health authorities")
    st.dataframe(frames["vch_vs_other"].head(25), use_container_width=True, hide_index=True)

with right:
    st.subheader("Case volume vs median wait")
    scatter_data = frames["ha_comparison"].dropna(subset=["case_volume", "median_wait_days"])
    st.plotly_chart(
        px.scatter(
            scatter_data,
            x="case_volume",
            y="median_wait_days",
            color="health_authority",
            hover_data=["procedure_name"],
            labels={"case_volume": "Case volume", "median_wait_days": "Median wait days"},
        ),
        use_container_width=True,
    )

st.subheader("VCH hospital p90 tail risk")
hospital_tail = frames["vch_hospital_p90"].head(30).sort_values("p90_wait_days")
st.plotly_chart(
    px.bar(
        hospital_tail,
        x="p90_wait_days",
        y="procedure_name",
        color="hospital",
        orientation="h",
        hover_data=["median_wait_days", "case_volume"],
        labels={"p90_wait_days": "90th percentile wait days", "procedure_name": "Procedure"},
    ),
    use_container_width=True,
)

st.subheader("Health authority case-volume trend")
st.plotly_chart(
    px.line(
        frames["ha_volume_trend"],
        x="reporting_year",
        y="total_case_volume",
        color="health_authority",
        markers=True,
        labels={"reporting_year": "Fiscal year start", "total_case_volume": "Completed cases"},
    ),
    use_container_width=True,
)
