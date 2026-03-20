# 06 — Constance Settings N+1

**Status:** Needs fix
**Impact:** 42 events, 15+ SELECT queries on first request or cache miss
**File:** `modules/core/karrio/server/core/signals.py` (`initialize_settings` / `update_settings`)

## Root Cause

The `update_settings()` function iterates through all constance configuration keys, reading each one individually via `getattr(config, key)`:

```python
# Current pattern (simplified)
for key in CONSTANCE_CONFIG.keys():
    value = getattr(config, key)  # SELECT from constance table — 1 query per key
    if value != expected:
        setattr(config, key, expected)
```

With 15+ configuration keys, this produces 15+ individual SELECT queries.

### Cache Behavior

- **With Redis cache** (`CONSTANCE_DATABASE_CACHE_BACKEND = "default"`): The first access per key populates the cache. Subsequent accesses within the cache TTL are free. But the initial population still hits the DB once per key.
- **Without Redis cache**: Every access hits the database. There is no caching layer, so every request that triggers `update_settings` produces 15+ queries.

## Current vs. Optimal

| Scenario | Current Queries | Optimal Queries |
|----------|----------------|----------------|
| No cache, 15 keys | 15 SELECTs | 1 SELECT ... WHERE key IN (...) |
| Redis cache, cold | 15 SELECTs (then cached) | 1 SELECT (then cached) |
| Redis cache, warm | 0 | 0 |

## Proposed Fix

### Pre-Warm Cache with Single Query

Before iterating through keys, fetch all constance values in one query and populate the cache:

```python
from constance.backends.database.models import Constance

def update_settings(config, settings_dict):
    keys = list(settings_dict.keys())

    # Single query to fetch all current values
    existing = dict(
        Constance.objects.filter(key__in=keys).values_list("key", "value")
    )

    # Now iterate — values are already in memory, no DB hits
    updates = []
    creates = []
    for key, expected in settings_dict.items():
        current = existing.get(key)
        if current != expected:
            if current is not None:
                updates.append((key, expected))
            else:
                creates.append(Constance(key=key, value=expected))

    # Batch write changes
    if creates:
        Constance.objects.bulk_create(creates)
    if updates:
        for key, value in updates:
            # Use bulk approach or single query per changed key
            Constance.objects.filter(key=key).update(value=value)
```

### Alternative: Pre-Warm Constance Cache

If you need to keep using the constance API (`getattr(config, key)`), pre-warm the cache before the loop:

```python
from constance.backends.database.models import Constance

def _prewarm_constance_cache(keys):
    """Fetch all keys in one query and populate constance's internal cache."""
    from django.core.cache import caches
    cache_backend = getattr(settings, 'CONSTANCE_DATABASE_CACHE_BACKEND', None)
    if cache_backend:
        cache = caches[cache_backend]
        values = dict(
            Constance.objects.filter(key__in=keys).values_list("key", "value")
        )
        for key, value in values.items():
            cache.set(f"constance:constance:{key}", value)

def update_settings(config, settings_dict):
    _prewarm_constance_cache(list(settings_dict.keys()))

    # Now these hit cache, not DB
    for key, expected in settings_dict.items():
        value = getattr(config, key)
        ...
```

## Prevention

- Never loop through individual config key lookups — batch-fetch all keys first
- When using constance (or similar key-value config stores), always pre-warm the cache if reading multiple keys
- If Redis is available, ensure `CONSTANCE_DATABASE_CACHE_BACKEND` is configured to avoid repeated DB hits
