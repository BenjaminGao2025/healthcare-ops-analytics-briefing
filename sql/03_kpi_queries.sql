/*
Healthcare Ops Analytics Briefing
KPI query skeletons for executive and analyst reporting.
*/

-- Q1
-- KPI: National median wait by procedure, latest year.
-- Intended audience: Exec
SELECT
    p.procedure_name,
    f.reporting_year,
    f.median_wait_days
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_name = 'Canada'
  -- TODO: filter to latest reporting year.
;

-- Q2
-- KPI: National p90 wait by procedure, latest year.
-- Intended audience: Exec
SELECT
    p.procedure_name,
    f.reporting_year,
    f.p90_wait_days
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_name = 'Canada'
  -- TODO: filter to latest reporting year.
;

-- Q3
-- KPI: Percent meeting benchmark by procedure and province, latest year.
-- Intended audience: Exec
SELECT
    p.procedure_name,
    g.geo_name AS province_name,
    f.reporting_year,
    f.pct_meeting_benchmark
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_type = 'province'
  -- TODO: filter to latest reporting year.
;

-- Q4
-- KPI: Year-over-year change in median wait by procedure for Canada.
-- Intended audience: Analyst
SELECT
    p.procedure_name,
    f.reporting_year,
    f.median_wait_days
    -- TODO: add lag and year-over-year change calculation.
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_name = 'Canada'
  -- TODO: order by procedure and year.
;

-- Q5
-- KPI: BC vs Canada gap in median wait by procedure, latest year.
-- Intended audience: Exec
SELECT
    p.procedure_name,
    f.reporting_year,
    g.geo_name,
    f.median_wait_days
    -- TODO: pivot or self-join BC and Canada values.
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_name IN ('British Columbia', 'Canada')
  -- TODO: filter to latest reporting year.
;

-- Q6
-- KPI: Vancouver Coastal vs other BC health authorities, median wait by procedure.
-- Intended audience: Exec
SELECT
    p.procedure_name,
    g.geo_name AS health_authority,
    f.reporting_year,
    f.median_wait_days
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_type = 'health_authority'
  AND g.province_code = 'BC'
  -- TODO: filter to latest reporting year and compare Vancouver Coastal.
;

-- Q7
-- KPI: Top 5 procedures with largest year-over-year deterioration in BC.
-- Intended audience: Analyst
SELECT
    p.procedure_name,
    f.reporting_year,
    f.median_wait_days
    -- TODO: calculate year-over-year deterioration and limit to five.
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_name = 'British Columbia'
  -- TODO: add latest comparable years.
;

-- Q8
-- KPI: Top 5 hospitals in VCH with longest waits.
-- Intended audience: Exec
SELECT
    p.procedure_name,
    g.geo_name AS hospital_name,
    f.reporting_year,
    f.median_wait_days
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_type = 'hospital'
  -- TODO: restrict to VCH parent geography and latest year.
;

-- Q9
-- KPI: Case volume vs median wait correlation input by procedure and health authority.
-- Intended audience: Analyst
SELECT
    p.procedure_name,
    g.geo_name AS health_authority,
    f.reporting_year,
    f.case_volume,
    f.median_wait_days
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE g.geo_type = 'health_authority'
  -- TODO: export this result for correlation analysis.
;

-- Q10
-- KPI: Largest p90 minus median gap as a tail-risk indicator.
-- Intended audience: Exec
SELECT
    p.procedure_name,
    g.geo_name,
    f.reporting_year,
    f.p90_wait_days,
    f.median_wait_days
    -- TODO: calculate p90_wait_days - median_wait_days and rank.
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE f.p90_wait_days IS NOT NULL
  -- TODO: filter to latest reporting year.
;

-- Q11
-- KPI: Coverage check for missing procedure, geography, and year cells.
-- Intended audience: Data quality
SELECT
    p.procedure_name,
    g.geo_name,
    y.reporting_year
    -- TODO: left join expected grid to fact_wait_time and flag missing rows.
FROM dim_procedure AS p
CROSS JOIN dim_geography AS g
CROSS JOIN (
    SELECT DISTINCT reporting_year FROM fact_wait_time
) AS y
WHERE g.geo_type IN ('country', 'province', 'health_authority', 'hospital')
  -- TODO: identify missing combinations.
;

-- Q12
-- KPI: Benchmark compliance trend over five years for selected procedures.
-- Intended audience: Exec
SELECT
    p.procedure_name,
    g.geo_name,
    f.reporting_year,
    f.pct_meeting_benchmark
FROM fact_wait_time AS f
JOIN dim_procedure AS p ON p.procedure_id = f.procedure_id
JOIN dim_geography AS g ON g.geo_id = f.geo_id
WHERE p.procedure_name IN ('TODO selected procedure')
  -- TODO: filter to the latest five years.
;
