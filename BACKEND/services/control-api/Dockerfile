FROM python:3.11-slim
WORKDIR /app
COPY backend/services/control-api/pyproject.toml ./pyproject.toml
COPY backend/services/control-api/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "control_api.main"]
