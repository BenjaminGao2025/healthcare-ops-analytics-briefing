/*
Healthcare Ops Analytics Briefing
Day 3 data quality checks for public aggregate healthcare reporting.

Each block is designed to run as a standalone PostgreSQL query after splitting
on the `-- DQ##` header line.
*/

-- DQ01 | Row counts per source per year | Data Quality
SELECT
  source_name,
  reporting_year,
  COUNT(*) AS row_count
FROM fact_wait_time
GROUP BY source_name, reporting_year
ORDER BY source_name, reporting_year;

-- DQ02 | Missing values per source | Data Quality
SELECT
  source_name,
  COUNT(*) AS total_rows,
  COUNT(*) FILTER (WHERE median_wait_days IS NULL) AS missing_median_wait_days,
  ROUND(
    COUNT(*) FILTER (WHERE median_wait_days IS NULL)::numeric / NULLIF(COUNT(*), 0) * 100,
    2
  ) AS missing_median_wait_days_pct,
  COUNT(*) FILTER (WHERE p90_wait_days IS NULL) AS missing_p90_wait_days,
  ROUND(
    COUNT(*) FILTER (WHERE p90_wait_days IS NULL)::numeric / NULLIF(COUNT(*), 0) * 100,
    2
  ) AS missing_p90_wait_days_pct,
  COUNT(*) FILTER (WHERE pct_meeting_benchmark IS NULL) AS missing_pct_meeting_benchmark,
  ROUND(
    COUNT(*) FILTER (WHERE pct_meeting_benchmark IS NULL)::numeric / NULLIF(COUNT(*), 0) * 100,
    2
  ) AS missing_pct_meeting_benchmark_pct,
  COUNT(*) FILTER (WHERE case_volume IS NULL) AS missing_case_volume,
  ROUND(
    COUNT(*) FILTER (WHERE case_volume IS NULL)::numeric / NULLIF(COUNT(*), 0) * 100,
    2
  ) AS missing_case_volume_pct
FROM fact_wait_time
GROUP BY source_name
ORDER BY source_name;

-- DQ03 | Duplicate fact keys | Data Quality
WITH duplicate_keys AS (
  SELECT
    source_name,
    procedure_id,
    geo_id,
    reporting_year,
    reporting_period,
    COUNT(*) AS rows_per_key
  FROM fact_wait_time
  GROUP BY source_name, procedure_id, geo_id, reporting_year, reporting_period
  HAVING COUNT(*) > 1
)
SELECT
  source_name,
  COUNT(*) AS duplicate_key_count,
  COALESCE(SUM(rows_per_key), 0) AS duplicate_row_count
FROM duplicate_keys
GROUP BY source_name
UNION ALL
SELECT
  source_name,
  0 AS duplicate_key_count,
  0 AS duplicate_row_count
FROM (
  SELECT DISTINCT source_name
  FROM fact_wait_time
) AS sources
WHERE NOT EXISTS (
  SELECT 1
  FROM duplicate_keys
  WHERE duplicate_keys.source_name = sources.source_name
)
ORDER BY source_name;

-- DQ04 | Out-of-range values | Data Quality
WITH checks AS (
  SELECT
    'negative_median_wait_days' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM fact_wait_time
  WHERE median_wait_days < 0
  UNION ALL
  SELECT
    'negative_p90_wait_days' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM fact_wait_time
  WHERE p90_wait_days < 0
  UNION ALL
  SELECT
    'p90_less_than_median' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM fact_wait_time
  WHERE median_wait_days IS NOT NULL
    AND p90_wait_days IS NOT NULL
    AND p90_wait_days < median_wait_days
  UNION ALL
  SELECT
    'pct_meeting_benchmark_outside_0_100' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM fact_wait_time
  WHERE pct_meeting_benchmark < 0
     OR pct_meeting_benchmark > 100
  UNION ALL
  SELECT
    'negative_case_volume' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM fact_wait_time
  WHERE case_volume < 0
)
SELECT
  issue_type,
  bad_row_count
FROM checks
ORDER BY issue_type;

-- DQ05 | Category drift and broken dimension links | Data Quality
WITH checks AS (
  SELECT
    'missing_procedure_dimension' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM fact_wait_time AS f
  LEFT JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
  WHERE p.procedure_id IS NULL
  UNION ALL
  SELECT
    'missing_geography_dimension' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM fact_wait_time AS f
  LEFT JOIN dim_geography AS g ON g.geo_id = f.geo_id
  WHERE g.geo_id IS NULL
  UNION ALL
  SELECT
    'blank_procedure_name' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM dim_procedure
  WHERE procedure_name IS NULL
     OR btrim(procedure_name) = ''
  UNION ALL
  SELECT
    'blank_geography_name' AS issue_type,
    COUNT(*) AS bad_row_count
  FROM dim_geography
  WHERE geo_name IS NULL
     OR btrim(geo_name) = ''
)
SELECT
  issue_type,
  bad_row_count
FROM checks
ORDER BY issue_type;

-- DQ06 | Freshness by source | Data Quality
SELECT
  source_name,
  MAX(loaded_at) AS max_loaded_at,
  ROUND(EXTRACT(EPOCH FROM (now() - MAX(loaded_at))) / 86400, 2) AS age_days,
  CASE
    WHEN MAX(loaded_at) < now() - interval '30 days' THEN 'warn'
    ELSE 'ok'
  END AS freshness_status
FROM fact_wait_time
GROUP BY source_name
ORDER BY source_name;

-- DQ07 | Reporting coverage by source and geography level | Data Quality
SELECT
  f.source_name,
  g.geo_type,
  f.reporting_year,
  COUNT(DISTINCT f.procedure_id) AS n_procedures,
  COUNT(*) AS n_rows
FROM fact_wait_time AS f
JOIN dim_geography AS g ON g.geo_id = f.geo_id
GROUP BY f.source_name, g.geo_type, f.reporting_year
ORDER BY f.source_name, g.geo_type, f.reporting_year;

-- DQ08 | Suppressed count summary | Data Quality
SELECT
  source_name,
  COUNT(*) AS total_rows,
  COUNT(*) FILTER (WHERE source_name = 'BC_MoH' AND case_volume IS NULL) AS suppressed_case_volume_rows,
  ROUND(
    COUNT(*) FILTER (WHERE source_name = 'BC_MoH' AND case_volume IS NULL)::numeric
    / NULLIF(COUNT(*), 0) * 100,
    2
  ) AS suppressed_case_volume_pct
FROM fact_wait_time
GROUP BY source_name
ORDER BY source_name;
