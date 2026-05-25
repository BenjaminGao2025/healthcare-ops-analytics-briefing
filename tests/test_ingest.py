"""Database checks for Day 1 wait-time ingestion."""

from __future__ import annotations

import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def database_url() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "healthops")
    password = os.getenv("POSTGRES_PASSWORD", "healthops")
    db = os.getenv("POSTGRES_DB", "healthops")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"


def postgres_unreachable() -> bool:
    try:
        engine = create_engine(database_url(), pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return False
    except SQLAlchemyError:
        return True


requires_postgres = pytest.mark.skipif(
    postgres_unreachable(),
    reason="Postgres is unreachable; start it with `make up` and apply schema with `make schema`.",
)


@requires_postgres
def test_fact_wait_time_not_empty() -> None:
    engine = create_engine(database_url(), pool_pre_ping=True)
    with engine.connect() as conn:
        row_count = conn.execute(text("SELECT COUNT(*) FROM fact_wait_time")).scalar_one()
    assert row_count > 0


@requires_postgres
def test_no_negative_wait_days() -> None:
    engine = create_engine(database_url(), pool_pre_ping=True)
    query = text(
        """
        SELECT COUNT(*)
        FROM fact_wait_time
        WHERE median_wait_days < 0
           OR p90_wait_days < 0
        """
    )
    with engine.connect() as conn:
        bad_rows = conn.execute(query).scalar_one()
    assert bad_rows == 0


@requires_postgres
def test_p90_geq_median_where_both_present() -> None:
    engine = create_engine(database_url(), pool_pre_ping=True)
    query = text(
        """
        SELECT COUNT(*)
        FROM fact_wait_time
        WHERE median_wait_days IS NOT NULL
          AND p90_wait_days IS NOT NULL
          AND p90_wait_days < median_wait_days
        """
    )
    with engine.connect() as conn:
        bad_rows = conn.execute(query).scalar_one()
    assert bad_rows == 0
