# Inspection Notes

Generated from public aggregate source files in `data/raw/`.

## CIHI wait times workbook

- File: `cihi_wait_times_20260524.xlsx`
- Sheet names: Instructions, Table 1, Methodology notes, Contact information
- Parsed table shape: 18965 rows x 12 columns
- Valid reporting rows: 18956
- Normalized fact-ready rows: 4150

### CIHI columns and dtypes

| column | dtype |
| --- | --- |
| Reporting level | object |
| Province | object |
| Region | object |
| Indicator | object |
| Metric | object |
| Data year | object |
| Unit of measurement | object |
| Indicator result | float64 |
| Column1 | float64 |
| Unnamed: 9 | object |
| Unnamed: 10 | float64 |
| Unnamed: 11 | float64 |

### CIHI sample rows

| Reporting level | Province | Region | Indicator | Metric | Data year | Unit of measurement | Indicator result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Provincial | Alberta | nan | Bladder Cancer Surgery | 50th Percentile | 2008 | Days | nan |
| Provincial | Alberta | nan | Bladder Cancer Surgery | 90th Percentile | 2008 | Days | nan |
| Provincial | Alberta | nan | Bladder Cancer Surgery | Volume | 2008 | Number of cases | nan |
| Provincial | Alberta | nan | Breast Cancer Surgery | 50th Percentile | 2008 | Days | nan |
| Provincial | Alberta | nan | Breast Cancer Surgery | 90th Percentile | 2008 | Days | nan |

### CIHI missingness

| column | missing_count | missing_pct |
| --- | --- | --- |
| Reporting level | 0 | 0.0 |
| Province | 0 | 0.0 |
| Region | 13500 | 71.22 |
| Indicator | 0 | 0.0 |
| Metric | 0 | 0.0 |
| Data year | 0 | 0.0 |
| Unit of measurement | 0 | 0.0 |
| Indicator result | 4368 | 23.04 |

### CIHI categorical distinct values

| column | distinct_count | sample_values |
| --- | --- | --- |
| Reporting level | 3 | Provincial, National, Regional |
| Province | 11 | Alberta, British Columbia, Canada, Manitoba, New Brunswick, Newfoundland and Labrador, Nova Scotia, Ontario, Prince Edward Island, Quebec, Saskatchewan |
| Region | 62 | South Zone, Calgary Zone, Central Zone (Alta.), Edmonton Zone, North Zone (Alta.), Interior Health, Fraser Health, Vancouver Coastal Health, Island Health, Northern Health, Interlake–Eastern Health Region, Southern Health Region, Prairie Mountain Health Region, Northern Health Region, Winnipeg–Churchill Health Region, South-East Zone (N.B.), South-West Zone (N.B.), Central Zone (N.B.), Northern Zone (N.B.), Horizon Health Network, Vitalité Health Network, Western Zone (N.L.), Labrador–Grenfell Zone, Eastern–Rural Zone, Eastern–Urban Zone |
| Indicator | 14 | Bladder Cancer Surgery, Breast Cancer Surgery, CABG, Cataract Surgery, Colorectal Cancer Surgery, CT Scan, Hip Fracture Repair, Hip Fracture Repair/Emergency and Inpatient, Hip Replacement, Knee Replacement, Lung Cancer Surgery, MRI Scan, Prostate Cancer Surgery, Radiation Therapy |
| Metric | 4 | 50th Percentile, 90th Percentile, Volume, % Meeting Benchmark |
| Data year | 27 | 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2019FY, 2019Q3Q4, 2020FY, 2020Q3Q4, 2021FY, 2021Q3Q4, 2022, 2022FY, 2022Q3Q4, 2023, 2023FY |
| Unit of measurement | 4 | Days, Number of cases, Proportion, Hours |

## BC surgical wait times CSV

- File: `bc_surgical_wait_20260524.csv`
- Parsed shape: 55024 rows x 8 columns
- Normalized fact-ready rows: 55024

### BC columns and dtypes

| column | dtype |
| --- | --- |
| FISCAL_YEAR | object |
| HEALTH_AUTHORITY | object |
| HOSPITAL_NAME | object |
| PROCEDURE_GROUP | object |
| WAITING | object |
| COMPLETED | object |
| COMPLETED_50TH_PERCENTILE | float64 |
| COMPLETED_90TH_PERCENTILE | float64 |

### BC sample rows

| FISCAL_YEAR | HEALTH_AUTHORITY | HOSPITAL_NAME | PROCEDURE_GROUP | WAITING | COMPLETED | COMPLETED_50TH_PERCENTILE | COMPLETED_90TH_PERCENTILE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2009/10 | All Health Authorities | All Facilities | Abdominoplasty | 52 | 100 | 9.1 | 42.6 |
| 2009/10 | All Health Authorities | All Facilities | All Other Procedures | 1366 | 6269 | 4.0 | 17.1 |
| 2009/10 | All Health Authorities | All Facilities | All Procedures | 72120 | 219484 | 5.3 | 24.3 |
| 2009/10 | All Health Authorities | All Facilities | Aortic Aneurysm Repair | 96 | 365 | 3.7 | 13.5 |
| 2009/10 | All Health Authorities | All Facilities | Appendectomy | 19 | 88 | 3.7 | 9.1 |

### BC missingness

| column | missing_count | missing_pct |
| --- | --- | --- |
| FISCAL_YEAR | 0 | 0.0 |
| HEALTH_AUTHORITY | 0 | 0.0 |
| HOSPITAL_NAME | 0 | 0.0 |
| PROCEDURE_GROUP | 0 | 0.0 |
| WAITING | 0 | 0.0 |
| COMPLETED | 0 | 0.0 |
| COMPLETED_50TH_PERCENTILE | 10900 | 19.81 |
| COMPLETED_90TH_PERCENTILE | 10900 | 19.81 |

### BC categorical distinct values

| column | distinct_count | sample_values |
| --- | --- | --- |
| FISCAL_YEAR | 16 | 2009/10, 2010/11, 2011/12, 2012/13, 2013/14, 2014/15, 2015/16, 2016/17, 2017/18, 2018/19, 2019/20, 2020/21, 2021/22, 2022/23, 2023/24, 2024/25 |
| HEALTH_AUTHORITY | 7 | All Health Authorities, Fraser, Interior, Northern, Provincial Health Services Authority, Vancouver Coastal, Vancouver Island |
| HOSPITAL_NAME | 66 | All Facilities, Abbotsford Regional Hospital And Cancer Centre, Burnaby Hospital, Chilliwack General Hospital, Delta Hospital, Eagle Ridge Hospital & Health Care Centre, Jim Pattison Outpatient Care And Surgery Centre, Langley Memorial Hospital, Peace Arch District Hospital, Ridge Meadows Hospital And Health Care Centre, Royal Columbian Hospital, Surrey Memorial Hospital, 100 Mile District General Hospital, Cariboo Memorial Hospital, Creston Valley Hospital, East Kootenay Regional Hospital, Elk Valley Hospital, Golden And District General Hospital, Kelowna General Hospital, Kootenay Boundary Regional Hospital, Kootenay Lake Hospital, Lillooet Hospital And Health Centre, Penticton Regional Hospital, Pleasant Valley Health Centre, Queen Victoria Hospital |
| PROCEDURE_GROUP | 85 | Abdominoplasty, All Other Procedures, All Procedures, Aortic Aneurysm Repair, Appendectomy, Bariatric Surgery, Biopsy in OR, Bladder Surgery, Bowel Resection, Breast Biopsy, Breast Reconstruction, Breast Reduction, CSF Drainage, Cataract Surgery, Cholecystectomy, Colostomy/Ileostomy, Cone Biopsy, Cranial Surgery, Cyst/Ganglion Removal, D&C and Related Surgery, Dental Surgery, Endarterectomy, Esophagectomy, Examination Under Anaesthetic, Excision Gynecomastia |

## Source-to-schema mapping

| source_file | source_column | target_table.column | transform_notes |
| --- | --- | --- | --- |
| cihi_wait_times_20260524.xlsx | Indicator | dim_procedure.procedure_name | Direct standard procedure name. |
| cihi_wait_times_20260524.xlsx | Reporting level | dim_geography.geo_type | National -> country; Provincial -> province; Regional -> health_region. |
| cihi_wait_times_20260524.xlsx | Province | dim_geography.geo_name / province_code | Province rows become geography rows; also maps parent province for regions. |
| cihi_wait_times_20260524.xlsx | Region | dim_geography.geo_name | Used when Reporting level is Regional; otherwise blank. |
| cihi_wait_times_20260524.xlsx | Data year | fact_wait_time.reporting_year / reporting_period | Leading year becomes integer year; suffix FY/Q3Q4 becomes reporting_period. |
| cihi_wait_times_20260524.xlsx | Metric | fact_wait_time metric columns | 50th Percentile, 90th Percentile, Volume, % Meeting Benchmark pivot to fact columns. |
| cihi_wait_times_20260524.xlsx | Unit of measurement | fact_wait_time.median_wait_days / p90_wait_days | Hours are divided by 24 to fit *_wait_days; range sanity check supports this conversion. |
| cihi_wait_times_20260524.xlsx | Indicator result | fact_wait_time.median_wait_days / p90_wait_days / pct_meeting_benchmark / case_volume | Value routed by Metric; missing results excluded from fact load. |
| bc_surgical_wait_20260524.csv | PROCEDURE_GROUP | dim_procedure.procedure_name | Direct procedure group label. |
| bc_surgical_wait_20260524.csv | HEALTH_AUTHORITY | dim_geography.geo_name / parent_geo_id | All Health Authorities -> British Columbia province; named HA -> health_authority. |
| bc_surgical_wait_20260524.csv | HOSPITAL_NAME | dim_geography.geo_name | All Facilities uses HA geography; otherwise hospital row under HA. |
| bc_surgical_wait_20260524.csv | FISCAL_YEAR | fact_wait_time.reporting_year / reporting_period | Start year becomes integer year; full fiscal label kept in reporting_period. |
| bc_surgical_wait_20260524.csv | COMPLETED | fact_wait_time.case_volume | <5 suppressed values become NULL rather than estimated. |
| bc_surgical_wait_20260524.csv | COMPLETED_50TH_PERCENTILE | fact_wait_time.median_wait_days | Source values appear to be weeks; multiplied by 7 to fit days. Range sanity check supports this conversion; confirm against source metadata before final publication. |
| bc_surgical_wait_20260524.csv | COMPLETED_90TH_PERCENTILE | fact_wait_time.p90_wait_days | Source values appear to be weeks; multiplied by 7 to fit days. Range sanity check supports this conversion; confirm against source metadata before final publication. |

## Range sanity checks

Run date: 2026-05-24.

### Source-level wait ranges

| source | n | min_med | avg_med | max_med | avg_p90 | max_p90 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BC_MoH | 44,124 | 0 | 54.1 | 998 | 160.9 | 1,793 |
| CIHI | 4,035 | 0 | 81.4 | 649 | 198.1 | 1,238 |

### Hip and knee comparison

| source | procedure_name | avg_med_days | n |
| --- | --- | ---: | ---: |
| CIHI | Hip Fracture Repair | 1.0 | 157 |
| CIHI | Hip Fracture Repair/Emergency and Inpatient | 1.0 | 77 |
| BC_MoH | Hip Replacement | 124.1 | 587 |
| CIHI | Hip Replacement | 145.9 | 770 |
| BC_MoH | Knee - ACL Repair | 78.1 | 735 |
| BC_MoH | Knee Arthroscopy | 58.0 | 798 |
| BC_MoH | Knee - Meniscectomy | 58.1 | 725 |
| BC_MoH | Knee Replacement | 153.7 | 598 |
| CIHI | Knee Replacement | 186.2 | 774 |

### Hip fracture check

| source | procedure_name | avg_med_days | min_d | max_d |
| --- | --- | ---: | ---: | ---: |
| CIHI | Hip Fracture Repair | 0.97 | 0.485069444444446 | 1.70833333333333 |
| CIHI | Hip Fracture Repair/Emergency and Inpatient | 1.01 | 0.395833333333333 | 1.49583333333333 |

Interpretation: BC wait-time percentiles are not 7x larger than CIHI after the weeks-to-days conversion, and hip/knee replacement values are in the same broad range across sources. CIHI hip fracture values are close to 1 day after hours-to-days normalization.

## Day 2 — KPI sanity check (2026-05-24)

### Row count per KPI

| KPI | Rows returned |
| --- | ---: |
| K01 | 13 |
| K02 | 93 |
| K03 | 13 |
| K04 | 25 |
| K05 | 53 |
| K06 | 117 |
| K07 | 484 |
| K08 | 20 |
| K09 | 81 |
| K10 | 401 |
| K11 | 30 |
| K12 | 6 |

### Filters and matching notes

- No procedure-name `ILIKE` matching was needed for Day 2 KPIs.
- K08 uses the exact BC_MoH health authority geography: `geo_name = 'Vancouver Coastal'` and `geo_type = 'health_authority'`.
- K10 uses the geography hierarchy for VCH hospitals: hospital rows whose `parent_geo_id` points to `Vancouver Coastal` (`geo_id = 118`).
- K04 aggregates CIHI rows to one trend point per `procedure_name` x `reporting_year` because CIHI can contain multiple reporting periods in the same leading year.

### Anomalies and hypotheses

- No KPI returned 0 rows.
- K02 returns 93 rows rather than a full 100-row 10-procedure x 10-province grid because not every top-volume procedure has a latest-year provincial row for every province in the loaded CIHI table.
- K05 returns fewer rows than K06 because `pct_meeting_benchmark` is not populated for every procedure x province row.

### Sanity narrative

The largest latest-year BC vs Canada median gaps in CIHI are MRI Scan (+29.3 days), Knee Replacement (+14.3 days), and CT Scan (+8.2 days), which makes the executive gap KPI focus on access-sensitive diagnostic and orthopedic areas. In latest-year BC_MoH data for Vancouver Coastal, the longest median waits are Dental Surgery (226.1 days), Varicose Veins Ligation/Stripping (193.2 days), and Other Ear Surgery (179.9 days), which are plausible non-urgent surgical categories for an operational drilldown.
