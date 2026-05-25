/*
Healthcare Ops Analytics Briefing
Data quality query skeletons for public aggregate healthcare reporting.
*/

-- Row counts per source per year
SELECT
    source_name,
    reporting_year,
    COUNT(*) AS row_count
FROM fact_wait_time
WHERE 1 = 1
  -- TODO: review row-count changes by source and year.
GROUP BY source_name, reporting_year;

-- Missing values per column, count and percentage
SELECT
    source_name,
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE median_wait_days IS NULL) AS missing_median_wait_days,
    COUNT(*) FILTER (WHERE p90_wait_days IS NULL) AS missing_p90_wait_days,
    COUNT(*) FILTER (WHERE pct_meeting_benchmark IS NULL) AS missing_pct_meeting_benchmark,
    COUNT(*) FILTER (WHERE case_volume IS NULL) AS missing_case_volume
    -- TODO: add percentages for each missing-value count.
FROM fact_wait_time
WHERE 1 = 1
GROUP BY source_name;

-- Duplicate procedure, geography, year, and period keys
SELECT
    procedure_id,
    geo_id,
    reporting_year,
    reporting_period,
    COUNT(*) AS duplicate_count
FROM fact_wait_time
WHERE 1 = 1
GROUP BY procedure_id, geo_id, reporting_year, reporting_period
HAVING COUNT(*) > 1;

-- Out-of-range values
SELECT
    wait_time_id,
    source_name,
    median_wait_days,
    p90_wait_days,
    pct_meeting_benchmark,
    case_volume
FROM fact_wait_time
WHERE median_wait_days < 0
   OR p90_wait_days < 0
   OR p90_wait_days < median_wait_days
   OR pct_meeting_benchmark > 100
   OR pct_meeting_benchmark < 0
   OR case_volume < 0
   -- TODO: add any source-specific range checks.
;

-- Category drift for procedure names not in dim_procedure
SELECT
    f.procedure_id,
    COUNT(*) AS row_count
FROM fact_wait_time AS f
LEFT JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
WHERE p.procedure_id IS NULL
  -- TODO: replace with staging-table procedure-name checks after ingest exists.
GROUP BY f.procedure_id;

-- Freshness by source, warn when older than 30 days
SELECT
    source_name,
    MAX(loaded_at) AS max_loaded_at,
    CASE
        WHEN MAX(loaded_at) < now() - interval '30 days' THEN 'warn'
        ELSE 'ok'
    END AS freshness_status
FROM fact_wait_time
WHERE 1 = 1
  -- TODO: decide whether source-specific refresh thresholds are needed.
GROUP BY source_name;
