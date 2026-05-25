/*
Healthcare Ops Analytics Briefing
Day 2 KPI queries for executive, operational, and data quality reporting.

Each block is designed to run as a standalone PostgreSQL query after splitting
on the `-- K##` header line.
*/

-- K01 | National median wait, latest year, by procedure | Executive
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'CIHI'
)
SELECT
  p.procedure_name,
  ROUND(f.median_wait_days::numeric, 1) AS median_wait_days,
  ROUND(f.p90_wait_days::numeric, 1) AS p90_wait_days,
  ROUND(f.pct_meeting_benchmark::numeric, 1) AS pct_meeting_benchmark,
  f.case_volume
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_year AS y ON y.reporting_year = f.reporting_year
WHERE f.source_name = 'CIHI'
  AND g.geo_name = 'Canada'
ORDER BY p.procedure_name;

-- K02 | Provincial median wait, latest year, top 10 procedures by volume | Executive
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'CIHI'
),
top_procedures AS (
  SELECT
    f.procedure_id,
    f.case_volume
  FROM fact_wait_time AS f
  JOIN dim_geography AS g ON g.geo_id = f.geo_id
  JOIN latest_year AS y ON y.reporting_year = f.reporting_year
  WHERE f.source_name = 'CIHI'
    AND g.geo_name = 'Canada'
    AND f.case_volume IS NOT NULL
  ORDER BY case_volume DESC
  LIMIT 10
)
SELECT
  p.procedure_name,
  g.geo_name AS province,
  ROUND(f.median_wait_days::numeric, 1) AS median_wait_days,
  ROUND(f.p90_wait_days::numeric, 1) AS p90_wait_days
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_year AS y ON y.reporting_year = f.reporting_year
JOIN top_procedures AS tp ON tp.procedure_id = f.procedure_id
WHERE f.source_name = 'CIHI'
  AND g.geo_type = 'province'
ORDER BY p.procedure_name, g.geo_name;

-- K03 | BC vs Canada gap, latest year | Executive
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'CIHI'
),
comparison AS (
  SELECT
    f.procedure_id,
    MAX(CASE WHEN g.geo_name = 'British Columbia' THEN f.median_wait_days END) AS bc_median,
    MAX(CASE WHEN g.geo_name = 'Canada' THEN f.median_wait_days END) AS canada_median
  FROM fact_wait_time AS f
  JOIN dim_geography AS g ON g.geo_id = f.geo_id
  JOIN latest_year AS y ON y.reporting_year = f.reporting_year
  WHERE f.source_name = 'CIHI'
    AND g.geo_name IN ('British Columbia', 'Canada')
  GROUP BY f.procedure_id
)
SELECT
  p.procedure_name,
  ROUND(c.bc_median::numeric, 1) AS bc_median,
  ROUND(c.canada_median::numeric, 1) AS canada_median,
  ROUND((c.bc_median - c.canada_median)::numeric, 1) AS gap_days,
  ROUND(((c.bc_median - c.canada_median) / NULLIF(c.canada_median, 0) * 100)::numeric, 1) AS gap_pct
FROM comparison AS c
JOIN dim_procedure AS p ON p.procedure_id = c.procedure_id
WHERE c.bc_median IS NOT NULL
  AND c.canada_median IS NOT NULL
ORDER BY gap_days DESC, p.procedure_name;

-- K04 | 5-year median wait trend, top 5 procedures | Operational
WITH latest_years AS (
  SELECT DISTINCT reporting_year
  FROM fact_wait_time
  WHERE source_name = 'CIHI'
  ORDER BY reporting_year DESC
  LIMIT 5
),
latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM latest_years
),
top_procedures AS (
  SELECT
    f.procedure_id,
    SUM(f.case_volume) AS case_volume
  FROM fact_wait_time AS f
  JOIN dim_geography AS g ON g.geo_id = f.geo_id
  JOIN latest_year AS y ON y.reporting_year = f.reporting_year
  WHERE f.source_name = 'CIHI'
    AND g.geo_name = 'Canada'
    AND f.case_volume IS NOT NULL
  GROUP BY f.procedure_id
  ORDER BY case_volume DESC
  LIMIT 5
)
SELECT
  p.procedure_name,
  f.reporting_year,
  ROUND(AVG(f.median_wait_days)::numeric, 1) AS median_wait_days
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_years AS y ON y.reporting_year = f.reporting_year
JOIN top_procedures AS tp ON tp.procedure_id = f.procedure_id
WHERE f.source_name = 'CIHI'
  AND g.geo_name = 'Canada'
GROUP BY p.procedure_name, f.reporting_year
ORDER BY p.procedure_name, f.reporting_year;

-- K05 | % meeting benchmark by procedure x province, latest year | Executive
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'CIHI'
)
SELECT
  p.procedure_name,
  g.geo_name AS province,
  ROUND(f.pct_meeting_benchmark::numeric, 1) AS pct_meeting_benchmark
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_year AS y ON y.reporting_year = f.reporting_year
WHERE f.source_name = 'CIHI'
  AND g.geo_type = 'province'
  AND f.pct_meeting_benchmark IS NOT NULL
ORDER BY f.pct_meeting_benchmark ASC, p.procedure_name, g.geo_name;

-- K06 | p90 tail risk by procedure x province, latest year | Operational
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'CIHI'
)
SELECT
  p.procedure_name,
  g.geo_name AS province,
  ROUND(f.median_wait_days::numeric, 1) AS median_wait_days,
  ROUND(f.p90_wait_days::numeric, 1) AS p90_wait_days,
  ROUND((f.p90_wait_days / NULLIF(f.median_wait_days, 0))::numeric, 1) AS p90_to_median_ratio
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_year AS y ON y.reporting_year = f.reporting_year
WHERE f.source_name = 'CIHI'
  AND g.geo_type = 'province'
  AND f.p90_wait_days IS NOT NULL
  AND f.median_wait_days IS NOT NULL
ORDER BY p90_to_median_ratio DESC NULLS LAST, p.procedure_name, g.geo_name;

-- K07 | BC Health Authority comparison, latest fiscal year | Executive
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'BC_MoH'
)
SELECT
  g.geo_name AS health_authority,
  p.procedure_name,
  ROUND(f.median_wait_days::numeric, 1) AS median_wait_days,
  f.case_volume
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_year AS y ON y.reporting_year = f.reporting_year
WHERE f.source_name = 'BC_MoH'
  AND g.geo_type = 'health_authority'
ORDER BY g.geo_name, p.procedure_name;

-- K08 | VCH top 20 long-wait procedures, latest fiscal year | Operational
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'BC_MoH'
)
SELECT
  p.procedure_name,
  ROUND(f.median_wait_days::numeric, 1) AS median_wait_days,
  ROUND(f.p90_wait_days::numeric, 1) AS p90_wait_days,
  f.case_volume
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_year AS y ON y.reporting_year = f.reporting_year
WHERE f.source_name = 'BC_MoH'
  AND g.geo_name = 'Vancouver Coastal'
  AND g.geo_type = 'health_authority'
  AND f.median_wait_days IS NOT NULL
ORDER BY f.median_wait_days DESC, p.procedure_name
LIMIT 20;

-- K09 | VCH vs other BC HAs gap, latest fiscal year | Executive
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'BC_MoH'
),
vch AS (
  SELECT
    f.procedure_id,
    f.median_wait_days AS vch_median
  FROM fact_wait_time AS f
  JOIN dim_geography AS g ON g.geo_id = f.geo_id
  JOIN latest_year AS y ON y.reporting_year = f.reporting_year
  WHERE f.source_name = 'BC_MoH'
    AND g.geo_name = 'Vancouver Coastal'
    AND g.geo_type = 'health_authority'
    AND f.median_wait_days IS NOT NULL
),
other_has AS (
  SELECT
    f.procedure_id,
    AVG(f.median_wait_days) AS bc_other_avg_median
  FROM fact_wait_time AS f
  JOIN dim_geography AS g ON g.geo_id = f.geo_id
  JOIN latest_year AS y ON y.reporting_year = f.reporting_year
  WHERE f.source_name = 'BC_MoH'
    AND g.geo_type = 'health_authority'
    AND g.geo_name <> 'Vancouver Coastal'
    AND f.median_wait_days IS NOT NULL
  GROUP BY f.procedure_id
)
SELECT
  p.procedure_name,
  ROUND(v.vch_median::numeric, 1) AS vch_median,
  ROUND(o.bc_other_avg_median::numeric, 1) AS bc_other_avg_median,
  ROUND((v.vch_median - o.bc_other_avg_median)::numeric, 1) AS gap_days
FROM vch AS v
JOIN other_has AS o ON o.procedure_id = v.procedure_id
JOIN dim_procedure AS p ON p.procedure_id = v.procedure_id
ORDER BY gap_days DESC, p.procedure_name;

-- K10 | VCH hospital-level p90, latest fiscal year | Operational
WITH latest_year AS (
  SELECT MAX(reporting_year) AS reporting_year
  FROM fact_wait_time
  WHERE source_name = 'BC_MoH'
),
vch AS (
  SELECT geo_id
  FROM dim_geography
  WHERE geo_name = 'Vancouver Coastal'
    AND geo_type = 'health_authority'
)
SELECT
  g.geo_name AS hospital,
  p.procedure_name,
  ROUND(f.p90_wait_days::numeric, 1) AS p90_wait_days,
  ROUND(f.median_wait_days::numeric, 1) AS median_wait_days,
  f.case_volume
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_year AS y ON y.reporting_year = f.reporting_year
JOIN vch ON vch.geo_id = g.parent_geo_id
WHERE f.source_name = 'BC_MoH'
  AND g.geo_type = 'hospital'
  AND f.p90_wait_days IS NOT NULL
ORDER BY f.p90_wait_days DESC, g.geo_name, p.procedure_name;

-- K11 | Case volume trend by HA, last 5 fiscal years | Operational
WITH latest_years AS (
  SELECT DISTINCT reporting_year
  FROM fact_wait_time
  WHERE source_name = 'BC_MoH'
  ORDER BY reporting_year DESC
  LIMIT 5
)
SELECT
  g.geo_name AS health_authority,
  f.reporting_year,
  SUM(f.case_volume) AS total_case_volume
FROM fact_wait_time AS f
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_years AS y ON y.reporting_year = f.reporting_year
WHERE f.source_name = 'BC_MoH'
  AND g.geo_type = 'health_authority'
  AND f.case_volume IS NOT NULL
GROUP BY g.geo_name, f.reporting_year
ORDER BY g.geo_name, f.reporting_year;

-- K12 | Reporting coverage by source x geo level | Data Quality
WITH latest_periods AS (
  SELECT DISTINCT ON (source_name, geo_id)
    source_name,
    geo_id,
    reporting_year,
    reporting_period
  FROM fact_wait_time
  ORDER BY source_name, geo_id, reporting_year DESC, reporting_period DESC
)
SELECT
  f.source_name,
  g.geo_type,
  MAX(f.reporting_year) AS latest_reporting_year,
  MAX(lp.reporting_period) AS latest_reporting_period,
  COUNT(DISTINCT f.procedure_id) AS n_procedures,
  COUNT(*) AS n_rows
FROM fact_wait_time AS f
JOIN dim_geography AS g ON g.geo_id = f.geo_id
JOIN latest_periods AS lp ON lp.source_name = f.source_name
  AND lp.geo_id = f.geo_id
GROUP BY f.source_name, g.geo_type
ORDER BY f.source_name, g.geo_type;
