"""Transform raw public extracts into standardized reporting tables."""

from __future__ import annotations

from pathlib import Path


def normalize_wait_time_columns(input_path: Path) -> list[dict[str, object]]:
    """Normalize source columns into a common wait-time record shape."""
    raise NotImplementedError


def build_geography_lookup(records: list[dict[str, object]]) -> dict[str, int]:
    """Build a geography lookup from standardized records."""
    raise NotImplementedError
