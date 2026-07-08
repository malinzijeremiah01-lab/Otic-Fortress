FROM python:3.11-slim
WORKDIR /app
COPY backend/services/audit-custody/pyproject.toml ./pyproject.toml
COPY backend/services/audit-custody/src ./src
RUN pip install --no-cache-dir fastapi uvicorn pydantic
CMD ["python", "-m", "audit_custody.main"]
