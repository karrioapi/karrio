# Rate Sheet Editor: Weight Range by Zone Pricing Grid

<!-- ENHANCEMENT: Feature enhancement to the rate sheet editor -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.4 |
| Date | 2026-02-04 |
| Status | Implementation Complete — QA & Testing Remaining |
| Owner | Engineering Team |
| Type | Enhancement |
| Reference | [AGENTS.md](../AGENTS.md) |

---

## Current Status (2026-02-04)

| Phase | Status | Summary |
|-------|--------|---------|
| Phase 1: Backend Model + GraphQL | **Done** | All model methods, inputs, mutations, and schema registration complete (base + admin) |
| Phase 2: JTL Shipping App | **Done** | ServiceRateDetailView, AddWeightRangeDialog, preset Popovers, per-cell delete, clone support, full parity with Karrio UI. Editor restructured to 2-tab layout with inline CRUD. |
| Phase 3: Karrio Dashboard + Admin | **Done** | Shared UI components, hooks (dashboard + admin), preset Popovers, per-cell delete, clone support |
| Phase 4: Polish + Backward Compat | **Done** | Backward compat, empty states, frontend + backend validation, virtual scroll, service-tab UI, preset Popovers, per-cell delete, cross-surface parity, modal layering, per-service weight ranges, condensed tabs, carrier gate, Karrio Dashboard v1.4 parity — all done |
| Phase 5: Testing | **Not started** | No unit or integration tests written yet. This is the primary remaining gap |

### Recent Changes (v1.4) — Editor Restructuring & UX Polish

**Structural overhaul (JTL + Karrio):**
- **5 tabs to 2** — Consolidated Rate Sheet, Services, Zones, Weight Ranges, Surcharges into just "Rate Sheet" and "Surcharges". Services/Zones/Weight Ranges tabs removed; all CRUD moved inline to the rate grid.
- **Service sub-tabs with inline CRUD** — Services appear as horizontal tabs within Rate Sheet. Each shows hover-reveal edit (Pencil) and delete (Trash2) icons. `AddServicePopover` with presets/clone/create at end of tab bar.
- **Zone inline CRUD on column headers** — Hover-reveal edit, delete, unlink icons with `bg-muted` background to prevent text overlap. Zone headers wrapped in `Tooltip` (countries + transit days).
- **Weight range inline CRUD on row labels** — Hover-reveal edit (Pencil) and delete (Trash2) icons. Labels wrapped in `Tooltip` (rate count + avg rate). `AddWeightRangePopover` replaces plain button in toolbar.
- **Karrio Dashboard parity** — Ported all v1.4 changes to `karrio/packages/ui/components/`: `add-service-popover.tsx`, `add-weight-range-popover.tsx`, `edit-weight-range-dialog.tsx` (new); `service-rate-detail-view.tsx`, `surcharge-editor-dialog.tsx`, `rate-sheet-editor.tsx` (updated). Backend overlap validation added to `sheet.py:add_weight_range()`.
- **Staged/committed pattern** — Zone and surcharge add operations use staged pattern: object created in memory, dialog opened for editing, only committed to state on save. Cancel undoes any service linkings made during dialog.

**New components (4 files):**
- `tooltip.tsx` — `@floating-ui/react` tooltip with configurable placement and delay
- `AddServicePopover.tsx` — Preset/clone/create popover with `iconOnly` mode for tab bar
- `AddWeightRangePopover.tsx` — Missing ranges, carrier presets, and custom range sections
- `EditWeightRangeDialog.tsx` — Portal-based dialog for editing `max_weight` with overlap validation

**Layout & widths:**
- Weight column: 160px → 200px. Zone column: 112px → 140px. Inline `style` replaces Tailwind w-* classes.
- Tab header: condensed/default shadcn style (removed `flex-1` stretch)
- Service tabs: single-line `overflow-x-auto` with hidden scrollbar (no wrap, no visible scrollbar)

**Modal layering & dialog safety:**
- `Modal.tsx`, `ConfirmDialog.tsx` raised to `z-[100]` (from `z-50`) to layer above Sheet
- All dialog backdrops `stopPropagation`; ESC handlers `stopImmediatePropagation` + capture phase
- `SheetContent` `onPointerDownOutside`/`onInteractOutside` prevent close when any dialog open
- `handleSheetOpenChange` guards all dialog open states

**Cell editing behavior:**
- No value loss on blur: empty/invalid input reverts to previous value instead of deleting
- Explicit Trash2 icon for cell rate deletion (replaced tiny X), `h-3 w-3` with `hover:bg-destructive/10`
- `onDeleteRate` wired in both edit and create modes (was edit-only)

**Per-service weight range scoping (create mode):**
- Adding a weight range creates rates only for the current service's zones (not all services)
- Removing a weight range removes rates only for the current service; global range kept if other services use it
- Confirm dialog: "from this service? Rates for other services will not be affected."

**Other improvements:**
- CSV preview filters out empty/zero-rate rows
- Create mode: disabled overlay "Select a carrier to get started" when no carrier selected
- Surcharge editor: "Select All" / "Deselect All" toggle for linked services
- `getServiceWeightRanges(serviceId)` and `getMissingWeightRanges(serviceId)` for per-service range filtering

### Recent Changes (v1.3)

- **Preset Popover dropdowns on all tabs** — Replaced plain "Add" buttons with Popover dropdowns across all four tabs (Zones, Surcharges, Weight Ranges, Services) in both Karrio UI and JTL Shipping App. Each Popover shows up to three sections: carrier default presets (from `references.ratesheets[carrierName]`), clone existing items, and "Create new". Presets that have already been added are filtered out.
- **Clone functionality** — Added clone support for services, zones, and surcharges. Cloning creates a copy with a new generated ID and "(copy)" suffix on the name, then opens the editor dialog for customization.
- **Per-cell rate deletion** — Added `onDeleteRate` callback to `ServiceRateDetailView` in both frontends. A small "X" button appears on hover for each cell that has a rate value, calling `deleteServiceRate` mutation. Supports both edit mode (persisted via mutation) and create mode (local state removal).
- **Admin schema parity fix** — Added three missing mutations to admin schema: `DeleteServiceRateMutation`, `AddWeightRangeMutation`, `RemoveWeightRangeMutation`. Both base and admin schemas now have all 18 rate sheet mutations at full parity.
- **Full JTL shipping-app parity** — Surgically updated all shipping-app tab components (`ServicesTab`, `ZonesTab`, `SurchargesTab`, `WeightRangesTab`, `ServiceRateDetailView`, `RateSheetEditor`) to match exact feature set from Karrio UI, adapted for shipping-app conventions (`lucide-react` icons, `@/components/ui/` imports, `apiReferences` naming, `toast.success/error` pattern).

### Recent Changes (v1.2)

- **Replaced overview grid with service tabs** — The wide `WeightRateGrid` overview (all services as column groups) has been replaced by a service-tab approach. Each tab shows a `ServiceRateDetailView` (weight x zone grid) for one service at a time. This matches how Excel rate cards are structured.
- **Enhanced `ServiceRateDetailView`** — Added `onAddWeightRange`, `onRemoveWeightRange`, `onAddZoneToService` optional props. Added per-row delete button on weight range rows, "+" column for zone management, toolbar below the grid, and improved weight range label format.
- **Auto-select first service** — Both editors now auto-select the first service tab on load, or when the current service is deleted.
- **Removed `WeightRateGrid` from rendering** — The overview grid component is no longer rendered in either editor. Utility exports (`deriveWeightRanges`, `buildRateLookupMap`) are still used. Removed unused `RateSheetTable` from Karrio create mode rendering.
- **Cleaned up type casts** — Removed unnecessary `(service as any).zone_ids` casts in JTL where the GraphQL generated type already includes `zone_ids`.

### Next Steps (Priority Order)

1. ~~**Backend validation**~~ — **Done.** Added overlap/boundary checks to `add_weight_range()` in `sheet.py` (min_weight >= 0, max_weight > min_weight, overlap detection)
2. ~~**Karrio UI parity**~~ — **Done.** Applied v1.4 restructuring (2-tab layout, inline CRUD, per-service weight ranges, condensed tabs, carrier gate, surcharge select-all, staged/committed pattern) to Karrio Dashboard editor
3. **Unit tests** — Model methods: `get_weight_ranges()`, `add_weight_range()`, `remove_weight_range()`
4. **Integration tests** — GraphQL mutations: `addWeightRange`, `removeWeightRange`, `deleteServiceRate`
5. **Performance test** — Verify grid handles large rate sheets (20 services x 10 zones x 15 weight brackets = 3000 cells)
6. **Cleanup** — Extract `buildRateLookupMap()` and `deriveWeightRanges()` from `WeightRateGrid` files into dedicated utility files; delete `WeightRateGrid` component files if no longer imported
7. **Seed script** — Update `bin/seed_rate_sheets.py` with real carrier rate card data from negotiated contracts

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Open Questions & Decisions](#open-questions--decisions)
3. [Problem Statement](#problem-statement)
4. [Goals & Success Criteria](#goals--success-criteria)
5. [Alternatives Considered](#alternatives-considered)
6. [Technical Design](#technical-design)
7. [Edge Cases & Failure Modes](#edge-cases--failure-modes)
8. [Implementation Plan](#implementation-plan)
9. [Testing Strategy](#testing-strategy)
10. [Risk Assessment](#risk-assessment)
11. [Migration & Rollback](#migration--rollback)
12. [Appendices](#appendices)

---

## Executive Summary

Upgrade the Rate Sheet Editor to support **granular weight-range-by-zone pricing** within the context of each service. The current editor displays a flat `Service Level x Zone` grid with a single rate per intersection. Real-world carrier rate cards (DHL, UPS, DPD, FedEx) define rates as a **3-dimensional matrix: Weight Bracket x Zone x Service**. This PRD adds that missing dimension to both the backend CRUD API and the frontend editor UI, enabling users to define price grids that match actual carrier contract rate cards.

### Key Architecture Decisions

1. **Implicit weight brackets**: Weight ranges are derived from unique `(min_weight, max_weight)` pairs in `service_rates`, not stored as a separate first-class field. This keeps the data model unchanged.
2. **Per-service weight ranges in create mode**: Adding a weight range creates rate entries only for the current service. Removing removes only the current service's rates; the global range is cleaned up only when unused by all services. In edit mode, backend operations remain global (all service-zone combos). (Updated in v1.4 — previously fully shared.)
3. **Service-tab UI**: Per-service tab navigation where each tab shows a clean weight x zone grid for one service at a time — matching how Excel rate cards are structured. In v1.4, the JTL shipping app was consolidated from 5 tabs to 2 (Rate Sheet + Surcharges) with all CRUD moved inline.
4. **Granular + batch mutations**: Add individual service rate CRUD mutations alongside existing batch operations for efficient inline cell editing.
5. **Safe cell editing**: Blur with empty/invalid input reverts to the previous value. Deletion requires an explicit trash icon click. No accidental data loss from focus changes.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Weight bracket rows in rate grid | Excel/CSV import (separate PRD) |
| Granular CRUD for individual ServiceRateType entries | Per-kg marginal rates ("M Rate/kg") |
| Service-tab navigation with per-service weight x zone grid | Minimum charge floors |
| Auto-select first service, weight range management in grid | Cost/COGS editing (deferred) |
| Add/remove weight range operations | Rate calculation engine changes |
| Backend mutations for weight range management | Surcharge per-weight-bracket rules |
| Admin + base GraphQL schema updates (18 mutations each) | System/default rate sheet templates |
| Preset Popover dropdowns with carrier defaults + clone | |
| Per-cell rate deletion (explicit Trash2 icon on hover) | |
| Clone functionality for services, zones, surcharges | |
| 2-tab layout: Rate Sheet + Surcharges (inline CRUD) | |
| Per-service weight range scoping (create mode) | |
| Modal layering, carrier gate, surcharge select-all | |
| **JTL Shipping App** (`apps/shipping-app/`) | |
| **Karrio Dashboard** (`karrio/packages/ui/`, `karrio/packages/hooks/`) | |
| **Karrio Admin** (`karrio/packages/admin/`, `karrio/packages/hooks/admin-rate-sheets.ts`) | |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Weight range scope | Fully shared | All services use the same weight brackets for grid consistency | 2026-01-30 |
| D2 | Special rate types (M Rate/kg, Minimum) | Deferred | Focus on the core weight bracket grid first | 2026-01-30 |
| D3 | Excel/CSV import | Separate PRD | Design data model to support import but implement later | 2026-01-30 |
| D4 | UI layout | Service tabs (per-service only) | Overview grid replaced by service-tab navigation in v1.2. Cleaner UX matching Excel rate card structure; overview was too wide with many services. | 2026-02-03 |
| D5 | Weight bracket data model | Implicit on service_rates | Derive brackets from unique (min_weight, max_weight) pairs; no new DB field | 2026-01-30 |
| D6 | CRUD granularity | Both granular + batch | Single-rate CRUD for inline editing, batch for bulk operations | 2026-01-30 |
| D7 | Cost editing | Rate only for now | Defer cost/COGS editing to follow-up | 2026-01-30 |
| D8 | Add button UX | Preset Popover dropdown | Three-section Popover (carrier presets, clone existing, create new) replaces plain "Add" button on all tabs. Carrier presets come from `references.ratesheets[carrierName]`, filtered to exclude already-added items | 2026-02-04 |
| D9 | Per-cell rate deletion | Delete button on hover | Small "X" icon appears on hover for cells with values. Calls `deleteServiceRate` mutation (edit mode) or removes from local state (create mode) | 2026-02-04 |
| D10 | Admin schema parity | Mirror all base mutations | Admin schema must register the same rate sheet mutations as base. Three missing mutations (`DeleteServiceRate`, `AddWeightRange`, `RemoveWeightRange`) were added to achieve 18-mutation parity | 2026-02-04 |
| D11 | Clone naming | "(copy)" suffix | Cloned entities get a new ID and "(copy)" appended to name/label. `service_code` is preserved as-is during clone (only display name changes) | 2026-02-04 |
| D12 | Tab layout (JTL) | 2 tabs (Rate Sheet + Surcharges) | Consolidated from 5 tabs. Services/Zones/Weight Ranges CRUD moved inline to the rate grid for faster workflow. Standalone tab components kept as reference. | 2026-02-04 |
| D13 | Weight range scope in create mode | Per-service | Adding/removing weight ranges in create mode affects only the current service. Global list updated only when no service references a range. Matches how users think about per-service rate cards. | 2026-02-04 |
| D14 | Cell deletion UX | Explicit trash icon | Clearing a cell's input on blur reverts to previous value (no data loss). Deletion requires clicking the explicit Trash2 icon on the cell. Prevents accidental rate deletion. | 2026-02-04 |
| D15 | Carrier gate in create mode | Disabled overlay | Tab content disabled with "Select a carrier to get started" overlay until carrier selected. Prevents users from configuring services/zones before carrier defaults are available. | 2026-02-04 |
| D16 | Surcharge service linking | Select All toggle | "Select All" / "Deselect All" button in surcharge editor's linked services section. Reduces clicks when a surcharge applies to all services. | 2026-02-04 |

### Edge Cases Requiring Input

| Edge Case | Impact | Proposed Handling | Needs Input? |
|-----------|--------|-------------------|--------------|
| Existing rate sheets with no weight ranges | Grid would be empty | Show empty state with prompt to "Add Weight Range" | No |
| Service with no zones assigned | No columns to display | Show message "Assign zones to this service first" | No |
| Weight range overlap (e.g., 0-5, 3-10) | Ambiguous rate lookup | Prevent overlap in UI validation; backend rejects overlapping ranges | No |

---

## Problem Statement

### Current State

The editor renders a flat **Service Level x Zone** grid with one rate cell per intersection:

```
┌─────────────────┬──────────┬──────────┬──────────┐
│  Service Level  │ DACH Reg │ EU Core  │ North Am │
├─────────────────┼──────────┼──────────┼──────────┤
│ FedEx Connect   │  54.99   │  59.99   │          │
│ FedEx Economy   │  64.99   │  84.99   │ 139.99   │
│ FedEx Priority  │  94.99   │ 109.99   │ 179.99   │
└─────────────────┴──────────┴──────────┴──────────┘
```

The current `RateSheetTable` component (`RateSheetTable.tsx:139`) iterates over services as rows and zones as columns. Each `EditableCell` holds a single rate value. There is **no weight dimension** visible in the grid.

```typescript
// Current: services as rows, zones as columns
// RateSheetTable.tsx - row virtualizer counts services
const rowVirtualizer = useVirtualizer({
    count: services.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48,
});
```

The backend `ServiceRateType` already has `min_weight` and `max_weight` fields, and `batch_update_service_rates` uses `(service_id, zone_id, min_weight, max_weight)` as the composite key. However, the frontend never populates these fields, so all service_rates have `min_weight=0, max_weight=0`.

### Desired State

The editor uses **service tabs** where each tab shows a **Weight Bracket x Zone** grid for one service:

```
Service tabs:  [DPD Classic] [DPD Express] [DPD Air]

DPD Classic (selected):

  Weight (KG)    │  Zone: DE  │  Zone EU  │  Zone 1C  │ +
─────────────────┼────────────┼───────────┼───────────┼───
 Up to 3.0 KG    │   5.35     │   6.43    │   8.13    │
 Up to 5.0 KG    │   5.89     │   7.06    │   8.96    │
 Up to 10.0 KG   │   6.82     │   7.79    │   9.98    │
 Up to 20.0 KG   │   9.98     │  11.03    │  13.97    │  [x]
 Up to 31.5 KG   │  13.05     │  14.26    │  17.38    │  [x]
─────────────────┴────────────┴───────────┴───────────┴───
                  [+ Add Weight Range]
```

Note: The `[x]` delete buttons appear on hover for weight range rows. The `+` column header adds a new zone to the service.

### Problems

1. **No weight dimension in UI**: The current grid has no concept of weight brackets, making it impossible to enter carrier rate cards that vary by weight.
2. **Flat rate assumption**: The frontend always sends `min_weight=0, max_weight=0`, wasting the backend's existing weight bracket support.
3. **Missing granular CRUD**: No mutation to create/delete a single service rate entry. The only option is batch update, which requires the frontend to track all dirty state.
4. **No weight range management**: No operation to add/remove a weight range across all services and zones atomically.
5. **Single view limitation**: No per-service detail view for focused editing of a single service's rates across weight brackets and zones. (**Resolved** in v1.2 with service-tab approach.)

---

## Goals & Success Criteria

### Goals

1. Users can define rate grids matching real carrier rate cards (weight x zone x service)
2. Weight ranges are shared across all services with consistent bracket boundaries
3. Both overview and per-service views support inline cell editing with autosave
4. Individual cells can be created, updated, and deleted via granular GraphQL mutations

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Rate grid supports weight bracket rows | Weight brackets derived from service_rates | Must-have |
| Service-tab navigation with per-service grid | Each tab shows weight x zone grid for one service | Must-have |
| Auto-select first service on load | First service selected automatically when services change | Must-have |
| Add/remove weight range operations work | Creates/removes service_rate entries across all service-zone combos | Must-have |
| Granular single-rate CRUD mutations | Create, update, delete individual service_rate entries | Must-have |
| Existing flat-rate rate sheets load correctly | Backward compatible with min_weight=0, max_weight=0 entries | Must-have |
| Inline cell editing with autosave | Changes persisted via individual mutations on blur/enter | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [x] Weight bracket grid rendering (service-tab per-service view)
- [x] Add/remove weight range UI + backend mutations
- [x] Granular service rate CRUD mutations (add, update, delete)
- [x] Backward compatibility with existing rate sheets (no weight brackets = single flat row fallback)
- [x] Admin + base GraphQL schema parity (18 mutations each, verified 2026-02-04)
- [x] JTL Shipping App grid implementation (`apps/shipping-app/`)
- [x] Karrio Dashboard grid implementation (`karrio/packages/ui/components/`)
- [x] Karrio Admin hooks + integration (`karrio/packages/hooks/admin-rate-sheets.ts`)
- [x] Preset Popover dropdowns on all tabs (carrier defaults + clone + create new)
- [x] Per-cell rate deletion (explicit Trash2 icon on hover, safe blur behavior)
- [x] Cross-surface parity: JTL Shipping App matches Karrio UI feature set
- [x] 2-tab layout with inline service/zone/weight CRUD (JTL Shipping App, v1.4)
- [x] Per-service weight range scoping in create mode (v1.4)
- [x] Modal layering: dialogs layer above Sheet without dismissing it (v1.4)
- [x] Carrier gate: disabled overlay in create mode when no carrier selected (v1.4)
- [x] Surcharge "Select All" for service linking (v1.4)
- [x] Backend weight range overlap validation (`sheet.py:add_weight_range()` — input + overlap checks)
- [x] Karrio Dashboard parity with v1.4 JTL restructuring (2-tab layout, inline CRUD, staged pattern, new components)
- [ ] Unit + integration tests for backend model methods and GraphQL mutations

**Nice-to-have (P1):**
- [x] Inline autosave (mutation on cell blur/Enter) instead of batch save
- [x] Clone functionality for services, zones, surcharges
- [x] Tooltips on zone headers (countries, transit days) and weight labels (rate count, avg)
- [x] CSV preview filters empty/zero-rate rows
- [ ] Weight range reordering/sorting controls
- [ ] Keyboard navigation between grid cells (Tab, Arrow keys)
- [ ] Empty cell placeholder with click-to-create behavior

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| A) First-class `weight_brackets` JSONField on RateSheet | Explicit labels, ordering, IDs for brackets | Extra field, sync burden between brackets and service_rates, migration needed | **Rejected** |
| B) Implicit brackets from service_rates (min_weight, max_weight) | No schema change, derives brackets from data, simpler model | No explicit label/ordering field, labels computed from max_weight | **Selected** |
| C) Per-service weight ranges | Each service defines own brackets independently | Inconsistent grid rows across services, more complex UI | **Rejected** |

### Trade-off Analysis

Option B was selected because:
- The existing `service_rates` JSONField already supports `min_weight`/`max_weight` per entry
- Weight bracket labels are easily derived: `"Up to {max_weight} {weight_unit}"`
- Ordering is determined by sorting `max_weight` ascending
- No database migration required - the field structure is unchanged
- The "fully shared" constraint ensures all services have the same set of weight rows, so deriving brackets from any service's rates is consistent

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.

### Existing Code Analysis

#### Backend (shared across all frontends)

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| RateSheet model with service_rates | `karrio/modules/core/karrio/server/providers/models/sheet.py` | Extend with weight range helper methods |
| `_make_rate_key()` composite key | `sheet.py:244` | Already uses `service_id:zone_id:min_weight:max_weight` - reuse as-is |
| `batch_update_service_rates()` | `sheet.py:307` | Reuse for bulk weight range operations |
| `remove_service_rate()` | `sheet.py:338` | Reuse for individual rate deletion |
| `update_service_rate()` | `sheet.py:270` | Reuse for individual rate upsert |
| GraphQL ServiceRateType | `schemas/base/types.py` | Already exposes min_weight, max_weight - no change |
| GraphQL ServiceRateInput | `schemas/base/inputs.py` | Already accepts min_weight, max_weight - no change |
| BatchUpdateServiceRatesMutation | `schemas/base/mutations.py:856` | Reuse for bulk rate updates |
| UpdateServiceRateMutation | `schemas/base/mutations.py:822` | Reuse for single rate updates |

#### Frontend Surface 1: JTL Shipping App (`apps/shipping-app/`)

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| RateSheetEditor (1873 lines) | `apps/shipping-app/src/modules/shipping/components/RateSheetEditor.tsx` | Update to integrate new weight-bracket grid + per-service tabs |
| RateSheetTable (367 lines) | `apps/shipping-app/src/modules/shipping/components/RateSheetTable.tsx` | Replace with `WeightRateGrid` (weight-row layout) |
| ZonesTab, ServicesTab, SurchargesTab | `apps/shipping-app/src/modules/shipping/components/` | Keep as-is (unchanged tabs) |
| ServiceEditorDialog | `apps/shipping-app/src/modules/shipping/components/ServiceEditorDialog.tsx` | Keep as-is |
| EmbeddedZone type | `apps/shipping-app/src/modules/shipping/types/rate-sheet-types.ts` | Extend with `WeightRange`, `RateCellKey`, `RateLookupMap` |
| useRateSheetMutations hook | `apps/shipping-app/src/modules/shipping/hooks/useRateSheets.ts` | Add weight range + delete rate mutations |
| RateSheetService | `apps/shipping-app/src/modules/shipping/services/rate-sheet-service.ts` | Add GraphQL operations for new mutations |
| UI library | shadcn/ui, Radix primitives | Consistent with existing app patterns |

#### Frontend Surface 2: Karrio Dashboard (`karrio/packages/`)

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| rate-sheet-editor (1663 lines) | `karrio/packages/ui/components/rate-sheet-editor.tsx` | Update to integrate new weight-bracket grid + per-service tabs |
| rate-sheet-table (426 lines) | `karrio/packages/ui/components/rate-sheet-table.tsx` | Replace with weight-row layout grid |
| rate-sheet-dialog | `karrio/packages/ui/components/rate-sheet-dialog.tsx` | Keep as-is (link dialog) |
| RateSheetModalEditor | `karrio/packages/ui/core/modals/rate-sheet-editor.tsx` | Update modal wrapper to support new grid |
| rate-sheet-edit-modal | `karrio/packages/ui/core/modals/rate-sheet-edit-modal.tsx` | Update to support new grid |
| rate-sheet-list | `karrio/packages/ui/core/forms/rate-sheet-list.tsx` | Keep as-is (list view) |
| useRateSheetMutation hook | `karrio/packages/hooks/rate-sheet.ts` | Add weight range + delete rate mutations |
| Connections rate-sheets | `karrio/packages/core/modules/Connections/rate-sheets.tsx` | Update integration point if needed |
| UI library | Radix UI + custom styling | Consistent with existing Karrio patterns |

#### Frontend Surface 3: Karrio Admin (`karrio/packages/admin/`)

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| rate-sheets-table | `karrio/packages/admin/components/rate-sheets-table.tsx` | Update if it embeds rate editing |
| useRateSheetMutation (admin) | `karrio/packages/hooks/admin-rate-sheets.ts` | Add weight range + delete rate mutations (admin endpoints) |
| Admin GraphQL schema | `karrio/modules/graph/karrio/server/graph/schemas/admin/` | Mirror all base schema changes |

#### Cross-Surface Notes

| Aspect | JTL Shipping App | Karrio Dashboard | Karrio Admin |
|--------|-----------------|------------------|--------------|
| Editor type | Sheet (right sidebar) | Modal-based | Modal + table |
| UI framework | shadcn/ui | Radix + custom | Radix + custom |
| API client | Custom `executeGraphQLQuery` | `@karrio` GraphQL client | `@karrio` admin client |
| State management | React Query | React Query | React Query |
| Code sharing | Independent | Shared `karrio/packages` | Shared `karrio/packages` |
| Hooks file | `useRateSheets.ts` | `rate-sheet.ts` | `admin-rate-sheets.ts` |

> **Important**: The Karrio Dashboard and Admin share the same `karrio/packages/ui/components/` and `karrio/packages/hooks/` code. Changes there propagate to both. The JTL Shipping App is independent and must be updated separately.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          FRONTEND SURFACES                               │
├────────────────────┬───────────────────────┬────────────────────────────┤
│                    │                       │                             │
│  JTL Shipping App  │   Karrio Dashboard    │     Karrio Admin            │
│  (apps/shipping-   │  (karrio/packages/    │  (karrio/packages/          │
│   app/src/)        │   ui/components/)     │   admin/components/)        │
│                    │                       │                             │
│  ┌──────────────┐  │  ┌──────────────┐    │  ┌──────────────┐          │
│  │RateSheetEdit │  │  │rate-sheet-   │    │  │rate-sheets-  │          │
│  │or.tsx        │  │  │editor.tsx    │    │  │table.tsx     │          │
│  │  + WeightRate│  │  │  + WeightRate│    │  │  (admin view)│          │
│  │    Grid (new)│  │  │    Grid (new)│    │  └──────┬───────┘          │
│  └──────┬───────┘  │  └──────┬───────┘    │         │                   │
│         │          │         │             │         │                   │
│  ┌──────▼───────┐  │  ┌──────▼───────┐    │  ┌──────▼───────┐          │
│  │useRateSheet  │  │  │rate-sheet.ts │    │  │admin-rate-   │          │
│  │Mutations.ts  │  │  │(hooks)       │    │  │sheets.ts     │          │
│  │(hooks)       │  │  │              │    │  │(admin hooks)  │          │
│  └──────┬───────┘  │  └──────┬───────┘    │  └──────┬───────┘          │
│         │          │         │             │         │                   │
├─────────┼──────────┴─────────┼─────────────┴─────────┼──────────────────┤
│         └────────────────────┼───────────────────────┘                   │
│                              ▼                                           │
│                   GraphQL API (base + admin)                             │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Mutations (18 total, base + admin parity):                        │   │
│  │  - CreateRateSheet / UpdateRateSheet / DeleteRateSheet            │   │
│  │  - DeleteService                                                   │   │
│  │  - AddZone / UpdateZone / DeleteZone                              │   │
│  │  - AddSurcharge / UpdateSurcharge / DeleteSurcharge / BatchSurch  │   │
│  │  - UpdateServiceRate / BatchUpdateServiceRates / DeleteServiceRate│   │
│  │  - AddWeightRange / RemoveWeightRange                             │   │
│  │  - UpdateServiceZoneIds / UpdateServiceSurchargeIds               │   │
│  │                                                                    │   │
│  │  Query (unchanged):                                               │   │
│  │  - ServiceRateType already has min_weight/max_weight fields       │   │
│  │  - Weight ranges derived client-side via deriveWeightRanges()     │   │
│  └──────────────────────────────┬───────────────────────────────────┘   │
│                                  ▼                                       │
│                       Django Model (sheet.py)                            │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  NEW: get_weight_ranges(), add_weight_range(), remove_weight_    │   │
│  │       range()                                                     │   │
│  │  EXISTING: update_service_rate(), remove_service_rate(),          │   │
│  │            batch_update_service_rates()                            │   │
│  │                                                                    │   │
│  │  service_rates JSONField (unchanged):                              │   │
│  │  [{ service_id, zone_id, rate, min_weight, max_weight }]          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Sequence Diagram: Add Weight Range

```
┌────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────┐
│  User  │     │ Frontend │     │  GraphQL API │     │  Model   │
└───┬────┘     └────┬─────┘     └──────┬───────┘     └────┬─────┘
    │               │                   │                   │
    │ Click "+Add   │                   │                   │
    │ Weight Range" │                   │                   │
    │──────────────>│                   │                   │
    │               │                   │                   │
    │               │ Enter max_weight  │                   │
    │<──────────────│ (e.g., 5.0)       │                   │
    │               │                   │                   │
    │ Confirm       │                   │                   │
    │──────────────>│                   │                   │
    │               │                   │                   │
    │               │ addWeightRange    │                   │
    │               │ mutation          │                   │
    │               │──────────────────>│                   │
    │               │                   │                   │
    │               │                   │ add_weight_range  │
    │               │                   │ (0, 5.0)          │
    │               │                   │──────────────────>│
    │               │                   │                   │
    │               │                   │  For each         │
    │               │                   │  (service, zone): │
    │               │                   │  create entry     │
    │               │                   │  with rate=0      │
    │               │                   │<──────────────────│
    │               │                   │                   │
    │               │ Updated rate_sheet │                   │
    │               │ with new rows     │                   │
    │               │<──────────────────│                   │
    │               │                   │                   │
    │ Grid shows    │                   │                   │
    │ new row       │                   │                   │
    │<──────────────│                   │                   │
    │               │                   │                   │
```

### Sequence Diagram: Inline Cell Edit

```
┌────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────┐
│  User  │     │ Frontend │     │  GraphQL API │     │  Model   │
└───┬────┘     └────┬─────┘     └──────┬───────┘     └────┬─────┘
    │               │                   │                   │
    │ Click cell    │                   │                   │
    │ (5kg/Zone DE/ │                   │                   │
    │  DPD Classic) │                   │                   │
    │──────────────>│                   │                   │
    │               │                   │                   │
    │ Type "5.89"   │                   │                   │
    │──────────────>│                   │                   │
    │               │                   │                   │
    │ Press Enter   │                   │                   │
    │ or blur       │                   │                   │
    │──────────────>│                   │                   │
    │               │                   │                   │
    │               │ updateServiceRate │                   │
    │               │ mutation {        │                   │
    │               │  service_id,      │                   │
    │               │  zone_id,         │                   │
    │               │  rate: 5.89,      │                   │
    │               │  min_weight: 3.0, │                   │
    │               │  max_weight: 5.0  │                   │
    │               │ }                 │                   │
    │               │──────────────────>│                   │
    │               │                   │ update_service_   │
    │               │                   │ rate()            │
    │               │                   │──────────────────>│
    │               │                   │                   │
    │               │                   │ Upsert by         │
    │               │                   │ composite key     │
    │               │                   │<──────────────────│
    │               │                   │                   │
    │               │ Success           │                   │
    │               │<──────────────────│                   │
    │               │                   │                   │
    │ Cell updated  │                   │                   │
    │<──────────────│                   │                   │
    │               │                   │                   │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      DATA MODEL (Unchanged)                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  RateSheet.service_rates (JSONField):                             │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ service_id  │ zone_id │ min_wt │ max_wt │ rate  │ cost  │    │
│  ├─────────────┼─────────┼────────┼────────┼───────┼───────┤    │
│  │ svc_classic │ zone_de │  0     │  3.0   │  5.35 │ null  │    │
│  │ svc_classic │ zone_de │  3.0   │  5.0   │  5.89 │ null  │    │
│  │ svc_classic │ zone_de │  5.0   │ 10.0   │  6.82 │ null  │    │
│  │ svc_classic │ zone_eu │  0     │  3.0   │  6.43 │ null  │    │
│  │ svc_classic │ zone_eu │  3.0   │  5.0   │  7.06 │ null  │    │
│  │ svc_express │ zone_de │  0     │  3.0   │  8.13 │ null  │    │
│  │ svc_express │ zone_de │  3.0   │  5.0   │  8.96 │ null  │    │
│  │ ...         │ ...     │  ...   │  ...   │  ...  │ ...   │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                      DERIVED WEIGHT RANGES                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  get_weight_ranges() →                                            │
│  ┌───────────┬───────────┬──────────────────┐                    │
│  │ min_weight│ max_weight│ label            │                    │
│  ├───────────┼───────────┼──────────────────┤                    │
│  │    0      │    3.0    │ "Up to 3.0 kg"   │                    │
│  │    3.0    │    5.0    │ "Up to 5.0 kg"   │                    │
│  │    5.0    │   10.0    │ "Up to 10.0 kg"  │                    │
│  └───────────┴───────────┴──────────────────┘                    │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                   FRONTEND GRID STRUCTURE                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Service Tab Grid (ServiceRateDetailView):                        │
│  Navigation = service tabs (auto-select first service)            │
│  Rows = weight_ranges (derived CLIENT-SIDE, sorted by max_weight) │
│  Columns = zones assigned to selected service (via zone_ids)      │
│  Cell value = service_rates.find(svc, zone, min_wt, max_wt).rate │
│  Optional: + column for adding zones, row delete for weight ranges│
│  Optional: toolbar below grid for adding weight ranges            │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Data Models

#### Backend: New Model Methods (sheet.py)

```python
# karrio/modules/core/karrio/server/providers/models/sheet.py

def get_weight_ranges(self) -> list:
    """Derive unique weight ranges from service_rates, sorted by max_weight."""
    seen = {}
    for rate in self.service_rates or []:
        min_wt = rate.get("min_weight", 0) or 0
        max_wt = rate.get("max_weight", 0) or 0
        key = (min_wt, max_wt)
        if key not in seen and key != (0, 0):
            seen[key] = {
                "min_weight": min_wt,
                "max_weight": max_wt,
            }
    return sorted(seen.values(), key=lambda r: r["max_weight"])

def add_weight_range(self, min_weight: float, max_weight: float):
    """Add a new weight range by creating service_rate entries for all service-zone combos."""
    service_rates = list(self.service_rates or [])
    existing_keys = {self._make_rate_key(r) for r in service_rates}

    for service in self.services.all():
        for zone_id in service.zone_ids or []:
            new_rate = {
                "service_id": service.id,
                "zone_id": zone_id,
                "rate": 0,
                "min_weight": min_weight,
                "max_weight": max_weight,
            }
            key = self._make_rate_key(new_rate)
            if key not in existing_keys:
                service_rates.append(new_rate)
                existing_keys.add(key)

    self.service_rates = service_rates
    self.save(update_fields=["service_rates"])

def remove_weight_range(self, min_weight: float, max_weight: float):
    """Remove all service_rate entries matching the given weight range."""
    self.service_rates = [
        sr for sr in (self.service_rates or [])
        if not (
            (sr.get("min_weight", 0) or 0) == min_weight
            and (sr.get("max_weight", 0) or 0) == max_weight
        )
    ]
    self.save(update_fields=["service_rates"])
```

#### Backend: GraphQL Types (types.py) — No Changes Needed

> **Decision D5 applies here.** Weight ranges are **not** exposed as a separate GraphQL type or query field. The existing `ServiceRateType` already includes `min_weight` and `max_weight` fields. Frontends derive unique weight brackets client-side from the `service_rates` array using `deriveWeightRanges()` helpers. The backend `get_weight_ranges()` model method is used only internally by `add_weight_range()` and `remove_weight_range()` operations — it is not exposed via GraphQL.

```python
# EXISTING — no changes needed
@strawberry.type
class ServiceRateType:
    service_id: str
    zone_id: str
    rate: float
    cost: typing.Optional[float] = None
    min_weight: typing.Optional[float] = None   # ← weight bracket data
    max_weight: typing.Optional[float] = None   # ← weight bracket data
    transit_days: typing.Optional[int] = None
    transit_time: typing.Optional[float] = None
```

#### Backend: New GraphQL Inputs (inputs.py)

```python
@strawberry.input
class AddWeightRangeMutationInput:
    rate_sheet_id: str
    min_weight: float
    max_weight: float

@strawberry.input
class RemoveWeightRangeMutationInput:
    rate_sheet_id: str
    min_weight: float
    max_weight: float

@strawberry.input
class DeleteServiceRateMutationInput:
    rate_sheet_id: str
    service_id: str
    zone_id: str
    min_weight: typing.Optional[float] = strawberry.UNSET
    max_weight: typing.Optional[float] = strawberry.UNSET
```

#### Backend: New GraphQL Mutations (mutations.py)

```python
@strawberry.type
class AddWeightRangeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.AddWeightRangeMutationInput
    ) -> "AddWeightRangeMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )

        try:
            rate_sheet.add_weight_range(
                min_weight=input["min_weight"],
                max_weight=input["max_weight"],
            )
        except ValueError as e:
            raise exceptions.ValidationError({"weight_range": str(e)})

        return AddWeightRangeMutation(rate_sheet=rate_sheet)


@strawberry.type
class RemoveWeightRangeMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.RemoveWeightRangeMutationInput
    ) -> "RemoveWeightRangeMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )

        try:
            rate_sheet.remove_weight_range(
                min_weight=input["min_weight"],
                max_weight=input["max_weight"],
            )
        except ValueError as e:
            raise exceptions.ValidationError({"weight_range": str(e)})

        return RemoveWeightRangeMutation(rate_sheet=rate_sheet)


@strawberry.type
class DeleteServiceRateMutation(utils.BaseMutation):
    rate_sheet: typing.Optional[types.RateSheetType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.DeleteServiceRateMutationInput
    ) -> "DeleteServiceRateMutation":
        rate_sheet = providers.RateSheet.access_by(info.context.request).get(
            id=input["rate_sheet_id"]
        )

        min_weight = input.get("min_weight")
        max_weight = input.get("max_weight")
        min_wt = None if utils.is_unset(min_weight) else min_weight
        max_wt = None if utils.is_unset(max_weight) else max_weight

        rate_sheet.remove_service_rate(
            service_id=input["service_id"],
            zone_id=input["zone_id"],
            min_weight=min_wt,
            max_weight=max_wt,
        )

        return DeleteServiceRateMutation(rate_sheet=rate_sheet)
```

#### Frontend: Updated Types (rate-sheet-types.ts)

```typescript
/**
 * Derived weight range (from service_rates)
 */
export interface WeightRange {
  min_weight: number;
  max_weight: number;
}

/**
 * Rate cell lookup key
 */
export type RateCellKey = `${string}:${string}:${number}:${number}`;
// Format: "service_id:zone_id:min_weight:max_weight"

/**
 * Rate cell value in the grid
 */
export interface RateCellValue {
  rate: number;
  cost?: number | null;
  transit_days?: number | null;
  transit_time?: number | null;
}

/**
 * Indexed rate lookup map for O(1) cell access
 */
export type RateLookupMap = Map<RateCellKey, RateCellValue>;
```

#### Frontend: Grid Data Derivation

```typescript
/**
 * Build lookup structures from raw rate sheet data.
 * Called once when rate sheet data loads or updates.
 */
function buildGridData(rateSheet: RateSheetData) {
  // 1. Derive weight ranges from service_rates
  const weightRangeSet = new Map<string, WeightRange>();
  for (const sr of rateSheet.service_rates ?? []) {
    const minW = sr.min_weight ?? 0;
    const maxW = sr.max_weight ?? 0;
    const key = `${minW}:${maxW}`;
    if (key !== "0:0" && !weightRangeSet.has(key)) {
      weightRangeSet.set(key, { min_weight: minW, max_weight: maxW });
    }
  }
  const weightRanges = [...weightRangeSet.values()]
    .sort((a, b) => a.max_weight - b.max_weight);

  // 2. Build rate cell lookup map
  const rateLookup: RateLookupMap = new Map();
  for (const sr of rateSheet.service_rates ?? []) {
    const key: RateCellKey =
      `${sr.service_id}:${sr.zone_id}:${sr.min_weight ?? 0}:${sr.max_weight ?? 0}`;
    rateLookup.set(key, {
      rate: sr.rate,
      cost: sr.cost,
      transit_days: sr.transit_days,
      transit_time: sr.transit_time,
    });
  }

  return { weightRanges, rateLookup };
}
```

### API Changes

**New Mutations (base + admin):**

| Mutation | Input | Description |
|----------|-------|-------------|
| `addWeightRange` | `{ rate_sheet_id, min_weight, max_weight }` | Creates service_rate entries for all service-zone combos at this weight range |
| `removeWeightRange` | `{ rate_sheet_id, min_weight, max_weight }` | Removes all service_rate entries matching this weight range |
| `deleteServiceRate` | `{ rate_sheet_id, service_id, zone_id, min_weight?, max_weight? }` | Deletes a single service_rate entry |

**Existing Mutations (unchanged, but now used with weight data):**

| Mutation | Change |
|----------|--------|
| `updateServiceRate` | Frontend now populates `min_weight` and `max_weight` fields |
| `batchUpdateServiceRates` | Frontend now includes weight bracket data in batch payloads |

**No New Query Fields:**

> Weight ranges are derived client-side from `ServiceRateType.min_weight` / `max_weight` (Decision D5). No `WeightRangeType` or `weight_ranges` query field is needed. See "Frontend: Grid Data Derivation" section for the `deriveWeightRanges()` implementation.

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Rate sheet with no service_rates | `weight_ranges` returns empty list | Grid shows empty state: "Add a weight range to start configuring rates" |
| Legacy rate sheet with all min_weight=0, max_weight=0 | `get_weight_ranges()` filters out (0,0) entries | Grid shows flat view (no weight dimension); user can add weight ranges to upgrade |
| Adding weight range when no services exist | `add_weight_range()` creates no entries (no service-zone combos) | UI shows warning: "Add services and zones before adding weight ranges" |
| Adding weight range when service has no zone_ids | No entries created for that service | Service column group shows no cells for this weight range |
| Removing a weight range with rates entered | All service_rates for that weight range deleted | Confirm dialog warns: "This will delete X rate entries" |
| Adding a zone to a service after weight ranges exist | Zone column appears but cells empty for all weight brackets | User fills in rates manually (or batch update) |
| Overlapping weight ranges (e.g., 0-5 and 3-10) | Rejected by validation | Frontend validates: new max_weight must be > largest existing max_weight (append-only ordering) |
| Very large grid (20 services x 10 zones x 15 weight brackets = 3000 cells) | Grid remains responsive | Virtual scrolling for both rows and columns |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Concurrent edits to same rate sheet | Last write wins, data loss | Optimistic UI with conflict detection (compare timestamps) |
| `add_weight_range` creates large batch of empty entries | Performance impact on save | Batch insert in single `save()` call, not per-entry |
| Frontend sends stale min_weight/max_weight in mutation | Wrong rate entry updated/created | Use composite key `_make_rate_key()` for deterministic matching |
| GraphQL response too large (many service_rates) | Slow page load | Paginate service_rates or lazy-load per-service on tab switch |

### Security Considerations

- [x] Authorization: rate sheet access via `access_by(request)` (existing pattern) — all 3 new mutations use it
- [x] No secrets in rate data
- [x] All mutations wrapped in `@transaction.atomic`
- [x] Input validation: min_weight >= 0, max_weight > min_weight (frontend + backend)
- [ ] Rate values validated as non-negative floats (backend missing)

---

## Implementation Plan

### Phase 1: Backend - Model Methods + GraphQL

> **Note:** `WeightRangeType` and `weight_ranges` resolver are intentionally omitted (Decision D5). Weight ranges are derived client-side from `ServiceRateType.min_weight/max_weight`. The backend `get_weight_ranges()` is used only internally by `add/remove_weight_range()`.

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `get_weight_ranges()` method to RateSheet | `karrio/modules/core/karrio/server/providers/models/sheet.py` | **Done** | S |
| Add `add_weight_range()` method to RateSheet | `sheet.py` | **Done** | S |
| Add `remove_weight_range()` method to RateSheet | `sheet.py` | **Done** | S |
| Add `AddWeightRangeMutationInput` | `karrio/modules/graph/karrio/server/graph/schemas/base/inputs.py` | **Done** | S |
| Add `RemoveWeightRangeMutationInput` | `inputs.py` | **Done** | S |
| Add `DeleteServiceRateMutationInput` | `inputs.py` | **Done** | S |
| Add `AddWeightRangeMutation` | `karrio/modules/graph/karrio/server/graph/schemas/base/mutations.py` | **Done** | S |
| Add `RemoveWeightRangeMutation` | `mutations.py` | **Done** | S |
| Add `DeleteServiceRateMutation` | `mutations.py` | **Done** | S |
| Register new mutations in schema root | `karrio/modules/graph/karrio/server/graph/schemas/base/schema.py` | **Done** | S |
| Mirror mutations in admin GraphQL schema | `karrio-insiders/modules/admin/karrio/server/admin/schemas/base/__init__.py` | **Done** (3 missing mutations added: `DeleteServiceRate`, `AddWeightRange`, `RemoveWeightRange`) | S |

### Phase 2: Frontend - JTL Shipping App Grid Refactor

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add new TypeScript types (`WeightRange`, `RateCellKey`, `RateLookupMap`) | `apps/shipping-app/src/modules/shipping/types/rate-sheet-types.ts` | **Done** | S |
| Add GraphQL queries/mutations for weight range operations | `apps/shipping-app/src/modules/shipping/hooks/useRateSheets.ts` | **Done** | M |
| Add GraphQL operations to service layer | `apps/shipping-app/src/modules/shipping/services/rate-sheet-service.ts` | **Done** | M |
| Build `WeightRateGrid` component (overview grid — replaced by service tabs in v1.2) | `apps/shipping-app/src/modules/shipping/components/WeightRateGrid.tsx` (new) | **Done** (utilities still used) | L |
| Build `ServiceRateDetailView` component (primary per-service grid) | `apps/shipping-app/src/modules/shipping/components/ServiceRateDetailView.tsx` (new) | **Done** | L |
| Add "Add Weight Range" dialog/popover | `apps/shipping-app/src/modules/shipping/components/AddWeightRangeDialog.tsx` (new) | **Done** | S |
| Update `RateSheetEditor` to integrate new grid + per-service tabs | `apps/shipping-app/src/modules/shipping/components/RateSheetEditor.tsx` | **Done** | M |
| Restructure editor: 5 tabs → 2 tabs, inline CRUD (v1.4) | `RateSheetEditor.tsx` | **Done** | L |
| Create `tooltip.tsx` (`@floating-ui/react`) | `apps/shipping-app/src/components/ui/tooltip.tsx` (new) | **Done** | S |
| Create `AddServicePopover.tsx` | `apps/shipping-app/src/modules/shipping/components/AddServicePopover.tsx` (new) | **Done** | S |
| Create `AddWeightRangePopover.tsx` | `apps/shipping-app/src/modules/shipping/components/AddWeightRangePopover.tsx` (new) | **Done** | S |
| Create `EditWeightRangeDialog.tsx` | `apps/shipping-app/src/modules/shipping/components/EditWeightRangeDialog.tsx` (new) | **Done** | S |
| Update `RateSheetTable` or deprecate in favor of `WeightRateGrid` | `apps/shipping-app/src/modules/shipping/components/RateSheetTable.tsx` | **Done** | M |
| Wire inline cell editing to granular `updateServiceRate` mutation | `WeightRateGrid.tsx`, `ServiceRateDetailView.tsx` | **Done** | M |
| Wire "Add Weight Range" / "Remove Weight Range" to mutations | `AddWeightRangeDialog.tsx`, grid components | **Done** | S |
| Update generated GraphQL TypeScript types | `apps/shipping-app/src/types/graphql/types.ts` (codegen) | **Done** | S |

**Dependencies:** Phase 2 depends on Phase 1 completion (GraphQL schema must be available).

### Phase 3: Frontend - Karrio Dashboard + Admin Grid Refactor

> The Karrio Dashboard and Admin share `karrio/packages/ui/` and `karrio/packages/hooks/`. Changes propagate to both surfaces.

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add weight range + delete rate mutations to dashboard hooks | `karrio/packages/hooks/rate-sheet.ts` | **Done** | M |
| Add weight range + delete rate mutations to admin hooks | `karrio/packages/hooks/admin-rate-sheets.ts` | **Done** | M |
| Build `WeightRateGrid` component for Karrio UI (replaced by service tabs in v1.2) | `karrio/packages/ui/components/weight-rate-grid.tsx` (new) | **Done** (utilities still used) | L |
| Build `ServiceRateDetailView` component for Karrio UI (primary per-service grid) | `karrio/packages/ui/components/service-rate-detail-view.tsx` (new) | **Done** | L |
| Add "Add Weight Range" dialog for Karrio UI | `karrio/packages/ui/components/add-weight-range-dialog.tsx` (new) | **Done** | S |
| Update `rate-sheet-editor.tsx` to integrate new grid + per-service tabs | `karrio/packages/ui/components/rate-sheet-editor.tsx` | **Done** | M |
| Update `rate-sheet-table.tsx` or deprecate in favor of weight grid | `karrio/packages/ui/components/rate-sheet-table.tsx` | **Done** | M |
| Update modal editor to support new grid | `karrio/packages/ui/core/modals/rate-sheet-editor.tsx` | **Done** | M |
| Update `rate-sheet-edit-modal.tsx` | `karrio/packages/ui/core/modals/rate-sheet-edit-modal.tsx` | **Done** | M |
| Update admin rate sheets table if it embeds editing | `karrio/packages/admin/components/rate-sheets-table.tsx` | **Done** | S |
| Update Connections integration point | `karrio/packages/core/modules/Connections/rate-sheets.tsx` | **Done** | S |
| Wire inline cell editing to granular mutations (Karrio) | `weight-rate-grid.tsx`, `service-rate-detail-view.tsx` | **Done** | M |

**Dependencies:** Phase 3 depends on Phase 1. Can run in parallel with Phase 2 (different codebase surfaces).

### Phase 4: Polish + Backward Compatibility (all surfaces)

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Handle legacy rate sheets (no weight brackets) gracefully | All grid components (both apps) | **Done** — flat row `[{min_weight: 0, max_weight: 0}]` fallback | S |
| Add empty state UI for no weight ranges / no services | All grid components (both apps) | **Done** — empty states in `WeightRateGrid`, `WeightRangesTab`, `ServiceRateDetailView` | S |
| Add weight range overlap validation (frontend) | `AddWeightRangeDialog` (both apps) | **Done** — overlap prevention + positive value checks in dialog | S |
| Add weight range overlap validation (backend) | `sheet.py:add_weight_range()` | **Done** — input validation (min >= 0, max > min) + overlap detection against existing ranges | S |
| Virtual scrolling for large grids | `WeightRateGrid` (both apps) | **Done** — `@tanstack/react-virtual` `useVirtualizer` | M |
| Preset Popover dropdowns on all tabs (Karrio UI) | `karrio/packages/ui/components/{zones,surcharges,weight-ranges,services}-tab.tsx` | **Done** | M |
| Preset Popover dropdowns on all tabs (JTL Shipping App) | `apps/shipping-app/src/modules/shipping/components/{Zones,Surcharges,WeightRanges,Services}Tab.tsx` | **Done** | M |
| Clone functionality (service, zone, surcharge) | `rate-sheet-editor.tsx` (both apps) | **Done** | M |
| Per-cell rate deletion (Karrio UI) | `karrio/packages/ui/components/service-rate-detail-view.tsx` | **Done** | S |
| Per-cell rate deletion (JTL Shipping App) | `apps/shipping-app/src/modules/shipping/components/ServiceRateDetailView.tsx` | **Done** — Trash2 icon, safe blur (v1.4) | S |
| Cross-surface parity: JTL Shipping App vs Karrio UI | All tab components, editor, detail view | **Done** (verified 2026-02-04) | M |
| Modal layering: dialogs above Sheet (JTL) | `Modal.tsx`, `ConfirmDialog.tsx`, `RateSheetEditor.tsx` | **Done** — z-[100], stopPropagation, capture ESC (v1.4) | M |
| Condensed tab header + carrier gate (JTL) | `RateSheetEditor.tsx` | **Done** — shadcn-style tabs, disabled overlay (v1.4) | S |
| Surcharge "Select All" for services (JTL) | `SurchargeEditorDialog.tsx` | **Done** (v1.4) | S |
| Per-service weight range scoping (JTL create mode) | `RateSheetEditor.tsx` | **Done** — add/remove per-service, global cleanup (v1.4) | M |
| Column width + service tab overflow (JTL) | `ServiceRateDetailView.tsx`, `RateSheetEditor.tsx` | **Done** — 200/140px, hidden scrollbar (v1.4) | S |
| Cross-surface QA: manual functional testing across JTL, Dashboard, Admin | All surfaces | **Pending** | M |

### Phase 5: Testing (backend + frontend)

> No tests have been written yet for any of the new backend methods or GraphQL mutations. This is the primary remaining gap.

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Unit tests for `get_weight_ranges()` | `karrio/modules/core/karrio/server/providers/tests/` | **Pending** | S |
| Unit tests for `add_weight_range()` | `karrio/modules/core/karrio/server/providers/tests/` | **Pending** | S |
| Unit tests for `remove_weight_range()` | `karrio/modules/core/karrio/server/providers/tests/` | **Pending** | S |
| Integration tests for `AddWeightRangeMutation` | `karrio/modules/graph/karrio/server/graph/tests/` | **Pending** | M |
| Integration tests for `RemoveWeightRangeMutation` | `karrio/modules/graph/karrio/server/graph/tests/` | **Pending** | M |
| Integration tests for `DeleteServiceRateMutation` | `karrio/modules/graph/karrio/server/graph/tests/` | **Pending** | M |
| Backward compatibility test: load flat-rate sheet, verify grid renders | Manual or E2E | **Pending** | S |
| Large grid performance test (20 services x 10 zones x 15 brackets) | Manual | **Pending** | S |

**Dependencies:** Phase 5 can run in parallel with remaining Phase 4 items.

---

## Testing Strategy

> **CRITICAL**: All tests must follow `AGENTS.md` guidelines exactly.

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests (Model) | `karrio/modules/core/karrio/server/providers/tests/` | 90%+ for new methods |
| Integration Tests (GraphQL) | `karrio/modules/graph/karrio/server/graph/tests/` | All new mutations |
| Frontend Tests (JTL App) | `apps/shipping-app/src/modules/shipping/__tests__/` | Grid rendering + interaction |
| Frontend Tests (Karrio UI) | `karrio/packages/ui/__tests__/` or co-located | Grid rendering + interaction |
| Cross-Surface QA | Manual / E2E | Feature parity across all 3 surfaces |

### Test Cases

#### Unit Tests: Model Methods

```python
"""Tests for RateSheet weight range methods."""

import unittest
from unittest.mock import patch, ANY, MagicMock


class TestRateSheetWeightRanges(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_weight_ranges_empty(self):
        """Verify empty service_rates returns empty weight ranges."""
        rate_sheet = MagicMock()
        rate_sheet.service_rates = []
        # Should return []

    def test_get_weight_ranges_filters_zero_zero(self):
        """Verify (0, 0) entries are excluded from derived weight ranges."""
        rate_sheet = MagicMock()
        rate_sheet.service_rates = [
            {"service_id": "svc_1", "zone_id": "zone_1", "rate": 5.0,
             "min_weight": 0, "max_weight": 0},
        ]
        # Should return []

    def test_get_weight_ranges_deduplicates(self):
        """Verify duplicate weight ranges across services are deduplicated."""
        rate_sheet = MagicMock()
        rate_sheet.service_rates = [
            {"service_id": "svc_1", "zone_id": "zone_1", "rate": 5.0,
             "min_weight": 0, "max_weight": 3.0},
            {"service_id": "svc_1", "zone_id": "zone_2", "rate": 6.0,
             "min_weight": 0, "max_weight": 3.0},
            {"service_id": "svc_1", "zone_id": "zone_1", "rate": 7.0,
             "min_weight": 3.0, "max_weight": 5.0},
        ]
        # Should return [{"min_weight": 0, "max_weight": 3.0}, {"min_weight": 3.0, "max_weight": 5.0}]

    def test_get_weight_ranges_sorted_by_max_weight(self):
        """Verify weight ranges are sorted ascending by max_weight."""
        rate_sheet = MagicMock()
        rate_sheet.service_rates = [
            {"service_id": "svc_1", "zone_id": "zone_1", "rate": 7.0,
             "min_weight": 5.0, "max_weight": 10.0},
            {"service_id": "svc_1", "zone_id": "zone_1", "rate": 5.0,
             "min_weight": 0, "max_weight": 3.0},
        ]
        # Should return sorted by max_weight: [3.0, 10.0]

    def test_add_weight_range_creates_entries(self):
        """Verify add_weight_range creates entries for all service-zone combos."""
        # Setup rate_sheet with 2 services, each with 2 zones
        # Call add_weight_range(0, 5.0)
        # Verify 4 new service_rate entries created (2 services x 2 zones)

    def test_add_weight_range_no_duplicates(self):
        """Verify add_weight_range skips existing service-zone-weight combos."""
        # Setup rate_sheet with existing entry for svc_1/zone_1/0/5.0
        # Call add_weight_range(0, 5.0)
        # Verify only missing combos are created

    def test_remove_weight_range_deletes_entries(self):
        """Verify remove_weight_range removes all entries for that weight range."""
        # Setup rate_sheet with entries at (0, 3.0) and (3.0, 5.0)
        # Call remove_weight_range(0, 3.0)
        # Verify only (3.0, 5.0) entries remain
```

#### Integration Tests: GraphQL Mutations

```python
"""Tests for weight range GraphQL mutations."""

import unittest


class TestWeightRangeMutations(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_add_weight_range_mutation(self):
        """Verify addWeightRange creates rate entries and returns updated sheet."""
        # Create rate sheet with services and zones
        # Call addWeightRange mutation
        # print(response)
        # Assert rate_sheet.weight_ranges includes new range
        # Assert service_rates entries created

    def test_remove_weight_range_mutation(self):
        """Verify removeWeightRange deletes rate entries for that range."""
        # Setup rate sheet with weight ranges
        # Call removeWeightRange mutation
        # print(response)
        # Assert weight_ranges no longer includes removed range

    def test_delete_service_rate_mutation(self):
        """Verify deleteServiceRate removes a single rate entry."""
        # Setup rate sheet with service_rates
        # Call deleteServiceRate with specific service_id, zone_id, min/max weight
        # print(response)
        # Assert specific entry removed, others intact

    def test_weight_ranges_query_field(self):
        """Verify weight_ranges resolver returns derived ranges."""
        # Setup rate sheet with service_rates
        # Query rate_sheet { weight_ranges { min_weight max_weight } }
        # print(response)
        # Assert returns correct sorted, deduplicated ranges
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run model unit tests
python -m unittest discover -v -f karrio/modules/core/karrio/server/providers/tests

# Run GraphQL integration tests
karrio test --failfast karrio.server.graph.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Large service_rates JSONField (1000+ entries) | Slow save/load | Medium | Monitor JSON size; consider pagination for very large sheets |
| Frontend grid performance with many cells | UI lag | Medium | Virtual scrolling with `@tanstack/react-virtual` (already used) |
| Breaking existing rate sheets | Data loss | Low | Backward compatible: (0,0) weight entries still work, grid falls back to flat view |
| Admin/base schema drift | API inconsistency | Low | Mirror all changes in both schemas in same PR. **Resolved**: parity verified at 18 mutations each (2026-02-04) |
| Race condition on concurrent add_weight_range | Duplicate entries | Low | `@transaction.atomic` on mutations + composite key dedup |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: All existing mutations unchanged. New mutations are additive. Existing clients sending `min_weight=0, max_weight=0` continue to work.
- **Data compatibility**: No schema migration needed. Existing `service_rates` entries with `min_weight=0, max_weight=0` are treated as "no weight bracket" and filtered from `get_weight_ranges()`. The grid renders them as a single flat row or shows an empty state prompting the user to add weight ranges.
- **Feature flags**: None required. The new grid is the default for all rate sheets. Legacy rate sheets degrade gracefully.

### Rollback Procedure

1. **Identify issue**: Grid not rendering, mutations failing, or data corruption
2. **Stop rollout**: Revert frontend deployment (grid changes are frontend-only for display)
3. **Revert changes**: Revert backend mutations if data corruption detected. Model methods are additive and don't modify existing behavior.
4. **Verify recovery**: Confirm existing rate sheets load correctly in the old flat grid layout

---

## Appendices

### Appendix A: Weight Range Label Derivation

Weight range labels are computed from `max_weight` and the rate sheet's weight unit:

| min_weight | max_weight | Weight Unit | Display Label |
|------------|------------|-------------|---------------|
| 0 | 3.0 | KG | "Up to 3.0 kg" |
| 3.0 | 5.0 | KG | "Up to 5.0 kg" |
| 5.0 | 10.0 | KG | "Up to 10.0 kg" |
| 0 | 1.0 | LB | "Up to 1.0 lb" |

The weight unit is derived from the first service's `weight_unit` field, or defaults to `"KG"`.

### Appendix B: Rate Card Data Example (from Excel screenshots)

**UPS Standard (Germany):**

| Weight Range | Zone 601 | Zone 603 | Zone 604 | Zone 605 | Zone 606 | Zone 703 |
|-------------|----------|----------|----------|----------|----------|----------|
| 0.5 kg | 4.65 | 8.00 | 11.35 | 10.00 | 14.10 | 14.00 |
| 1 kg | 4.75 | 8.00 | 11.50 | 10.00 | 14.40 | 14.00 |
| 1.5 kg | 4.80 | 8.00 | 11.65 | 10.00 | 14.70 | 14.00 |
| 2 kg | 4.80 | 8.00 | 11.80 | 10.00 | 15.00 | 16.00 |
| 3 kg | 5.50 | 9.15 | 13.70 | 11.00 | 18.40 | 18.00 |
| 4 kg | 6.05 | 9.60 | 14.60 | 12.00 | 19.20 | 18.00 |
| 5 kg | 6.25 | 10.00 | 15.50 | 13.00 | 20.00 | 18.00 |
| 10 kg | 5.75 | 12.00 | 20.00 | 15.00 | 23.00 | 23.00 |
| 15 kg | 10.05 | 15.00 | 21.50 | 20.00 | 29.00 | 27.00 |
| 20 kg | 12.40 | 19.00 | 28.50 | 26.00 | 37.00 | 35.00 |
| 30 kg | 18.00 | 28.00 | 41.00 | 36.00 | 52.00 | 50.00 |

**DPD Classic Parcel (Zone 1):**

| Weight | Zone 1A (AT/BE/LU/NL) | Zone 1B (CH/CZ/DK/LI) | Zone 1C (FR/GB/MC) | Zone 1D (HU/IT/PL/SI/SK) | Zone 1E (ES/IE/PT/SE) |
|--------|------------------------|------------------------|---------------------|--------------------------|------------------------|
| Up to 3.0 kg | 5.35 | 6.43 | 8.13 | 9.74 | 11.20 |
| Up to 5.0 kg | 5.89 | 7.06 | 8.96 | 10.71 | 12.46 |
| Up to 10.0 kg | 6.82 | 7.79 | 9.98 | 11.93 | 13.92 |
| Up to 20.0 kg | 9.98 | 11.03 | 13.97 | 16.31 | 18.45 |
| Up to 31.5 kg | 13.05 | 14.26 | 17.38 | 19.96 | 22.30 |

These examples represent the data structure this feature enables users to configure directly in the Rate Sheet Editor.

### Appendix C: Composite Key Format

Service rate entries are uniquely identified by the composite key:

```
{service_id}:{zone_id}:{min_weight}:{max_weight}
```

Examples:
- `svc_dpd_classic:zone_1a:0:3.0` - DPD Classic, Zone 1A, up to 3.0 kg
- `svc_dpd_classic:zone_1a:3.0:5.0` - DPD Classic, Zone 1A, 3.0-5.0 kg
- `svc_ups_standard:zone_601:0:0.5` - UPS Standard, Zone 601, up to 0.5 kg

This key format is already implemented in `RateSheet._make_rate_key()` at `sheet.py:244`.

### Appendix D: Preset Popover Pattern

All four tabs (Zones, Surcharges, Weight Ranges, Services) share the same three-section Popover dropdown pattern for adding items:

```
┌─────────────────────┐
│ Add zone             │  ← section header
├─────────────────────┤
│ Zone 1               │  ← carrier defaults (from references.ratesheets[carrierName])
│ Zone 2               │     filtered to exclude already-added items
│ Zone 3               │
├─────────────────────┤
│ Clone existing       │  ← label (zones/surcharges/services only; not weight ranges)
│ ↪ Zone A             │     copies item with "(copy)" suffix + new ID
│ ↪ Zone B             │     opens editor dialog after clone
├─────────────────────┤
│ + Create new zone    │  ← always shown; opens editor dialog or custom dialog
└─────────────────────┘
```

**Data sources per tab:**

| Tab | Carrier Presets Source | Clone Source | "Create new" Action |
|-----|----------------------|-------------|---------------------|
| Services | `ratesheets[carrier].services` (filtered by `service_code`) | Existing services | Open service editor dialog |
| Zones | `ratesheets[carrier].zones` (filtered by `label`) | Existing zones | Open zone editor dialog |
| Surcharges | `ratesheets[carrier].surcharges` (filtered by `name`) | Existing surcharges | Open surcharge editor dialog |
| Weight Ranges | `ratesheets[carrier].service_rates` (unique `min/max_weight` pairs) | N/A (no clone) | Open AddWeightRangeDialog |

**Cross-surface implementation:**

| Component | Karrio UI | JTL Shipping App |
|-----------|-----------|-------------------|
| Icons | `@radix-ui/react-icons` (`PlusIcon`, `Cross2Icon`) | `lucide-react` (`Plus`, `X`) |
| Popover | `@karrio/ui/components/ui/popover` | `@/components/ui/popover` |
| References | `references.ratesheets[carrierName]` | `apiReferences.ratesheets[carrierName]` |
| Toast | `toast({ variant })` | `toast.success()` / `toast.error()` |

### Appendix E: Full GraphQL Mutation List (18 mutations)

Both base (`karrio/modules/graph/`) and admin (`karrio-insiders/modules/admin/`) schemas register the same 18 rate sheet mutations:

| # | Mutation | Input Type | Description |
|---|----------|-----------|-------------|
| 1 | `create_rate_sheet` | `CreateRateSheetMutationInput` | Create a new rate sheet |
| 2 | `update_rate_sheet` | `UpdateRateSheetMutationInput` | Update rate sheet metadata |
| 3 | `delete_rate_sheet` | `DeleteMutationInput` | Delete a rate sheet |
| 4 | `delete_service` | `DeleteServiceMutationInput` | Delete a service from rate sheet |
| 5 | `add_zone` | `AddZoneMutationInput` | Add a zone to rate sheet |
| 6 | `update_zone` | `UpdateZoneMutationInput` | Update zone properties |
| 7 | `delete_zone` | `DeleteZoneMutationInput` | Delete a zone from rate sheet |
| 8 | `add_surcharge` | `AddSurchargeMutationInput` | Add a surcharge to rate sheet |
| 9 | `update_surcharge` | `UpdateSurchargeMutationInput` | Update surcharge properties |
| 10 | `delete_surcharge` | `DeleteSurchargeMutationInput` | Delete a surcharge |
| 11 | `batch_update_surcharges` | `BatchUpdateSurchargesMutationInput` | Batch update surcharges |
| 12 | `update_service_rate` | `UpdateServiceRateMutationInput` | Upsert a single service rate |
| 13 | `batch_update_service_rates` | `BatchUpdateServiceRatesMutationInput` | Batch update service rates |
| 14 | `delete_service_rate` | `DeleteServiceRateMutationInput` | Delete a single service rate |
| 15 | `add_weight_range` | `AddWeightRangeMutationInput` | Add weight range (creates entries for all service-zone combos) |
| 16 | `remove_weight_range` | `RemoveWeightRangeMutationInput` | Remove weight range (deletes all matching entries) |
| 17 | `update_service_zone_ids` | `UpdateServiceZoneIdsMutationInput` | Update zone assignments for a service |
| 18 | `update_service_surcharge_ids` | `UpdateServiceSurchargeIdsMutationInput` | Update surcharge assignments for a service |
