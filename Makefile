PYTHON ?= python

.PHONY: up down psql schema load kpis quality app test lint fmt

up:
	docker compose up -d

down:
	docker compose down

psql:
	docker exec -it healthops_pg psql -U healthops -d healthops

schema:
	docker exec -i healthops_pg psql -U healthops -d healthops -f /sql/01_schema.sql

load:
	$(PYTHON) -m src.ingest

kpis:
	$(PYTHON) -m src.kpi

quality:
	$(PYTHON) -m src.quality

app:
	streamlit run app/streamlit_app.py

test:
	pytest -q

lint:
	ruff check .

fmt:
	ruff format .
