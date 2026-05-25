"""Data quality monitor dashboard page."""

from __future__ import annotations

import streamlit as st


st.title("Data Quality Monitor")

st.write(
    "Reporting confidence view for completeness, duplicate keys, validity "
    "checks, category drift, and source freshness."
)

st.info("TODO: implement row counts by source and year.")
st.info("TODO: implement missing values by column.")
st.info("TODO: implement duplicate reporting key checks.")
st.info("TODO: implement out-of-range value checks.")
st.info("TODO: implement category drift checks.")
st.info("TODO: implement source freshness checks.")
