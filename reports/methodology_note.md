# Methodology Note

## Purpose

This portfolio project demonstrates how public aggregate healthcare wait-time data can be transformed into executive-ready reporting, operational drilldowns, and data quality monitoring.

## Data Boundary

- Uses public aggregate sources only: CIHI wait-time tables and BC_MoH surgical wait-time exports.
- No patient-level data.
- No VCH internal data.
- No clinical decision support or patient-specific inference.

## Transformations

- CIHI national, provincial, and regional rows are normalized into shared procedure, geography, year, period, and KPI fields.
- BC_MoH fiscal-year surgical rows are normalized into province, health authority, and hospital geographies.
- BC_MoH percentile definitions are documented by the [B.C. wait-time data collection page](https://www2.gov.bc.ca/gov/content/health/accessing-health-care/surgical-wait-times/understanding-wait-times/wait-time-data-collection). The downloaded public export does not include a separate field-level metadata sheet, so `COMPLETED_50TH_PERCENTILE` and `COMPLETED_90TH_PERCENTILE` are interpreted as weeks and converted to days based on public reporting context plus range checks against CIHI hip/knee procedure magnitudes documented in `INSPECTION_NOTES.md`.
- CIHI Hip Fracture Repair values reported in hours are converted to days for table consistency and called out in the Executive Summary.
- Suppressed or unavailable case-volume values are preserved as nulls rather than estimated.

## Interpretation Limits

- CIHI and BC_MoH are not perfect substitutes; they answer overlapping but different reporting questions.
- Missing benchmark percentages and suppressed volumes should be visible in dashboard caveats.
- Load recency reflects when the database was refreshed, not the source publication date.
- Results are appropriate for portfolio demonstration and planning-style analytics, not for operational claims about live health-system performance.
