"""KPI calculation helpers for aggregate healthcare operations reporting."""

from __future__ import annotations


def calculate_bc_vs_canada_gap(bc_value: float, canada_value: float) -> float:
    """Calculate the difference between BC and Canada benchmark values."""
    raise NotImplementedError


def calculate_tail_risk_gap(p90_wait_days: float, median_wait_days: float) -> float:
    """Calculate the p90 minus median wait-time gap."""
    raise NotImplementedError
