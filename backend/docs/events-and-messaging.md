# Events and Messaging Architecture

This document is the backend contract for moving Otic Fortress domain events between services. It covers the event model, the processing pipeline, and the messaging package that transports events through Redpanda locally and Kafka-compatible Azure Event Hubs in production.

## Architecture at a glance

```text
Domain service
  -> EventEnvelope + typed payload (fortress-events)
  -> EventPublisher (fortress-messaging)
  -> Redpanda / Kafka topic
  -> KafkaEventConsumer in a worker
  -> classify, validate, normalize, and build records
  -> activity, findings, audit, delivery, or reporting services
```

The shared packages deliberately separate two concerns:

- `fortress-events` defines what an event means: canonical type names, the common envelope, and typed payload models.
- `fortress-messaging` defines how an event is transported: topic names, producer acknowledgement, consumer groups, JSON serialization, and broker lifecycle.

Business services use `EventPublisher`, not an `aiokafka` client directly. This keeps service code independent of the deployed broker and makes it easy to test with `InMemoryEventBus`.

## Events

All inter-service events use `fortress_events.EventEnvelope`. The envelope includes a unique `event_id`, canonical `event_type`, `tenant_id`, `source_service`, occurrence time, optional tracing identifiers, and a JSON-object `payload`.

Canonical event types are defined in `packages/fortress-events/src/fortress_events/types.py`. Supported names include `model_invocation`, `tool_invocation`, `governance_decision`, `activity_record_created`, `finding_created`, `audit_event`, `dead_letter_event`, `raw_archive_metadata`, `replay_manifest`, and `unified_decision_record`.

Producers must emit canonical snake-case type names. The activity pipeline accepts legacy dot-case and kebab-case spellings only to normalize externally supplied events; new backend code must not rely on aliases.

The activity pipeline processes an event in this order:

1. Classify its explicit type or infer a type from the payload shape.
2. Validate required envelope fields, payload shape, and type support.
3. Normalize it to the shared internal representation.
4. Group compatible events into tenant-safe activity records.
5. Store or publish the derived activity, finding, audit, or replay outcome.

An event that fails validation must not be silently discarded. The receiving worker should log enough correlation data to diagnose it and route the original payload to the relevant dead-letter topic when that workflow is enabled.

## Messaging package

The implementation lives in `packages/fortress-messaging/src/fortress_messaging`.

| Component | Responsibility |
| --- | --- |
| `EventBus` | Small producer protocol used by application services. |
| `EventPublisher` | Service-facing publisher that returns a broker-neutral `PublishResult`. |
| `KafkaEventBus` | Lazy `aiokafka` producer with `acks=all`, idempotence, UTF-8 keys/headers, and compact JSON values. |
| `KafkaEventConsumer` | Async JSON-object consumer that invokes a handler then commits its offset. |
| `InMemoryEventBus` | Non-durable test double that records messages and acknowledgements. |
| `Topic` | Canonical topic enum; `ALL_TOPICS` exposes the complete set. |

`KafkaEventBus` starts only when it first publishes and can be safely closed during service shutdown. A successful `publish` means the broker returned topic, partition, and offset metadata; failed broker writes raise `MessagePublishError` rather than looking successful.

`KafkaEventConsumer` uses explicit commits. It commits only after the async handler completes successfully. If the handler raises, no commit is made and the exception is propagated to the worker supervisor. This supplies at-least-once delivery, so consumers must make their writes idempotent using event ID or another stable business key.

## Topic catalogue

| Topic | Producer / purpose | Main consumer |
| --- | --- | --- |
| `fortress.raw.telemetry` | Raw agent and integration telemetry | Activity pipeline worker |
| `fortress.normalized.events` | Validated, normalized domain events | Activity and intelligence workflows |
| `fortress.activity.records` | Built activity records | Activity API, reporting |
| `fortress.findings` | Findings and anomalies | Intelligence, dashboard, delivery |
| `fortress.audit.events` | Immutable audit-relevant events | Audit custody |
| `fortress.dlq.telemetry` | Raw telemetry that cannot be processed | Operations / replay workflow |
| `fortress.dlq.transformation` | Events that fail normalization or transformation | Operations / replay workflow |
| `fortress.replay.telemetry` | Replay requests and replay metadata | Activity pipeline worker |

Topic names are backend-owned API. Do not rename one or reuse it for a different payload contract without a migration plan and a new versioned event schema.

## Service integration

Create one broker instance during application startup and close it on shutdown. Use the internal Docker endpoint from containers (`redpanda:9092`) and the host endpoint for local processes (`localhost:19092`).

```python
from fortress_messaging import EventPublisher, KafkaEventBus, Topic

bus = KafkaEventBus("redpanda:9092", client_id="ingestion-api")
publisher = EventPublisher(bus)

await publisher.publish(
    Topic.RAW_TELEMETRY,
    key=event.tenant_id,
    event=event.model_dump(mode="json"),
    headers={"trace-id": event.trace_id or ""},
)

# At application shutdown
await bus.close()
```

Use a stable consumer group per logical worker (for example, `activity-pipeline-v1`). Multiple replicas in the same group share partitions; independent downstream services require their own groups. Keys should normally be tenant IDs or another ordering boundary so related messages stay partition ordered.

## Local operations

The backend Docker compose file provides Redpanda and Redpanda Console. Start the stack from `BACKEND`:

```powershell
docker compose up -d
```

Redpanda is available at `localhost:19092`; the console is available at `http://localhost:8080`. The `fortress-messaging` package declares `aiokafka` as its Kafka client dependency. Install or lock workspace dependencies before running a service that uses the Kafka adapters.

## Verification

Messaging unit tests exercise acknowledgement handling, lazy producer lifecycle, JSON serialization, broker-error propagation, consumer delivery/commit order, and configuration validation. Run the full backend suite from `BACKEND`:

```powershell
python -m pytest
```

These tests use fakes and do not need a live broker. A deployment smoke test should additionally publish a valid envelope to Redpanda, verify the expected consumer group advances, and confirm the resulting downstream record.
