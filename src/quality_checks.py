"""Data quality checks for aggregate public healthcare reporting data."""

from __future__ import annotations


def find_negative_wait_values(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return rows with impossible negative wait-time values."""
    raise NotImplementedError


def find_duplicate_reporting_keys(rows: list[dict[str, object]]) -> list[tuple[object, ...]]:
    """Return duplicate procedure, geography, year, and period keys."""
    raise NotImplementedError
