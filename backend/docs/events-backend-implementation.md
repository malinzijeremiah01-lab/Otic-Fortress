# Events Backend Implementation

## Scope

This pass focused only on the backend events foundation:

- Shared event type definitions.
- Activity pipeline event classification, validation, normalization, and record building.
- Activity API record models, in-memory repository/service, and routes.
- Event schema contract cleanup.
- Focused and full backend test coverage.

## Branching note

The requested branch naming convention is:

- `feature-events_types`
- `feature-events_events_activity`

This local workspace does not currently contain a `.git` directory, so a branch could not be created from here. Run the branch command from a real Git clone before committing:

```powershell
git checkout -b feature-events_events_activity
```

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

### Activity pipeline worker

Implemented event processing primitives in `services/activity-pipeline-worker`:

- `EventTypeClassifier` now canonicalizes explicit event types and infers model/tool/governance events from payload shape.
- `SchemaValidator` now rejects non-dict payloads, missing required fields, and unsupported event types.
- `Normalizer` now emits a consistent `NormalizedEvent` model.
- `RecordBuilder` now groups related events into an activity record with tenant validation, event counts, event types, occurrence range, and summary counts.

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

### Event schemas

Completed previously empty event schema files:

- `schemas/events/raw_archive_metadata.v1.json`
- `schemas/events/unified_decision_record.v1.json`

### Test configuration

Updated backend pytest configuration so service packages can be imported from backend-root test runs and duplicate test filenames across services do not collide during collection.

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
