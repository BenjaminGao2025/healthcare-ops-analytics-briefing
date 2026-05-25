#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
from pathlib import Path

from sqlalchemy import create_engine, text

from src.ingest import database_url_from_env

engine = create_engine(database_url_from_env(), pool_pre_ping=True)
schema_sql = Path("sql/01_schema.sql").read_text(encoding="utf-8")

with engine.begin() as conn:
    for statement in schema_sql.split(";"):
        if statement.strip():
            conn.execute(text(statement))
PY

python -m src.ingest
python -m src.kpi
python -m src.quality
python -m src.eda
python -m src.portfolio_artifacts

exec python -m streamlit run app/streamlit_app.py \
  --server.address=0.0.0.0 \
  --server.port=8501 \
  --server.headless=true \
  --browser.gatherUsageStats=false
