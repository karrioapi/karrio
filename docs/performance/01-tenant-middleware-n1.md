# 01 — Tenant Middleware N+1

**Status:** Needs fix
**Impact:** 1,150 events — affects every HTTP request
**File:** `ee/platform/modules/tenants/karrio/server/tenants/middleware.py`

## Root Cause

`CustomTenantMiddleware.get_tenant()` resolves the current tenant from the request hostname. When the exact hostname does not match a `Domain` record (common in local development and containerized deployments), the method falls through to try up to 4 alternative hostnames:

1. Exact hostname lookup (e.g., `app.example.com:8000`)
2. `localhost` variant
3. `0.0.0.0` variant
4. `127.0.0.1` variant
5. Hostname without port

Each attempt calls `super().get_tenant()`, which executes a `SELECT` on the `Domain` model. In the worst case this produces **5 DB queries per request** before a tenant is resolved.

There is no caching — even if the same hostname was resolved 1 second ago, the next request repeats all queries.

## Current Behavior

| Scenario | Queries per request |
|----------|-------------------|
| Exact hostname match | 1 |
| First alternative matches | 2 |
| Last alternative matches | 5 |
| No match (error) | 5 |

At 1,150 observed events, the average overhead is significant — especially for API-heavy workloads where every millisecond of latency compounds.

## Optimal Behavior

**1 query per unique hostname**, then 0 queries for subsequent requests with the same hostname (until cache expires).

## Proposed Fix

### Option A: Request-Scoped Thread-Local Cache

Cache the hostname-to-tenant mapping in thread-local storage, cleared at the end of each request.

```python
import threading

_tenant_cache = threading.local()

class CustomTenantMiddleware(TenantMiddleware):
    def get_tenant(self, model, hostname, request):
        cache = getattr(_tenant_cache, 'map', None)
        if cache is None:
            _tenant_cache.map = {}
            cache = _tenant_cache.map

        if hostname in cache:
            return cache[hostname]

        tenant = self._resolve_tenant(model, hostname, request)
        cache[hostname] = tenant
        return tenant

    def _resolve_tenant(self, model, hostname, request):
        # existing fallback logic here
        ...

    def process_request(self, request):
        result = super().process_request(request)
        return result

    # Clear cache at end of request
    def process_response(self, request, response):
        _tenant_cache.map = {}
        return super().process_response(request, response)
```

### Option B: Process-Level Cache with TTL

For deployments where tenants rarely change, cache at the process level with a short TTL (e.g., 60 seconds). This eliminates DB queries entirely for warm hostnames.

```python
from functools import lru_cache
import time

_cache = {}
_cache_ttl = 60  # seconds

class CustomTenantMiddleware(TenantMiddleware):
    def get_tenant(self, model, hostname, request):
        now = time.monotonic()
        entry = _cache.get(hostname)
        if entry and (now - entry[1]) < _cache_ttl:
            return entry[0]

        tenant = self._resolve_tenant(model, hostname, request)
        _cache[hostname] = (tenant, now)
        return tenant
```

### Option C: Single Query with IN Clause

Instead of trying hostnames sequentially, query all candidate hostnames in one query.

```python
def get_tenant(self, model, hostname, request):
    candidates = self._hostname_candidates(hostname)
    domain = (
        Domain.objects
        .select_related('tenant')
        .filter(domain__in=candidates)
        .first()
    )
    if domain is None:
        raise self.TENANT_NOT_FOUND_EXCEPTION(...)
    return domain.tenant

def _hostname_candidates(self, hostname):
    """Return all hostnames to try, in priority order."""
    candidates = [hostname]
    # add localhost, .0.0.0, 127.0.0.1, without-port variants
    ...
    return candidates
```

**Recommended approach:** Option C (single query) combined with Option B (process-level TTL cache). This gives 1 query on cache miss and 0 queries on cache hit.

## Prevention

Any middleware that performs DB lookups MUST cache the result per-request at minimum. Process-level caching with TTL is preferred for data that changes infrequently (like tenant-hostname mappings).
