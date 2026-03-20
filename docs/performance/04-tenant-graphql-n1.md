# 04 — Tenant GraphQL N+1

**Status:** Already fixed
**Impact:** 207 events (historical, before fix)
**File:** `ee/platform/modules/tenants/karrio/server/tenants/models.py`

## Root Cause (Historical)

The GraphQL `api_domains` resolver on the Client (tenant) type accessed `self.domains.all()` without prefetching. Each Client in a list query triggered a separate SELECT on the Domain table.

## Fix Applied

### Manager-Level Prefetch

The `ClientManager` declares `prefetch_related("domains")` on the default queryset:

```python
class ClientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("domains")
```

This means every query through the manager (including GraphQL list queries) automatically prefetches domains in a single additional query, regardless of how many clients are returned.

### Resolver Uses Prefetch Cache

The `api_domains` resolver accesses the prefetch cache via `self.domains.all()`:

```python
def api_domains(self):
    return self.domains.all()
```

Since `domains` was already prefetched by the manager, `.all()` returns the cached result without hitting the database.

## Critical Lesson: Never .order_by() on Prefetched Relations

The code includes an explicit comment warning against this:

```python
# DO NOT call .order_by() as it creates a new queryset and bypasses prefetch cache
```

When you call `.order_by()` on a prefetched relation, Django creates a **new** queryset that is not connected to the prefetch cache. This silently re-introduces the N+1:

```python
# BAD — bypasses prefetch cache, causes N+1
def api_domains(self):
    return self.domains.all().order_by("domain")  # new queryset = new DB query

# GOOD — uses prefetch cache, sorts in Python
def api_domains(self):
    return sorted(self.domains.all(), key=lambda d: d.domain)
```

Other operations that create new querysets and bypass prefetch cache:
- `.filter()` on a prefetched relation
- `.exclude()` on a prefetched relation
- `.annotate()` on a prefetched relation
- `.order_by()` on a prefetched relation

## Reusable Pattern

### Declare Prefetch on the Manager

```python
class MyModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("related_set")
```

### Use Prefetch Cache in Resolvers/Properties

```python
def resolve_related_items(self):
    # .all() returns prefetch cache — zero queries
    return self.related_set.all()
```

### When to Use Prefetch Objects for Complex Cases

```python
from django.db.models import Prefetch

class MyModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                "related_set",
                queryset=RelatedModel.objects.select_related("nested_fk").order_by("name"),
            )
        )
```

This lets you control the prefetch queryset (add filters, ordering, nested select_related) while keeping the cache benefit.

## Query Count

| Scenario | Queries |
|----------|---------|
| Before fix: 50 clients listed | 1 (clients) + 50 (domains) = 51 |
| After fix: 50 clients listed | 1 (clients) + 1 (domains prefetch) = 2 |
