# Data Dictionary

Version: v0.3 — 2026-05-24

## Tables

- `dim_procedure`: Standardized procedure names, categories, and benchmark metadata used in wait-time reporting.
- `dim_geography`: Geography hierarchy for Canada, province, health authority, hospital, and community-level records.
- `fact_wait_time`: Core wait-time KPI table by procedure, geography, reporting year, and reporting period.
- `dim_community`: Aggregate community indicators used for context and equity-aware interpretation.

## Columns

### `fact_wait_time`

| Column | Type | Definition | Example |
|---|---|---|---|
| `wait_time_id` | `bigserial` | Surrogate primary key for a wait-time fact row. | `1` |
| `source_name` | `text` | Public source that supplied the row. | `CIHI`, `BC_MoH` |
| `procedure_id` | `integer` | Foreign key linking the row to `dim_procedure`; procedure examples include hip replacement and cataract surgery. | Links to `Hip Replacement` |
| `geo_id` | `integer` | Foreign key linking the row to `dim_geography`; geography examples include Canada, British Columbia, Vancouver Coastal Health, and Richmond Hospital. | Links to `Canada` |
| `reporting_year` | `integer` | Leading calendar or fiscal year, normalized from source labels. | `2024` |
| `reporting_period` | `text` | Period label from the source file. | `Apr-Sep`, `FY 2024/25`, `Q3Q4 2023` |
| `median_wait_days` | `numeric` | Median wait time normalized to days. | `42.0` |
| `p90_wait_days` | `numeric` | 90th percentile wait time normalized to days. | `182.0` |
| `pct_meeting_benchmark` | `numeric` | Percentage of cases meeting the relevant benchmark, when available. | `75.4` |
| `case_volume` | `integer` | Number of completed procedures or cases represented by the row, where source suppression allows a value. | `1586` |
| `loaded_at` | `timestamptz` | Timestamp when the row was loaded into PostgreSQL. | `2026-05-24 14:30:00-07` |

## KPI definitions

| KPI | Plain-English definition | Formula / source field | Audience |
|---|---|---|---|
| Median wait | Days waited by the median patient for the procedure in the reporting period. | `fact_wait_time.median_wait_days` | Exec / Operational |
| 90th-percentile wait | The wait length that 9 in 10 patients fall under; signals tail risk. | `fact_wait_time.p90_wait_days` | Exec / Operational |
| % meeting benchmark | Share of patients whose wait was within the procedure's national benchmark. | `fact_wait_time.pct_meeting_benchmark` | Exec |
| Case volume | Number of completed procedures in the reporting period. | `fact_wait_time.case_volume` | Exec / Operational |
| BC vs Canada gap | BC median wait minus Canada median wait for the same procedure and year. Positive = BC is slower. | `median_wait_days[BC] - median_wait_days[Canada]` (computed) | Exec |

## KPI Catalog

| ID | Name | Audience | Source | Key output columns | Query file |
|---|---|---|---|---|---|
| K01 | National median wait, latest year, by procedure | Executive | CIHI | `procedure_name`, `median_wait_days`, `p90_wait_days`, `pct_meeting_benchmark`, `case_volume` | `sql/03_kpi_queries.sql` |
| K02 | Provincial median wait, latest year, top 10 procedures by volume | Executive | CIHI | `procedure_name`, `province`, `median_wait_days`, `p90_wait_days` | `sql/03_kpi_queries.sql` |
| K03 | BC vs Canada gap, latest year | Executive | CIHI | `procedure_name`, `bc_median`, `canada_median`, `gap_days`, `gap_pct` | `sql/03_kpi_queries.sql` |
| K04 | 5-year median wait trend, top 5 procedures | Operational | CIHI | `procedure_name`, `reporting_year`, `median_wait_days` | `sql/03_kpi_queries.sql` |
| K05 | % meeting benchmark by procedure x province, latest year | Executive | CIHI | `procedure_name`, `province`, `pct_meeting_benchmark` | `sql/03_kpi_queries.sql` |
| K06 | p90 tail risk by procedure x province, latest year | Operational | CIHI | `procedure_name`, `province`, `median_wait_days`, `p90_wait_days`, `p90_to_median_ratio` | `sql/03_kpi_queries.sql` |
| K07 | BC Health Authority comparison, latest fiscal year | Executive | BC_MoH | `health_authority`, `procedure_name`, `median_wait_days`, `case_volume` | `sql/03_kpi_queries.sql` |
| K08 | VCH top 20 long-wait procedures, latest fiscal year | Operational | BC_MoH | `procedure_name`, `median_wait_days`, `p90_wait_days`, `case_volume` | `sql/03_kpi_queries.sql` |
| K09 | VCH vs other BC HAs gap, latest fiscal year | Executive | BC_MoH | `procedure_name`, `vch_median`, `bc_other_avg_median`, `gap_days` | `sql/03_kpi_queries.sql` |
| K10 | VCH hospital-level p90, latest fiscal year | Operational | BC_MoH | `hospital`, `procedure_name`, `p90_wait_days`, `median_wait_days`, `case_volume` | `sql/03_kpi_queries.sql` |
| K11 | Case volume trend by HA, last 5 fiscal years | Operational | BC_MoH | `health_authority`, `reporting_year`, `total_case_volume` | `sql/03_kpi_queries.sql` |
| K12 | Reporting coverage by source x geo level | Data Quality | CIHI / BC_MoH | `source_name`, `geo_type`, `latest_reporting_year`, `latest_reporting_period`, `n_procedures`, `n_rows` | `sql/03_kpi_queries.sql` |

## Source coverage

| Source | Years covered | Geos covered | Procedures covered | Rows loaded |
|---|---|---|---|---|
| CIHI | 2008-2024 plus FY/Q3Q4 labels for selected pandemic periods | Canada, provinces, and health regions where available | 14 indicators | 4,150 |
| BC_MoH | 2009/10-2024/25 fiscal years | British Columbia, health authorities, and hospitals | 85 procedure groups | 55,024 |

## Open questions

- CIHI `Data year` includes standard April-September rows plus `FY` and `Q3Q4` suffixes. The loader keeps the leading year in `reporting_year` and stores the suffix in `reporting_period`; confirm this is the preferred reporting convention.
- CIHI hip fracture repair uses hours for some wait metrics. The loader divides hours by 24 to fit `*_wait_days`; range sanity checks support the conversion, but the dashboard should likely display these procedures in hours for healthcare readers.
- BC Surgical Wait Times has fiscal-year labels such as `2024/25`. The loader stores `2024` as `reporting_year` and `FY 2024/25` as `reporting_period`; verify this with the final reporting narrative.
- BC Surgical Wait Times percentile values appear to be in weeks. The loader multiplies them by 7 to fit `*_wait_days`; range sanity checks support the conversion, but confirm against source metadata before final publication.
- BC suppressed counts such as `<5` are stored as NULL rather than approximated, to avoid inventing case volume.
- VCH Community Profiles are not loaded in Day 1; the profile PDF extraction plan still needs to be defined.
