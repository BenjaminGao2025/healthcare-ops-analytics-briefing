/*
Healthcare Ops Analytics Briefing
PostgreSQL 16 schema for public Canadian healthcare operations reporting.

This schema stores aggregate public wait-time and community context records.
It is not designed for patient-level records or internal health authority data.
*/

CREATE TABLE IF NOT EXISTS dim_procedure (
    procedure_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    procedure_name text NOT NULL UNIQUE,
    procedure_group text,
    benchmark_days numeric,
    source_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dim_geography (
    geo_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    geo_name text NOT NULL,
    geo_type text NOT NULL,
    province_code text,
    parent_geo_id integer REFERENCES dim_geography(geo_id),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT dim_geography_unique UNIQUE (geo_name, geo_type, province_code)
);

CREATE TABLE IF NOT EXISTS fact_wait_time (
    wait_time_id bigserial PRIMARY KEY,
    source_name text NOT NULL,
    procedure_id integer NOT NULL REFERENCES dim_procedure(procedure_id),
    geo_id integer NOT NULL REFERENCES dim_geography(geo_id),
    reporting_year integer NOT NULL,
    reporting_period text NOT NULL,
    median_wait_days numeric,
    p90_wait_days numeric,
    pct_meeting_benchmark numeric,
    case_volume integer,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dim_community (
    community_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    geo_id integer REFERENCES dim_geography(geo_id),
    indicator_name text NOT NULL,
    indicator_year integer,
    indicator_value numeric,
    indicator_unit text,
    source_name text NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fact_wait_time_procedure_geo_year
    ON fact_wait_time(procedure_id, geo_id, reporting_year);
