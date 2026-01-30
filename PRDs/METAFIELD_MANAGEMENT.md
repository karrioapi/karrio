# Metafield Management Settings Page & Entity Editor Integration

<!-- ENHANCEMENT: Feature enhancement PRD -->

| Field | Value |
|-------|-------|
| Project | Karrio |
| Version | 1.0 |
| Date | 2026-01-29 |
| Status | Planning |
| Owner | Dashboard Team |
| Type | Enhancement |
| Reference | [AGENTS.md](../AGENTS.md) |

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Resolved Decisions](#resolved-decisions)
3. [Problem Statement](#problem-statement)
4. [Goals & Success Criteria](#goals--success-criteria)
5. [Alternatives Considered](#alternatives-considered)
6. [Technical Design](#technical-design)
7. [Edge Cases & Failure Modes](#edge-cases--failure-modes)
8. [Implementation Plan](#implementation-plan)
9. [Testing Strategy](#testing-strategy)
10. [Risk Assessment](#risk-assessment)
11. [Migration & Rollback](#migration--rollback)

---

## Executive Summary

Add a dedicated "Custom fields" settings page for full metafield CRUD management, plus a reusable `MetafieldEditor` component embedded in entity forms (shipments, orders, trackers, carrier connections). Global metafields (without object attachment) serve as reusable templates that appear as suggestions in entity editors.

### Key Architecture Decisions

1. **Frontend-only work**: Backend GraphQL API is fully complete (queries, mutations, filters). All work is on the frontend.
2. **"Custom fields" label**: User-facing name in settings navigation (maps to `Metafield` model internally).
3. **Global metafields as templates**: Unattached metafields act as suggestions when editing entity metafields; entity editors allow both creating new definitions inline and assigning values to existing ones.

### Scope

| In Scope | Out of Scope |
|----------|--------------|
| Settings page with full CRUD, filtering, pagination | REST API endpoints for metafields |
| Metafield editor in shipment, order, tracker, carrier connection forms | Bulk import/export of metafields |
| GraphQL operations, types, hooks for metafields | New backend model changes |
| Global metafield templates as suggestions | Metafield permissions/roles system |
| Dynamic value input per metafield type | Custom metafield validation rules |

---

## Resolved Decisions

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| D1 | Entity editor scope | Both create & assign | Users can define new metafield keys inline AND assign values to existing definitions |
| D2 | Settings nav label | "Custom fields" | Intuitive for non-technical users |
| D3 | Global metafield templates | Yes, as suggestions | Unattached metafields serve as reusable templates suggested in entity editors |

---

## Problem Statement

### Current State

Metafields exist as a fully functional backend model (`core.Metafield`) with GraphQL CRUD API, but there is **no dashboard UI** for managing them. The only way to interact with metafields is through raw GraphQL queries.

```typescript
// Current: No metafield management UI exists
// Users must use GraphQL playground or API calls directly
// No frontend hooks, types, or components for metafields
```

### Desired State

```typescript
// Settings page: /settings/metafields with full CRUD
// Reusable MetafieldEditor in entity forms
<MetafieldEditor objectType="shipment" objectId={shipment.id} />

// Hook for data fetching
const { query, filter, setFilter } = useMetafields({ object_type: "shipment" });
const { createMetafield, updateMetafield, deleteMetafield } = useMetafieldMutation();
```

### Problems

1. **No UI for metafield management**: Users cannot create, view, edit, or delete metafields from the dashboard
2. **No metafield editor in entity forms**: Shipments, orders, trackers, and carrier connections lack custom field editing
3. **No frontend infrastructure**: Missing GraphQL operations, TypeScript types, and React hooks for metafields

---

## Goals & Success Criteria

### Goals

1. Full CRUD metafield management from the dashboard settings page
2. Inline metafield editing in entity detail/edit forms with template suggestions
3. Consistent UI patterns matching existing settings pages (products, addresses)

### Success Criteria

| Metric | Target | Priority |
|--------|--------|----------|
| Settings page CRUD operations | All 4 operations (create, read, update, delete) functional | Must-have |
| Entity editor integration | MetafieldEditor embedded in shipment and order pages | Must-have |
| Dynamic value input | All 7 metafield types render correct input controls | Must-have |
| Template suggestions | Global metafields appear as suggestions in entity editors | Nice-to-have |

### Launch Criteria

**Must-have (P0):**
- [ ] Settings page at `/settings/metafields` with table, filters, create/edit/delete
- [ ] `useMetafields` and `useMetafieldMutation` hooks
- [ ] GraphQL operations and TypeScript types for metafields
- [ ] `MetafieldEditor` component embedded in shipment and order detail pages
- [ ] Dynamic value input per metafield type (text, number, boolean, json, date, datetime, password)

**Nice-to-have (P1):**
- [ ] MetafieldEditor in tracker preview sheet
- [ ] MetafieldEditor in carrier connection edit dialog
- [ ] Global metafield template suggestions in entity editors

---

## Alternatives Considered

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Dedicated settings page + reusable entity editor | Full CRUD control, consistent patterns, reusable component | More files to create | **Selected** |
| Extend existing metadata editor for metafields | Less new code | Different data model (metadata is key-value dict, metafields are typed model instances), conflation of concepts | Rejected |
| Settings page only, no entity integration | Simpler scope | Users must navigate away from entities to manage fields | Rejected |

### Trade-off Analysis

The selected approach creates more files but maintains clear separation between metadata (untyped key-value pairs stored as JSON) and metafields (typed, validated fields with schema). The `MetafieldEditor` component is reusable across all entity types, reducing long-term maintenance. The pattern mirrors the existing `ProductsManagement` + `ProductEditDialog` approach used in the product catalog settings page.

---

## Technical Design

> **IMPORTANT**: Before designing, carefully study related existing code and utilities.
> Search the codebase for similar patterns to reuse. Never reinvent the wheel.
> Follow `AGENTS.md` coding style exactly as the original authors.

### Existing Code Analysis

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| `ProductsManagement` | `packages/ui/components/products-management.tsx` | Pattern reference for settings page (table + dialog + CRUD) |
| `ProductEditDialog` | Same file, line 136 | Pattern for metafield edit dialog (react-hook-form + zod) |
| Settings page wrapper | `packages/core/modules/Settings/products.tsx` | Exact pattern for settings page module |
| Dashboard page route | `apps/dashboard/src/app/(base)/(dashboard)/settings/products/page.tsx` | Exact pattern for Next.js page |
| Settings navigation | `packages/ui/components/settings-navigation.tsx` | Add "Custom fields" tab entry |
| `EnhancedMetadataEditor` | `packages/ui/components/enhanced-metadata-editor.tsx` | Reference for inline editor UX (NOT reused - different data model) |
| `useProducts` hook | `packages/hooks/product.ts` | Pattern for `useMetafields` hook |
| `DELETE_METAFIELD` | `packages/types/graphql/queries.ts:3214` | Already exists, reuse directly |
| `MetafieldTypeEnum` | `packages/types/graphql/ee/types.ts:2899` | Must duplicate to base types.ts |
| Metafield GraphQL schema | `modules/graph/karrio/server/graph/schemas/base/` | Backend is complete - types.py:553, inputs.py:692, mutations at __init__.py:452 |

### Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────────┐
│  Settings Page   │────>│  useMetafields   │────>│  GraphQL API         │
│  /settings/      │     │  useMetafield    │     │  metafields(filter)  │
│  metafields      │     │  Mutation        │     │  create_metafield    │
└─────────────────┘     └──────────────────┘     │  update_metafield    │
                                                  │  delete_metafield    │
┌─────────────────┐     ┌──────────────────┐     └──────────────────────┘
│  Entity Forms    │────>│  MetafieldEditor │────────────┘
│  (Shipment,      │     │  Component       │
│   Order, etc.)   │     └──────────────────┘
└─────────────────┘
```

### Sequence Diagram

```
┌────────┐     ┌──────────┐     ┌────────────┐     ┌──────────┐
│  User  │     │ Settings │     │   Hooks    │     │ GraphQL  │
│        │     │   Page   │     │            │     │   API    │
└───┬────┘     └────┬─────┘     └─────┬──────┘     └────┬─────┘
    │               │                  │                  │
    │  1. Navigate  │                  │                  │
    │──────────────>│                  │                  │
    │               │  2. useMetafields│                  │
    │               │─────────────────>│                  │
    │               │                  │  3. GET_METAFIELDS
    │               │                  │─────────────────>│
    │               │                  │                  │
    │               │                  │  4. Response     │
    │               │                  │<─────────────────│
    │               │  5. Render table │                  │
    │               │<─────────────────│                  │
    │  6. Display   │                  │                  │
    │<──────────────│                  │                  │
    │               │                  │                  │
    │  7. Create    │                  │                  │
    │──────────────>│                  │                  │
    │               │  8. Mutation     │                  │
    │               │─────────────────>│                  │
    │               │                  │  9. CREATE       │
    │               │                  │─────────────────>│
    │               │                  │  10. Result      │
    │               │                  │<─────────────────│
    │               │  11. Invalidate  │                  │
    │               │<─────────────────│                  │
    │               │                  │                  │
```

### Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    METAFIELD MANAGEMENT FLOW                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Settings Page                                                   │
│  ┌──────────┐    ┌───────────────┐    ┌──────────────┐          │
│  │ Filters  │───>│ useMetafields │───>│ GraphQL API  │          │
│  │ (type,   │    │ (query+cache) │    │ metafields() │          │
│  │  key,    │    └───────────────┘    └──────────────┘          │
│  │  object) │                                                    │
│  └──────────┘                                                    │
│                                                                  │
│  Entity Editor                                                   │
│  ┌──────────┐    ┌───────────────┐    ┌──────────────┐          │
│  │ Metafield│───>│ useMetafields │───>│ GraphQL API  │          │
│  │ Editor   │    │ (filtered by  │    │ metafields() │          │
│  │ (inline) │    │  object_type  │    │ + create/    │          │
│  └──────────┘    │  + object_id) │    │   update/    │          │
│       │          └───────────────┘    │   delete     │          │
│       │                               └──────────────┘          │
│       │          ┌───────────────┐                               │
│       └─────────>│ Global fields │  (template suggestions)      │
│                  │ (no object)   │                               │
│                  └───────────────┘                               │
└──────────────────────────────────────────────────────────────────┘
```

### Data Models

The backend `Metafield` model already exists. Frontend types mirror it:

```typescript
// TypeScript type (to add in packages/types/graphql/types.ts)
export enum MetafieldTypeEnum {
  boolean = "boolean",
  date = "date",
  date_time = "date_time",
  json = "json",
  number = "number",
  password = "password",
  text = "text",
}

interface MetafieldType {
  id: string;
  key: string;
  type: MetafieldTypeEnum;
  value: string;
  parsed_value: any;
  is_required: boolean;
  object_type?: string;
  object_id?: string;
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes (read) | Unique identifier, auto-generated |
| `key` | string | Yes | Field name/key (e.g., "customs_code") |
| `type` | MetafieldTypeEnum | Yes | Value type constraint |
| `value` | string | Yes | Serialized field value |
| `parsed_value` | any | No (read) | Deserialized value returned by API |
| `is_required` | boolean | No | Whether field is mandatory, default `false` |
| `object_type` | string | No | ContentType model name (e.g., "shipment") |
| `object_id` | string | No | ID of the associated entity |

---

## Edge Cases & Failure Modes

### Edge Cases

| Scenario | Expected Behavior | Handling |
|----------|-------------------|----------|
| JSON value with invalid syntax | Show validation error, prevent save | Zod `superRefine` validates JSON.parse on json type |
| Duplicate metafield key on same object | API returns error | Display GraphQL error messages in toast |
| Metafield on deleted object | Orphaned metafield visible in settings | Show object_id with "(deleted)" indicator if object not found |
| Very long JSON value | Truncate in table view | Show first 100 chars with "..." ellipsis in table |
| Empty value on required metafield | Prevent save | Form validation via zod schema |
| Password type display | Mask value in table and editor | Show masked characters in table, use password input in editor |

### Failure Modes

| What Can Go Wrong | Impact | Mitigation |
|-------------------|--------|------------|
| GraphQL mutation fails | User sees error | Display error toast with message from API |
| Network timeout on metafield list | Empty/stale data | React Query retry + staleTime cache |
| Invalid object_type in filter | Empty results | GraphQL resolver returns empty set (handled in backend) |
| Content type mismatch | Metafield not linked properly | Validate object_type against known types in select dropdown |

---

## Implementation Plan

### Phase 1: GraphQL Operations & TypeScript Types

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add `GET_METAFIELDS`, `GET_METAFIELD`, `CREATE_METAFIELD`, `UPDATE_METAFIELD` GraphQL operations | `packages/types/graphql/queries.ts` | Pending | S |
| Add `MetafieldTypeEnum`, query/mutation result interfaces, input types | `packages/types/graphql/types.ts` | Pending | M |
| Add `MetafieldType` export alias | `packages/types/base.ts` | Pending | S |

**GraphQL operations to add** (after existing `DELETE_METAFIELD` at line 3214):

```graphql
# GET_METAFIELDS
query get_metafields($filter: MetafieldFilter) {
  metafields(filter: $filter) {
    page_info { count has_next_page has_previous_page start_cursor end_cursor }
    edges {
      node {
        id key type value parsed_value is_required object_type object_id
      }
    }
  }
}

# GET_METAFIELD
query get_metafield($id: String!) {
  metafield(id: $id) {
    id key type value parsed_value is_required object_type object_id
  }
}

# CREATE_METAFIELD
mutation create_metafield($data: CreateMetafieldInput!) {
  create_metafield(input: $data) {
    metafield { id key type value is_required object_type object_id }
    errors { field messages }
  }
}

# UPDATE_METAFIELD
mutation update_metafield($data: UpdateMetafieldInput!) {
  update_metafield(input: $data) {
    metafield { id key type value is_required object_type object_id }
    errors { field messages }
  }
}
```

### Phase 2: React Hook

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create `useMetafields` list hook and `useMetafieldMutation` CRUD hook | `packages/hooks/metafield.ts` (NEW) | Pending | M |

**Dependencies:** Phase 2 depends on Phase 1 completion.

Follow exact pattern from `packages/hooks/product.ts`:
- `useMetafields({ filter, setVariablesToURL, preloadNextPage })` returns `{ query, filter, setFilter }`
- `useMetafieldMutation()` returns `{ createMetafield, updateMetafield, deleteMetafield }`

### Phase 3: Settings Page Components

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create MetafieldEditDialog (react-hook-form + zod + dynamic value input) | `packages/ui/components/metafield-edit-dialog.tsx` (NEW) | Pending | L |
| Create MetafieldsManagement (table + filters + CRUD) | `packages/ui/components/metafields-management.tsx` (NEW) | Pending | L |
| Create settings page module wrapper | `packages/core/modules/Settings/metafields.tsx` (NEW) | Pending | S |
| Create Next.js page route | `apps/dashboard/src/app/(base)/(dashboard)/settings/metafields/page.tsx` (NEW) | Pending | S |
| Add "Custom fields" tab to settings navigation | `packages/ui/components/settings-navigation.tsx` | Pending | S |

**Dependencies:** Phase 3 depends on Phase 2 completion.

**MetafieldEditDialog design:**
- `react-hook-form` with `zodResolver` (matching ProductEditDialog pattern)
- Dynamic value input based on selected type:
  - `text` → `<Input>`, `number` → `<Input type="number">`, `boolean` → `<Checkbox>`
  - `json` → `<Textarea>` with JSON validation, `date` → `<Input type="date">`
  - `date_time` → `<Input type="datetime-local">`, `password` → `<Input type="password">`
- Fields: key, type, value, is_required, object_type (select), object_id (optional input)
- When used from entity editor: object_type and object_id are pre-filled and hidden

**MetafieldsManagement design** (matching `ProductsManagement` pattern):
- Filter bar: key search input, object_type select, type select
- Table columns: Key, Type (badge), Value (truncated), Required, Object Type, Actions
- Empty state with create button
- Pagination (Previous/Next)
- ConfirmationDialog for delete

**Settings navigation entry** (add after "Product catalog"):
```typescript
{ key: "metafields", label: "Custom fields", href: "/settings/metafields" },
```

### Phase 4: Reusable MetafieldEditor Component

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Create MetafieldEditor for embedding in entity forms | `packages/ui/components/metafield-editor.tsx` (NEW) | Pending | L |

**Dependencies:** Phase 4 depends on Phase 3 completion (reuses MetafieldEditDialog).

**MetafieldEditor props:**
```typescript
interface MetafieldEditorProps {
  objectType: string;   // e.g., "shipment", "order", "tracking"
  objectId: string;     // e.g., "shp_xxx"
}
```

**Behavior:**
- Fetches metafields for the given object via `useMetafields({ object_type, object_id })`
- Also fetches global (unattached) metafields as template suggestions
- Displays existing metafields as key-value rows with type badges
- "Add field" button opens MetafieldEditDialog with pre-filled object_type/object_id
- Edit/Delete actions per row
- Template suggestions: when adding a new field, show dropdown of existing global metafield keys

### Phase 5: Entity Form Integration

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Add MetafieldEditor to shipment detail page | `packages/core/modules/Shipments/shipment.tsx` | Pending | S |
| Add MetafieldEditor to order detail page | `packages/core/modules/Orders/order.tsx` | Pending | S |
| Add MetafieldEditor to tracker preview sheet | `packages/ui/components/tracking-preview-sheet.tsx` | Pending | S |
| Add MetafieldEditor to carrier connection dialog | `packages/ui/components/carrier-connection-dialog.tsx` | Pending | S |

**Dependencies:** Phase 5 depends on Phase 4 completion.

**Integration pattern** (add after existing Metadata section in each entity):
```tsx
{/* Custom Fields section - add after existing Metadata */}
<div className="mt-6">
  <h4 className="text-xl font-semibold mb-3">Custom Fields</h4>
  <MetafieldEditor objectType="shipment" objectId={entity_id} />
</div>
```

**Entity to object_type mapping:**

| Entity | object_type value | Location of edit form |
|--------|-------------------|----------------------|
| Shipment | `"shipment"` | `packages/core/modules/Shipments/shipment.tsx` (sidebar) |
| Order | `"order"` | `packages/core/modules/Orders/order.tsx` (sidebar) |
| Tracker | `"tracking"` | `packages/ui/components/tracking-preview-sheet.tsx` |
| Carrier Connection | (verify ContentType model name) | `packages/ui/components/carrier-connection-dialog.tsx` |

### Phase 6: Exports & Build Verification

| Task | Files | Status | Effort |
|------|-------|--------|--------|
| Export new components from UI package index | `packages/ui/components/index.tsx` (if exists) | Pending | S |
| Export new hook from hooks package | `packages/hooks/index.ts` (if exists) | Pending | S |
| Verify TypeScript builds pass | All packages | Pending | S |

**Dependencies:** Phase 6 depends on all previous phases.

---

## Testing Strategy

### Test Categories

| Category | Location | Coverage |
|----------|----------|----------|
| Backend (existing) | `modules/graph/karrio/server/graph/tests/test_metafield.py` | Already complete |
| Frontend hooks | Manual verification via dashboard | Functional testing |
| Settings page | Manual E2E | Create, list, filter, edit, delete flows |
| Entity editor | Manual E2E | Add/edit/delete metafields on shipments and orders |

### Manual Verification Steps

1. Navigate to `/settings/metafields` and verify empty state with "Create" button
2. Create a global metafield (no object) and verify it appears in table
3. Create metafield attached to object_type "shipment" and verify it appears when filtered
4. Filter by object_type, type, key search and verify correct results
5. Edit a metafield and verify values update correctly
6. Delete a metafield and verify removal from table with confirmation dialog
7. Navigate to a shipment detail and verify "Custom Fields" section is visible
8. Add metafield from entity editor and verify it appears attached to shipment
9. Verify global metafield keys appear as suggestions in entity editor

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| MetafieldTypeEnum already in ee/types.ts | Low | High | Duplicate to base types.ts; EE can still use its own |
| object_type values don't match ContentType.model | Medium | Low | Verify Django ContentType model names for each entity |
| Component naming collision (MetafieldType in GraphQL vs React) | Low | Medium | Use `MetafieldType` for GraphQL, component names are `MetafieldEditDialog`, `MetafieldsManagement` |
| Missing carrier connection ContentType | Medium | Medium | Verify exact model name before Phase 5 integration |
| Breaking changes to existing pages | Low | Low | Additive-only changes; entity editor sections are new DOM nodes |

---

## Migration & Rollback

### Backward Compatibility

- **No backend changes**: All work is frontend-only
- **No database migrations**: Backend model and GraphQL schema already exist
- **Additive only**: New pages, components, and hooks don't affect existing functionality
- **API compatibility**: No changes to existing GraphQL operations or REST endpoints

### Rollback Procedure

1. **Identify issue**: Check browser console for errors on settings page or entity forms
2. **Stop rollout**: Revert the frontend deployment
3. **Revert changes**: Remove new files and the settings-navigation entry to restore previous state
4. **Verify recovery**: Confirm existing settings pages and entity forms render correctly

---

## Appendices

### Appendix A: Files Summary

**New Files (8):**

| # | File | Purpose |
|---|------|---------|
| 1 | `packages/types/graphql/queries.ts` | Add 4 GraphQL operations (after line 3224) |
| 2 | `packages/types/graphql/types.ts` | Add MetafieldTypeEnum + interfaces |
| 3 | `packages/hooks/metafield.ts` | New hook file |
| 4 | `packages/ui/components/metafield-edit-dialog.tsx` | Edit/create dialog |
| 5 | `packages/ui/components/metafields-management.tsx` | Settings page component |
| 6 | `packages/ui/components/metafield-editor.tsx` | Reusable entity editor |
| 7 | `packages/core/modules/Settings/metafields.tsx` | Page module wrapper |
| 8 | `apps/dashboard/src/app/(base)/(dashboard)/settings/metafields/page.tsx` | Route |

**Modified Files (5-6):**

| # | File | Change |
|---|------|--------|
| 1 | `packages/ui/components/settings-navigation.tsx` | Add "Custom fields" tab |
| 2 | `packages/types/base.ts` | Add MetafieldType export |
| 3 | `packages/core/modules/Shipments/shipment.tsx` | Add MetafieldEditor |
| 4 | `packages/core/modules/Orders/order.tsx` | Add MetafieldEditor |
| 5 | `packages/ui/components/tracking-preview-sheet.tsx` | Add MetafieldEditor |
| 6 | `packages/ui/components/carrier-connection-dialog.tsx` | Add MetafieldEditor |

### Appendix B: Dynamic Value Input Mapping

| MetafieldTypeEnum | Input Component | Validation |
|-------------------|-----------------|------------|
| `text` | `<Input type="text">` | Required check only |
| `number` | `<Input type="number">` | Numeric validation |
| `boolean` | `<Checkbox>` | None (always valid) |
| `json` | `<Textarea>` | JSON.parse validation |
| `date` | `<Input type="date">` | Date format validation |
| `date_time` | `<Input type="datetime-local">` | DateTime format validation |
| `password` | `<Input type="password">` | Required check only |
