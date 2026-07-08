FROM python:3.11-slim
WORKDIR /app
COPY backend/services/intelligence-worker/pyproject.toml ./pyproject.toml
COPY backend/services/intelligence-worker/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "intelligence_worker.main"]
