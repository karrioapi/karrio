# Query Optimization Patterns

## Overview

This directory documents N+1 query issues discovered in the Karrio codebase, their root causes, fixes applied, and reusable patterns to prevent regressions.

### Issue Index

| # | Issue | File(s) | Events | Queries | Status |
|---|-------|---------|--------|---------|--------|
| 01 | Tenant Middleware N+1 | `ee/platform/.../tenants/middleware.py` | 1,150 | 5/request (worst) | Needs fix |
| 02 | Tracking Batch N+1 | `modules/events/.../tracking.py` | 108 | — | Already optimized |
| 03 | Task Execution Logging N+1 | `modules/admin/.../worker/signals.py` | 38 | — | Already optimized |
| 04 | Tenant GraphQL N+1 | `ee/platform/.../tenants/models.py` | 207 | — | Already fixed |
| 05 | Rate Sheet CRUD N+1 | `modules/core/.../serializers/abstract.py`, `modules/graph/.../serializers.py` | 56 | ~76/mutation | Needs fix |
| 06 | Constance Settings N+1 | `modules/core/.../core/signals.py` | 42 | 15+/request | Needs fix |

### Priority

1. **Tenant Middleware** — affects every single request (1,150 events)
2. **Tenant GraphQL** — already fixed, high event count (207 events)
3. **Tracking Batch** — already optimized (108 events)
4. **Rate Sheet CRUD** — affects admin mutations (56 events, 76 queries each)
5. **Constance Settings** — affects first request after cache miss (42 events)
6. **Task Execution Logging** — already optimized, acceptable by design (38 events)

---

## Reusable Patterns Catalog

### 1. Request-Scoped Caching

Cache DB results for the lifetime of a single HTTP request. Use when the same lookup repeats within a request cycle.

```python
# Option A: Thread-local storage
import threading

_request_cache = threading.local()

def get_tenant(hostname):
    cache = getattr(_request_cache, 'tenants', None)
    if cache is None:
        _request_cache.tenants = {}
        cache = _request_cache.tenants
    if hostname not in cache:
        cache[hostname] = Domain.objects.select_related('tenant').get(domain=hostname).tenant
    return cache[hostname]

# Option B: functools.lru_cache (process-scoped, use with TTL wrapper)
```

### 2. Bulk Writes

Never call `model.save()` in a loop. Collect changes in memory and write once.

```python
# BAD — N queries
for item in items:
    obj = Model(**item)
    obj.save()

# GOOD — 1 query
objects = [Model(**item) for item in items]
Model.objects.bulk_create(objects)

# BAD — N queries
for obj in objects:
    obj.status = "updated"
    obj.save()

# GOOD — 1 query
for obj in objects:
    obj.status = "updated"
Model.objects.bulk_update(objects, fields=["status"])
```

### 3. Prefetch Conventions

Declare prefetch requirements on the Manager so all queries benefit automatically.

```python
class ClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("domains")
```

Never call `.order_by()` on a prefetched relation — it creates a new queryset and bypasses the prefetch cache.

```python
# BAD — bypasses prefetch cache
self.domains.all().order_by("domain")

# GOOD — uses prefetch cache, sort in Python if needed
sorted(self.domains.all(), key=lambda d: d.domain)
```

### 4. Batch Config Fetch

When reading multiple config keys, fetch all values in one query before iterating.

```python
# BAD — N queries
for key in keys:
    value = getattr(config, key)

# GOOD — 1 query
from constance.backends.database.models import Constance
all_values = dict(
    Constance.objects.filter(key__in=keys).values_list("key", "value")
)
for key in keys:
    value = all_values.get(key, defaults.get(key))
```

### 5. Split Create/Update

Avoid `update_or_create()` under high concurrency — it acquires SELECT FOR UPDATE locks.

```python
# BAD — lock contention
obj, created = Model.objects.update_or_create(pk=pk, defaults={...})

# GOOD — split operations
try:
    Model.objects.create(pk=pk, **data)
except IntegrityError:
    Model.objects.filter(pk=pk).update(**data)
```

---

## Prevention Checklist

Use this checklist during code review for any PR that touches DB queries:

- [ ] No `model.save()` inside a loop — use `bulk_create` / `bulk_update`
- [ ] No `model.related_field.attr` without `select_related()` on the queryset
- [ ] No `model.related_set.all()` without `prefetch_related()` on the queryset
- [ ] No `.order_by()` on prefetched relations
- [ ] No individual config key lookups in a loop — batch fetch
- [ ] Middleware DB lookups are cached per-request
- [ ] `update_or_create()` not used in high-concurrency paths
- [ ] M2M additions use `.set()` or `.add(*list)` instead of individual `.add()` calls

## How to Detect N+1s

1. **Django Debug Toolbar** — shows query count per request in development
2. **django-silk** — profiles queries with call stacks
3. **Sentry Performance** — tracks query count in production
4. **Manual audit** — search for `.save()` inside `for` loops
