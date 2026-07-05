name=logging_node_example.js
// Minimal Node.js logging + OpenTelemetry + Application Insights snippet
// Install: npm i @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @azure/monitor-opentelemetry applicationinsights winston
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const appInsights = require('applicationinsights');
const winston = require('winston');

// Initialize Application Insights (fallback if not using OTLP)
appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING)
  .setAutoCollectConsole(false)
  .setAutoCollectRequests(true)
  .start();

// OpenTelemetry SDK initialization (OTLP to collector)
const sdk = new NodeSDK({
  traceExporter: undefined, // configure OTLP exporter via env or sdk
  instrumentations: [ getNodeAutoInstrumentations() ]
});
sdk.start();

// Winston logger with structured JSON
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  defaultMeta: { service: process.env.OTEL_SERVICE_NAME || 'fortress-node' },
  transports: [
    new winston.transports.Console()
  ]
});

// Example usage
logger.info('service-start', { correlationId: process.env.CORRELATION_ID || 'unknown', tenantId: 'acme', eventType: 'startup' });

// When handling message events or HTTP requests include correlation and trace ids in structured payloads
module.exports = logger;