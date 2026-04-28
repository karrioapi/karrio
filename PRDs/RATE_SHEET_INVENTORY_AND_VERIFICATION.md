# Rate Sheet Inventory + Manual Verification Report

**Status:** Verification round complete · 2026-04-14
**Stack tested:** local (admin :3104, karrio :5002) with `admin@example.com / demo`
**Source CSV:** `/Users/danielk/Downloads/JTL_Shipping_Master_FinalV4.xlsx` →
regenerated via `karrio/bin/regenerate-rate-sheets` → `~/Downloads/rate-sheets/DHL-DE.csv` (87 rows).

This is the post-implementation inventory. It documents every rate-sheet
feature (frontend + backend), tags each one with verification status, and
lists the regressions found + fixed during the manual Playwright walk.

---

## A. End-to-end verification — what works after this PR

### A.1 Import flow (Create new rate sheet)

| Step | Observed | Status |
|---|---|---|
| Click "Add Rate Sheet" → editor opens | sheet panel `Create Rate Sheet` renders with Edit/Import/Export tabs | ✅ |
| Click "Import" tab | drop-zone + file picker visible | ✅ |
| Upload `DHL-DE.csv` | dry-run validates: `87 unchanged, 0 added` (when reimporting) or `87 added` (fresh) | ✅ FIXED — was `7 unchanged` before this PR |
| Diff table | one row per (service × zone × weight × options-bundle) variant — 87 distinct rows visible | ✅ FIXED |
| Click "Confirm Import" | sheet closes, returns to list, dhl_parcel_de card shows "3 Services" | ✅ |
| Persisted state (GraphQL) | 3 canonical services + 87 rate rows preserved with `meta.options` + `meta.shipping_method` per row | ✅ verified live |

### A.2 Persisted data shape (verified via `/admin/graphql` against the imported sheet)

```
=== dhl_parcel_de (rsht_xxx) — 3 services, 87 rate rows ===
Services:
  - dhl_parcel_de_retoure        | DHL Retoure Online    | metadata.shipping_method='DHL Retoure Online'
  - dhl_parcel_de_paket          | DHL Paket             | metadata.shipping_method='DHL Paket'
  - dhl_parcel_de_kleinpaket     | DHL Kleinpaket        | metadata.shipping_method='DHL Kleinpaket'

Service rates (excerpt — dhl_parcel_de_retoure, 3 variant rows at flat 0.001-31.501 kg):
  rate=6.19  options={}                                         shipping_method='DHL Retoure Online'
  rate=6.19  options={'qr_code': True}                          shipping_method='DHL Retoure Online - QR Code'
  rate=6.34  options={'gogreen_plus': True, 'qr_code': True}    shipping_method='DHL Retoure Online GoGreen Plus - QR Code'

Service rates (excerpt — dhl_parcel_de_kleinpaket, 2 variant rows):
  rate=3.39  options={}                                         shipping_method='DHL KleinPaket'
  rate=3.49  options={'gogreen_plus': True}                     shipping_method='DHL Kleinpaket GoGreen Plus'

dhl_parcel_de_paket: 82 variant rate rows (5 weight buckets × ~16 option combos).
```

This is the canonical model: **canonical service_codes, options as the variant discriminator, per-rate `shipping_method` for display.**

---

## B. Regressions found + fixed during this verification

### B.1 `compute_diff` collapsed variant rows (CRITICAL)
**Symptom:** dry-run preview reported `7 unchanged` after importing the regenerated 87-row CSV. Variants were invisible.
**Root cause:** `_rate_key` in `compute_diff` keyed on `(service, zone, st, min, max)` — same tuple for every variant. The `incoming_map` dict comprehension collapsed 87 rows into 7.
**Fix:** `_rate_key` now returns a 6-tuple including a stable options fingerprint (sorted `key=value|...` from `rate.meta.options`). `_diff_row` exposes the fingerprint as `row['options']` and the per-variant `shipping_method` as `row['shipping_method']`.
**Verified:** dry-run now reports `87 unchanged` on re-import. Variant identity surfaced in diff rows. Commit `6bc77ca0`.

### B.2 Service-level `shipping_method` polluted by arbitrary variant
**Symptom:** `ServiceLevel.metadata.shipping_method` for the `dhl_parcel_de_paket` service was `"DHL Paket Visual Age Check 16+"` — an arbitrary variant name, not the canonical "DHL Paket".
**Root cause:** `build_rate_sheet_input_from_flat` did first-row-wins for the service-level lift. With 22 rows mapping to one canonical service_code, the first row's variant name won.
**Fix:** Service-level `shipping_method` now prefers the no-options (canonical) variant. Per-rate `meta.shipping_method` keeps each row's own variant name.
**Verified:** service-level metadata now shows `"DHL Paket"`, `"DHL Kleinpaket"`, `"DHL Retoure Online"` — clean canonical names. Variant names ride per-row.

---

## C. Feature inventory — admin rate-sheet module

Tagged with verification status: ✅ verified working · 🟡 not yet exercised in this verification pass · ⚠️ known limitation/follow-up.

### C.1 Rate-sheet list page (`RateSheetsPage.tsx`)
| Feature | Status | Notes |
|---|---|---|
| Card grid with carrier logo / counts / actions | ✅ | dhl_parcel_de card shows "3 Services" after import |
| Search by name/carrier (debounced 500ms) | 🟡 | not exercised |
| Empty / loading / error states | 🟡 | not triggered |
| Add Rate Sheet button → opens editor with `id=new` | ✅ | |
| Three-dot menu Edit / Delete | 🟡 | not exercised |

### C.2 Rate-sheet editor (`rate-sheet-editor.tsx`)
| Feature | Status | Notes |
|---|---|---|
| Edit / Import / Export top tabs | ✅ | |
| Carrier dropdown, sheet name, currency, origin countries, weight/dimension units | 🟡 | not exercised in this pass |
| Service tabs in left column | 🟡 | tabs render after import (see post-import editor screenshot) |
| Save → CREATE_RATE_SHEET / UPDATE_RATE_SHEET mutation | ✅ | indirect via import flow |

### C.3 Service editor dialog (`service-editor-dialog.tsx`)
| Feature | Status | Notes |
|---|---|---|
| 6 tabs: General / Transit / Features / Logistics / Limits / Surcharges | 🟡 | not opened in this verification pass |
| 14-flag features object incl. labelless / notification / address_validation | ✅ | backend GraphQL `ServiceLevelFeaturesInput` accepts all 14 (regression test in PR) |

### C.4 Zones (`zone-editor-dialog.tsx`, `zones-tab.tsx`)
| Feature | Status |
|---|---|
| Create / edit / delete zone | 🟡 not exercised |
| Per-service zone assignment (zone_ids) | ✅ DHL-DE imports a single `DE` zone linked to all 3 services |

### C.5 Surcharges (`surcharges-tab.tsx`, `surcharge-editor-dialog.tsx`)
| Feature | Status |
|---|---|
| Shared surcharge CRUD | 🟡 not exercised |
| AMOUNT vs PERCENTAGE | 🟡 |

### C.6 Rate grid (`weight-rate-grid.tsx`, `service-rate-detail-view.tsx`)
| Feature | Status |
|---|---|
| Editable cells | 🟡 not exercised |
| Weight range CRUD | 🟡 |
| Edit Service Rate dialog: Plans → Custom Margin (`meta.plan_costs[markup_id]`) | ✅ wiring verified end-to-end in #444; plan_cost columns of regenerated CSV emit `meta.plan_costs` correctly |
| Excluded markups / surcharges per cell | 🟡 not exercised |

### C.7 Markups / Brokerage tab (`markups-tab.tsx`, `markup-editor-dialog.tsx`)
| Feature | Status |
|---|---|
| Markup CRUD | 🟡 |
| Scoping (carrier_codes, service_codes, connection_ids, organizations) | ✅ accepted by backend (verified earlier) |
| Sheet-level `excluded_markup_ids` toggle | 🟡 |
| Per-service exclusions | 🟡 |

### C.8 CSV import (`rate-sheet-import-panel.tsx`, `batch_rate_sheets.py`)
| Feature | Status | Notes |
|---|---|---|
| Drag-drop OR file picker | ✅ file-picker path verified |
| Dry-run preview with diff summary | ✅ FIXED — variant rows now visible |
| `create_mode` flag forces unique slug | ✅ wired (this PR) |
| Plan-cost override resolution (`plan_margin_<slug>_eur` → `rate.meta.plan_costs`) | ✅ |
| Per-rate options (dynamic `option_*` columns) → `rate.meta.options` | ✅ |
| Per-rate `shipping_method` → `rate.meta.shipping_method` | ✅ |
| Service-level `shipping_method` lift (canonical only) | ✅ FIXED |
| `notes` column kept as legacy alias | ✅ |
| Duplicate-row validator includes options fingerprint | ✅ |

### C.9 CSV preview grid (`rate-sheet-csv-preview.tsx`)
| Feature | Status |
|---|---|
| One row per variant bundle (rate-level granularity) | ✅ admin PR #58 (paired) |
| Dynamic markup / surcharge columns | 🟡 not exercised in this pass |
| Feature-gated markup toggles | 🟡 |

### C.10 Export (`export_rate_sheet_xlsx`)
| Feature | Status |
|---|---|
| Round-trip safe export | 🟡 not exercised in this pass |
| `shipping_method` column in output | ✅ in code; not verified live |
| ⚠️ Doesn't yet emit `option_*` columns (pre-PR limitation) | ⚠️ deferred — re-import will lose variant identity |

### C.11 Rate resolver runtime
| Feature | Status |
|---|---|
| `rate.meta.plan_costs[markup_id]` honored as override (vs default markup.amount) | ✅ verified in #444 with green tests |
| Rate response includes `meta.shipping_method` per-rate | ✅ wired in #444 (universal SDK proxy + resolver) |
| Options-based filtering (request `options.gogreen_plus=true` → matching variant rate) | ⚠️ not yet implemented in resolver — separate PR; today rates with options just coexist as siblings |

---

## D. APIs — endpoints relevant to rate sheets

### Admin GraphQL (`POST /admin/graphql`)

| Operation | Verified |
|---|---|
| `rate_sheets` query | ✅ used in this verification |
| `rate_sheet` query | ✅ |
| `create_rate_sheet` mutation | ✅ via import |
| `update_rate_sheet` mutation | 🟡 not exercised in this pass |
| `delete_rate_sheet` mutation | 🟡 |
| Service / zone / surcharge / weight-range mutations | 🟡 |
| `create_markup` / `update_markup` / `delete_markup` | 🟡 |

### Admin REST

| Endpoint | Verified |
|---|---|
| `POST /admin/batches/data/import` (multipart, dry_run / rate_sheet_id / create_mode) | ✅ |
| `GET /v1/batches/data/export/rate_sheet.xlsx?id=…` | 🟡 |

### Token / auth

| Endpoint | Verified |
|---|---|
| `POST /api/token` (admin@example.com / demo) | ✅ used to obtain JWT for raw GraphQL inspection |

---

## E. What's still on the follow-up list (explicitly out of this PR)

1. **Rate resolver options filtering** — when a rate request includes `options.gogreen_plus=true`, the resolver should pick the variant rate row whose `meta.options` matches. Today multiple variant rows coexist but the resolver doesn't filter — picks "first match".
2. **Other carriers in `CARRIER_SERVICE_MAP`** — only `dhl_parcel_de` is authored. Asendia, Chronopost, DPD, ParcelOne, UPS-DE, UPS-NL still fall back to slugified composite codes (and trip the duplicate validator).
3. **Export path emits `option_*` columns** — current export path doesn't (yet) include the option columns, so re-import → variant identity lost.
4. **Admin frontend `create_mode=true` body** — backend accepts it; admin UI still needs to send it from the import panel when `isEditMode=false`.
5. **Session stability** (admin logout / drag-drop re-login) — separate from rate-sheet logic; tracked separately.

---

## F. Test consolidation plan (next step after this verification)

Now that the manual flow works end-to-end, write the following tests to lock it in:

1. `karrio.server.data.tests.test_rate_sheet_import`
   - `test_options_fingerprint_keeps_variants_distinct_in_diff` — incoming has 2 rows same key + diff options → diff has 2 rows.
   - `test_service_metadata_shipping_method_uses_canonical_no_options_variant`.
   - `test_dynamic_option_column_lifts_to_meta_options`.
2. `admin/e2e/_manual-inspect.spec.ts` → split into focused specs:
   - `rate-sheet-import-canonical-services.spec.ts` (fresh import → 3 services + 87 rates).
   - `rate-sheet-import-dry-run-shows-variants.spec.ts` (re-import → 87 unchanged).
3. End-to-end rate-quote integration test once resolver options filtering lands.

Until those tests exist, the manual `_manual-inspect.spec.ts` script (in the admin repo) is a reproducible verification harness — pointed at staging or local stack via env vars.
