.PHONY: up down psql schema load app test lint fmt

up:
	docker compose up -d

down:
	docker compose down

psql:
	docker exec -it healthops_pg psql -U healthops -d healthops

schema:
	docker exec -i healthops_pg psql -U healthops -d healthops -f /sql/01_schema.sql

load:
	python -m src.ingest

app:
	streamlit run app/streamlit_app.py

test:
	pytest -q

lint:
	ruff check .

fmt:
	ruff format .
