# Opus Review Guide

## Review Goal

Review this repository as a portfolio project for a Junior Business Advisor, Data & Analytics application. Prioritize correctness, honesty, healthcare reporting fit, and whether the project demonstrates executive-ready communication.

## Architecture review

- Check whether the flow from raw public files to PostgreSQL to KPI/data-quality/EDA/reporting artifacts is clear and repeatable.
- Check whether module boundaries are reasonable: ingest, KPI, quality, EDA, dashboard data, and portfolio artifacts.
- Check whether generated reports match the stated public-data boundaries.

## Data review

- Verify that no patient-level or internal VCH data is used.
- Review the CIHI and BC_MoH unit assumptions, especially BC weeks-to-days conversion and CIHI hip-fracture hours-to-days conversion.
- Review the handling of suppressed/null case volumes and missing benchmark values.

## Dashboard review

- Assess whether the dashboard pages are useful for healthcare leaders and analysts.
- Check whether caveats are visible without overwhelming the executive summary.
- Review chart choices for clarity and misleading comparisons.

## Code review

- Run `make load`, `make kpis`, `make quality`, `make eda`, `make artifacts`, `pytest -q`, and `ruff check . --exclude data/raw --exclude .venv`.
- Look for brittle SQL filters, hidden source assumptions, unhandled DB failures, and duplicated query logic.

## Output expected

Return findings first, ordered by severity, with file/line references where possible. Then provide a short summary of strengths and a prioritized fix list before dashboard deployment.
