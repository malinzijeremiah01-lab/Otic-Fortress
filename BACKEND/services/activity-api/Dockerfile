FROM python:3.11-slim
WORKDIR /app
COPY backend/services/activity-api/pyproject.toml ./pyproject.toml
COPY backend/services/activity-api/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "activity_api.main"]
