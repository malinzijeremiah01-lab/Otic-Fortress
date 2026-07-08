FROM python:3.11-slim
WORKDIR /app
COPY backend/services/delivery-worker/pyproject.toml ./pyproject.toml
COPY backend/services/delivery-worker/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "delivery_worker.main"]
