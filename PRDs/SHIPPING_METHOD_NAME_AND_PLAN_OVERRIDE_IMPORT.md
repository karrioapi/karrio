# PRD — Shipping Method Display Name + Plan-Override CSV Import

**Status:** Draft · 2026-04-13
**Author:** Daniel K
**Scope:** `karrio/modules/data`, `karrio/modules/sdk` (rating_proxy), `modules/shipping`, `admin` app

---

## Summary

Two linked defects in the rate-sheet CSV pipeline:

1. The `notes` column is (mis-)used to carry a human-friendly shipping method name.
   It must become a first-class **`shipping_method`** column, stored as a
   **service-level override**, and surfaced in the rate response instead of the
   service code/name when present.
2. The per-plan cost columns (`plan_cost_start`, `plan_cost_advanced`, `plan_cost_pro`,
   `plan_cost_enterprise`) are currently written to rate meta as flat keys that the
   rate resolver ignores. They must be imported as proper **custom-margin overrides**
   (the same feature exposed by the Edit Service Rate dialog's "Plans → Custom
   Margin" section) keyed by `markup_id`, via `meta.plan_costs` / `meta.plan_cost_types`.

---

## Background

### Current `notes` handling

`karrio/modules/data/karrio/server/data/resources/rate_sheets.py:317`

```python
notes = _str(row.get("notes"))
if notes:
    meta["notes"] = notes
```

Values like `"DHL KleinPaket 0-1kg"` land on **rate-level meta** per row. They are
never consulted by the rate resolver and have no UX surface beyond the CSV preview.

### Current plan-column handling

Same file, lines 297–310:

```python
plan_fields = [
    "plan_rate_start", "plan_cost_start",
    "plan_rate_advanced", "plan_cost_advanced",
    "plan_rate_pro", "plan_cost_pro",
    "plan_rate_enterprise", "plan_cost_enterprise",
]
for field in surcharge_fields + plan_fields:
    val = _float(row.get(field))
    if val is not None:
        meta[field] = val
```

Result on `rate.meta`:

```json
{ "plan_rate_start": 4.08, "plan_cost_start": 4.08, ... }
```

### The real override contract

`karrio/modules/sdk/karrio/universal/mappers/rating_proxy.py:511` only reads:

```python
_plan_costs = _zone_meta.get("plan_costs") or {}   # { markup_id: cost }
```

and the admin UI writes (`service-rate-editor-dialog.tsx:140-155`):

```json
"meta": {
  "plan_costs":      { "<markup_id>": 4.08 },
  "plan_cost_types": { "<markup_id>": "AMOUNT" }
}
```

where `markup_id` is resolved from `markup.meta.plan == "start"|"advanced"|"pro"|"enterprise"`.
The importer does not build this shape today — the flat keys are dead data for shipping.

---

## Decisions (resolved)

| # | Question | Decision |
|---|---|---|
| Q1 | `shipping_method` scope — service-level or rate-level? | **Service-level.** Stored in `ServiceLevel.metadata["shipping_method"]`. CSV rows for the same `service_code` must agree on the value; the last non-empty wins if they diverge, with a row-level warning in the import report. |
| Q2 | How does the importer resolve `plan_cost_<slug>` → markup? | Match `markup.meta.plan == "<slug>"` on **active** admin markups. Prefer markups scoped to the rate sheet's carrier (`markup.carrier_codes` contains the carrier) when multiple match. If no markup matches for a given slug, **skip silently but surface in the import report**. Cost type is always `"AMOUNT"` (CSV expresses absolute amounts). |
| Q3 | `notes` column backward compatibility? | Accept **both** `shipping_method` and legacy `notes` as input. `shipping_method` wins when both are present. New export always emits `shipping_method`. `notes` header still accepted to avoid breaking existing sheets. |

---

## Architecture

```
CSV upload
  │
  ▼
┌─────────────────────────────────────────────────┐
│  rate_sheets.py  (data module)                   │
│                                                  │
│  _build_rate_meta(row, plan_markup_index)        │
│    ├── collect service-level shipping_method    │
│    │      (attach to service, not rate)         │
│    ├── for slug in ("start","advanced",…):      │
│    │   mid = plan_markup_index[carrier][slug]   │
│    │   if mid and row["plan_cost_<slug>"]:      │
│    │     plan_costs[mid] = cost                 │
│    │     plan_cost_types[mid] = "AMOUNT"        │
│    └── meta["plan_costs"], meta["plan_cost_types"]│
└──────────────────┬──────────────────────────────┘
                   │ plan_markup_index built once via
                   │ Markup.objects.filter(active=True, meta__plan__isnull=False)
                   ▼
            ServiceLevel.metadata = { shipping_method: … }
            ServiceRate.meta      = { plan_costs, plan_cost_types, … }

Rate request flow (rating_proxy.py)
  │
  ▼
┌─────────────────────────────────────────────────┐
│  rate.meta.shipping_method                      │
│     = ServiceLevel.metadata.shipping_method     │ ← new (lift from service)
│  rate.service                                   │
│     = service.service_code                      │ ← unchanged (machine key)
│                                                  │
│  consumers (rate list UI, labels) fall back:    │
│     shipping_method or service_name             │
└─────────────────────────────────────────────────┘
```

---

## Implementation plan

### Phase A — CSV import + SDK (karrio repo)

1. `karrio/modules/data/karrio/server/data/resources/rate_sheets.py`
   - Add `"shipping_method"` to `OPTIONAL_COLUMNS`, right after `"service_name"`.
   - New helper `_build_plan_markup_index()` — returns `{carrier_name: {plan_slug: markup_id}}` queried once per import.
   - In the row → rate loop, emit `plan_costs` / `plan_cost_types` instead of flat `plan_cost_<slug>` keys. Leave flat keys out (silent data).
   - In the row → service loop, collect `shipping_method` (prefer `shipping_method` column, fall back to `notes` column) and set `ServiceLevel.metadata["shipping_method"]`. Multi-row conflicts produce a warning, last non-empty wins.
   - Export path (the `EXPORT_COLUMNS` tuple at line 1321): rename `notes` → `shipping_method` and bump column width. Keep reading `notes` as an alias on import only.
   - Update `test_rate_sheet_import.py` fixtures + assertions.

2. `karrio/modules/sdk/karrio/universal/mappers/rating_proxy.py`
   - Lift `ServiceLevel.metadata["shipping_method"]` into `_rate_meta["shipping_method"]` when set.
   - No change to `service` field (stays as `service_code`).

### Phase B — Rate resolver wiring (shipping-platform repo)

3. `modules/shipping/karrio/server/shipping/services/rate_resolver.py`
   - Ensure `meta.shipping_method` survives all merge steps (markup application, surcharge attribution).
   - No new logic — just don't drop it.

4. GraphQL — no schema change. `rate.meta` already marshals free-form JSON;
   `shipping_method` rides along.

### Phase C — Admin UI

5. `admin/src/components/rate-sheet/service-editor-dialog.tsx` (General tab)
   - New field **Shipping method (display name)** under Description.
   - Bound to `metadata.shipping_method`.
   - Saved on create/update.

6. `admin/src/components/rate-sheet/rate-sheet-csv-preview.tsx`
   - New column **Shipping method** inserted **immediately after `service_name`** in the preview grid.
   - Value sourced from the service's `metadata.shipping_method` (constant per service in the preview).

### Phase D — REST endpoint coverage

7. Locate the rates endpoint (`/api/v1/proxy/rates` response serializer).
   - Assert `shipping_method` is not filtered out of `meta` in either the REST or GraphQL response shapes.
   - Add an explicit field on the rate response if the meta passthrough proves too fragile — TBD during implementation.

### Phase E — Tests

| Test | Framework | File |
|---|---|---|
| CSV import writes `shipping_method` to service metadata | `karrio test` | `karrio/modules/data/.../tests/test_rate_sheet_import.py` |
| CSV import writes `meta.plan_costs` keyed by markup_id | `karrio test` | same |
| Legacy `notes` column still read as alias | `karrio test` | same |
| Plan column with no matching markup → warning, not crash | `karrio test` | same |
| Export uses `shipping_method` column name | `karrio test` | same |
| Rate response includes `meta.shipping_method` when service has it | `karrio test` | `modules/shipping/karrio/server/shipping/tests/test_rate_resolver.py` |
| Rate response honors `plan_costs` override over default markup | `karrio test` | `test_plan_based_pricing.py` (extend) |
| Admin service-editor shows + saves Shipping method | Playwright | `admin/e2e/service-editor.spec.ts` (extend) |
| Admin CSV preview shows Shipping method column after Service | Playwright | `admin/e2e/csv-preview.spec.ts` (extend) |
| Full CSV round-trip: upload CSV with plan_cost_*, request rate, see custom margin applied | Playwright | `admin/e2e/rate-sheet-import.spec.ts` (extend) |

---

## Out of scope

- Changing the override unit (PERCENTAGE vs AMOUNT). CSV is always AMOUNT.
- Per-rate `shipping_method` overrides (user confirmed service-level only).
- New GraphQL schema fields; all data rides `meta`.
- Migrating existing rate sheets' flat `plan_cost_*` meta keys — new imports will use the override shape; existing data stays as-is until re-imported.

---

## Rollout

1. Land PRD.
2. Implement Phases A–B in karrio repo on one branch; test with `karrio test` + the SDK unittest suite.
3. Implement Phase C–D in admin repo on one branch.
4. Cross-repo e2e verified manually by importing a supplied CSV (e.g. `DHL-DE.csv`) and observing:
   - Service metadata shows the shipping method.
   - Edit Service Rate dialog shows `plan_cost_*` values pre-filled as Custom Margins.
   - Rate response returns `meta.shipping_method`.
   - Rate response respects the custom margin for the active plan.
5. Merge both PRs behind no feature flag (import-only change, no user-visible breakage).
