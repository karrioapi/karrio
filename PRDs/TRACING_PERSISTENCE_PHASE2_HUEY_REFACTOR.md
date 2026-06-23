# Tracing Persistence Phase 2: Move API Thread Async to Huey DB Task

| Field     | Value            |
| --------- | ---------------- |
| Project   | Karrio           |
| Version   | 1.0              |
| Date      | 2026-06-09       |
| Status    | Planning         |
| Owner     | Server/Core Team |
| Type      | Refactoring      |
| Reference | AGENTS.md        |

---

## Executive Summary

Phase 1 mitigates idle PostgreSQL session buildup by cleaning DB connections in API-side async threads.
Phase 2 removes this risk class entirely by migrating tracing persistence from request-local thread execution to the existing Huey `db_task` pattern already used for server background ORM work.

### Key Decisions

1. Persist tracing records via Huey `db_task` instead of `@utils.async_wrapper`.
2. Keep existing tracing record schema and payload shape unchanged.
3. Keep deduplication by `request_log_id` in worker task logic.
4. Roll out behind existing `PERSIST_SDK_TRACING` flag with no API contract changes.

### Scope

| In Scope                                      | Out of Scope                           |
| --------------------------------------------- | -------------------------------------- |
| Move persistence execution path to Huey task  | Changes to tracing record model fields |
| Keep existing dedupe and org-link behavior    | Tracing UI/query redesign              |
| Add task-focused tests and integration checks | Broad logging/telemetry redesign       |

---

## Problem Statement

### Current State

Tracing persistence for API requests is triggered in middleware and currently uses an async wrapper backed by a thread executor in server core utils.

Relevant files:

- `modules/core/karrio/server/core/middleware.py`
- `modules/core/karrio/server/tracing/utils.py`
- `modules/core/karrio/server/core/utils.py`

### Why Change

Even with Phase 1 cleanup, API request handling still depends on ad hoc thread async for ORM persistence.
Karrio already has a standard and safer background ORM pattern via Huey `db_task` wrappers in events tasks.

### Desired State

API middleware enqueues a Huey tracing persistence task. Worker-side execution handles ORM writes and org-linking under known task lifecycle semantics.

---

## Existing Code Analysis

| Component               | Location                                                                | Reuse Strategy                                       |
| ----------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------- |
| Tracing save entrypoint | `modules/core/karrio/server/tracing/utils.py`                           | Split into enqueue + worker task body                |
| Request middleware hook | `modules/core/karrio/server/core/middleware.py`                         | Keep call site stable, change implementation beneath |
| Huey task pattern       | `modules/events/karrio/server/events/task_definitions/base/__init__.py` | Mirror `@db_task` + tenant-aware style               |
| Worker settings         | `apps/api/karrio/server/settings/workers.py`                            | Reuse existing queue execution model                 |

---

## Architecture Overview

```text
Before (current)

HTTP Request
   |
   v
SessionContext middleware
   |
   v
save_tracing_records()
   |
   v
ThreadPoolExecutor (API process)
   |
   v
ORM bulk_create("tracing-record")


After (phase 2)

HTTP Request
   |
   v
SessionContext middleware
   |
   v
enqueue_tracing_records_task(...)
   |
   v
Huey queue
   |
   v
Huey worker db_task
   |
   v
ORM bulk_create("tracing-record")
```

## Sequence

```text
Client -> API: request
API -> Middleware: complete response
Middleware -> Tracing Utils: enqueue(payload)
Tracing Utils -> Huey: task.delay(payload)
Huey Worker -> DB: dedupe check + bulk_create
Huey Worker -> DB: bulk_link_org (if org)
```

---

## Technical Design

1. Create a dedicated tracing persistence task function in server-side tasks module.
2. Move ORM write logic from nested async closure into task body.
3. Keep payload minimal and serializable:
    - actor_id
    - org_id
    - schema
    - tracer context values (`request_id`, `request_log_id`, `object_id`)
    - flattened tracing records list (key, timestamp, record, connection metadata)
4. Preserve behavior:
    - skip when `PERSIST_SDK_TRACING` is false
    - skip when no records or no actor
    - preserve request_log_id dedupe check
    - preserve org linking
5. Keep middleware call shape unchanged to minimize blast radius.

### Compatibility Notes

- No API schema changes.
- No migration required.
- Existing tracing readers remain unchanged.

---

## Implementation Plan

| Step | Change                                                   | Files                                                                                    |
| ---- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1    | Add Huey db_task for tracing persistence                 | `modules/events/karrio/server/events/task_definitions/base/*.py`                         |
| 2    | Refactor tracing util to enqueue task payload            | `modules/core/karrio/server/tracing/utils.py`                                            |
| 3    | Keep middleware integration stable                       | `modules/core/karrio/server/core/middleware.py`                                          |
| 4    | Add tests for enqueue + worker persistence behavior      | `modules/core/karrio/server/core/tests/*`, `modules/events/karrio/server/events/tests/*` |
| 5    | Validate under load and compare pg_stat_activity profile | ops verification                                                                         |

---

## Testing Strategy

1. Unit tests
    - enqueue is called once per request context with expected payload
    - worker task no-ops on empty records or missing actor
    - worker task dedupe by `request_log_id`
2. Integration tests
    - middleware path still results in saved tracing records
    - org links are created correctly when org exists
3. Non-functional validation
    - run load test with tracing enabled
    - compare idle `karrio.api` DB sessions before/after

---

## Risks and Mitigations

| Risk                               | Impact                            | Mitigation                                                                          |
| ---------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------- |
| Task payload missing context field | Missing metadata in trace records | Contract test asserting payload keys                                                |
| Queue lag delays trace visibility  | Delayed debugging data            | Document eventual consistency; keep synchronous fallback toggle for troubleshooting |
| Duplicate writes in retries        | Data noise                        | Keep request_log_id dedupe guard in task                                            |

---

## Migration and Rollback

### Migration

- Deploy code with task path enabled.
- Keep `PERSIST_SDK_TRACING` configurable for staged rollout.

### Rollback

- Revert to previous tracing utils implementation.
- Disable tracing persistence (`PERSIST_SDK_TRACING=False`) if immediate operational relief is needed.

---

## Definition of Done

- [ ] Tracing persistence no longer uses API-side thread async path.
- [ ] Tracing writes run through Huey `db_task` worker path.
- [ ] Existing tracing metadata and dedupe behavior preserved.
- [ ] Tests added and passing for enqueue and persistence logic.
- [ ] Load validation shows stable/expected idle DB session count.
