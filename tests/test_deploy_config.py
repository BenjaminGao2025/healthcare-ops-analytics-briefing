"""Tests for 7840 deployment configuration."""

from __future__ import annotations

from pathlib import Path


DEPLOY_DIR = Path("deploy/7840")


def test_7840_deploy_files_exist() -> None:
    assert (DEPLOY_DIR / "Dockerfile").exists()
    assert (DEPLOY_DIR / "docker-compose.yml").exists()
    assert (DEPLOY_DIR / "start.sh").exists()


def test_compose_uses_external_proxy_network_env() -> None:
    compose = (DEPLOY_DIR / "docker-compose.yml").read_text(encoding="utf-8")
    assert "healthops-postgres" in compose
    assert "healthops-streamlit" in compose
    assert "PROXY_NETWORK" in compose
    assert "mga-ai" not in compose


def test_start_script_bootstraps_db_before_streamlit() -> None:
    script = (DEPLOY_DIR / "start.sh").read_text(encoding="utf-8")
    assert script.index("sql/01_schema.sql") < script.index("python -m src.ingest")
    assert "python -m streamlit run app/streamlit_app.py" in script
    assert "--server.address=0.0.0.0" in script
