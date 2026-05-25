# Data Dictionary

Version: 0.1

## Tables

- `dim_procedure`: Standardized procedure names, categories, and benchmark metadata used in wait-time reporting.
- `dim_geography`: Geography hierarchy for Canada, province, health authority, hospital, and community-level records.
- `fact_wait_time`: Core wait-time KPI table by procedure, geography, reporting year, and reporting period.
- `dim_community`: Aggregate community indicators used for context and equity-aware interpretation.

## Columns

### `fact_wait_time`

| Column | Type | Definition |
|---|---|---|
| `wait_time_id` | `bigserial` | Surrogate primary key for a wait-time fact row. |
| `source_name` | `text` | Public source that supplied the row, such as CIHI or BC Surgical Wait Times. |
| `procedure_id` | `integer` | Foreign key linking the row to `dim_procedure`. |
| `geo_id` | `integer` | Foreign key linking the row to `dim_geography`. |
| `reporting_year` | `integer` | Calendar or fiscal reporting year, depending on source documentation. |
| `reporting_period` | `text` | Period label from the source file, such as annual, quarter, or month. |
| `median_wait_days` | `numeric` | Median wait time in days for the procedure and geography. |
| `p90_wait_days` | `numeric` | 90th percentile wait time in days for the procedure and geography. |
| `pct_meeting_benchmark` | `numeric` | Percentage of cases meeting the relevant benchmark, when available. |
| `case_volume` | `integer` | Number of cases, procedures, or records represented by the row. |
| `loaded_at` | `timestamptz` | Timestamp when the row was loaded into PostgreSQL. |

## KPI definitions

| KPI | Plain-English definition | Formula / source field | Audience |
|---|---|---|---|
| Median wait | Days waited by the median patient for the procedure in the reporting period. | `fact_wait_time.median_wait_days` | Exec / Operational |
| 90th-percentile wait | The wait length that 9 in 10 patients fall under; signals tail risk. | `fact_wait_time.p90_wait_days` | Exec / Operational |
| % meeting benchmark | Share of patients whose wait was within the procedure's national benchmark. | `fact_wait_time.pct_meeting_benchmark` | Exec |
| Case volume | Number of procedures completed in the reporting period. | `fact_wait_time.case_volume` | Exec / Operational |
| BC vs Canada gap | BC median wait minus Canada median wait for the same procedure and year. Positive = BC is slower. | `median_wait_days[BC] - median_wait_days[Canada]` (computed) | Exec |

## Open Questions

- CIHI 各年份的报告口径是否完全一致（reporting period boundaries, procedure definitions）？需要在加载前对齐。
- BC Surgical Wait Times 是否区分 "scheduled" vs "completed"？两套口径不能混。
- VCH Community Profiles 的指标 vintage（年份）是否一致？不同社区可能不同年份。
- Benchmark 阈值（e.g. hip 26 weeks）需要单独建表还是写进 `dim_procedure.benchmark_days`？
- p90 数据在 CIHI 表里不是所有年份/省份都有 — 缺失策略是 NULL 还是不入库？
