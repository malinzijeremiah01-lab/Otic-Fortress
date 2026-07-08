FROM python:3.11-slim
WORKDIR /app
COPY backend/services/ingestion-api/pyproject.toml ./pyproject.toml
COPY backend/services/ingestion-api/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "ingestion_api.main"]
