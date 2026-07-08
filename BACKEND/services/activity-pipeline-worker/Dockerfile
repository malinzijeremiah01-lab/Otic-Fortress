FROM python:3.11-slim
WORKDIR /app
COPY backend/services/activity-pipeline-worker/pyproject.toml ./pyproject.toml
COPY backend/services/activity-pipeline-worker/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "activity_pipeline_worker.main"]
