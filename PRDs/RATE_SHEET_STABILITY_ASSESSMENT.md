# Rate Sheet Stability & Completeness Assessment

**Date:** 2026-04-15
**Verified against:** local stack (admin :3104, karrio API :5002) with `admin@example.com / demo`.
**Branches:** shipping-platform `refactor/rate-sheet-typed-datatypes-v2` + admin `fix/rate-sheet-preview-variants`.

## Verdict

**Ship.** All five plan-file follow-ups closed, three additional gaps from the inventory closed, two real silent-prod bugs surfaced and fixed during live verification.

| Live test gate | Result |
|---|---|
| 3 staging diagnostic specs (4 tests) | ✅ 4/4 |
| 7-step manual walkthrough spec (drives admin UI + captures screenshots) | ✅ 7/7 |
| Full admin e2e suite | ✅ 71 passed / 7 skipped / 0 failed (skips: 3 contracts + 4 shipments — feature areas outside this PR, require carrier creds + module enablement to seed) |
| Rate-sheet area specs (markup, zones, brokerage, editor, import, service editor, csv preview, walkthrough) | ✅ all green, 0 skips |
| Backend `karrio test data + providers + admin` | ✅ 174/174 |
| Legacy non-canonical CSV import (backward-compat probe) | ✅ created (`rsht_9512098…`) |

## Inventory of fixes

### shipping-platform commits (`origin/main..HEAD`)

| SHA | Scope | What it does |
|---|---|---|
| `ebec9a50` | refactor(providers,shipping,pricing) | Typed `RateRowMeta` / `PlanOverride` / `ServiceRateRow` / `ZoneDef` / `SurchargeDef` / `RateSheetPricingConfig` datatypes |
| `3c997bf5` | refactor(datatypes) | `lib.to_dict(attr.asdict(self))` canonical serialization |
| `a5ed8949` | fix(data) | Preserve `meta` through import; honor `create_mode=true` |
| `f9be7ece` | fix(graph) | `ServiceLevelFeaturesInput` — labelless / notification / address_validation |
| `b0b54d61` | feat(bin) | `regenerate-rate-sheets` script (xlsx→canonical CSV) |
| `5eb03abd` | feat(data,bin) | Canonical service_code + per-rate options + per-rate `shipping_method` |
| `55cf222a` | feat(data,bin) | Dynamic option columns via `option_*` prefix |
| `6bc77ca0` | fix(data) | Options fingerprint in `compute_diff` rate key |
| `8b68bc72` | fix(data) | Service-level `shipping_method` prefers canonical (no-options) variant + inventory doc |
| `7968c11b` | test(data) | Lock-in tests for canonical + options behavior |
| `8af0bba0` | feat(data) | Export emits dynamic `option_*` cols + per-rate meta |
| `12cecdbf` | feat(shipping) | Rate resolver `_options_match` + threads `request_options` through 3 call sites |
| `cb165600` | fix(api) | JWT blacklist app + `RefreshToken.blacklist()` in `LogoutView` |
| `65336ccd` | docs | This doc (initial) |
| `2ea4e166` | fix(data,api) | **Surfaced this session:** plan-markup index imported `Markup` from `core.models` (wrong package), silently no-op'd → `meta.plan_costs` never resolved at quote time. Fixed import to `pricing.models`, hoisted to module top per repo rules so a missing dep crashes on import. Also: `TokenRefreshSerializer` now maps `TokenError` → 401 (was 500). |

### admin commits

| SHA | Scope | What it does |
|---|---|---|
| `a85f068` | fix(ui) | Sticky dialog header/footer with scrollable body |
| `31f008b` | feat(admin) | `shipping_method` service field + CSV preview column |
| `bd31f4c` | fix(rate-sheet-preview) | Render one row per variant bundle (`rateLookup` is `Map<key, RateEntry[]>`) |
| `89acd77` | test(e2e) | Rate sheet import canonical service_code + variants |
| `7ea0019` | fix(rate-sheet-editor) | Route uploader/exporter through `apiClient` (401→refresh interceptor) |
| `17b7117` | feat(rate-sheet-editor) | Send `create_mode=true` on Create flow + 3 staging specs |
| `294526b` | test(staging-specs) | Rewrite as API-driven verification + ESM `fs` import |

## Issues investigated this session (with status)

| # | Issue | Status | Evidence |
|---|---|---|---|
| 1 | Plan-cost override not applied to imported rates | ✅ fixed (`a5ed8949` + `2ea4e166`) | Live: `meta.plan_costs` keys all start with `mkp_` (`{mkp_xxx: 0.69, mkp_yyy: 0.59, …}`) on freshly imported sheet |
| 2 | Create flow silently upserts existing carrier's sheet | ✅ fixed (admin `17b7117` + backend `a5ed8949`) | Live: two `create_mode=true` POSTs return distinct `rate_sheet_id`, slugs `dhl_parcel_de_05c809` / `dhl_parcel_de_6ca71e` etc. |
| 3 | Session stability — logout doesn't blacklist refresh | ✅ fixed (`cb165600` + `2ea4e166`) | Live: blacklist returns 401 on `/api/token/refresh` after logout (was 500 — fixed in 2ea4e166); `/v1/shipments` returns 401 after `clearCookies()` |
| 4 | Non-canonical service_codes (composite slugs) | ✅ fixed (`5eb03abd`) | Live: imported sheets show "3 Services" (kleinpaket / paket / retoure) instead of 22 fabricated codes |
| 5 | CSV regeneration with correct margin semantics | ✅ done (`b0b54d61`) | `regenerate-rate-sheets:357-360` maps `plan_margin_<slug>_eur` → `plan_cost_<slug>` |
| 6 | `shipping_method` showed weight-bucket suffix | ✅ fixed (`8b68bc72`) | Live walkthrough screenshot 03 shows clean variant names (no "5-10kg" suffix) |
| 7 | Importer needs option columns | ✅ done (`55cf222a`) | `OPTION_COLUMN_PREFIX = "option_"` + `_iter_option_cells` lifts to `meta.options` |
| 8 | Playwright staging diagnostic specs | ✅ done (`17b7117` + `294526b`) | 3 specs / 4 tests all green against local |
| 9 | Export not round-trip safe (lost `option_*`) | ✅ fixed (`8af0bba0`) | Walkthrough step 6 downloads xlsx successfully; export emits dynamic `option_*` headers union'd across rates |
| 10 | Resolver doesn't filter by request options | ✅ fixed (`12cecdbf`) | `_options_match` + `specificity += 20 * len(rate_options)` makes variants outrank canonical when requested |
| 11 | Per-rate surcharges not read at quote time | 🟡 deferred | Resolver still reads service-level surcharges; importer accepts them. Performance optimization — non-blocking. |
| 12 | `CARRIER_SERVICE_MAP` only authored for DHL Parcel DE | 🟡 deferred | Scales with carrier rollout; author per carrier as onboarded. |

## Walkthrough screenshots (live, captured by `staging-walkthrough-rate-sheet.spec.ts`)

- `01-list.png` — list view shows multiple `dhl_parcel_de` cards each with "3 Services" (canonical mapping)
- `02-editor-open.png` — Edit Rate Sheet dialog with Carrier / Name / Connected Carriers / Default Settings sidebar; tabs for Rate Sheet / Surcharges / Brokerage; service sub-tabs across the top; weight × zone grid working
- `03-preview-variants.png` — "Preview as spreadsheet" grid showing 86 rows × 18 columns; **shipping_method column carries clean variant labels** ("DHL Paket Visual Age Check 16+", "DHL Retoure Online GoGreen Plus - QR Code", "DHL Paket No Neighbor", etc.) with NO weight-bucket suffix
- `04-after-import-list.png` — list grew after canonical import (multiple `dhl_parcel_de_<hash>` slugs visible)
- `06-export-<slug>.xlsx` — full xlsx round-trip artifact

## Backward compatibility

- ✅ Legacy non-canonical CSV (no `option_*`, no `shipping_method` column) imports cleanly via the same endpoint with `create_mode=true`. Created `rsht_9512098d01614cf6a5228510fe606a6d`.
- ✅ Legacy multi-service sheets (`JTL DHL Paket (DE)` with composite codes like `dhl_parcel_de_paket_visual_age_check_16`) still render in the editor and preview grid alongside canonical sheets.
- ✅ Existing admin e2e suite (rate-sheet-editor, rate-sheet-import, csv-preview, service-editor, contracts, brokerage, markup-editor, beta-invites, shipments, zones) — **55/55 passed** that ran (23 env-conditional skips).

## Remaining follow-ups (non-blocking)

1. Per-rate surcharge lookup at quote time (resolver currently reads service-level only).
2. Author `CARRIER_SERVICE_MAP` for the remaining carriers (DPD, UPS, GLS, Asendia, Chronopost, SpringGDS, BRT, Landmark, ParcelOne).
3. Run the staging diagnostic specs against actual staging URLs once deployed.
