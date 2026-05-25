"""Static tests for published scope and repository health signals."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(".")


def test_unloaded_community_scope_is_not_advertised() -> None:
    paths = [
        ROOT / "README.md",
        ROOT / "data/data_dictionary.md",
        ROOT / "data/raw/SOURCE.md",
        ROOT / "sql/01_schema.sql",
        ROOT / "src/ingest.py",
    ]
    forbidden = [
        "dim_community",
        "Community Health Profiles",
        "vch_community",
        "community-level",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            assert phrase not in text, f"{phrase!r} remains in {path}"


def test_readme_uses_real_ci_badge() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "build-placeholder" not in readme
    assert "actions/workflows/ci.yml/badge.svg" in readme
    assert (ROOT / ".github/workflows/ci.yml").exists()
