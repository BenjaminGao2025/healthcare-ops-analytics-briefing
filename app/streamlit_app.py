"""Streamlit entry point for the healthcare operations analytics briefing."""

from __future__ import annotations

import streamlit as st


st.set_page_config(
    page_title="Healthcare Ops Analytics Briefing",
    layout="wide",
)

st.title("Healthcare Ops Analytics Briefing")

st.write(
    "A public Canadian healthcare operations analytics demo focused on wait-time "
    "visibility, data quality, and executive-ready reporting."
)
st.write(
    "Use the sidebar pages to review the executive summary, operational "
    "drilldown, data quality monitor, and responsible-use notes."
)

st.caption("Last updated: TODO")

st.warning(
    "Data-source disclaimer: all data used is publicly available. This project "
    "does not use any patient-level or VCH internal data."
)
