# 05 — Rate Sheet CRUD N+1

**Status:** Needs fix
**Impact:** 56 events, ~76 queries per mutation
**Files:**
- `modules/core/karrio/server/serializers/abstract.py` (`save_many_to_many_data`)
- `modules/graph/karrio/server/graph/serializers.py` (`_RateSheetSerializerMixin`)

## Root Cause

Rate sheet create/update mutations trigger multiple layers of individual saves:

### Layer 1: save_many_to_many_data

The generic `save_many_to_many_data()` function loops through M2M items, calling `serializer.save()` and `parent.add()` individually:

```python
# Current pattern (simplified)
for item_data in items:
    serializer = ItemSerializer(data=item_data)
    serializer.is_valid()
    instance = serializer.save()   # INSERT — 1 query
    parent_field.add(instance)     # M2M INSERT — 1 query
```

For 20 services, this produces 40 queries (20 INSERTs + 20 M2M adds).

### Layer 2: process_zones

Each zone is added or updated individually, and each call triggers `self.save(update_fields=["zones"])`:

```python
# Current pattern (simplified)
for zone_data in zones:
    self.add_zone(zone_data)       # modifies JSON field
    self.save(update_fields=["zones"])  # UPDATE — 1 query per zone
```

For 15 zones, this produces 15 UPDATE queries.

### Layer 3: process_surcharges

Same pattern as zones:

```python
for surcharge_data in surcharges:
    self.add_surcharge(surcharge_data)
    self.save(update_fields=["surcharges"])  # UPDATE — 1 query per surcharge
```

For 10 surcharges, this produces 10 UPDATE queries.

## Query Breakdown

| Operation | Current Queries | Optimal Queries |
|-----------|----------------|----------------|
| Service INSERTs | 20 | 1 (bulk_create) |
| Service M2M adds | 20 | 1 (.set() or .add(*list)) |
| Zone UPDATEs | 15 | 1 (batch in memory, single save) |
| Surcharge UPDATEs | 10 | 1 (batch in memory, single save) |
| Service rates batch | ~10 | 1 (already has batch method) |
| Rate sheet save | 1 | 1 |
| **Total** | **~76** | **~6** |

## Existing Batch Methods

The model already has batch methods that are underutilized:

- `batch_update_service_rates()` — updates all service rates in one operation
- `batch_update_surcharges()` — updates all surcharges in one operation

These methods exist but the serializer code does not use them.

## Proposed Fix

### Fix 1: Batch M2M Service Creation

```python
# Instead of individual saves + adds:
instances = []
for item_data in items:
    serializer = ItemSerializer(data=item_data)
    serializer.is_valid(raise_exception=True)
    instances.append(serializer.create(serializer.validated_data))

# Bulk create all services
created = ServiceModel.objects.bulk_create(instances)

# Single M2M set
parent_field.set(created)
```

### Fix 2: Batch Zone Processing

```python
# Instead of save-per-zone:
def process_zones(self, zones_data):
    zones = list(self.zones or [])
    for zone_data in zones_data:
        # modify zones list in memory (add/update)
        ...
    self.zones = zones
    self.save(update_fields=["zones"])  # single UPDATE
```

### Fix 3: Batch Surcharge Processing

```python
# Same pattern as zones:
def process_surcharges(self, surcharges_data):
    surcharges = list(self.surcharges or [])
    for surcharge_data in surcharges_data:
        # modify surcharges list in memory (add/update)
        ...
    self.surcharges = surcharges
    self.save(update_fields=["surcharges"])  # single UPDATE
```

### Fix 4: Use Existing Batch Methods

Wire the serializer to call `batch_update_service_rates()` and `batch_update_surcharges()` instead of the per-item methods.

## Prevention

- Never call `model.save()` inside a loop for JSON field modifications — collect changes in memory and save once
- Never call `parent_field.add(item)` inside a loop — use `parent_field.set(items)` or `parent_field.add(*items)`
- When batch methods exist on the model, the serializer must use them
