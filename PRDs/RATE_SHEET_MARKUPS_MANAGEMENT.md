# Rate Sheet Editor: Markups Management & Preview Enhancements

<!-- ENHANCEMENT: Feature enhancement to the rate sheet editor -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-02-15 |
| Status | Planning |
| Owner | Engineering Team |
| Type | Enhancement |
| Reference | [AGENTS.md](../AGENTS.md) |
| Parent PRD | [RATE_SHEET_EDITOR_PARITY_UPGRADE.md](./RATE_SHEET_EDITOR_PARITY_UPGRADE.md) |

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

Add a **Markups management tab** to the rate sheet editor (admin mode only) that provides full CRUD operations on `pricing.Markup` records. Enhance the CSV/spreadsheet **preview** to compute and display calculated surcharge values (not raw amounts) and add computed columns for applicable markups (brokerage-fee, insurance, etc.). Introduce a structured `meta` JSONField on the Markup model to categorize markups by type and plan.

### Key Architecture Decisions

1. **No direct relationship between RateSheet and Markup**: The `pricing.Markup` model continues to be applied dynamically post-rate-calculation. The Markups tab in the rate sheet editor is a convenience UI for admin CRUD — it does not create any FK or embedded JSON link between rate sheets and markups.
2. **New `meta` JSONField on Markup model**: A new `meta` field (separate from existing `metadata`) stores structured categorization: `{ type, plan, show_in_preview }`. This avoids overloading the existing `metadata` field.
3. **Admin-only visibility**: The Markups tab only appears when `isAdmin={true}` on the rate sheet editor. Non-admin users never see markup information.
4. **Individual computed columns**: Each markup gets its own column in the preview, showing calculated individual amounts (not cumulative totals). A final "Total Rate" column sums everything.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Markups tab (admin-only) with full CRUD on `pricing.Markup` | Linking markups to specific rate sheets via FK |
| New `meta` JSONField on Markup model | Changing the markup application pipeline (`apply_charge`) |
| Preview: calculated surcharge values (base + fixed / base * %) | New pricing tiers or plan management UI |
| Preview: computed columns for markups with `show_in_preview` | Non-admin markup visibility or read-only views |
| Markup type classification (`brokerage-fee`, `insurance`, etc.) | Automatic markup-to-service assignment |
| Migration for `meta` field | Renaming existing `metadata` field |

---

## Open Questions & Decisions

### Resolved Decisions

| # | Decision | Choice | Rationale | Date |
|---|----------|--------|-----------|------|
| D1 | Data model for markups in rate sheet | No FK/embed — use existing `pricing.Markup` model with dynamic application | Keeps rate sheet self-contained; markups apply at rate-calculation time | 2026-02-15 |
| D2 | Surcharge type access control | Admin-only via Markups tab | Non-admin Surcharges tab remains unchanged; brokerage/insurance types only manageable by admins | 2026-02-15 |
| D3 | Preview column stacking | One column per markup | Each individual markup gets its own computed column regardless of type | 2026-02-15 |
| D4 | Plan field format | Free-form string | Admins type any plan name for flexibility | 2026-02-15 |
| D5 | Calculation display | Individual amounts only + final Total | Each markup column shows its own amount; a "Total Rate" column at the end | 2026-02-15 |
| D6 | Markups CRUD scope | Full CRUD on `pricing.Markup` from rate sheet editor | Direct create/edit/delete, not read-only links | 2026-02-15 |
| D7 | `meta` field vs `metadata` | New `meta` JSONField (separate from existing `metadata`) | Avoids overloading existing field; dedicated structured data | 2026-02-15 |
| D8 | Preview column visibility | `meta.show_in_preview` flag | Per-markup boolean in meta dict; no schema change needed | 2026-02-15 |
| D9 | Markup tab list scope | All markups in system | Show all markups regardless of carrier; admin sees full picture | 2026-02-15 |

---

## Problem Statement

### Current State

The rate sheet editor's CSV preview shows **raw surcharge amounts** without computing them against base rates:

```typescript
// rate-sheet-csv-preview.tsx — current behavior
// Surcharge column just shows the raw amount value
return row.surcharges[colKey] != null
  ? row.surcharges[colKey].toFixed(2)
  : "";
// A 10% surcharge on a $50 base rate shows "10" not "$5.00"
```

Platform-level markups (`pricing.Markup`) are managed exclusively through a separate admin page (`packages/core/modules/Shippers/markups.tsx`). When configuring rate sheets, admins have no way to see how markups will affect final prices or manage markups in the context of the rate sheet they're editing.

The `Markup` model has no structured way to categorize markups by business type (brokerage fee, insurance, notification, etc.) or subscription plan:

```python
# Current Markup model — metadata is unstructured
metadata = models.JSONField(default=dict, blank=True)
# No convention for type categorization or plan filtering
```

### Desired State

```typescript
// Preview shows CALCULATED surcharge values
// For fixed: amount directly
// For percentage: base_rate * (amount / 100)
const calculatedAmount = surcharge.surcharge_type === "percentage"
  ? baseRate * (surcharge.amount / 100)
  : surcharge.amount;

// Plus computed markup columns with show_in_preview flag
// Each markup column shows: calculated markup amount for that row's base rate
```

```python
# Markup model with structured meta field
meta = models.JSONField(default=dict, blank=True)
# meta = {
#   "type": "brokerage-fee",           # brokerage-fee | insurance | surcharge | notification | address-validation
#   "plan": "scale",                    # free-form string, e.g. subscription tier name
#   "show_in_preview": true,            # whether to show computed column in rate sheet preview
# }
```

### Problems

1. **Misleading preview data**: Percentage surcharges show raw percentage values (e.g., "10") instead of calculated amounts (e.g., "$5.00"), making rate sheet review unreliable.
2. **No markup visibility in rate sheet context**: Admins must switch between the rate sheet editor and a separate markups page to understand final pricing.
3. **No markup categorization**: All markups are treated equally — no way to distinguish brokerage fees from insurance charges from notification fees.
4. **No plan-based filtering**: Markups cannot be associated with subscription plans for tiered pricing.

---

## Goals & Success Criteria

### Goals

1. Add a Markups management tab to the rate sheet editor that appears only in admin mode
2. Fix surcharge preview to show calculated values instead of raw amounts
3. Add computed markup columns to the preview for markups flagged with `show_in_preview`
4. Introduce `meta` JSONField on Markup model for type/plan/preview categorization

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Markups tab visible only in admin mode | 100% — never shown to non-admin users | Must-have |
| Preview surcharge values are calculated correctly | Fixed: show amount; Percentage: show base * % | Must-have |
| Computed markup columns in preview | One column per markup with `show_in_preview=true` | Must-have |
| Full CRUD on Markup from rate sheet editor | Create, edit, delete markups | Must-have |
| `meta` field stores type, plan, show_in_preview | Schema validates on save | Must-have |
| Final "Total Rate" column in preview | Sum of base + surcharges + all shown markups | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] Markups tab renders only when `isAdmin={true}`
- [ ] Preview calculates surcharge amounts correctly (fixed and percentage)
- [ ] `meta` JSONField added to Markup model with migration
- [ ] Existing `useMarkups` / `useMarkupMutation` hooks reused in rate sheet editor
- [ ] Markup editor dialog supports `meta.type`, `meta.plan`, `meta.show_in_preview`

**Nice-to-have (P1):**
- [ ] "Total Rate" column as the last computed column
- [ ] Filtering markups by type in the Markups tab
- [ ] Visual badge/chip showing markup type on each card

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Embed markups as JSONField on RateSheet (like surcharges) | Self-contained per rate sheet; no external dependencies | Duplicates data; diverges from pricing pipeline; breaks dynamic application | **Rejected** |
| Link markups via FK from RateSheet to Markup | Explicit relationship; easy querying | Couples rate sheet to pricing module; complicates rate sheet serialization | **Rejected** |
| CRUD on `pricing.Markup` from rate sheet editor (no FK) | Reuses existing model and hooks; no data coupling; markups apply dynamically | No per-rate-sheet scoping; admin sees all markups | **Selected** |
| Read-only markup view in rate sheet editor | Simple; no mutation surface | Admins still need to switch to separate page for edits | **Rejected** |

### Trade-off Analysis

The selected approach maximizes reuse — the existing `useMarkups`, `useMarkupMutation`, and `useMarkupForm` hooks in `packages/hooks/admin-markups.ts` already provide complete CRUD. The rate sheet editor simply embeds these hooks within a new tab. The preview computation is purely client-side, reading all markups and filtering by `meta.show_in_preview`.

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| Markup CRUD hooks | `packages/hooks/admin-markups.ts` | Reuse `useMarkups`, `useMarkupMutation`, `useMarkupForm` directly in new tab |
| Markup GraphQL queries | `packages/types/graphql/admin-ee/queries.ts` | Reuse `GET_MARKUPS`, `CREATE_MARKUP`, `UPDATE_MARKUP`, `DELETE_MARKUP` |
| Admin Markups page | `packages/core/modules/Shippers/markups.tsx` | Reference for UI patterns (card layout, form structure) |
| Rate sheet editor tabs | `packages/ui/components/rate-sheet-editor.tsx:2330-2349` | Extend tab array and union type |
| Surcharges tab | `packages/ui/components/surcharges-tab.tsx` | Template for Markups tab card layout |
| Surcharge editor dialog | `packages/ui/components/surcharge-editor-dialog.tsx` | Reference for dialog pattern |
| CSV preview | `packages/ui/components/rate-sheet-csv-preview.tsx` | Modify surcharge column rendering + add markup columns |
| Pricing Markup model | `modules/pricing/karrio/server/pricing/models.py` | Add `meta` field |
| Admin Markup GraphQL types | `modules/admin/karrio/server/admin/schemas/base/types.py` | Add `meta` field to type |
| Admin Markup GraphQL inputs | `modules/admin/karrio/server/admin/schemas/base/inputs.py` | Add `meta` to input types |
| `isAdmin` prop | `packages/ui/components/rate-sheet-editor.tsx:171` | Already accepted, currently unused — use for conditional tab rendering |

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RATE SHEET EDITOR (admin mode)                            │
│                                                                             │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐                                │
│  │Rate Sheet│  │ Surcharges │  │ Markups  │  ◄── NEW TAB (isAdmin only)    │
│  │   Tab    │  │    Tab     │  │   Tab    │                                 │
│  └──────────┘  └────────────┘  └──────────┘                                 │
│       │              │               │                                      │
│       │              │               ▼                                      │
│       │              │        ┌──────────────┐                              │
│       │              │        │ useMarkups() │  ◄── Existing admin hook     │
│       │              │        │ useMarkup    │                              │
│       │              │        │   Mutation() │                              │
│       │              │        └──────┬───────┘                              │
│       │              │               │                                      │
│       ▼              ▼               ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │                   CSV PREVIEW                                    │        │
│  │  [Fixed Cols] [Surcharge Cols*] [Markup Cols**] [Total Rate]    │        │
│  │                                                                  │        │
│  │  * Surcharges: now show CALCULATED values                        │        │
│  │  ** Markups: computed columns for meta.show_in_preview=true      │        │
│  └─────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
         │                                          │
         ▼                                          ▼
┌─────────────────┐                    ┌────────────────────────┐
│   RateSheet     │                    │   pricing.Markup       │
│   (JSONField    │                    │   (Django model)       │
│   surcharges)   │                    │   + meta JSONField     │
│                 │                    │   (type, plan,         │
│   No FK to      │                    │    show_in_preview)    │
│   Markup        │                    │                        │
└─────────────────┘                    └────────────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌────────────────┐     ┌─────────────┐     ┌─────────────┐
│ Admin  │     │  RateSheet     │     │  Admin GQL  │     │  pricing    │
│ User   │     │  Editor (UI)   │     │  API        │     │  .Markup DB │
└───┬────┘     └───────┬────────┘     └──────┬──────┘     └──────┬──────┘
    │                  │                     │                   │
    │  1. Open editor  │                     │                   │
    │  (admin mode)    │                     │                   │
    │─────────────────>│                     │                   │
    │                  │                     │                   │
    │                  │  2. GET_MARKUPS     │                   │
    │                  │────────────────────>│                   │
    │                  │                     │  3. Query all     │
    │                  │                     │─────────────────>│
    │                  │                     │  4. Return list   │
    │                  │                     │<─────────────────│
    │                  │  5. Markup list     │                   │
    │                  │<────────────────────│                   │
    │                  │                     │                   │
    │  6. Click        │                     │                   │
    │  "Markups" tab   │                     │                   │
    │─────────────────>│                     │                   │
    │                  │                     │                   │
    │  7. See all      │                     │                   │
    │  markups list    │                     │                   │
    │<─────────────────│                     │                   │
    │                  │                     │                   │
    │  8. Create/Edit  │                     │                   │
    │  markup          │                     │                   │
    │─────────────────>│                     │                   │
    │                  │  9. CREATE/UPDATE   │                   │
    │                  │  _MARKUP mutation   │                   │
    │                  │────────────────────>│                   │
    │                  │                     │  10. Persist      │
    │                  │                     │─────────────────>│
    │                  │                     │  11. Confirm      │
    │                  │                     │<─────────────────│
    │                  │  12. Updated list   │                   │
    │                  │<────────────────────│                   │
    │                  │                     │                   │
    │  13. Open        │                     │                   │
    │  Preview         │                     │                   │
    │─────────────────>│                     │                   │
    │                  │                     │                   │
    │  14. See computed│                     │                   │
    │  surcharge +     │                     │                   │
    │  markup columns  │                     │                   │
    │<─────────────────│                     │                   │
    │                  │                     │                   │
```

### Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         PREVIEW COMPUTATION FLOW                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐   ┌──────────────┐   ┌────────────────┐   ┌──────────────┐  │
│  │ Base Rate│──>│ + Surcharges │──>│ + Markup Cols  │──>│  Total Rate  │  │
│  │ (from    │   │ (calculated) │   │ (calculated)   │   │  (sum all)   │  │
│  │ service  │   │              │   │                │   │              │  │
│  │ rates)   │   │ fixed: amt   │   │ per markup:    │   │              │  │
│  │          │   │ %: base*%/100│   │ AMOUNT: amt    │   │              │  │
│  │          │   │              │   │ %: base*%/100  │   │              │  │
│  └──────────┘   └──────────────┘   └────────────────┘   └──────────────┘  │
│                                                                             │
│  Surcharges: from RateSheet.surcharges (per service.surcharge_ids)          │
│  Markups: from pricing.Markup where meta.show_in_preview = true             │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

#### Backend: New `meta` field on Markup model

```python
# modules/pricing/karrio/server/pricing/models.py

class Markup(core.Entity):
    # ... existing fields ...

    # NEW: Structured metadata for categorization
    meta = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Structured categorization metadata.
        {
            "type": "brokerage-fee",       # brokerage-fee | insurance | surcharge | notification | address-validation
            "plan": "scale",               # Free-form plan/tier name (e.g., "launch", "scale", "enterprise")
            "show_in_preview": true         # Whether to show computed column in rate sheet preview
        }
        """,
    )

    # existing metadata field remains unchanged
    metadata = models.JSONField(default=dict, blank=True)
```

#### GraphQL Type Update

```python
# modules/admin/karrio/server/admin/schemas/base/types.py

@strawberry.type
class MarkupType:
    # ... existing fields ...
    meta: Optional[utils.JSON] = None  # NEW
```

```python
# modules/admin/karrio/server/admin/schemas/base/inputs.py

@strawberry.input
class CreateMarkupMutationInput:
    # ... existing fields ...
    meta: Optional[utils.JSON] = strawberry.UNSET  # NEW

@strawberry.input
class UpdateMarkupMutationInput:
    # ... existing fields ...
    meta: Optional[utils.JSON] = strawberry.UNSET  # NEW
```

#### Frontend: Extended types

```typescript
// packages/types/graphql/admin-ee/types.ts — update MarkupType

interface MarkupMeta {
  type?: "brokerage-fee" | "insurance" | "surcharge" | "notification" | "address-validation";
  plan?: string;
  show_in_preview?: boolean;
}

// In the generated types, meta will appear as:
// meta: Record<string, any> | null;
```

#### Rate Sheet Editor Tab Extension

```typescript
// rate-sheet-editor.tsx — extend tab union type
const [activeTab, setActiveTab] = useState<
  "rate_sheet" | "surcharges" | "markups"
>("rate_sheet");

// Tab array (conditional on isAdmin)
const tabs = useMemo(() => {
  const base = [
    { id: "rate_sheet" as const, label: "Rate Sheet" },
    { id: "surcharges" as const, label: "Surcharges" },
  ];
  if (isAdmin) {
    base.push({ id: "markups" as const, label: "Markups" });
  }
  return base;
}, [isAdmin]);
```

### Preview Enhancement: Calculated Surcharge Values

```typescript
// rate-sheet-csv-preview.tsx — FlatRow type extension
interface FlatRow {
  // ... existing fields ...
  surcharges: Record<string, number>;  // NOW: calculated values, not raw amounts
  markups: Record<string, number>;     // NEW: calculated markup values
  totalRate: number | null;            // NEW: sum of base + surcharges + markups
}

// Build surcharge amounts — CALCULATED instead of raw
const surchAmounts: Record<string, number> = {};
surchargeAmountMap.forEach((surcharge, sid) => {
  if (linkedIds.has(sid)) {
    const { amount, surcharge_type } = surcharge;
    surchAmounts[sid] = surcharge_type === "percentage"
      ? (rate ?? 0) * (amount / 100)
      : amount;
  }
});

// Build markup amounts — for markups with meta.show_in_preview
const markupAmounts: Record<string, number> = {};
previewMarkups.forEach((markup) => {
  const amt = markup.markup_type === "PERCENTAGE"
    ? (rate ?? 0) * (markup.amount / 100)
    : markup.amount;
  markupAmounts[markup.id] = amt;
});

// Total rate
const surchargeTotal = Object.values(surchAmounts).reduce((a, b) => a + b, 0);
const markupTotal = Object.values(markupAmounts).reduce((a, b) => a + b, 0);
const totalRate = (rate ?? 0) + surchargeTotal + markupTotal;
```

### Preview Columns Update

```typescript
// Surcharge columns — unchanged structure, but values are now calculated
const surchargeColumns = useMemo(() =>
  surcharges.filter((s) => s.name).map((s) => ({
    key: `surch_${s.id}`,
    label: `${s.name} (${s.surcharge_type === "percentage" ? `${s.amount}%` : "$"})`,
    width: 110,
  })),
  [open, surcharges]
);

// Markup columns — only for markups with meta.show_in_preview
const markupColumns = useMemo(() => {
  if (!isAdmin || !markups) return [];
  return markups
    .filter((m) => m.active && m.meta?.show_in_preview)
    .map((m) => ({
      key: `mkp_${m.id}`,
      label: `${m.name} (${m.markup_type === "PERCENTAGE" ? `${m.amount}%` : "$"})`,
      width: 120,
    }));
}, [open, markups, isAdmin]);

// Total column
const totalColumn = { key: "totalRate", label: "Total Rate", width: 100 };

// All columns combined
const allColumns = useMemo(() =>
  [...FIXED_COLUMNS, ...surchargeColumns, ...markupColumns, totalColumn],
  [surchargeColumns, markupColumns]
);
```

### Markups Tab Component

```typescript
// NEW FILE: packages/ui/components/markups-tab.tsx

interface MarkupsTabProps {
  // No rate-sheet-specific props needed — markups are global
  onEditMarkup: (markup: MarkupType) => void;
  onAddMarkup: () => void;
  onRemoveMarkup: (markupId: string) => void;
  markups: MarkupType[];
  isLoading: boolean;
}

// Card layout following surcharges-tab.tsx pattern:
// - Empty state: "No markups configured yet"
// - Each markup card shows: name, type badge, amount, plan badge, active status
// - Meta fields visible: type (colored badge), plan (gray badge), show_in_preview (eye icon)
```

### Markup Editor Dialog

```typescript
// NEW FILE: packages/ui/components/markup-editor-dialog.tsx

// Extends the existing useMarkupForm hook from packages/hooks/admin-markups.ts
// Adds meta fields (type, plan, show_in_preview) to the form

// Form sections:
// 1. General: name, amount, markup_type (AMOUNT/PERCENTAGE), active, is_visible
// 2. Categorization: meta.type (select), meta.plan (text input), meta.show_in_preview (toggle)
// 3. Filters: carrier_codes, service_codes, connection_ids, organization_ids
//    (reuses existing useMarkupForm hook's handleCarrierChange etc.)
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `meta` | JSONField | No | Structured categorization metadata |
| `meta.type` | string | No | Markup category: `brokerage-fee`, `insurance`, `surcharge`, `notification`, `address-validation` |
| `meta.plan` | string | No | Free-form plan/tier name for plan-based pricing |
| `meta.show_in_preview` | boolean | No | Whether to show computed column in rate sheet CSV preview. Default: `false` |

### API Changes

**No new endpoints required.** The existing admin GraphQL mutations (`create_markup`, `update_markup`, `delete_markup`) are extended to accept the `meta` field. The existing `GET_MARKUPS` query returns the `meta` field.

**Updated GraphQL schema:**

```graphql
type MarkupType {
  # ... existing fields ...
  meta: JSON          # NEW
}

input CreateMarkupMutationInput {
  # ... existing fields ...
  meta: JSON          # NEW
}

input UpdateMarkupMutationInput {
  # ... existing fields ...
  meta: JSON          # NEW
}
```

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| Base rate is 0 or null | Percentage surcharges/markups compute to 0 | Use `(rate ?? 0)` as base for all calculations |
| No markups with `show_in_preview` | No markup columns in preview; only surcharge columns | `markupColumns` array is empty; `allColumns` excludes them |
| Markup has no `meta` field (legacy data) | Treated as having no type, no plan, `show_in_preview=false` | Optional chaining: `m.meta?.show_in_preview` defaults to falsy |
| Admin creates markup then switches to non-admin view | Markups tab disappears; preview hides markup columns | Tab conditional on `isAdmin`; markup columns conditional on `isAdmin` |
| Percentage markup with very large amount (e.g., 500%) | Calculated value may be surprisingly large | Show in preview as-is; admin responsibility to set reasonable values |
| Multiple markups with same name | Each gets its own column; names may be confusing | Column label includes markup type indicator |
| Markup deleted while rate sheet editor is open | Stale data until query refetch | `useMarkups` has `staleTime: 5000`; mutation triggers `invalidateCache` |
| Surcharge is percentage type with no service linked | Row shows 0 in that column | `linkedIds` check excludes unlinked surcharges; no calculation needed |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| Admin GraphQL API unreachable | Markups tab shows loading/error state | Use existing `query.isLoading` / `query.isError` from `useMarkups` |
| Migration fails on `meta` field | Markup model unchanged; editor graceful degradation | `meta` defaults to `dict` (empty); no required fields |
| Large number of markups (100+) | Preview becomes wide with many columns | Only markups with `meta.show_in_preview=true` generate columns; most won't |
| Concurrent admin edits to same markup | Last write wins | Acceptable for admin-only feature; low concurrency expected |

### Security Considerations

- [x] Markups tab only visible when `isAdmin={true}` — enforced both by UI conditional rendering and by using admin GraphQL hooks which require admin authentication
- [x] Admin GraphQL mutations already require staff/admin permissions
- [x] No new API endpoints exposed to non-admin users
- [x] `meta` field accepts arbitrary JSON — validate at UI level (type select, plan text, boolean toggle)

---

## Implementation Plan

### Phase 1: Backend — `meta` Field on Markup Model

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `meta` JSONField to Markup model | `modules/pricing/karrio/server/pricing/models.py` | Pending | S |
| Create Django migration | `modules/pricing/karrio/server/pricing/migrations/` | Pending | S |
| Add `meta` to admin GraphQL MarkupType | `modules/admin/karrio/server/admin/schemas/base/types.py` | Pending | S |
| Add `meta` to admin GraphQL inputs | `modules/admin/karrio/server/admin/schemas/base/inputs.py` | Pending | S |
| Update mutation resolvers to handle `meta` | `modules/admin/karrio/server/admin/schemas/base/mutations.py` | Pending | S |

### Phase 2: Frontend — Preview Enhancements

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Fix surcharge preview to show calculated values | `packages/ui/components/rate-sheet-csv-preview.tsx` | Pending | M |
| Update `surchargeAmountMap` to include surcharge type | `packages/ui/components/rate-sheet-csv-preview.tsx` | Pending | S |
| Add `markups` prop and computed markup columns | `packages/ui/components/rate-sheet-csv-preview.tsx` | Pending | M |
| Add "Total Rate" column | `packages/ui/components/rate-sheet-csv-preview.tsx` | Pending | S |
| Update `FlatRow` type with markups and totalRate | `packages/ui/components/rate-sheet-csv-preview.tsx` | Pending | S |
| Update `formatCell` for new column types | `packages/ui/components/rate-sheet-csv-preview.tsx` | Pending | S |

### Phase 3: Frontend — Markups Tab & Editor

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create `markups-tab.tsx` component | `packages/ui/components/markups-tab.tsx` | Pending | M |
| Create `markup-editor-dialog.tsx` component | `packages/ui/components/markup-editor-dialog.tsx` | Pending | L |
| Add `meta.type` select, `meta.plan` input, `meta.show_in_preview` toggle to editor | `packages/ui/components/markup-editor-dialog.tsx` | Pending | M |
| Update GraphQL queries to include `meta` field | `packages/types/graphql/admin-ee/queries.ts` | Pending | S |
| Update generated TypeScript types | `packages/types/graphql/admin-ee/types.ts` | Pending | S |
| Extend `useMarkupForm` hook for `meta` fields | `packages/hooks/admin-markups.ts` | Pending | S |
| Add conditional "Markups" tab to rate sheet editor | `packages/ui/components/rate-sheet-editor.tsx` | Pending | M |
| Wire `useMarkups`/`useMarkupMutation` into editor | `packages/ui/components/rate-sheet-editor.tsx` | Pending | M |
| Pass markups data to CSV preview component | `packages/ui/components/rate-sheet-editor.tsx` | Pending | S |

**Dependencies:** Phase 2 and Phase 3 depend on Phase 1 (backend `meta` field). Phase 2 and Phase 3 can proceed in parallel after Phase 1.

---

## Testing Strategy

### Test Categories

| Category | Location | Coverage Target |
|----------|----------|-----------------|
| Unit Tests (backend) | `modules/pricing/tests/` | meta field serialization, migration |
| Unit Tests (frontend) | Preview calculation logic | Surcharge + markup computation correctness |
| Integration Tests | Admin GraphQL API | CRUD mutations with meta field |
| E2E Tests | Rate sheet editor | Tab visibility, preview columns |

### Test Cases

#### Backend Unit Tests

```python
"""Test meta field on Markup model."""

import unittest
from karrio.server.pricing.models import Markup

class TestMarkupMeta(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_markup_with_meta(self):
        """Verify meta field stores type, plan, show_in_preview."""
        markup = Markup.objects.create(
            name="Test Brokerage Fee",
            amount=5.0,
            markup_type="PERCENTAGE",
            meta={
                "type": "brokerage-fee",
                "plan": "scale",
                "show_in_preview": True,
            }
        )
        markup.refresh_from_db()
        print(markup.meta)

        self.assertEqual(markup.meta["type"], "brokerage-fee")
        self.assertEqual(markup.meta["plan"], "scale")
        self.assertTrue(markup.meta["show_in_preview"])

    def test_markup_meta_defaults_to_empty_dict(self):
        """Verify meta defaults to {} for legacy markups."""
        markup = Markup.objects.create(
            name="Legacy Markup",
            amount=1.0,
            markup_type="AMOUNT",
        )
        markup.refresh_from_db()
        print(markup.meta)

        self.assertEqual(markup.meta, {})

    def test_markup_meta_preserves_existing_metadata(self):
        """Verify meta field is independent of existing metadata field."""
        markup = Markup.objects.create(
            name="Dual Field Markup",
            amount=2.0,
            markup_type="AMOUNT",
            metadata={"legacy_key": "value"},
            meta={"type": "insurance", "show_in_preview": True},
        )
        markup.refresh_from_db()
        print(markup.metadata)
        print(markup.meta)

        self.assertEqual(markup.metadata, {"legacy_key": "value"})
        self.assertEqual(markup.meta["type"], "insurance")
```

#### Frontend Preview Calculation Tests

```typescript
// Preview calculation verification (manual / E2E):
// Given: base rate = $50.00
//   Surcharge (fixed, $3.00): column shows "$3.00"
//   Surcharge (percentage, 10%): column shows "$5.00" (not "10")
//   Markup (PERCENTAGE, 5%, show_in_preview=true): column shows "$2.50"
//   Markup (AMOUNT, $1.50, show_in_preview=true): column shows "$1.50"
//   Total Rate: $50.00 + $3.00 + $5.00 + $2.50 + $1.50 = $62.00
```

### Running Tests

```bash
# From repository root
source bin/activate-env

# Run pricing module tests
python -m unittest discover -v -f modules/pricing/tests

# Run admin schema tests
karrio test --failfast karrio.server.admin.tests
```

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| `meta` field conflicts with existing `metadata` usage | Medium | Low | Fields are completely separate; `meta` is new, `metadata` unchanged |
| Preview performance with many markup columns | Medium | Low | Only `show_in_preview=true` markups generate columns; most won't |
| Admin accidentally deletes markup used in production | High | Low | Markup deletion already exists in current admin UI; no new risk surface |
| Breaking change to existing markup serialization | High | Low | `meta` has `default=dict`; backward compatible |
| Confusion between `meta` and `metadata` fields | Medium | Medium | Clear documentation; editor UI labels meta fields distinctly |

---

## Migration & Rollback

### Backward Compatibility

- **API compatibility**: Adding `meta` as an optional JSONField with `default=dict` is fully backward compatible. Existing API consumers that don't send `meta` will get `{}` by default.
- **Data compatibility**: No existing data is modified. The `metadata` field is untouched. New `meta` field defaults to empty dict.
- **Feature flags**: The Markups tab is gated by `isAdmin` prop, which is already set by calling components. No feature flag needed.

### Data Migration

```python
# Migration: add meta field to Markup model
# This is a simple AddField migration — no data transformation needed

from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("pricing", "NNNN_previous_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="markup",
            name="meta",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="Structured categorization metadata: {type, plan, show_in_preview}",
            ),
        ),
    ]
```

### Rollback Procedure

1. **Identify issue**: Admin reports broken markup management or preview errors
2. **Stop rollout**: Revert frontend deployment (Markups tab disappears; preview reverts to raw surcharge values)
3. **Revert changes**: Django migration is reversible (RemoveField); no data loss since `meta` is new
4. **Verify recovery**: Existing markup CRUD on admin page continues to work; rate sheet editor shows only Rate Sheet + Surcharges tabs

---

## Appendices

### Appendix A: Markup Type Categories

| Type | Description | Typical Use Case | Default `show_in_preview` |
|------|-------------|------------------|---------------------------|
| `brokerage-fee` | Platform brokerage/commission fee | Admin margin on resold shipping rates | `true` |
| `insurance` | Shipment insurance charge | Per-parcel or percentage-of-value insurance | `true` |
| `surcharge` | Generic additional charge | Fuel surcharge, peak season, remote area | `false` |
| `notification` | SMS/email notification fee | Delivery notification charges | `false` |
| `address-validation` | Address validation service fee | Per-shipment address validation | `false` |

### Appendix B: Preview Column Order

```
| Type | From | Zone | Carrier | Service Code | Service Name | Min Wt | Max Wt | Max L | Max W | Max H | Base Rate | Currency |
| --- surcharge columns (calculated) --- |
| Fuel (10%) | Handling ($2.00) | ... |
| --- markup columns (meta.show_in_preview=true) --- |
| Brokerage Fee (5%) | Insurance (2%) | ... |
| Total Rate |
```

### Appendix C: Existing Admin Markups Page Reference

The existing admin markups page (`packages/core/modules/Shippers/markups.tsx`) provides a full-page CRUD interface. The new Markups tab in the rate sheet editor will provide a **subset** of this functionality embedded in the editor context:

- Same `useMarkups` / `useMarkupMutation` hooks
- Same GraphQL queries/mutations
- Simplified card layout (inspired by `surcharges-tab.tsx`)
- Additional `meta` fields in the editor dialog
