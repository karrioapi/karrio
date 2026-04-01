# PRD: Rate Sheet Excel/CSV Import & Export

**Status:** Finalised — Implementation Ready  
**Author:** Daniel K  
**Created:** 2026-03-13  
**Updated:** 2026-03-13 (all design questions answered)  
**Module:** `karrio.server.data` + `karrio` (rate sheet editor element) + `jtlshipping/admin` (e2e tests)

---

## 1. Problem Statement

Rate sheets are currently seeded via a 6,000-line Python script (`bin/seed_rate_sheets.py`) that parses a presentation-oriented Excel workbook through 1,718 lines of custom mapping logic (`bin/seed_lib/excel_parser.py`). This creates several problems:

- **No self-service**: Adding or updating rates requires a developer to run a script
- **Brittle mapping**: The parser handles 5 different Excel structural patterns; any format change breaks it
- **No in-product UI**: Rate configuration is entirely outside the product
- **No export**: There is no way to export a rate sheet back to a usable format

---

## 2. Proposed Solution

A first-class **Rate Sheet Import/Export** feature consisting of:

1. **Standardised Excel/CSV template** — 6-sheet workbook (README + 5 data sheets), columns map 1:1 to the karrio API. Lives at `templates/rate-sheet-template.xlsx` at the repo root.
2. **Karrio API extension** — extend `POST /v1/batches/data/import` with `resource_type=rate_sheet`; add export endpoint.
3. **Rate sheet editor UI extension** — import/export toggle embedded directly in the existing `rate-sheet-editor.tsx` in `karrio/packages/ui/components/`, **not** a separate admin page.
4. **Seed script update** — replace the complex Excel parser with a ~80-line flat reader that auto-detects old vs. new format.
5. **API tests** — in `karrio/modules/data/` covering all import/export scenarios.
6. **E2E tests** — Playwright tests in `jtlshipping/admin` covering the full import/export workflow.

---

## 3. Excel Template Format (redesigned 2026-03-13 — single flat sheet)

Template file location: **`templates/rate-sheet-template.xlsx`** (repo root of `jtlshipping/shipping-platform`)

A sample populated with ALL carrier data from Rajiv's rate sheets is at `templates/rate-sheet-sample.xlsx`.

**Design decision:** Collapsed from 5-6 cross-referenced sheets to 2 sheets total. Every row in the main sheet is fully self-contained — no ID cross-referencing, no separate zones/services/surcharges sheets. This matches the mental model of Rajiv's existing format while using karrio service codes.

| Sheet | Purpose |
|---|---|
| `README` | Instructions, field descriptions, carrier index |
| `service_rates` | **The only data sheet** — one fully-denormalised row per (carrier × service × zone × weight range) |

### `service_rates` columns (all inline)

```
carrier_name, service_code, carrier_service_code, service_name, shipment_type,
origin_country, zone_label, country_codes,
min_weight, max_weight, weight_unit, max_length, max_width, max_height, dimension_unit,
currency, base_rate, cost, transit_days, transit_time,
plan_rate_start, plan_cost_start, plan_rate_advanced, plan_cost_advanced,
plan_rate_pro, plan_cost_pro, plan_rate_enterprise, plan_cost_enterprise,
tracked, b2c, b2b, first_mile, last_mile, form_factor, signature,
fuel_surcharge, seasonal_surcharge, customs_surcharge,
energy_surcharge, road_toll, security_surcharge,
notes
```

Key fields:
- `service_code` — karrio canonical code (e.g. `dhl_parcel_de_paket`) from `carrier-metadata.json`
- `carrier_service_code` — actual API code (e.g. `V01PAK`) from `carrier-metadata.json` values
- `shipment_type` — `outbound` / `returns` / `pickup` (from Rajiv's Type column: SHIPPING/RETURNS/PICKUPS)
- `cost` — Total COGS including all surcharge components (Rajiv's "Total COGS")
- Surcharge columns — individual surcharge amounts inline (fuel, seasonal, customs, energy, road toll, security)
- Feature columns — `tracked`, `b2c`, `b2b`, `first_mile`, `last_mile`, `form_factor`, `signature` per row

Weight ranges are explicit numbers, eliminating the Spring label parsing bug.

---

## 4. Architecture

### 4.1 Templates folder (`templates/` at repo root)

```
templates/
  rate-sheet-template.xlsx       ← blank template (versioned in git)
  rate-sheet-sample.xlsx         ← populated sample with real carrier data
  README.md                      ← how to use the templates
```

This folder is the canonical source for templates distributed to users/partners. The seed script also reads from here by default.

### 4.2 Backend — `karrio/modules/data`

**Extend existing REST endpoint:**
```
POST /v1/batches/data/import
  resource_type=rate_sheet
  data_file=<xlsx or csv>
→ 202 { batch_id, status: "queued" }    ← async BatchOperation
```

**New export endpoint:**
```
GET /v1/batches/data/export?resource_type=rate_sheet&id={rate_sheet_id}
→ 200 application/vnd.openxmlformats...  ← downloads populated xlsx
```

**Files to add/modify:**
```
karrio/modules/data/karrio/server/data/
  serializers/
    base.py                      ← add `rate_sheet` to ResourceType enum
  resources/
    rate_sheets.py               ← NEW: parse Excel/CSV → upsert via GraphQL mutations
  serializers/
    batch_rate_sheets.py         ← NEW: BatchOperation handler + export generator
  tests/
    test_rate_sheet_import.py    ← NEW: API tests (see §7)
```

**Upsert logic:** match on `slug` → update if found, create if not. One file = one rate sheet.

**Format auto-detection:**
```python
def detect_format(wb):
    if 'service_rates' in wb.sheetnames:
        return 'new_template'   # 6-sheet karrio format
    else:
        return 'legacy'         # old seed script format → fallback to excel_parser.py
```

**Validation errors** returned as structured JSON before any writes:
```json
{
  "errors": [
    {"sheet": "service_rates", "row": 14, "field": "zone_id", "message": "zone 'de_zone99' not found in zones sheet"}
  ]
}
```

### 4.3 Rate Sheet Editor UI — `karrio` (shipping-platform)

**Location:** `karrio/packages/ui/components/rate-sheet-editor.tsx` (existing component, ~2868 lines)

**New UX:** Add a toggle/tab strip next to the existing CSV preview and Save buttons:

```
[ Edit ]  [ Import ]  [ Export ]          [ Save ]
```

- **Edit** (default): the existing grid editor
- **Import**: shows file picker → upload → two-step validate/preview/confirm flow (see §4.4)
- **Export**: immediately triggers download of the current rate sheet as `.xlsx`

The import/export views are **modes** within the editor, not separate pages. This keeps the feature reusable — any surface that embeds `<RateSheetEditor>` gets import/export for free.

**Import mode entry points:**
- Creating a new rate sheet: file picker is shown as the primary action (alongside the empty grid)
- Editing an existing rate sheet: "Import" tab replaces rates from file

### 4.4 Import Flow (two-step, in editor)

```
Step 1 — Upload & Validate
  User selects .xlsx or .csv
  POST /v1/batches/data/import (resource_type=rate_sheet, dry_run=true)
  ↓
  Loading spinner → "Validating..."
  ↓
  If errors: show inline error list (sheet · row · field · message)
  If OK: advance to Step 2

Step 2 — Preview Diff
  Full diff table showing every changed rate:
    ┌─────────────────────────────────────────────────────────────┐
    │ Service           Zone       Weight      Old Rate  New Rate │
    │ DHL Paket         Germany    0–2 kg      6.19      6.50  ↑  │
    │ DHL Kleinpaket    Germany    0–1 kg      3.43      3.43  =  │
    │ DHL Paket Express [NEW]      0–2 kg      —         9.90  +  │
    └─────────────────────────────────────────────────────────────┘
  Summary counts: X services · Y rate rows · Z zones · A updated · B new · C removed
  
  [ Cancel ]  [ Confirm Import ]
  ↓
  POST /v1/batches/data/import (without dry_run)
  Poll BatchOperation → show progress bar
  On complete: switch back to Edit mode, grid refreshes with new data
```

### 4.5 Seed Script — `bin/seed_rate_sheets.py`

Add new flat reader alongside existing parser:

```python
# Auto-detect and route
def parse_workbook(filepath):
    wb = openpyxl.load_workbook(filepath)
    if 'service_rates' in wb.sheetnames:
        return parse_new_template(wb)   # ~80 lines, 1:1 column mapping
    else:
        return parse_legacy_excel(wb)   # existing excel_parser.py logic

# New flat reader
def parse_new_template(wb):
    rate_sheet = rows(wb['rate_sheet'])
    zones      = rows(wb['zones'])
    services   = rows(wb['services'])
    surcharges = rows(wb['surcharges'])
    rates      = rows(wb['service_rates'])
    return build_rate_sheet_input(rate_sheet, zones, services, surcharges, rates)
```

---

## 5. Data Validation Rules

| Rule | Error message |
|---|---|
| All required columns present | `Missing required column '{col}' in sheet '{sheet}'` |
| `zone_id` in service_rates → exists in zones | `zone_id '{id}' not found in zones sheet (row {n})` |
| `service_id` in service_rates → exists in services | `service_id '{id}' not found in services sheet (row {n})` |
| `surcharge_ids` in service_rates → exist in surcharges | `surcharge_id '{id}' not found in surcharges sheet (row {n})` |
| `shipment_type` is `outbound`, `returns`, or `pickup` (or blank → defaults to `outbound`) | `Invalid shipment_type '{val}' — must be outbound, returns, or pickup (row {n})` |
| `min_weight < max_weight` or both 0 (flat rate) | `min_weight must be less than max_weight (row {n})` |
| No duplicate `(service_id, zone_id, min_weight, max_weight)` | `Duplicate rate row for {service_id}/{zone_id}/{min}-{max} kg (rows {a}, {b})` |
| `carrier_name` is a registered karrio carrier | `Unknown carrier_name '{name}'` |
| At least one rate row exists | `service_rates sheet is empty` |

---

## 6. API Tests — `karrio/modules/data/karrio/server/data/tests/test_rate_sheet_import.py`

```python
class RateSheetImportTests(APITestCase):
    def test_import_creates_new_rate_sheet(self)
    def test_import_upserts_by_slug(self)
    def test_import_validation_errors_returned_before_write(self)
    def test_import_csv_service_rates_only(self)
    def test_export_generates_valid_xlsx(self)
    def test_export_reimport_roundtrip(self)   # export → import → same data
    def test_dry_run_returns_diff_without_writing(self)
    def test_legacy_format_still_accepted(self)
    def test_invalid_carrier_name_rejected(self)
    def test_duplicate_rate_rows_rejected(self)
```

---

## 7. E2E Tests — `jtlshipping/admin` Playwright

File: `admin/e2e/rate-sheet-import-export.spec.ts`

```typescript
// Full workflow tests
test('upload new rate sheet via Excel → validates → shows diff → confirms → grid refreshes')
test('upload to existing rate sheet → shows updated rate rows in diff')
test('upload file with errors → inline error list shown, no import committed')
test('export rate sheet → downloads valid xlsx with all 6 sheets')
test('export → edit → re-import → shows only changed rows in diff')
test('CSV upload (service_rates only) → updates rates on existing sheet')
test('cancel on preview step → no changes written')
test('import mode toggle → switches between edit/import/export views')
```

---

## 8. Decisions (All Finalised 2026-03-13)

| # | Question | Decision |
|---|---|---|
| Q1 | Who can upload? | Extend existing `/v1/batches/data/import`. Not admin-only — users can import rate sheets too. Add `rate_sheet` to `ResourceType`. |
| Q2 | Create vs update? | Upsert by slug. Slug match → update; no match → create. |
| Q3 | Async or sync? | Always async (`BatchOperation`, consistent with existing pattern). |
| Q4 | CSV support? | Both CSV and Excel. CSV = `service_rates` sheet only (flat format). Excel = full 6-sheet workbook. |
| Q5 | Upload UI placement? | Embedded in `rate-sheet-editor.tsx` as Import/Export mode tabs. Not a separate admin page. Create = primary action on empty editor. Update = Import tab on existing editor. |
| Q6 | Preview/dry-run? | Two-step: validate → full diff table → user confirms. Full diff table (option B) — every changed rate highlighted. |
| Q7 | Seed script backward compat? | Auto-detect by `service_rates` sheet presence. New format → flat reader; old format → `excel_parser.py`. |
| Q8 | Export? | Yes — in scope. Download current rate sheet as populated xlsx. |
| Q9 | One file = one carrier? | One upload = one rate sheet. |
| Q10 | Error handling? | Inline error list (sheet, row, field, message) in the editor UI. |
| Q11 | Preview diff style? | **B — full diff table** (every changed rate highlighted, with summary counts above). Upload UI is in **karrio** (shipping-platform), not admin app. |
| Q12 | API tests? | Mandatory. 10 test cases covering import, upsert, dry-run, export, roundtrip, CSV, legacy compat, validation failures. |
| Q13 | Templates location? | `templates/` folder at **repo root** of `jtlshipping/shipping-platform`. Contains blank template + populated sample + README. |
| Q14 | E2E tests? | Mandatory. Playwright in `jtlshipping/admin` covering the full import/export workflow (8 test cases). |

---

## 9. Implementation Plan

### PR 1 — Backend (`shipping-platform` / karrio module)
- [ ] Add `rate_sheet` to `ResourceType` enum
- [ ] `resources/rate_sheets.py` — Excel/CSV parser for new format
- [ ] `serializers/batch_rate_sheets.py` — BatchOperation handler
- [ ] Export endpoint: `GET /v1/batches/data/export?resource_type=rate_sheet&id=...`
- [ ] `dry_run=true` param support returning diff JSON
- [ ] Auto-detect legacy vs. new format
- [ ] `test_rate_sheet_import.py` — 10 API test cases

### PR 2 — Templates folder (`shipping-platform` repo root)
- [ ] `templates/rate-sheet-template.xlsx` — blank 6-sheet template
- [ ] `templates/rate-sheet-sample.xlsx` — populated with real JTL carrier data (built from connector CSVs)
- [ ] `templates/README.md`

### PR 3 — UI (`shipping-platform` / karrio packages)
- [ ] Add Import/Export mode toggle to `rate-sheet-editor.tsx` (next to existing CSV preview + Save)
- [ ] `RateSheetImportPanel` component — file picker, Step 1 validation error display
- [ ] `RateSheetDiffPreview` component — full diff table (Step 2 confirmation)
- [ ] Export button — `GET /v1/batches/data/export` → file download
- [ ] Poll `BatchOperation` during import, progress bar, refresh editor on complete

### PR 4 — E2E tests (`jtlshipping/admin`)
- [ ] `admin/e2e/rate-sheet-import-export.spec.ts` — 8 Playwright test cases
- [ ] Test fixtures: sample xlsx files in `admin/e2e/fixtures/`

---

## 10. Out of Scope

- Multi-carrier batch upload (one file = multiple rate sheets)
- Downloadable error report as CSV (inline error list only)
- Rate sheet versioning / history
- Real-time collaborative editing
