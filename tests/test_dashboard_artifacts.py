"""Tests for final dashboard data and executive artifact generation."""

from __future__ import annotations

from pathlib import Path

import pytest
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from src.dashboard_data import dashboard_summary, load_dashboard_frames
from src.ingest import database_url_from_env
from src.portfolio_artifacts import (
    DECK_PDF_FILE,
    EXCEL_FILE,
    METHODOLOGY_FILE,
    REVIEW_GUIDE_FILE,
    build_methodology_note,
    build_review_guide,
    write_excel_workbook,
)


def postgres_unreachable() -> bool:
    try:
        engine = sa.create_engine(database_url_from_env(), pool_pre_ping=True)
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        return False
    except SQLAlchemyError:
        return True


requires_postgres = pytest.mark.skipif(
    postgres_unreachable(),
    reason="Postgres is unreachable; start it with `make up` and load data with `make load`.",
)


@requires_postgres
def test_dashboard_frames_include_expected_sections() -> None:
    frames = load_dashboard_frames()
    expected = {
        "executive_national",
        "bc_gaps",
        "vch_long_waits",
        "vch_hospital_p90",
        "quality_missingness",
        "quality_validity",
        "quality_freshness",
    }
    assert expected.issubset(frames)
    for name in expected:
        assert not frames[name].empty


@requires_postgres
def test_dashboard_summary_has_portfolio_headline_metrics() -> None:
    summary = dashboard_summary(load_dashboard_frames())
    assert summary["top_gap_procedure"] == "MRI Scan"
    assert summary["top_vch_wait_procedure"] == "Dental Surgery"
    assert summary["bc_missing_case_volume_rows"] == 9688


def test_methodology_and_review_guide_have_required_sections() -> None:
    methodology = build_methodology_note()
    review_guide = build_review_guide()
    assert "# Methodology Note" in methodology
    assert "No patient-level data" in methodology
    assert "# Opus Review Guide" in review_guide
    assert "Architecture review" in review_guide


def test_artifact_paths_are_stable() -> None:
    assert METHODOLOGY_FILE == Path("reports/methodology_note.md")
    assert REVIEW_GUIDE_FILE == Path("reports/opus_review_guide.md")
    assert DECK_PDF_FILE == Path("reports/board_briefing_deck.pdf")
    assert EXCEL_FILE == Path("excel/healthcare_ops_analytics_workbook.xlsx")


@requires_postgres
def test_excel_workbook_can_be_written() -> None:
    output_path = write_excel_workbook()
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_streamlit_pages_do_not_have_todo_placeholders() -> None:
    for path in Path("app").rglob("*.py"):
        assert "TODO" not in path.read_text(encoding="utf-8")


def test_make_app_sets_project_import_path() -> None:
    makefile = Path("Makefile").read_text(encoding="utf-8")
    assert "PYTHONPATH=. $(PYTHON) -m streamlit run app/streamlit_app.py" in makefile
