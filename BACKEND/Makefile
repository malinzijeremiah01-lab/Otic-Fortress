.PHONY: local-up local-down test run-ingestion run-control run-activity

local-up:
	docker compose up -d

local-down:
	docker compose down

test:
	pytest -q

run-ingestion:
	uvicorn ingestion_api.main:app --reload --port 8001

run-control:
	uvicorn control_api.main:app --reload --port 8002

run-activity:
	uvicorn activity_api.main:app --reload --port 8003
