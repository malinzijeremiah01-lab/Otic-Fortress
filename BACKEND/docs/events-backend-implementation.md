# Events Backend Implementation

## What Events Are

Events are the backend's structured record of something important that happened in the Otic Fortress control plane. They describe activity such as a model call, a tool call, a governance decision, an audit action, a finding, an archive operation, or the creation of an activity record.

Instead of every service inventing its own payload shape, events give the backend a shared language. Each event has a type, tenant, identifier, optional trace context, and payload. That makes it possible for services to validate incoming activity, classify it, correlate related actions, build higher-level records, and later expose those records through APIs and dashboards.

In this project, events are especially important because Otic Fortress is an AI governance platform. The backend needs to answer questions such as:

- Which tenant did this activity belong to?
- Which agent, model, or tool was involved?
- Was a governance decision made?
- Were policy checks, approvals, findings, or audit actions attached to the activity?
- Can the activity be reconstructed later for evidence, reporting, or compliance?

Events are the raw building blocks that make those answers possible.

## What Events Do

The events layer supports the backend in four main ways.

### Capture activity

Events capture important system and AI-governance actions as structured data. A model invocation, tool invocation, governance decision, finding, audit event, or archive event can all be represented in a consistent format.

### Standardize contracts

Event types and JSON schemas define the expected shape of backend event payloads. This reduces ambiguity between services and makes it easier to test whether producers and consumers are speaking the same language.

### Power the activity pipeline

The activity pipeline uses events to classify, validate, normalize, and group related activity. Multiple low-level events can become a single activity record that is easier for APIs, dashboards, auditors, and workers to consume.

### Support governance and evidence

Because events include tenant, trace, payload, and schema information, they can support audit trails, evidence bundles, replay workflows, compliance reports, anomaly detection, and future persistent activity history.

## Event Flow

The current backend event flow is:

1. A service or SDK emits an event-like payload.
2. The pipeline validates required fields such as `event_id`, `tenant_id`, `event_type`, and `payload`.
3. The pipeline normalizes the event into a canonical shape.
4. The event type is standardized or inferred from the payload.
5. Related events are grouped into an activity record.
6. The Activity API exposes activity records through create, list, and get endpoints.

This gives the backend a clean path from raw event activity to queryable activity records.

## Scope

This pass focused only on the backend events foundation:

- Shared event type definitions.
- Activity pipeline event classification, validation, normalization, and record building.
- Activity API record models, in-memory repository/service, and routes.
- Event schema contract cleanup.
- Focused and full backend test coverage.

## Branching note

The events activity work was committed on:

- `feature-events_events_activity`

The related naming convention for future event type work is:

- `feature-events_types`

## Docker

The backend infrastructure stack was started from the backend root:

```powershell
cd BACKEND
docker compose up -d
```

The compose stack started PostgreSQL, Redis, Redpanda, Redpanda Console, MinIO, and Jaeger successfully.

Redis was changed from `redis:7` to `redis:7-alpine` in `docker-compose.yml` because the local `redis:7` image repeatedly exited with an entrypoint `exec format error`, while the official Redis 7 Alpine image started correctly.

## What Was Implemented

### Shared event types

Added canonical event type support in `packages/fortress-events/src/fortress_events/types.py`.

Implemented:

- `EventType`
- `CANONICAL_EVENT_TYPES`
- `normalize_event_type`
- `is_supported_event_type`

The normalizer supports canonical snake-case values and common aliases such as dot-case and kebab-case.

This is the foundation for keeping event names predictable across the backend. For example, payloads that arrive as `model.invocation`, `model-invocation`, or `model_invocation` can be resolved to the same canonical event type.

### Activity pipeline worker

Implemented event processing primitives in `services/activity-pipeline-worker`:

- `EventTypeClassifier` now canonicalizes explicit event types and infers model/tool/governance events from payload shape.
- `SchemaValidator` now rejects non-dict payloads, missing required fields, and unsupported event types.
- `Normalizer` now emits a consistent `NormalizedEvent` model.
- `RecordBuilder` now groups related events into an activity record with tenant validation, event counts, event types, occurrence range, and summary counts.

This means the pipeline is no longer just a placeholder. It can now take raw event dictionaries and turn them into normalized, validated, grouped activity data.

### Activity API

Implemented the activity record backend surface in `services/activity-api`:

- `ActivityRecordCreate`
- `ActivityRecord`
- `ActivityRecordRepository`
- `ActivityRecordService`
- `POST /v1/activity-records/`
- `GET /v1/activity-records/`
- `GET /v1/activity-records/{record_id}`

The repository is intentionally in-memory because the current project does not yet include database migrations or persistent storage wiring for activity records.

This gives the backend an API surface for working with activity records while leaving room to replace the repository with PostgreSQL-backed persistence when the database layer is ready.

### Event schemas

Completed previously empty event schema files:

- `schemas/events/raw_archive_metadata.v1.json`
- `schemas/events/unified_decision_record.v1.json`

These schemas matter because contract tests can now verify that every event schema file is valid JSON. They also document the expected event payload shape for archive metadata and unified decision records.

### Test configuration

Updated backend pytest configuration so service packages can be imported from backend-root test runs and duplicate test filenames across services do not collide during collection.

## What Has Been Developed On Events

This events work developed the backend's first concrete event activity foundation:

- A canonical event type system for shared backend event names.
- Alias handling so common naming variations still resolve to the same event type.
- Validation rules for required event structure.
- Normalization from raw event dictionaries into consistent event objects.
- Payload-based event type inference for model, tool, and governance activity.
- Activity record construction from one or more related events.
- Activity API endpoints for creating, listing, and fetching records.
- Event schema cleanup so event contracts are parseable and testable.
- Test coverage across the shared event package, pipeline worker, and Activity API.

In simple terms: before this work, much of the events area was present as structure and placeholders. After this work, the backend has a working event-to-activity-record path that can be tested and extended.

## Current Limitations

The current implementation is intentionally foundational. The Activity API repository is in-memory, so records are not yet persisted after process restart. The next backend step should be to connect activity records to the database once migrations and storage ownership are defined.

The event flow also does not yet run as a full asynchronous Redpanda consumer pipeline. The core classification, validation, normalization, and record-building logic is ready, but the worker orchestration can be expanded later.

## Tests Added

Added tests for:

- Event type normalization and support checks.
- Schema validation for supported, incomplete, and unknown events.
- Event normalization and event type inference.
- Activity record building and cross-tenant rejection.
- Activity API create, list, get, and missing-record behavior.

## Verification

Full backend test suite:

```powershell
& 'C:\Users\hp 850\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest
```

Result:

```text
35 passed, 1 warning
```

The remaining warning comes from the installed `httpx`/FastAPI test client stack and is not caused by the event implementation.
