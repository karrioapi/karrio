# 03 — Task Execution Logging N+1

**Status:** Already optimized
**Impact:** 38 events
**File:** `modules/admin/karrio/server/admin/worker/signals.py`

## Context

The task execution logging system records Huey task lifecycle events (enqueued, started, completed, errored) into the database. Each task emits signals at different stages, and the signal handler writes a log record.

## Existing Optimization: Split Create/Update

The handler uses a split create/update pattern instead of `update_or_create()` to avoid SELECT FOR UPDATE lock contention under high concurrency.

```python
# Pattern used:
try:
    TaskExecution.objects.create(
        task_id=task_id,
        status="enqueued",
        ...
    )
except IntegrityError:
    TaskExecution.objects.filter(task_id=task_id).update(
        status="enqueued",
        ...
    )
```

### Why Not update_or_create?

`update_or_create()` in Django:

1. Runs `SELECT ... FOR UPDATE` to check existence
2. Either creates or updates

Under high concurrency (many tasks completing simultaneously), the FOR UPDATE lock creates contention. The split pattern avoids this:

- **Create path** — single INSERT, no lock
- **Update path** — only triggered on IntegrityError (race condition), uses a simple UPDATE without row-level lock

## Why Individual Creates Are Acceptable

Unlike batch processing (where you control the loop), task logging is **signal-driven**:

- Each task emits its own signal independently
- Signals fire at unpredictable times (task A completes, task B starts, task C errors)
- There is no natural "batch boundary" to collect and bulk-write

Batching would require a buffer with a flush timer, adding complexity and latency for minimal gain. At 38 events, the overhead is negligible.

## Reusable Pattern

Use the split create/update pattern when:

1. **High concurrency** — multiple workers/threads writing to the same table
2. **Unique constraint exists** — IntegrityError reliably signals duplicates
3. **Signal-driven writes** — no natural batch boundary

```python
# Template
try:
    Model.objects.create(**data)
except IntegrityError:
    Model.objects.filter(**lookup).update(**update_data)
```

### When NOT to Use This

- If you control the loop (use `bulk_create` / `bulk_update` instead)
- If you need the returned object (this pattern does not return the instance on the update path)
- If there is no unique constraint (IntegrityError will not fire, leading to duplicate rows)
