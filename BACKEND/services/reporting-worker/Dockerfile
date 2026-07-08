FROM python:3.11-slim
WORKDIR /app
COPY backend/services/reporting-worker/pyproject.toml ./pyproject.toml
COPY backend/services/reporting-worker/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "reporting_worker.main"]
