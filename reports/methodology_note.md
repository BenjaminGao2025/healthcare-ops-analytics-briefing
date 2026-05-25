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
- BC percentile fields are treated as weeks and converted to days after range sanity checks.
- Suppressed or unavailable case-volume values are preserved as nulls rather than estimated.

## Interpretation Limits

- CIHI and BC_MoH are not perfect substitutes; they answer overlapping but different reporting questions.
- Missing benchmark percentages and suppressed volumes should be visible in dashboard caveats.
- Results are appropriate for portfolio demonstration and planning-style analytics, not for operational claims about live health-system performance.
