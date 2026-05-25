"""Load public aggregate wait-time source files into PostgreSQL.

Idempotence choice: this loader keeps dimension rows and deletes/reloads
`fact_wait_time` rows per source (`CIHI`, `BC_MoH`) on every run. That avoids
inventing a fact natural key before source formats are fully stabilized while
keeping repeated Day 1 loads deterministic.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine


LOGGER = logging.getLogger(__name__)

PROVINCE_CODES = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Nova Scotia": "NS",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Canada": "CA",
}

BC_HEALTH_AUTHORITIES = {
    "Fraser",
    "Interior",
    "Northern",
    "Provincial Health Services Authority",
    "Vancouver Coastal",
    "Vancouver Island",
}


def discover_raw_files(raw_dir: Path) -> dict[str, Path]:
    """Return the newest required public source files."""
    cihi_files = sorted(raw_dir.glob("cihi_wait_times_*.xlsx"))
    bc_files = sorted(raw_dir.glob("bc_surgical_wait_*.csv"))
    missing = []
    if not cihi_files:
        missing.append("data/raw/cihi_wait_times_<YYYYMMDD>.xlsx")
    if not bc_files:
        missing.append("data/raw/bc_surgical_wait_<YYYYMMDD>.csv")
    if missing:
        raise FileNotFoundError("Missing required raw files: " + ", ".join(missing))
    return {"CIHI": cihi_files[-1], "BC_MoH": bc_files[-1]}


def database_url_from_env() -> str:
    """Build a SQLAlchemy URL from environment variables."""
    load_dotenv()
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "healthops")
    password = os.getenv("POSTGRES_PASSWORD", "healthops")
    db = os.getenv("POSTGRES_DB", "healthops")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"


def parse_reporting_year(value: Any) -> tuple[int, str]:
    """Return integer year and reporting period from source year labels."""
    label = str(value).strip()
    if "/" in label:
        return int(label.split("/")[0]), f"FY {label}"
    year = int(label[:4])
    if label.endswith("FY"):
        return year, f"FY {year}"
    if label.endswith("Q3Q4"):
        return year, f"Q3Q4 {year}"
    return year, "Apr-Sep"


def to_nullable_int(value: Any) -> int | None:
    """Convert source counts to integers, preserving suppressed values as null."""
    if pd.isna(value):
        return None
    text_value = str(value).strip()
    if not text_value or text_value.startswith("<"):
        return None
    return int(float(text_value.replace(",", "")))


def numeric_or_none(value: Any) -> float | None:
    """Convert numeric source cells to floats."""
    if pd.isna(value):
        return None
    return float(value)


def upsert_procedure(conn: Connection, procedure_name: str, source_name: str) -> int:
    """Upsert one procedure and return its id."""
    result = conn.execute(
        text(
            """
            INSERT INTO dim_procedure (procedure_name, procedure_group, source_name)
            VALUES (:procedure_name, :procedure_group, :source_name)
            ON CONFLICT (procedure_name) DO UPDATE
            SET procedure_group = COALESCE(dim_procedure.procedure_group, EXCLUDED.procedure_group)
            RETURNING procedure_id
            """
        ),
        {
            "procedure_name": procedure_name,
            "procedure_group": procedure_name,
            "source_name": source_name,
        },
    )
    return int(result.scalar_one())


def upsert_geography(
    conn: Connection,
    geo_name: str,
    geo_type: str,
    province_code: str,
    parent_geo_id: int | None = None,
) -> int:
    """Upsert one geography and return its id."""
    result = conn.execute(
        text(
            """
            INSERT INTO dim_geography (geo_name, geo_type, province_code, parent_geo_id)
            VALUES (:geo_name, :geo_type, :province_code, :parent_geo_id)
            ON CONFLICT (geo_name, geo_type, province_code) DO UPDATE
            SET parent_geo_id = COALESCE(dim_geography.parent_geo_id, EXCLUDED.parent_geo_id)
            RETURNING geo_id
            """
        ),
        {
            "geo_name": geo_name,
            "geo_type": geo_type,
            "province_code": province_code,
            "parent_geo_id": parent_geo_id,
        },
    )
    return int(result.scalar_one())


def cihi_geography(row: pd.Series) -> tuple[str, str, str, str | None]:
    """Map a CIHI row to geography fields."""
    reporting_level = str(row["Reporting level"]).strip()
    province = str(row["Province"]).strip()
    region = row.get("Region")
    province_code = PROVINCE_CODES.get(province, province[:2].upper())
    if reporting_level == "National":
        return "Canada", "country", "CA", None
    if reporting_level == "Regional" and pd.notna(region):
        return str(region).strip(), "health_region", province_code, province
    return province, "province", province_code, None


def load_cihi_rows(path: Path) -> pd.DataFrame:
    """Normalize CIHI wait-time rows to fact table columns."""
    df = pd.read_excel(path, sheet_name="Table 1", header=1)
    df = df[df["Reporting level"].isin(["National", "Provincial", "Regional"])].copy()
    df = df.dropna(subset=["Province", "Indicator", "Metric", "Data year"])
    df["Indicator result"] = pd.to_numeric(df["Indicator result"], errors="coerce")
    df = df.dropna(subset=["Indicator result"])

    geo_parts = df.apply(cihi_geography, axis=1, result_type="expand")
    geo_parts.columns = ["geo_name", "geo_type", "province_code", "parent_geo_name"]
    df = pd.concat([df, geo_parts], axis=1)
    df["parent_geo_name"] = df["parent_geo_name"].fillna("")
    year_parts = df["Data year"].apply(parse_reporting_year)
    df["reporting_year"] = [part[0] for part in year_parts]
    df["reporting_period"] = [part[1] for part in year_parts]
    df["metric_name"] = df["Metric"].replace(
        {
            "50th Percentile": "median_wait_days",
            "90th Percentile": "p90_wait_days",
            "Volume": "case_volume",
            "% Meeting Benchmark": "pct_meeting_benchmark",
        }
    )
    df["metric_value"] = df["Indicator result"]
    hours_mask = df["Unit of measurement"].eq("Hours") & df["metric_name"].isin(
        ["median_wait_days", "p90_wait_days"]
    )
    df.loc[hours_mask, "metric_value"] = df.loc[hours_mask, "metric_value"] / 24

    index_cols = [
        "Indicator",
        "geo_name",
        "geo_type",
        "province_code",
        "parent_geo_name",
        "reporting_year",
        "reporting_period",
    ]
    wide = (
        df.pivot_table(
            index=index_cols,
            columns="metric_name",
            values="metric_value",
            aggfunc="first",
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    for column in ["median_wait_days", "p90_wait_days", "pct_meeting_benchmark", "case_volume"]:
        if column not in wide.columns:
            wide[column] = None
    wide["source_name"] = "CIHI"
    wide["parent_geo_name"] = wide["parent_geo_name"].replace("", None)
    return wide


def load_bc_rows(path: Path) -> pd.DataFrame:
    """Normalize BC surgical wait-time rows to fact table columns."""
    df = pd.read_csv(path)
    rows = []
    for row in df.itertuples(index=False):
        fiscal_year, health_authority, hospital_name, procedure_group = (
            str(row.FISCAL_YEAR).strip(),
            str(row.HEALTH_AUTHORITY).strip(),
            str(row.HOSPITAL_NAME).strip(),
            str(row.PROCEDURE_GROUP).strip(),
        )
        reporting_year, reporting_period = parse_reporting_year(fiscal_year)
        if health_authority == "All Health Authorities" and hospital_name == "All Facilities":
            geo_name, geo_type, parent_geo_name = "British Columbia", "province", None
        elif hospital_name == "All Facilities":
            geo_name, geo_type, parent_geo_name = health_authority, "health_authority", "British Columbia"
        else:
            geo_name, geo_type, parent_geo_name = hospital_name, "hospital", health_authority

        median_wait_days = numeric_or_none(row.COMPLETED_50TH_PERCENTILE)
        p90_wait_days = numeric_or_none(row.COMPLETED_90TH_PERCENTILE)
        rows.append(
            {
                "source_name": "BC_MoH",
                "Indicator": procedure_group,
                "geo_name": geo_name,
                "geo_type": geo_type,
                "province_code": "BC",
                "parent_geo_name": parent_geo_name,
                "reporting_year": reporting_year,
                "reporting_period": reporting_period,
                "median_wait_days": median_wait_days * 7 if median_wait_days is not None else None,
                "p90_wait_days": p90_wait_days * 7 if p90_wait_days is not None else None,
                "pct_meeting_benchmark": None,
                "case_volume": to_nullable_int(row.COMPLETED),
            }
        )
    return pd.DataFrame(rows)


def insert_fact_rows(conn: Connection, rows: pd.DataFrame, source_name: str) -> dict[str, int]:
    """Insert dimension and fact rows for one normalized source."""
    conn.execute(text("DELETE FROM fact_wait_time WHERE source_name = :source_name"), {"source_name": source_name})

    procedure_ids: dict[str, int] = {}
    geography_ids: dict[tuple[str, str, str], int] = {}

    for procedure_name in sorted(rows["Indicator"].dropna().unique()):
        procedure_ids[procedure_name] = upsert_procedure(conn, procedure_name, source_name)

    for _, row in rows.iterrows():
        parent_geo_id = None
        parent_geo_name = row.get("parent_geo_name")
        if pd.notna(parent_geo_name) and parent_geo_name:
            parent_type = "province" if parent_geo_name == "British Columbia" else "health_authority"
            parent_key = (str(parent_geo_name), parent_type, str(row["province_code"]))
            if parent_key not in geography_ids:
                geography_ids[parent_key] = upsert_geography(
                    conn,
                    str(parent_geo_name),
                    parent_type,
                    str(row["province_code"]),
                )
            parent_geo_id = geography_ids[parent_key]

        key = (str(row["geo_name"]), str(row["geo_type"]), str(row["province_code"]))
        if key not in geography_ids:
            geography_ids[key] = upsert_geography(
                conn,
                key[0],
                key[1],
                key[2],
                parent_geo_id,
            )

    payload = []
    for _, row in rows.iterrows():
        payload.append(
            {
                "source_name": source_name,
                "procedure_id": procedure_ids[str(row["Indicator"])],
                "geo_id": geography_ids[
                    (str(row["geo_name"]), str(row["geo_type"]), str(row["province_code"]))
                ],
                "reporting_year": int(row["reporting_year"]),
                "reporting_period": str(row["reporting_period"]),
                "median_wait_days": numeric_or_none(row["median_wait_days"]),
                "p90_wait_days": numeric_or_none(row["p90_wait_days"]),
                "pct_meeting_benchmark": numeric_or_none(row["pct_meeting_benchmark"]),
                "case_volume": to_nullable_int(row["case_volume"]),
            }
        )

    if payload:
        conn.execute(
            text(
                """
                INSERT INTO fact_wait_time (
                    source_name,
                    procedure_id,
                    geo_id,
                    reporting_year,
                    reporting_period,
                    median_wait_days,
                    p90_wait_days,
                    pct_meeting_benchmark,
                    case_volume
                )
                VALUES (
                    :source_name,
                    :procedure_id,
                    :geo_id,
                    :reporting_year,
                    :reporting_period,
                    :median_wait_days,
                    :p90_wait_days,
                    :pct_meeting_benchmark,
                    :case_volume
                )
                """
            ),
            payload,
        )

    return {
        "procedures_seen": len(procedure_ids),
        "geographies_seen": len(geography_ids),
        "fact_rows_inserted": len(payload),
    }


def load_wait_time_sources(raw_dir: Path, engine: Engine) -> dict[str, dict[str, int]]:
    """Load CIHI and BC wait-time sources into PostgreSQL."""
    files = discover_raw_files(raw_dir)
    normalized = {
        "CIHI": load_cihi_rows(files["CIHI"]),
        "BC_MoH": load_bc_rows(files["BC_MoH"]),
    }
    counts = {}
    with engine.begin() as conn:
        for source_name, rows in normalized.items():
            counts[source_name] = insert_fact_rows(conn, rows, source_name)
        conn.execute(
            text(
                """
                UPDATE dim_geography AS health_authority
                SET parent_geo_id = province.geo_id
                FROM dim_geography AS province
                WHERE health_authority.geo_type = 'health_authority'
                  AND health_authority.province_code = 'BC'
                  AND health_authority.parent_geo_id IS NULL
                  AND province.geo_name = 'British Columbia'
                  AND province.geo_type = 'province'
                  AND province.province_code = 'BC'
                """
            )
        )
        for table_name in ["dim_procedure", "dim_geography", "fact_wait_time", "dim_community"]:
            counts[table_name] = {
                "row_count": int(conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one())
            }
    return counts


def main() -> None:
    """Run the Day 1 loader."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    engine = create_engine(database_url_from_env(), pool_pre_ping=True)
    counts = load_wait_time_sources(Path("data/raw"), engine)
    for name, values in counts.items():
        LOGGER.info("%s: %s", name, values)


if __name__ == "__main__":
    main()
