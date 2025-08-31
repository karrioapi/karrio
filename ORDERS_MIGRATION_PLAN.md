# Orders List Page: Complete Bulma to shadcn/ui Migration Plan

## Overview
This document provides a comprehensive step-by-step plan to migrate the Orders list page (`/packages/core/modules/Orders/index.tsx`) from Bulma CSS framework to shadcn/ui components, following the exact same structure and patterns used in the migrated Shipments page (`/packages/core/modules/Shipments/index.tsx`).

## Component Analysis & Replacements

### Current Bulma Components → shadcn/ui Replacements

| Current Bulma Component | shadcn/ui Replacement | Status | Reference Location |
|------------------------|----------------------|--------|-------------------|
| `<header className="columns">` | `<header className="flex flex-col sm:flex-row">` | ✅ **COMPLETED** | Shipments page header |
| `<span className="title is-4">` | `<h1 className="text-2xl font-semibold">` | ✅ **COMPLETED** | Shipments page header |
| `<button className="button is-primary is-small">` | `<Button size="sm">` | ✅ **COMPLETED** | Shipments page buttons |
| `<div className="tabs">` | `<FiltersCard>` | ✅ **COMPLETED** | Shipments page filters |
| `<table className="table is-fullwidth">` | `<Table>` in `<StickyTableWrapper>` | ✅ **COMPLETED** | Shipments page table |
| `<input type="checkbox">` | `<Checkbox>` | ✅ **COMPLETED** | Shipments page checkboxes |
| `<StatusBadge>` (Bulma-based) | `<ShipmentsStatusBadge>` (reused shadcn) | ✅ **COMPLETED** | Reused existing shadcn component |
| `<OrdersFilter>` (Bulma-based) | `<OrdersFilter>` (new ShadCN version) | ✅ **COMPLETED** | Migrated to ShadCN Popover |
| `<Spinner>` (loading) | `<Skeleton>` | ✅ **COMPLETED** | Shipments page loading |
| Bulma pagination buttons | Custom Tailwind buttons | ✅ **COMPLETED** | Custom pagination implemented |
| `<ConfirmModal>` | `<ConfirmationDialog>` | ✅ **COMPLETED** | ShipmentMenu component |

### Components Analysis

#### OrderMenu Component Status
- **Modern Version**: `/packages/ui/components/order-menu.tsx` 
  - ✅ Already migrated to shadcn/ui (uses DropdownMenu, Button, etc.)
  - ✅ **FIXED**: Hover issues resolved by converting AppLink items to onClick handlers
  - ❌ Minor issue: Still uses old `ConfirmModalContext` - should use `ConfirmationDialog` pattern like ShipmentMenu
  - ✅ **Currently used by Orders list page** - no changes needed for our migration

- **Legacy Version**: `/packages/ui/core/components/order-menu.tsx`
  - ❌ Old Bulma-based version with custom dropdown logic
  - Used by individual order view page (`/packages/core/modules/Orders/order.tsx`)
  - Outside scope of this migration

### Components Needing Creation

#### 1. StatusBadge Migration ✅ **COMPLETED**
- **Solution**: Reuse existing `ShipmentsStatusBadge` component
- **Reason**: Identical color mappings and status support
- **No new component needed**: Avoids code duplication

#### 2. OrdersFilter Component ✅ **COMPLETED**
- **Path**: `/packages/ui/components/orders-filter.tsx` 
- **Based on**: `/packages/ui/components/shipments-filter.tsx`
- **Purpose**: Advanced filtering for orders with shadcn/ui components
- **Status**: Successfully created with ShadCN Popover, Button, Checkbox, Input, and Label components

---

## Recent Migration Work Completed

### OrdersFilter ShadCN Migration ✅ **COMPLETED**
**Date**: Recently completed
**File Created**: `/packages/ui/components/orders-filter.tsx`

**Technical Implementation**:
- **Framework**: Built using ShadCN UI components (Popover, Button, Checkbox, Input, Label)
- **Design Pattern**: Followed shipments-filter.tsx structure for consistency
- **Filter Fields Implemented**:
  - Address filter with text input
  - Order ID filter with comma-separated support
  - Source filter with comma-separated support (shopify, erp, etc.)
  - Date range filter (created_before, created_after)
  - Status multi-select using ORDER_STATUSES from @karrio/types
- **Features**: Clear/Done buttons, loading states, proper form validation
- **Integration**: Successfully imported and used in orders module

### OrderMenu Hover Issues Fix ✅ **COMPLETED**  
**Date**: Recently completed
**File Modified**: `/packages/ui/components/order-menu.tsx`

**Technical Solution**:
- **Problem**: AppLink components with `asChild` prop not inheriting ShadCN hover styles
- **Root Cause**: AppLink's nested `Link > a` structure preventing hover state propagation
- **Solution**: Converted AppLink items to onClick handlers (matching ShipmentMenu pattern)
- **Changes Made**:
  - Created `navigateToCreateLabel()` and `navigateToEditOrder()` functions using router.push()
  - Replaced `<DropdownMenuItem asChild><AppLink>` with `<DropdownMenuItem onClick={handler}>`
  - Removed unused AppLink import
  - Added proper cursor-pointer classes
- **Result**: All menu items now have consistent hover effects

---

## Step-by-Step Migration Plan

### Phase 1: Header Section Migration ✅ **COMPLETED**

#### Step 1.1: Replace Header Layout ✅ **COMPLETED**
**Target Section**: Lines 265-284 in Orders/index.tsx

**Current**:
```jsx
<header className="columns px-0 pb-0 pt-4">
  <div className="column">
    <span className="title is-4">Orders</span>
  </div>
  <div className="column has-text-right-desktop">
```

**Replace with**:
```jsx
<header className="flex flex-col sm:flex-row sm:items-center sm:justify-between px-0 pb-0 pt-4 mb-2">
  <div className="mb-4 sm:mb-0">
    <h1 className="text-2xl font-semibold text-gray-900">Orders</h1>
  </div>
  <div className="flex flex-row items-center gap-1 flex-wrap">
```

#### Step 1.2: Replace Header Buttons
**Target**: Convert all Bulma buttons to shadcn/ui Button components

**Tasks**:
- Replace `className="button is-primary is-small mx-1"` with `Button` component
- Update "Create order" button styling
- Update "Manage manifests" button styling
- Replace old `OrdersFilter` with new shadcn-based version

### Phase 2: Filter Cards Migration ✅ **COMPLETED**  

#### Step 2.1: Remove Bulma Tabs Structure
**Target Section**: Lines 286-362 in Orders/index.tsx

**Tasks**:
- Remove entire `<div className="tabs">` structure
- Remove all tab-related click handlers and active states
- Remove manual tab styling classes

#### Step 2.2: Implement FiltersCard Component
**Add after header section**:

```jsx
<FiltersCard
  filters={getFilterOptions()}
  activeFilter={filter?.status || []}
  onFilterChange={(status) => updateFilter({ status, offset: 0 })}
/>
```

**Define filter options**:
```jsx
const getFilterOptions = () => [
  {
    label: "All",
    value: []
  },
  {
    label: "Unfulfilled", 
    value: ["unfulfilled", "partial"]
  },
  {
    label: "Fulfilled",
    value: ["fulfilled", "delivered"]
  },
  {
    label: "Cancelled", 
    value: ["cancelled"]
  },
  {
    label: "Draft",
    value: [{source: "draft"}]
  }
];
```

### Phase 3: Loading State Migration ✅ **COMPLETED**

#### Step 3.1: Replace Spinner with Skeleton
**Target Section**: Line 364 in Orders/index.tsx

**Current**:
```jsx
{!query.isFetched && <Spinner />}
```

**Replace with**:
```jsx
{!query.isFetched && (
  <div className="bg-white rounded-lg shadow-sm border my-6 p-6">
    <div className="space-y-4">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="flex items-center space-x-4">
          <Skeleton className="h-4 w-4" />
          <Skeleton className="h-4 w-[100px]" />
          <Skeleton className="h-4 w-[80px]" />
          <Skeleton className="h-4 w-[120px]" />
          <Skeleton className="h-4 w-[100px]" />
          <Skeleton className="h-4 w-[80px]" />
          <Skeleton className="h-4 w-6" />
        </div>
      ))}
    </div>
  </div>
)}
```

### Phase 4: Table Structure Migration ✅ **COMPLETED**

#### Step 4.1: Replace Table Container
**Target Section**: Lines 368-602 in Orders/index.tsx

**Current**:
```jsx
<div className="table-container">
  <table className="orders-table table is-fullwidth">
```

**Replace with**:
```jsx
<StickyTableWrapper>
  <Table className="orders-table">
    <TableHeader>
    <TableBody>
  </Table>
</StickyTableWrapper>
```

#### Step 4.2: Migrate Table Header
**Tasks**:
- Replace `<tbody><tr>` with `<TableHeader><TableRow>`
- Replace `<td>` with `<TableHead>`
- Update checkbox column with shadcn/ui Checkbox
- Update column headers with proper classes
- Add sticky column classes where needed

**Target columns**:
- Checkbox column: `sticky-left` class
- Order # column
- Status column  
- Items column
- Ship To column
- Total column
- Date column
- Shipping Service column
- Action column: `sticky-right` class

#### Step 4.3: Migrate Bulk Actions Row
**Target**: Lines 386-434 in Orders/index.tsx

**Tasks**:
- Replace Bulma button groups with shadcn/ui Button components
- Update button styling from `button is-small is-default` to `Button variant="outline" size="sm"`
- Keep existing functionality for:
  - Print Labels
  - Print Invoices  
  - Document templates
- Maintain conditional rendering logic

#### Step 4.4: Migrate Table Body Rows
**Target**: Lines 458-599 in Orders/index.tsx

**Tasks**:
- Replace `<tr>` with `<TableRow>`
- Replace `<td>` with `<TableCell>`
- Update checkbox column with shadcn/ui Checkbox component
- Replace `StatusBadge` with `ShipmentsStatusBadge`
- Keep all existing logic for:
  - Order ID and source display
  - Line items calculation
  - Address formatting
  - Price calculation
  - Date formatting
  - Shipping service computation
- Update click handlers to work with new structure
- Add hover states and selection styling

#### Step 4.5: Update Event Handlers
**Tasks**:
- Update `handleSelection` function to work with shadcn/ui Checkbox
- Replace `ChangeEvent` pattern with `onCheckedChange` callback
- Create `handleCheckboxChange` function matching shipments page pattern:

```jsx
const handleCheckboxChange = (checked: boolean, name: string) => {
  if (name === "all") {
    setSelection(
      !checked
        ? []
        : (orders?.edges || []).map(({ node: { id } }) => id),
    );
  } else {
    setSelection(
      checked
        ? [...selection, name]
        : selection.filter((id) => id !== name),
    );
  }
};
```

### Phase 5: Pagination Migration ✅ **COMPLETED**

#### Step 5.1: Remove Bulma Pagination ✅ **COMPLETED**
**Target Section**: Lines 604-629 in Orders/index.tsx

**Tasks**:
- ✅ Remove entire Bulma pagination structure
- ✅ Remove manual Previous/Next button handlers

#### Step 5.2: Add Sticky Footer with ListPagination ✅ **COMPLETED**
**Add after table closing tag**:

```jsx
{/* Sticky Footer */}
<div className="sticky bottom-0 left-0 right-0 z-10 bg-white border-t border-gray-200 pb-16 md:pb-0">
  <ListPagination
    currentOffset={filter.offset as number || 0}
    pageSize={20}
    totalCount={orders?.page_info?.count || 0}
    hasNextPage={orders?.page_info?.has_next_page || false}
    onPageChange={(offset) => updateFilter({ offset })}
    className="px-2 py-3"
  />
</div>
```

### Phase 6: Empty State Migration ✅ **COMPLETED**

#### Step 6.1: Replace Empty State Card
**Target Section**: Lines 633-639 in Orders/index.tsx

**Current**:
```jsx
<div className="card my-6">
  <div className="card-content has-text-centered">
    <p>No order found.</p>
  </div>
</div>
```

**Replace with**:
```jsx
<div className="bg-white rounded-lg shadow-sm border my-6">
  <div className="p-6 text-center">
    <p>No order found.</p>
  </div>
</div>
```

### Phase 7: Context Provider Updates

#### Step 7.1: Update Context Providers
**Target Section**: Lines 38-42 in Orders/index.tsx

**Tasks**:
- Remove `ConfirmModal` from bundleContexts (replaced with ConfirmationDialog)
- Keep `OrderPreview` and `ModalProvider`
- Update to match shipments page pattern if needed

### Phase 8: Import Updates

#### Step 8.1: Remove Bulma-dependent Imports
**Remove these imports**:
- `ConfirmModal` (replace with ConfirmationDialog pattern)
- `Spinner` (replace with Skeleton)
- Current `OrdersFilter` (replace with new version)

#### Step 8.2: Add shadcn/ui Imports
**Add these imports**:
```jsx
import { FiltersCard } from "@karrio/ui/components/filters-card";
import { ListPagination } from "@karrio/ui/components/list-pagination";
import { StickyTableWrapper } from "@karrio/ui/components/sticky-table-wrapper";
import { 
  Table, 
  TableHeader, 
  TableBody, 
  TableHead, 
  TableRow, 
  TableCell 
} from "@karrio/ui/components/ui/table";
import { Button } from "@karrio/ui/components/ui/button";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Skeleton } from "@karrio/ui/components/ui/skeleton";
import { ShipmentsStatusBadge } from "@karrio/ui/components/shipments-status-badge";
import { OrdersFilter } from "@karrio/ui/components/orders-filter";
```

### Phase 9: CSS Class Migration ✅ **COMPLETED**

#### Step 9.1: Global Class Replacements
**Replace throughout the file**:

| Bulma Class | Tailwind Replacement |
|-------------|---------------------|
| `columns` | `flex` or `grid` |
| `column` | `flex-1` or grid column classes |
| `is-fullwidth` | `w-full` |
| `has-text-centered` | `text-center` |
| `has-text-right-desktop` | `sm:text-right` |
| `has-text-weight-bold` | `font-bold` |
| `has-text-weight-semibold` | `font-semibold` |
| `has-text-info` | `text-blue-600` |
| `has-text-grey` | `text-gray-600` |
| `has-text-grey-dark` | `text-gray-700` |
| `is-size-7` | `text-xs` |
| `is-vcentered` | `items-center` |
| `is-clickable` | `cursor-pointer` |
| `px-0`, `py-0`, etc. | Keep same (already Tailwind) |

### Phase 10: Create Missing Components

#### Step 10.1: Reuse ShipmentsStatusBadge Component ✅ **COMPLETED**
**Approach**: Direct reuse instead of creating new component

**Benefits**:
- No code duplication
- Identical color mappings already exist:
  - `unfulfilled` → violet (`bg-violet-50 text-violet-500`)
  - `partial` → cyan (`bg-cyan-50 text-cyan-500`) 
  - `fulfilled` → green (`bg-green-50 text-green-500`)
  - `delivered` → green (`bg-green-50 text-green-500`)
  - `cancelled` → gray (`bg-gray-50 text-gray-500`)
  - `draft` → violet (`bg-violet-50 text-violet-500`)
- Already supports all order status types
- Maintains consistency across the application

#### Step 10.2: Create OrdersFilter Component ✅ **COMPLETED**
**File**: `/packages/ui/components/orders-filter.tsx`

**Tasks Completed**:
- ✅ Copied ShipmentsFilter component structure using ShadCN Popover
- ✅ Replaced filter fields to match order requirements:
  - **Address**: Filter by shipping address (same as shipments)
  - **Order ID**: Multi-input field for filtering by order_id
  - **Source**: Multi-input field for filtering by order source (shopify, erp, etc.)
  - **Date**: Date range with created_before, created_after (same as shipments)
  - **Status**: Uses `ORDER_STATUSES` from `@karrio/types` with checkbox multi-select
- ✅ Updated reducer logic for order-specific fields
- ✅ Updated form validation and placeholder text
- ✅ Implemented proper ShadCN styling with hover states
- ✅ Successfully integrated with orders module

#### Step 10.3: Update Orders Page to Use ShipmentsStatusBadge ✅ **COMPLETED**
**Tasks Completed**:
- ✅ Replaced `StatusBadge` import with `ShipmentsStatusBadge`
- ✅ Updated component usage in table rows
- ✅ Verified identical color mappings
- ✅ OrdersFilter migration completed successfully

### Phase 11: Testing & Validation

#### Step 11.1: Functional Testing Checklist
- [ ] All filter combinations work correctly
- [ ] Bulk selection (select all/individual) works
- [ ] Bulk actions (print labels, invoices, templates) function
- [ ] Order preview modal opens correctly
- [ ] Pagination works with proper counts
- [ ] Sorting and filtering state persists in URL
- [ ] Mobile responsive behavior works
- [ ] Loading states display properly
- [ ] Empty state displays correctly

#### Step 11.2: Visual Testing Checklist
- [ ] Page layout matches Shipments page structure
- [ ] Status badges display correct colors
- [ ] Filter cards match design
- [ ] Table columns are properly sized
- [ ] Sticky columns work on mobile
- [ ] Hover states work correctly
- [ ] Button styling is consistent
- [ ] Typography matches design system

#### Step 11.3: Code Quality Checklist
- [ ] No Bulma classes remain in the code
- [ ] All TypeScript errors resolved
- [ ] No console errors or warnings
- [ ] Component imports are correct
- [ ] Event handlers properly typed
- [ ] Accessibility attributes maintained

---

## Success Criteria
1. **Complete Bulma Removal**: No Bulma classes or components remain
2. **Feature Parity**: All existing functionality works identically  
3. **Visual Consistency**: Orders page matches Shipments page design patterns
4. **Mobile Responsive**: Table and filters work properly on all screen sizes
5. **Performance**: No regression in loading times or responsiveness
6. **Type Safety**: All TypeScript compilation passes without errors

## Files Summary

### Files Created:
1. ~~`/packages/ui/components/orders-status-badge.tsx`~~ (Not needed - reused ShipmentsStatusBadge)
2. ✅ `/packages/ui/components/orders-filter.tsx` - **COMPLETED**

### Files to Modify:
1. `/packages/core/modules/Orders/index.tsx` (complete migration)

### Reference Files:
1. `/packages/core/modules/Shipments/index.tsx` (structure reference)
2. `/packages/ui/components/shipments-status-badge.tsx` (component reference)
3. `/packages/ui/components/shipments-filter.tsx` (component reference)
4. `/packages/ui/components/filters-card.tsx` (reusable component)
5. `/packages/ui/components/list-pagination.tsx` (reusable component)
6. `/packages/ui/components/sticky-table-wrapper.tsx` (reusable component)