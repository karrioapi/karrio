# Product Requirements Document: Rate Sheet Editor Parity Upgrade

**Project**: Karrio Rate Sheet Editor — Port JTL Improvements & Fix Gaps
**Version**: 1.0
**Date**: 2026-02-13
**Status**: Planning
**Owner**: Engineering Team
**Priority**: High

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Critical Bug Fixes](#critical-bug-fixes)
4. [Service Editor Gaps](#service-editor-gaps)
5. [UX Improvements](#ux-improvements)
6. [Feature Parity Items](#feature-parity-items)
7. [Implementation Plan](#implementation-plan)
8. [File Inventory](#file-inventory)
9. [Verification Checklist](#verification-checklist)

---

## Executive Summary

The JTL shipping-app (`apps/shipping-app`) has undergone significant iteration on its Rate Sheet Editor, resulting in many bug fixes, UX improvements, and new features that have NOT been ported to the Karrio packages editor (`karrio/packages/ui/components/rate-sheet-editor.tsx`). This PRD documents every gap between the two editors and provides a surgical implementation plan.

### Scope

**Source of truth** (reference): `apps/shipping-app/src/modules/shipping/components/`
**Target** (to be upgraded): `karrio/packages/ui/components/` + `karrio/packages/hooks/`

### Key Files (Karrio — Target)

| File | Lines | Purpose |
|------|-------|---------|
| `rate-sheet-editor.tsx` | ~2637 | Main editor component |
| `service-rate-detail-view.tsx` | ~552 | Per-service rate grid |
| `weight-rate-grid.tsx` | ~436 | Collapsible global grid |
| `modals/service-editor-modal.tsx` | ~400+ | Service create/edit modal |
| `zone-editor-dialog.tsx` | ~214 | Zone editor |
| `surcharge-editor-dialog.tsx` | ~234 | Surcharge editor |
| `surcharges-tab.tsx` | ~229 | Surcharges CRUD tab |
| `add-weight-range-dialog.tsx` | ~137 | Weight range creation |
| `add-weight-range-popover.tsx` | ~131 | Weight range quick-add |
| `edit-weight-range-dialog.tsx` | ~100+ | Weight range editing |
| `add-service-popover.tsx` | ~109 | Service quick-add popover |
| `multi-select.tsx` | ~215 | Multi-option selector |
| `rate-sheet-csv-preview.tsx` | ~400+ | CSV/spreadsheet preview |

### Key Files (JTL — Reference)

| File | Lines | Purpose |
|------|-------|---------|
| `RateSheetEditor.tsx` | ~3055 | Main editor (reference) |
| `ServiceEditorDialog.tsx` | ~900+ | Service editor with 6 tabs |
| `ServiceRateDetailView.tsx` | ~550 | Per-service rate grid |
| `SurchargesTab.tsx` | ~222 | Surcharges tab |
| `SurchargeEditorDialog.tsx` | ~300+ | Surcharge editor |
| `ZoneEditorDialog.tsx` | ~200+ | Zone editor |
| `AddWeightRangeDialog.tsx` | ~150+ | Weight range dialog |
| `AddWeightRangePopover.tsx` | ~130+ | Weight range popover |
| `EditWeightRangeDialog.tsx` | ~100+ | Weight range editing |
| `AddServicePopover.tsx` | ~109 | Service popover |
| `MultiSelect.tsx` | ~210 | Multi-select component |
| `FeaturesEditor.tsx` | ~250+ | Visual features editor |
| `Modal.tsx` | ~120 | Reusable modal (z-[100]) |
| `ConfirmDialog.tsx` | ~80+ | Confirmation dialog |
| `RateSheetCsvPreview.tsx` | ~400+ | CSV preview |

---

## Architecture Overview

Both editors share the same fundamental architecture:

- **Sheet-based layout**: Full-screen Radix Sheet with left sidebar + main content
- **Tabs**: Rate Sheet | Surcharges (top level) + Service sub-tabs (horizontal scroll)
- **Staged/committed pattern**: New objects staged in dialog, committed on save
- **Optimistic updates**: `editModeRatesOverride` overlays server data in edit mode
- **Per-service weight ranges**: `editModePendingRanges` tracks locally-added ranges
- **Refs for save detection**: `zoneSaveRef` / `surchargeSaveRef` distinguish save vs cancel

The JTL editor has diverged in several critical areas documented below.

---

## Critical Bug Fixes

### BUG-1: Service clone uses `service_code` for matching (breaks with duplicates)

**Severity**: Critical
**File**: `rate-sheet-editor.tsx` — `handleSaveService` (line ~848)

**Current Karrio Behavior**:
```javascript
setServices((prev) =>
  prev.map((s) =>
    s.service_code === selectedService.service_code
      ? { ...s, ...serviceData }
      : s
  )
);
```
When saving a cloned service, this matches by `service_code`. Since the clone shares the same `service_code` as the original, **both** services get updated with the clone's data, corrupting the original.

**JTL Fix** (reference `RateSheetEditor.tsx:710-718`):
```javascript
setServices((prev) =>
  prev.map((s) =>
    s.id === selectedService.id
      ? { ...s, ...serviceData }
      : s
  )
);
```
Match by `id` (which is always unique).

**Acceptance Criteria**:
- [ ] Editing a cloned service does not modify the original
- [ ] Editing the original does not modify the clone
- [ ] Both services retain independent data after save

---

### BUG-2: Service deletion uses `service_code` (deletes all services with same code)

**Severity**: Critical
**File**: `rate-sheet-editor.tsx` — `handleConfirmDelete` (line ~943)

**Current Karrio Behavior**:
```javascript
setServices((prev) =>
  prev.filter((s) => s.service_code !== serviceToDelete.service_code)
);
```
Deleting a clone removes ALL services with the same `service_code`, including the original.

**JTL Fix**:
```javascript
setServices((prev) =>
  prev.filter((s) => s.id !== serviceToDelete.id)
);
```

**Acceptance Criteria**:
- [ ] Deleting a cloned service keeps the original intact
- [ ] Deleting the original keeps the clone intact

---

### BUG-3: Clone service in edit mode has no rates

**Severity**: Critical
**File**: `rate-sheet-editor.tsx` — `handleCloneService` (line ~823)

**Current Karrio Behavior**:
```javascript
const clonedRates = localServiceRates
  .filter(sr => sr.service_id === service.id)
  .map(sr => ({ ...sr, service_id: newId }));
setLocalServiceRates((prev) => [...prev, ...clonedRates]);
```
In edit mode, `localServiceRates` is empty (only used in create mode). The clone gets zero rates. Additionally, the clone is immediately added to `services` before the dialog opens, which breaks the staged pattern.

**JTL Fix** (reference `RateSheetEditor.tsx:685-700`):

1. Clone rates from `serviceRatesData` (which includes the overlay), not just `localServiceRates`
2. Store cloned rates in `pendingServiceRates` (new state variable)
3. Do NOT add the clone to `services` immediately — only set `selectedService` + open dialog
4. On dialog save, add clone to services AND add pending rates to `editModeRatesOverride`

**Required State Addition**:
```typescript
const [pendingServiceRates, setPendingServiceRates] = useState<ServiceRate[]>([]);
```

**Required `handleCloneService` Rewrite**:
```javascript
const handleCloneService = (service) => {
  const newId = generateId("service");
  const newService = { ...service, id: newId, service_name: `${service.service_name} (copy)` };
  const clonedRates = serviceRatesData
    .filter(sr => sr.service_id === service.id)
    .map(sr => ({ ...sr, service_id: newId }));
  // Stage — don't add to services yet
  setPendingServiceRates(clonedRates);
  setSelectedService(newService);
  setServiceDialogOpen(true);
};
```

**Required `handleSaveService` Rewrite** (3-path pattern):
```javascript
const handleSaveService = (serviceData) => {
  const isExistingInList = selectedService && services.some(s => s.id === selectedService.id);

  if (selectedService && isExistingInList) {
    // Path 1: Edit existing service
    setServices(prev => prev.map(s => s.id === selectedService.id ? { ...s, ...serviceData } : s));
  } else if (selectedService) {
    // Path 2: New from clone/preset — add to list now
    const merged = { ...selectedService, ...serviceData };
    setServices(prev => [...prev, merged]);
    setDetailServiceId(merged.id); // Select new tab
    if (pendingServiceRates.length > 0) {
      if (isEditMode) {
        setEditModeRatesOverride(prev => {
          const base = prev ?? (existingRateSheet?.service_rates ?? []);
          return [...base, ...pendingServiceRates];
        });
      } else {
        setLocalServiceRates(prev => [...prev, ...pendingServiceRates]);
      }
      setPendingServiceRates([]);
    }
  } else {
    // Path 3: Brand new service
    const newService = { id: generateId('service'), ...serviceData, zones: [defaultZone] };
    setServices(prev => [...prev, newService]);
    setDetailServiceId(newService.id);
  }
  setServiceDialogOpen(false);
  setSelectedService(null);
  setPendingServiceRates([]);
};
```

**Acceptance Criteria**:
- [ ] Cloning a service in edit mode copies all weight ranges and rates
- [ ] Cloned rates are visible immediately in the rate grid
- [ ] Cloned rates survive save and are persisted to backend
- [ ] Cancelling the clone dialog discards pending rates

---

### BUG-4: New/cloned service tab not auto-selected

**Severity**: Medium
**File**: `rate-sheet-editor.tsx` — `handleSaveService`

**Current Karrio Behavior**: After creating or cloning a service, the user stays on whatever tab was previously active. They have to manually click the new service's tab.

**JTL Fix**: After adding a new service, call `setDetailServiceId(newService.id)` to auto-select its tab.

**Acceptance Criteria**:
- [ ] Creating a new service selects its tab
- [ ] Cloning a service selects the clone's tab
- [ ] Adding from preset selects the new service's tab

---

### BUG-5: `handleSaveService` edit path has no `isExistingInList` guard

**Severity**: High
**File**: `rate-sheet-editor.tsx` — `handleSaveService` (line ~844)

**Current Karrio Behavior**: The `selectedService` check doesn't distinguish between "editing existing in list" and "saving a newly staged clone". When `selectedService` is set (either for edit or clone), it always takes the edit path.

**JTL Fix**: Add `isExistingInList` check:
```javascript
const isExistingInList = selectedService && services.some(s => s.id === selectedService.id);
```
This creates three distinct paths (see BUG-3 for full implementation).

---

### BUG-6: `handleConfirmDelete` doesn't distinguish staged vs backend services

**Severity**: Medium
**File**: `rate-sheet-editor.tsx` — `handleConfirmDelete` (line ~912)

**Current Karrio Behavior**: Uses `serviceToDelete.id.startsWith("temp-")` but doesn't check for `service-` prefix IDs (from `generateId("service")`).

**JTL Fix**: Check both prefixes:
```javascript
const isBackendService = isEditMode &&
  originalStateRef.current?.serviceFields?.has(serviceToDelete.id);
```
(Requires `serviceFields` in `OriginalState` — see FEAT-3.)

---

## Service Editor Gaps

### GAP-1: Missing `transit_label` field (customer-facing transit label)

**Severity**: Medium
**File**: `modals/service-editor-modal.tsx`

**JTL Implementation** (`ServiceEditorDialog.tsx:52-58`):
```javascript
const TRANSIT_LABEL_OPTIONS = [
  { value: NONE_VALUE, label: "Not specified" },
  { value: "best_effort", label: "Best effort" },
  { value: "next_day", label: "Next day" },
  { value: "within_24h", label: "Within 24h" },
  { value: "within_48h", label: "Within 48h" },
];
```
Rendered as a `<Select>` dropdown on the Transit tab with description: "Displayed to customers in shipping rates".

**Required Changes**:
- Add `transit_label` to service form data
- Add Select dropdown on Transit tab
- Include in `featuresToObject()` output
- Already supported by backend (`ServiceLevelFeaturesInput` has `transit_label`)

---

### GAP-2: Missing `shipment_type` field (Outbound/Returns)

**Severity**: Medium
**File**: `modals/service-editor-modal.tsx`

**JTL Implementation** (`ServiceEditorDialog.tsx:46-50`):
```javascript
const SHIPMENT_TYPE_OPTIONS = [
  { value: NONE_VALUE, label: "Not specified" },
  { value: "outbound", label: "Outbound" },
  { value: "returns", label: "Returns" },
];
```
Rendered as a `<Select>` on the Logistics tab.

**Required Changes**:
- Add `shipment_type` to form data
- Add Select on Logistics tab
- Include in `featuresToObject()` output

---

### GAP-3: Missing `neighbor_delivery` and `labelless` feature flags

**Severity**: Medium
**File**: `modals/service-editor-modal.tsx`

**JTL Implementation** (`ServiceEditorDialog.tsx:29-42`):
The `SERVICE_FEATURES` array includes 12 features:
```
tracked, b2c, b2b, signature, insurance, express,
dangerous_goods, saturday_delivery, sunday_delivery,
multicollo, neighbor_delivery, labelless
```

**Current Karrio**: Missing `neighbor_delivery` and `labelless`. Only has the first 10.

**Required Changes**:
- Add to `SERVICE_FEATURES` array
- Add to `extractFeaturesArray()` function
- Already supported by backend GraphQL schema

---

### GAP-4: Missing `age_check` field

**Severity**: Low
**File**: `modals/service-editor-modal.tsx`

**JTL Implementation** (`ServiceEditorDialog.tsx:60-64`):
```javascript
const AGE_CHECK_OPTIONS = [
  { value: NONE_VALUE, label: "Not required" },
  { value: "16", label: "16+" },
  { value: "18", label: "18+" },
];
```

**Required Changes**:
- Add `age_check` to form data
- Add Select on Logistics tab
- Include in `featuresToObject()` output

---

### GAP-5: Form factor options mismatch

**Severity**: Low
**File**: `modals/service-editor-modal.tsx`

**JTL Implementation** (`ServiceEditorDialog.tsx:80-85`):
```javascript
const FORM_FACTOR_OPTIONS = [
  { value: NONE_VALUE, label: "Not specified" },
  { value: "parcel", label: "Parcel" },
  { value: "mailbox", label: "Mailbox" },
  { value: "pallet", label: "Pallet" },
];
```

**Current Karrio**: May have "Envelope" instead of "Mailbox". Needs verification and alignment.

---

### GAP-6: Service editor tab structure

**Severity**: Medium
**File**: `modals/service-editor-modal.tsx`

**JTL has 6 tabs** (`ServiceEditorDialog.tsx:131`):
1. **General**: Name, code, carrier code, description, currency, domicile/international/active
2. **Transit**: Transit days, transit time, **transit_label** (customer-facing)
3. **Features**: MultiSelect with 12 features
4. **Logistics**: First mile, last mile, form factor, age check, **shipment_type**
5. **Limits**: Weight (max, unit), dimensions (L×W×H, unit), volumetric weight (toggle + dim factor)
6. **Surcharges** (conditional): Linked surcharge checkboxes

**Current Karrio**: Verify tab structure matches. Likely missing Transit tab fields and Logistics tab fields.

---

### GAP-7: Default currency EUR vs USD

**Severity**: Low
**File**: `modals/service-editor-modal.tsx`

**JTL**: Default currency is `EUR` (European market focus)
**Karrio**: Default currency is `USD`

This may be intentional (different markets), but should be verified for consistency.

---

## UX Improvements

### UX-1: Weight range min defaults to 0

**Severity**: Medium
**File**: `add-weight-range-dialog.tsx`

**Current Karrio** (line 42-45):
```javascript
const derivedMinWeight =
  existingRanges.length > 0
    ? Math.max(...existingRanges.map((r) => r.max_weight))
    : 0;
```
Min weight is derived from the highest existing max_weight. Users wanted it to always be 0.

**JTL Fix** (`AddWeightRangeDialog.tsx:26`): Hardcodes `suggestedMin = 0`.

**Acceptance Criteria**:
- [ ] Custom weight range dialog always shows min_weight = 0 by default
- [ ] User can still modify min_weight
- [ ] Existing ranges still shown in AddWeightRangePopover for quick-add

---

### UX-2: Features MultiSelect dropdown too small

**Severity**: Low
**File**: `multi-select.tsx`

**Current Karrio** (line 168): `max-h-72` — already at 288px which is the JTL target.

**JTL Fix**: If Karrio already has `max-h-72`, this may already be at parity. Verify. If it still uses Command component with different max-height, adjust accordingly.

---

### UX-3: Features section needs description text

**Severity**: Low
**File**: Service editor — Features tab

**JTL Implementation**: Added helper text "Select the capabilities this service supports" and increased section padding (`space-y-4 py-2` instead of `space-y-3`).

---

## Feature Parity Items

### FEAT-1: `originalStateRef` needs `serviceFields` tracking

**Severity**: Medium
**File**: `rate-sheet-editor.tsx`

**Current Karrio `OriginalState`**:
```typescript
interface OriginalState {
  name: string;
  zones: Map<string, EmbeddedZone>;
  surcharges: Map<string, SharedSurcharge>;
  serviceRates: Map<string, { rate: number; cost?: number | null }>;
  serviceZoneIds: Map<string, string[]>;
  serviceSurchargeIds: Map<string, string[]>;
}
```

**JTL Addition**: `serviceFields: Map<string, { currency, features, use_volumetric, dim_factor, active, description, transit_days, ... }>` — tracks all service-level field values at load time. Used for:
1. Detecting service field changes to trigger full update vs granular updates
2. Distinguishing staged (not in `serviceFields`) vs backend services

**Required Changes**:
- Add `serviceFields` to `OriginalState` interface
- Populate during edit mode load
- Use in `handleConfirmDelete` to detect staged vs backend services
- Use in save flow to detect service field changes

---

### FEAT-2: `pendingServiceRates` state for staged clone rates

**Severity**: Critical (needed for BUG-3 fix)
**File**: `rate-sheet-editor.tsx`

Add `pendingServiceRates` state variable and wire it into:
- `handleCloneService` (populate)
- `handleSaveService` (consume and apply to overlay)
- `handleAddServiceFromPreset` (populate for edit mode presets)
- ServiceEditorDialog `onOpenChange` cancel handler (clear)

---

### FEAT-3: Granular vs full update save path

**Severity**: Medium
**File**: `rate-sheet-editor.tsx`

**JTL Implementation** (`RateSheetEditor.tsx:2109`): The edit mode save flow has two paths:

1. **Granular updates** (when only rate/zone/surcharge changes): Individual mutations for each changed entity — much smaller payloads
2. **Full update** (when structural changes: new/deleted services, zones, surcharges, or service field changes): Single `updateRateSheet` mutation with complete payload

**Current Karrio**: Verify which path(s) exist. If only full update, consider adding granular path for performance.

---

### FEAT-4: CSV Preview — surcharge columns

**Severity**: Low
**File**: `rate-sheet-csv-preview.tsx`

**JTL Implementation**: CSV preview includes dynamic surcharge columns per linked surcharge, showing surcharge amounts alongside base rates.

**Current Karrio**: Verify if surcharge columns are included. Port if missing.

---

## Implementation Plan

### Phase 1: Critical Bug Fixes (Highest Priority)

| ID | Issue | File | Effort |
|----|-------|------|--------|
| BUG-1 | `handleSaveService` matches by `service_code` | `rate-sheet-editor.tsx` | Low |
| BUG-2 | `handleConfirmDelete` matches by `service_code` | `rate-sheet-editor.tsx` | Low |
| BUG-3 | Clone in edit mode has no rates | `rate-sheet-editor.tsx` | High |
| BUG-4 | New service tab not auto-selected | `rate-sheet-editor.tsx` | Low |
| BUG-5 | Missing `isExistingInList` guard | `rate-sheet-editor.tsx` | Medium |

### Phase 2: Service Editor Parity

| ID | Issue | File | Effort |
|----|-------|------|--------|
| GAP-1 | Add `transit_label` field | `service-editor-modal.tsx` | Medium |
| GAP-2 | Add `shipment_type` field | `service-editor-modal.tsx` | Medium |
| GAP-3 | Add `neighbor_delivery` + `labelless` features | `service-editor-modal.tsx` | Low |
| GAP-4 | Add `age_check` field | `service-editor-modal.tsx` | Low |
| GAP-5 | Fix form factor options | `service-editor-modal.tsx` | Low |
| GAP-6 | Verify tab structure matches | `service-editor-modal.tsx` | Medium |

### Phase 3: UX & Polish

| ID | Issue | File | Effort |
|----|-------|------|--------|
| UX-1 | Weight range min defaults to 0 | `add-weight-range-dialog.tsx` | Low |
| UX-2 | Features dropdown sizing | `multi-select.tsx` | Low |
| UX-3 | Features section description | `service-editor-modal.tsx` | Low |

### Phase 4: Feature Parity

| ID | Issue | File | Effort |
|----|-------|------|--------|
| FEAT-1 | Add `serviceFields` to OriginalState | `rate-sheet-editor.tsx` | Medium |
| FEAT-2 | Add `pendingServiceRates` state | `rate-sheet-editor.tsx` | Medium |
| FEAT-3 | Granular vs full update save | `rate-sheet-editor.tsx` | High |
| FEAT-4 | CSV surcharge columns | `rate-sheet-csv-preview.tsx` | Low |

---

## File Inventory

### Files Requiring Modification

| File | Changes |
|------|---------|
| `karrio/packages/ui/components/rate-sheet-editor.tsx` | BUG-1–5, FEAT-1–3 |
| `karrio/packages/ui/components/modals/service-editor-modal.tsx` | GAP-1–6, UX-3 |
| `karrio/packages/ui/components/add-weight-range-dialog.tsx` | UX-1 |
| `karrio/packages/ui/components/multi-select.tsx` | UX-2 (verify) |
| `karrio/packages/ui/components/rate-sheet-csv-preview.tsx` | FEAT-4 |

### Files for Reference Only (JTL Source)

| File | Key Patterns to Port |
|------|---------------------|
| `apps/.../RateSheetEditor.tsx` | 3-path handleSaveService, pendingServiceRates, serviceFields |
| `apps/.../ServiceEditorDialog.tsx` | 6-tab structure, transit_label, shipment_type, age_check |
| `apps/.../FeaturesEditor.tsx` | Visual feature toggles (alternative to MultiSelect) |
| `apps/.../Modal.tsx` | z-[100] portal, ESC stopImmediatePropagation |
| `apps/.../ConfirmDialog.tsx` | Reusable confirm/cancel dialog |

---

## Verification Checklist

### After Phase 1 (Bug Fixes)

- [ ] Clone a service in edit mode → weight ranges and rates visible immediately
- [ ] Save the rate sheet → reopen → cloned service's rates are preserved
- [ ] Clone two services with the same service_code → both maintain independent data
- [ ] Delete a clone → original service is unaffected
- [ ] Delete the original → clone is unaffected
- [ ] Create/clone a service → its tab is auto-selected
- [ ] Cancel the clone dialog → no orphaned service in the tabs

### After Phase 2 (Service Editor)

- [ ] Transit tab shows transit_label dropdown with 4 options
- [ ] Logistics tab shows shipment_type (Outbound/Returns)
- [ ] Logistics tab shows age_check (Not required/16+/18+)
- [ ] Features tab shows 12 features including neighbor_delivery and labelless
- [ ] Form factor shows Mailbox (not Envelope)
- [ ] All new fields persist after save and display on reopen

### After Phase 3 (UX)

- [ ] Add Weight Range dialog defaults min to 0
- [ ] Features MultiSelect shows all 12 features without excessive scrolling
- [ ] Features tab has description text

### After Phase 4 (Feature Parity)

- [ ] Editing only a rate cell → granular mutation (small payload)
- [ ] Adding a new service → full update mutation (complete payload)
- [ ] CSV preview shows surcharge columns
- [ ] Service field changes (currency, features) detected correctly

---

## Items Deferred (Not in Scope)

| Item | Reason |
|------|--------|
| Service reordering (up/down arrows) | Needs backend `sort_order` field |
| Service tab order after save | Depends on backend order preservation |
| FeaturesEditor visual toggle component | Nice-to-have, MultiSelect is functional |
