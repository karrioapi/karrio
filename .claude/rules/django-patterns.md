# Django Patterns

## Multi-Tenancy (Critical)
All tenant-scoped models inherit from `OwnedEntity`. ALWAYS filter by org context.

```python
# BAD - leaks data across tenants
Shipment.objects.all()

# GOOD - properly scoped
Shipment.objects.filter(org=request.user.org)
```

## N+1 Query Prevention
- `model.save()` in loop → `bulk_update()` / `bulk_create()`
- `model.related_field.attr` → `select_related()`
- `model.related_set.all()` → `prefetch_related()`
- `update_or_create()` in high-concurrency → split `create()`/`filter().update()`

## URL Structure
```
/api/v1/<resource>/              → List/Create
/api/v1/<resource>/{id}/         → Retrieve/Update/Delete
/api/v1/<resource>/{id}/<action>/ → Custom actions
```

## ViewSet Conventions
- `GenericAPIView` for authenticated endpoints
- `APIView` for public endpoints
- Always define `Meta.fields` explicitly (never `'__all__'`)

## Migrations
- Use only Django operations: `AddField`, `RemoveField`, `RenameField`, `AlterField`, `RunPython`
- Never use `RunSQL` — must work across SQLite, PostgreSQL, MySQL

## Background Jobs (Huey)
- Use for: tracking updates, batch rates, document generation, webhook retries, data exports
- Don't use for: real-time user-facing operations
- Jobs run synchronously in tests (`HUEY['immediate'] = True`)
