# 02 — Tracking Batch N+1

**Status:** Already optimized
**Impact:** 108 events (historical, before optimization)
**File:** `modules/events/karrio/server/events/task_definitions/base/tracking.py`

## Context

The tracking batch system processes carrier tracking updates in bulk. Each batch run can update hundreds of trackers and create thousands of tracing records (API request/response logs).

## Existing Optimizations

### Bulk Tracing Records

Tracing records (API call logs) are collected in memory during the batch run and written in a single `bulk_create` call.

```python
# Pattern used:
# 1. Collect all tracing records during processing
tracing_records = []
for tracker in trackers:
    # ... process tracker, append to tracing_records ...

# 2. Single bulk write
TracingRecord.objects.bulk_create(tracing_records)
```

This replaces what would have been N individual `TracingRecord.objects.create()` calls with a single INSERT statement containing all records.

### Bulk Tracker Updates

Tracker model changes (status, events, estimated delivery) are batched and written with `bulk_update`.

```python
# Pattern used:
# 1. Modify tracker objects in memory
updated_trackers = []
for tracker in trackers:
    tracker.status = new_status
    tracker.events = new_events
    updated_trackers.append(tracker)

# 2. Single bulk update
Tracker.objects.bulk_update(
    updated_trackers,
    fields=["status", "events", "estimated_delivery", "updated_at"]
)
```

This replaces N individual `tracker.save()` calls with a single UPDATE statement.

## Why This Pattern Works

| Approach | Queries | DB Round Trips |
|----------|---------|---------------|
| Individual saves | N creates + N updates | 2N |
| Bulk operations | 1 bulk_create + 1 bulk_update | 2 |

For a batch of 100 trackers, this reduces queries from ~200 to 2.

## Reusable Pattern

When processing items in a batch:

1. **Collect** — iterate and build lists of objects to create/update in memory
2. **Write once** — use `bulk_create` for new records, `bulk_update` for modifications
3. **Specify fields** — always pass `fields=` to `bulk_update` to limit the UPDATE clause

### Caveats

- `bulk_create` does not call `Model.save()` or fire `post_save` signals — if you rely on those, you need explicit signal dispatch after the bulk operation
- `bulk_update` has a batch size limit (default varies by DB backend) — for very large batches, pass `batch_size=` parameter
- Neither method calls custom `save()` logic — any validation or side effects in `save()` must be handled separately
