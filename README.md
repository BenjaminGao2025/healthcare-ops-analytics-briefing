# Healthcare Ops Analytics Briefing

![CI](https://github.com/BenjaminGao2025/healthcare-ops-analytics-briefing/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)

A public Canadian healthcare operations analytics demo that turns wait-time and access data into executive-ready reporting, quality checks, and briefing artifacts.

Repository target: `https://github.com/BenjaminGao2025/healthcare-ops-analytics-briefing`

## What This Project Demonstrates

- SQL-based KPI extraction for healthcare access and wait-time indicators.
- Python analysis for descriptive statistics, trend exploration, and repeatable reporting.
- Streamlit dashboarding for leadership-facing summaries and operational drilldowns.
- Data quality checks for completeness, validity, duplicates, outliers, and freshness.
- Executive storytelling through concise summaries, briefing materials, and methodology notes.

## Data Sources

| Source | URL | Description |
|---|---|---|
| CIHI Wait Times for Priority Procedures | https://www.cihi.ca/en/explore-wait-times-for-priority-procedures-across-canada | National and provincial wait-time indicators for selected priority procedures. |
| BC Surgical Wait Times | https://www2.gov.bc.ca/gov/content/health/accessing-health-care/surgical-wait-times | British Columbia surgical wait-time context by procedure, region, and care setting where available. |

All data used is publicly available. This project does not use any patient-level or VCH internal data.

## Quickstart

Requires: Docker, Python 3.11, `make`.

```bash
# 1. Clone and enter
git clone https://github.com/BenjaminGao2025/healthcare-ops-analytics-briefing.git
cd healthcare-ops-analytics-briefing

# 2. Python environment
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Start Postgres (Docker)
make up

# 4. Create schema
make schema

# 5. Place raw data files into data/raw/ (see data/raw/SOURCE.md), then:
make load

# 6. Generate reports and review artifacts
make kpis
make quality
make eda
make artifacts

# 7. Launch the dashboard
make app
```

`make app` opens Streamlit on http://localhost:8501. `make artifacts` writes the tracked Markdown methodology/review/deck source files and regenerates the local PDF deck and Excel workbook.

Generated local files intentionally ignored by Git:

- `reports/board_briefing_deck.pdf`
- `excel/healthcare_ops_analytics_workbook.xlsx`

To stop Postgres: `make down`. To open a psql shell: `make psql`.

## Repo Structure

```text
healthcare-ops-analytics-briefing/
  .github/
    workflows/
      ci.yml
  README.md
  LICENSE
  .gitignore
  requirements.txt
  docker-compose.yml
  Makefile
  data/
    raw/
      SOURCE.md
      .gitkeep
    processed/
      .gitkeep
      INSPECTION_NOTES.md
      data_quality_first_run.md
      eda_summary.md
      kpi_first_run.md
    data_dictionary.md
  sql/
    01_schema.sql
    02_load.sql
    03_kpi_queries.sql
    04_data_quality_checks.sql
  notebooks/
    01_eda_wait_times.ipynb
    02_statistical_tests.ipynb
    03_bc_vs_canada_benchmark.ipynb
  src/
    __init__.py
    dashboard_data.py
    eda.py
    ingest.py
    kpi.py
    transform.py
    kpi_calculations.py
    portfolio_artifacts.py
    quality.py
    quality_checks.py
    plots.py
  app/
    streamlit_app.py
    pages/
      1_Executive_Summary.py
      2_Operational_Drilldown.py
      3_Data_Quality_Monitor.py
      4_Equity_and_Responsible_Use.py
  reports/
    .gitkeep
    analyst_report.md
    board_briefing_deck.md
    methodology_note.md
    opus_review_guide.md
  tests/
    __init__.py
    test_dashboard_artifacts.py
    test_eda.py
    test_ingest.py
    test_kpi_calculations.py
    test_kpi_queries.py
    test_scope_and_ci.py
    test_quality_checks.py
  excel/
    .gitkeep
```

## Generated Deliverables

- Streamlit dashboard: `make app`
- KPI first-run report: `data/processed/kpi_first_run.md`
- Data quality first-run report: `data/processed/data_quality_first_run.md`
- Analyst report: `reports/analyst_report.md`
- Methodology note: `reports/methodology_note.md`
- Board briefing deck source: `reports/board_briefing_deck.md`
- Local PDF deck and Excel workbook: `make artifacts`

## 7840 Deployment

The production-style deployment lives under `deploy/7840/` and is intended for the 7840 mini host, not for a local long-running service.

- `deploy/7840/docker-compose.yml` runs PostgreSQL 16 plus the Streamlit dashboard container.
- `deploy/7840/start.sh` applies the schema, reloads public raw data, regenerates reports/artifacts, then starts Streamlit.
- Copy `deploy/7840/.env.example` to `deploy/7840/.env`, set the reverse-proxy Docker network and database password there, and keep `.env` uncommitted.
- The app expects raw public files under `data/raw/` on the server and joins the existing reverse-proxy Docker network via `PROXY_NETWORK` from `deploy/7840/.env`.

## License

MIT.
