# Analyst Report

## Executive Readout

The largest latest-year BC vs Canada median-wait gap is MRI Scan at 29.3 days. In Vancouver Coastal, the longest latest-fiscal-year median wait is Dental Surgery at 226.1 days.

Data quality is suitable for a portfolio dashboard, with no duplicate fact keys or impossible wait values from Day 3 checks. The main caveat is BC_MoH case-volume suppression: 9,688 rows (17.6%) have null case volume and should stay visibly labeled rather than filled.

## National Wait-Time Snapshot

| procedure_name | median_wait_days | p90_wait_days | pct_meeting_benchmark | case_volume |
| --- | --- | --- | --- | --- |
| CT Scan | 15.8 | 128.0 |  | 1026885 |
| MRI Scan | 56.7 | 198.4 |  | 668620 |
| Cataract Surgery | 67.9 | 229.2 | 69.0 | 203920 |
| Radiation Therapy | 12.4 | 23.5 | 94.1 | 54217 |
| Knee Replacement | 150.7 | 386.8 | 61.4 | 42418 |
| Hip Replacement | 125.4 | 339.9 | 67.9 | 27591 |
| Breast Cancer Surgery | 23.1 | 47.4 |  | 18085 |
| Bladder Cancer Surgery | 27.9 | 66.5 |  | 13946 |

## BC vs Canada Gaps

| procedure_name | bc_median | canada_median | gap_days |
| --- | --- | --- | --- |
| MRI Scan | 86.0 | 56.7 | 29.3 |
| Knee Replacement | 165.0 | 150.7 | 14.3 |
| CT Scan | 24.0 | 15.8 | 8.2 |
| Hip Replacement | 133.0 | 125.4 | 7.6 |
| Radiation Therapy | 14.0 | 12.4 | 1.6 |
| CABG | 9.0 | 7.8 | 1.2 |
| Hip Fracture Repair | 1.5 | 1.0 | 0.4 |
| Breast Cancer Surgery | 21.0 | 23.1 | -2.1 |

## Vancouver Coastal Operational View

| procedure_name | median_wait_days | p90_wait_days | case_volume |
| --- | --- | --- | --- |
| Dental Surgery | 226.1 | 465.5 | 365 |
| Varicose Veins Ligation/Stripping | 193.2 | 493.5 | 355 |
| Other Ear Surgery | 179.9 | 424.2 | 114 |
| Tonsillectomy/Adenoidectomy | 147.7 | 364.0 | 483 |
| Knee Replacement | 130.9 | 399.0 | 2636 |
| Nasal Surgery | 112.0 | 378.7 | 1193 |
| Foot/Ankle Surgery | 111.3 | 538.3 | 276 |
| Hip Replacement | 111.3 | 322.7 | 1878 |
| Tympanoplasty | 104.3 | 452.9 | 212 |
| Sinus Surgery | 91.7 | 466.9 | 844 |

## Data Quality Caveats

| source_name | total_rows | missing_median_wait_days | missing_median_wait_days_pct | missing_case_volume | missing_case_volume_pct |
| --- | --- | --- | --- | --- | --- |
| BC_MoH | 55024 | 10900 | 19.8 | 9688 | 17.6 |
| CIHI | 4150 | 115 | 2.8 | 17 | 0.4 |

## Suggested Dashboard Implications

- Put BC vs Canada gaps in the executive summary, because they translate directly into leadership-facing variance.
- Put Vancouver Coastal procedure waits in the operational drilldown, because this is where managers can inspect local pressure points.
- Put missingness and suppressed case-volume rates in the data quality tab, because these limits affect interpretation.
