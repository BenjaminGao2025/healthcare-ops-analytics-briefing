# Data Quality First Run

Generated from public aggregate CIHI and BC_MoH wait-time data.

## DQ01 — Row counts per source per year

Audience: Data Quality

Rows returned: 33

| source_name | reporting_year | row_count |
| --- | --- | --- |
| BC_MoH | 2009 | 3357 |
| BC_MoH | 2010 | 3440 |
| BC_MoH | 2011 | 3473 |
| BC_MoH | 2012 | 3470 |
| BC_MoH | 2013 | 3453 |
| BC_MoH | 2014 | 3414 |
| BC_MoH | 2015 | 3407 |
| BC_MoH | 2016 | 3439 |
| BC_MoH | 2017 | 3449 |
| BC_MoH | 2018 | 3397 |
| BC_MoH | 2019 | 3409 |
| BC_MoH | 2020 | 3408 |
| BC_MoH | 2021 | 3477 |
| BC_MoH | 2022 | 3485 |
| BC_MoH | 2023 | 3473 |
| BC_MoH | 2024 | 3473 |
| CIHI | 2008 | 56 |
| CIHI | 2009 | 67 |
| CIHI | 2010 | 78 |
| CIHI | 2011 | 81 |
| CIHI | 2012 | 79 |
| CIHI | 2013 | 132 |
| CIHI | 2014 | 212 |
| CIHI | 2015 | 216 |
| CIHI | 2016 | 217 |
| CIHI | 2017 | 218 |
| CIHI | 2018 | 221 |
| CIHI | 2019 | 467 |
| CIHI | 2020 | 466 |
| CIHI | 2021 | 467 |
| CIHI | 2022 | 468 |
| CIHI | 2023 | 469 |
| CIHI | 2024 | 236 |

## DQ02 — Missing values per source

Audience: Data Quality

Rows returned: 2

| source_name | total_rows | missing_median_wait_days | missing_median_wait_days_pct | missing_p90_wait_days | missing_p90_wait_days_pct | missing_pct_meeting_benchmark | missing_pct_meeting_benchmark_pct | missing_case_volume | missing_case_volume_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BC_MoH | 55024 | 10900 | 19.81 | 10900 | 19.81 | 55024 | 100 | 9688 | 17.61 |
| CIHI | 4150 | 115 | 2.77 | 117 | 2.82 | 1763 | 42.48 | 17 | 0.41 |

## DQ03 — Duplicate fact keys

Audience: Data Quality

Rows returned: 2

| source_name | duplicate_key_count | duplicate_row_count |
| --- | --- | --- |
| BC_MoH | 0 | 0 |
| CIHI | 0 | 0 |

## DQ04 — Out-of-range values

Audience: Data Quality

Rows returned: 5

| issue_type | bad_row_count |
| --- | --- |
| negative_case_volume | 0 |
| negative_median_wait_days | 0 |
| negative_p90_wait_days | 0 |
| p90_less_than_median | 0 |
| pct_meeting_benchmark_outside_0_100 | 0 |

## DQ05 — Category drift and broken dimension links

Audience: Data Quality

Rows returned: 4

| issue_type | bad_row_count |
| --- | --- |
| blank_geography_name | 0 |
| blank_procedure_name | 0 |
| missing_geography_dimension | 0 |
| missing_procedure_dimension | 0 |

## DQ06 — Freshness by source

Audience: Data Quality

Rows returned: 2

| source_name | max_loaded_at | age_days | freshness_status |
| --- | --- | --- | --- |
| BC_MoH | 2026-05-24 21:46:15.192048+00:00 | 0.1 | ok |
| CIHI | 2026-05-24 21:46:15.192048+00:00 | 0.1 | ok |

## DQ07 — Reporting coverage by source and geography level

Audience: Data Quality

Rows returned: 92

| source_name | geo_type | reporting_year | n_procedures | n_rows |
| --- | --- | --- | --- | --- |
| BC_MoH | health_authority | 2009 | 85 | 445 |
| BC_MoH | health_authority | 2010 | 85 | 471 |
| BC_MoH | health_authority | 2011 | 84 | 483 |
| BC_MoH | health_authority | 2012 | 85 | 483 |
| BC_MoH | health_authority | 2013 | 85 | 485 |
| BC_MoH | health_authority | 2014 | 84 | 485 |
| BC_MoH | health_authority | 2015 | 84 | 485 |
| BC_MoH | health_authority | 2016 | 84 | 479 |
| BC_MoH | health_authority | 2017 | 84 | 477 |
| BC_MoH | health_authority | 2018 | 84 | 478 |
| BC_MoH | health_authority | 2019 | 84 | 476 |
| BC_MoH | health_authority | 2020 | 84 | 479 |
| BC_MoH | health_authority | 2021 | 84 | 486 |
| BC_MoH | health_authority | 2022 | 84 | 483 |
| BC_MoH | health_authority | 2023 | 85 | 484 |
| BC_MoH | health_authority | 2024 | 84 | 484 |
| BC_MoH | hospital | 2009 | 85 | 2827 |
| BC_MoH | hospital | 2010 | 85 | 2884 |
| BC_MoH | hospital | 2011 | 84 | 2906 |
| BC_MoH | hospital | 2012 | 85 | 2902 |
| BC_MoH | hospital | 2013 | 85 | 2883 |
| BC_MoH | hospital | 2014 | 84 | 2845 |
| BC_MoH | hospital | 2015 | 84 | 2838 |
| BC_MoH | hospital | 2016 | 84 | 2876 |
| BC_MoH | hospital | 2017 | 84 | 2888 |
| BC_MoH | hospital | 2018 | 84 | 2835 |
| BC_MoH | hospital | 2019 | 84 | 2849 |
| BC_MoH | hospital | 2020 | 84 | 2845 |
| BC_MoH | hospital | 2021 | 84 | 2907 |
| BC_MoH | hospital | 2022 | 84 | 2918 |
| BC_MoH | hospital | 2023 | 85 | 2904 |
| BC_MoH | hospital | 2024 | 84 | 2905 |
| BC_MoH | province | 2009 | 85 | 85 |
| BC_MoH | province | 2010 | 85 | 85 |
| BC_MoH | province | 2011 | 84 | 84 |
| BC_MoH | province | 2012 | 85 | 85 |
| BC_MoH | province | 2013 | 85 | 85 |
| BC_MoH | province | 2014 | 84 | 84 |
| BC_MoH | province | 2015 | 84 | 84 |
| BC_MoH | province | 2016 | 84 | 84 |
| BC_MoH | province | 2017 | 84 | 84 |
| BC_MoH | province | 2018 | 84 | 84 |
| BC_MoH | province | 2019 | 84 | 84 |
| BC_MoH | province | 2020 | 84 | 84 |
| BC_MoH | province | 2021 | 84 | 84 |
| BC_MoH | province | 2022 | 84 | 84 |
| BC_MoH | province | 2023 | 85 | 85 |
| BC_MoH | province | 2024 | 84 | 84 |
| CIHI | country | 2009 | 1 | 1 |
| CIHI | country | 2010 | 6 | 6 |
| CIHI | country | 2011 | 6 | 6 |
| CIHI | country | 2012 | 6 | 6 |
| CIHI | country | 2013 | 11 | 11 |
| CIHI | country | 2014 | 11 | 11 |
| CIHI | country | 2015 | 11 | 11 |
| CIHI | country | 2016 | 11 | 11 |
| CIHI | country | 2017 | 11 | 11 |
| CIHI | country | 2018 | 13 | 13 |
| CIHI | country | 2019 | 13 | 37 |
| CIHI | country | 2020 | 13 | 37 |
| CIHI | country | 2021 | 13 | 37 |
| CIHI | country | 2022 | 13 | 37 |
| CIHI | country | 2023 | 13 | 37 |
| CIHI | country | 2024 | 13 | 13 |
| CIHI | health_region | 2014 | 2 | 82 |
| CIHI | health_region | 2015 | 2 | 85 |
| CIHI | health_region | 2016 | 2 | 86 |
| CIHI | health_region | 2017 | 2 | 86 |
| CIHI | health_region | 2018 | 2 | 85 |
| CIHI | health_region | 2019 | 2 | 86 |
| CIHI | health_region | 2020 | 2 | 85 |
| CIHI | health_region | 2021 | 2 | 85 |
| CIHI | health_region | 2022 | 2 | 86 |
| CIHI | health_region | 2023 | 2 | 86 |
| CIHI | health_region | 2024 | 2 | 102 |
| CIHI | province | 2008 | 7 | 56 |
| CIHI | province | 2009 | 9 | 66 |
| CIHI | province | 2010 | 9 | 72 |
| CIHI | province | 2011 | 9 | 75 |
| CIHI | province | 2012 | 9 | 73 |
| CIHI | province | 2013 | 14 | 121 |
| CIHI | province | 2014 | 14 | 119 |
| CIHI | province | 2015 | 14 | 120 |
| CIHI | province | 2016 | 14 | 120 |
| CIHI | province | 2017 | 14 | 121 |
| CIHI | province | 2018 | 14 | 123 |
| CIHI | province | 2019 | 14 | 344 |
| CIHI | province | 2020 | 14 | 344 |
| CIHI | province | 2021 | 14 | 345 |
| CIHI | province | 2022 | 14 | 345 |
| CIHI | province | 2023 | 14 | 346 |
| CIHI | province | 2024 | 14 | 121 |

## DQ08 — Suppressed count summary

Audience: Data Quality

Rows returned: 2

| source_name | total_rows | suppressed_case_volume_rows | suppressed_case_volume_pct |
| --- | --- | --- | --- |
| BC_MoH | 55024 | 9688 | 17.61 |
| CIHI | 4150 | 0 | 0 |
