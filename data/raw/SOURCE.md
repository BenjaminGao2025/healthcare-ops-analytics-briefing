# Raw Data Source Log

| Source | URL | File pattern | Date downloaded | License | Notes |
|---|---|---|---|---|---|
| CIHI Wait Times (Priority Proc) | https://www.cihi.ca/en/explore-wait-times-for-priority-procedures-across-canada | `cihi_wait_times_<YYYYMMDD>.xlsx` | TBD | © CIHI. Used under CIHI Open Data terms. Attribution required. | Pull historical data tables for hip/knee/cataract/cancer/CT/MRI/etc. |
| BC Surgical Wait Times | https://www2.gov.bc.ca/gov/content/health/accessing-health-care/surgical-wait-times | `bc_surgical_wait_<YYYYMMDD>.csv` | TBD | Province of BC — Open Government Licence – BC. | Filter to Vancouver Coastal HA for the headline narrative. |
| VCH Community Health Profiles | https://www.vch.ca/en/community-health-profiles | `vch_community_profiles/<community>.pdf` | TBD | © Vancouver Coastal Health. Used for non-commercial portfolio demo with attribution. | PDFs; hand-extract indicators into `data/processed/vch_community_indicators.csv`. |

**Disclaimer:** All data is publicly available, aggregate, non-identifiable. No
patient-level data. No VCH internal data is used in this project.
