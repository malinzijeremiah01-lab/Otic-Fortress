FROM python:3.11-slim
WORKDIR /app
COPY backend/services/dashboard-bff/pyproject.toml ./pyproject.toml
COPY backend/services/dashboard-bff/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "dashboard_bff.main"]
