# Data Dictionary

Version: v0.8 — 2026-05-24

## Tables

- `dim_procedure`: Standardized procedure names, categories, and benchmark metadata used in wait-time reporting.
- `dim_geography`: Geography hierarchy for Canada, province, health authority, and hospital records.
- `fact_wait_time`: Core wait-time KPI table by procedure, geography, reporting year, and reporting period.

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

## Data Quality Check Catalog

| ID | Name | Purpose | Key output columns | Query file |
|---|---|---|---|---|
| DQ01 | Row counts per source per year | Confirm source coverage and year-level load shape. | `source_name`, `reporting_year`, `row_count` | `sql/04_data_quality_checks.sql` |
| DQ02 | Missing values per source | Quantify missing core metrics by source. | `source_name`, `total_rows`, `missing_*`, `missing_*_pct` | `sql/04_data_quality_checks.sql` |
| DQ03 | Duplicate fact keys | Detect duplicate source/procedure/geography/year/period rows. | `source_name`, `duplicate_key_count`, `duplicate_row_count` | `sql/04_data_quality_checks.sql` |
| DQ04 | Out-of-range values | Flag impossible waits, benchmark percentages, and volumes. | `issue_type`, `bad_row_count` | `sql/04_data_quality_checks.sql` |
| DQ05 | Category drift and broken dimension links | Check missing dimension references and blank dimension names. | `issue_type`, `bad_row_count` | `sql/04_data_quality_checks.sql` |
| DQ06 | Load recency by source | Warn when loaded database rows are older than 30 days. This does not measure source publication recency. | `source_name`, `max_loaded_at`, `age_days`, `freshness_status` | `sql/04_data_quality_checks.sql` |
| DQ07 | Reporting coverage by source and geography level | Show year-level row coverage by source and geography type. | `source_name`, `geo_type`, `reporting_year`, `n_procedures`, `n_rows` | `sql/04_data_quality_checks.sql` |
| DQ08 | Suppressed count summary | Summarize BC suppressed case-volume rows preserved as null. | `source_name`, `total_rows`, `suppressed_case_volume_rows`, `suppressed_case_volume_pct` | `sql/04_data_quality_checks.sql` |

## Analysis Artifacts

| Artifact | Purpose | Generated by |
|---|---|---|
| `data/processed/eda_summary.md` | Compact Day 4 EDA tables for source counts, national snapshot, BC gaps, VCH long waits, and quality caveats. | `make eda` |
| `reports/analyst_report.md` | Analyst-facing narrative report that translates KPI and quality results into dashboard implications. | `make eda` |
| `notebooks/01_eda_wait_times.ipynb` | Notebook entry point for interactive review of Day 4 EDA frames. | `make eda` |
| `reports/methodology_note.md` | One-page methodology note covering scope, data boundaries, transformations, and interpretation limits. | `make artifacts` |
| `reports/opus_review_guide.md` | Review instructions for an independent code and analytics review. | `make artifacts` |
| `reports/board_briefing_deck.md` | Six-page briefing deck source used to generate the local PDF. | `make artifacts` |
| `reports/board_briefing_deck.pdf` | Six-page board-style briefing deck generated locally and ignored by Git. | `make artifacts` |
| `excel/healthcare_ops_analytics_workbook.xlsx` | Excel workbook with summary, KPI, and quality tabs generated locally and ignored by Git. | `make artifacts` |

## Dashboard Data Frames

| Frame | Source query | Primary dashboard use |
|---|---|---|
| `national_snapshot` | K01 | Executive Summary national latest-year table. |
| `bc_gap` | K03 | Executive Summary BC vs Canada access gap chart. |
| `national_trend` | K04 | Operational Drilldown national 5-year trend. |
| `tail_risk` | K06 | Operational Drilldown p90-to-median risk review. |
| `bc_ha_comparison` | K07 | Operational Drilldown BC health authority comparison. |
| `vch_long_waits` | K08 | Executive Summary and Operational Drilldown VCH long-wait table. |
| `vch_vs_other_gap` | K09 | Operational Drilldown VCH vs other BC HA gap table. |
| `vch_hospital_p90` | K10 | Operational Drilldown VCH hospital p90 table. |
| `ha_volume_trend` | K11 | Operational Drilldown health-authority volume trend. |
| `missingness` | DQ02 | Data Quality Monitor missingness chart. |
| `duplicates` | DQ03 | Data Quality Monitor duplicate-key metric. |
| `validity` | DQ04 | Data Quality Monitor impossible-value checks. |
| `freshness` | DQ06 | Data Quality Monitor load recency status. |
| `suppressed_counts` | DQ08 | Data Quality Monitor suppressed/null case-volume metric. |

## Source coverage

| Source | Years covered | Geos covered | Procedures covered | Rows loaded |
|---|---|---|---|---|
| CIHI | 2008-2024 plus FY/Q3Q4 labels for selected pandemic periods | Canada, provinces, and health regions where available | 14 indicators | 4,150 |
| BC_MoH | 2009/10-2024/25 fiscal years | British Columbia, health authorities, and hospitals | 85 procedure groups | 55,024 |

## Open questions

- CIHI `Data year` includes standard April-September rows plus `FY` and `Q3Q4` suffixes. The loader keeps the leading year in `reporting_year` and stores the suffix in `reporting_period`; confirm this is the preferred reporting convention.
- CIHI hip fracture repair uses hours for some wait metrics. The loader divides hours by 24 to fit `*_wait_days`; range sanity checks support the conversion, but the dashboard should likely display these procedures in hours for healthcare readers.
- BC Surgical Wait Times has fiscal-year labels such as `2024/25`. The loader stores `2024` as `reporting_year` and `FY 2024/25` as `reporting_period`; verify this with the final reporting narrative.
- BC Surgical Wait Times percentile definitions are documented by the [B.C. wait-time data collection page](https://www2.gov.bc.ca/gov/content/health/accessing-health-care/surgical-wait-times/understanding-wait-times/wait-time-data-collection), but the downloaded public export does not include a separate field-level metadata sheet. The loader interprets `COMPLETED_50TH_PERCENTILE` and `COMPLETED_90TH_PERCENTILE` as weeks and multiplies by 7 to fit `*_wait_days`; range sanity checks support the conversion, and source-owner confirmation would be required before operational use.
- BC suppressed counts such as `<5` are stored as NULL rather than approximated, to avoid inventing case volume.
