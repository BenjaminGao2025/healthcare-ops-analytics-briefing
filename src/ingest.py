"""Load manually downloaded public source files into PostgreSQL-ready tables."""

from __future__ import annotations

from pathlib import Path


def discover_raw_files(raw_dir: Path) -> list[Path]:
    """Return public source files available for ingestion."""
    raise NotImplementedError


def load_wait_time_sources(raw_dir: Path, database_url: str) -> None:
    """Load public wait-time extracts into PostgreSQL."""
    raise NotImplementedError
