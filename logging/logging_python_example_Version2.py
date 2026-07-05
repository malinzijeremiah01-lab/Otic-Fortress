name=logging_python_example.py
# Minimal Python logging + OpenTelemetry + Application Insights snippet
# pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-requests azure-monitor-opentelemetry
import logging
import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

service_name = os.getenv("OTEL_SERVICE_NAME", "fortress-python-service")
resource = Resource.create({"service.name": service_name, "environment": os.getenv("ENVIRONMENT", "dev")})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"), insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

logger = logging.getLogger("fortress")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('{"timestamp":"%(asctime)s","severity":"%(levelname)s","service":"%(name)s","message":"%(message)s","correlationId":"%(correlationId)s"}')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Example log
logger.info('worker-started', extra={"correlationId": os.getenv("CORRELATION_ID", "unknown")})