"""Equity and responsible-use dashboard page."""

from __future__ import annotations

import streamlit as st

from src.dashboard_data import load_dashboard_frames
from src.portfolio_artifacts import build_methodology_note


@st.cache_data(ttl=600, show_spinner=False)
def frames_for_page():
    """Load cached dashboard frames for this page."""
    return load_dashboard_frames()


st.title("Equity and Responsible Use")

st.markdown(build_methodology_note())

try:
    frames = frames_for_page()
except Exception as exc:  # pragma: no cover - Streamlit runtime fallback
    st.error(f"Dashboard data is unavailable: {exc}")
    st.stop()

st.subheader("Current reporting caveats")
st.dataframe(frames["quality_missingness"], use_container_width=True, hide_index=True)

st.subheader("Responsible-use guardrails")
st.markdown(
    """
- Keep demographic and community context aggregate.
- Do not infer individual patient need, clinical priority, or site performance causality from this demo.
- Confirm source metadata before publishing operational claims.
- Keep suppressed counts as nulls and label them clearly.
"""
)
