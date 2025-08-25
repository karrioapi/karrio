# Shipments List Migration Plan: Bulma to Shadcn + Tailwind

## **⚠️ IMPORTANT NOTES - MUST FOLLOW BEFORE EVERY STEP**

### **Critical Migration Guidelines**

1. **🔍 Always Verify Before Acting**
   - Do not assume anything
   - Always check the plan, old components, and functionalities before each step
   - Review existing code patterns and styles thoroughly
   - Ensure nothing is missed function-wise or style-wise

2. **✅ Checkpoint After Each Step**
   - After each step, ask for UI verification and testing
   - Test yourself against the old code to ensure everything works fine
   - Compare functionality side-by-side with original implementation
   - Validate all interactive elements and user flows

3. **🔒 Maintain Full Functional Parity**
   - Maintain full functional parity at all times
   - Every feature, handler, and interaction must work identically
   - No functionality should be lost or degraded during migration
   - Preserve all existing user experience patterns

4. **🧹 Clean Code Practices**
   - Do not introduce unnecessary changes or leave dead code
   - Follow best practices so the code is production-ready
   - Remove all Bulma references completely
   - Ensure code is maintainable and follows project conventions

5. **🎯 Complete Migration Goal**
   - The end goal is complete migration of the page to Shadcn
   - There should be no references to Bulma left anywhere
   - Whenever this page is tagged or the next step is taken, always keep these points in mind
   - Achieve 100% Shadcn + Tailwind implementation

6. **📁 Component Organization & Legacy Preservation**
   - All new shadcn equivalent components must be stored in `/packages/ui/components`
   - Legacy components should not be changed at all during migration
   - Create new shadcn components alongside existing legacy ones
   - Maintain clear separation between old and new implementations

### **Before Each Step Checklist**
- [ ] Review the current step in the migration plan
- [ ] Examine existing code and components being modified
- [ ] Understand all functionality that needs to be preserved
- [ ] Plan the exact changes needed without breaking anything
- [ ] Identify any dependencies or side effects

### **After Each Step Verification**
- [ ] Test all functionality works identically to before
- [ ] Verify visual appearance matches or improves upon original
- [ ] Check for any console errors or warnings
- [ ] Validate responsive behavior if applicable
- [ ] Confirm no dead code or unused imports remain
- [ ] Ask for user verification and approval before proceeding

---

## **Current Features Inventory**

### **Core Functionality**
- [x] Header with title "Shipments" and action buttons (Create Label, Manage manifests)
- [x] ShipmentsFilter dropdown for advanced filtering
- [x] Tab-based status filters (All, Purchased, Delivered, Exception, Cancelled, Draft)
- [x] Bulk selection with "select all" checkbox functionality
- [x] Bulk actions toolbar (Print Labels, Print Invoices, Document Templates)
- [x] Data table with columns: Checkbox, Service, Status, Recipient, Reference, Date, Actions
- [x] Clickable rows to preview shipments
- [x] Individual shipment actions via three-dot dropdown menu
- [x] Basic pagination (Previous/Next buttons with offset logic)
- [x] Loading states (Spinner) and empty state messaging
- [x] Responsive carrier images and status badges

### **Data Handling**
- [x] GraphQL shipments query with page_info for pagination
- [x] Real-time selection state management
- [x] URL parameter synchronization for filters
- [x] Preload next page functionality

## **Component Migration Priority**

### **⚠️ IMPORTANT: Component Categorization**
Since the draft order PR is not merged yet, we need to separate components by their usage:

### **Priority 1: Shipments-Specific Components (Start Here)**
1. **ShipmentsFilter** → shadcn Popover + Form + Checkbox + Input + Button
2. **Tab/Card filters** → Custom Card-style components (per reference images)  
3. **ShipmentPreview** → shadcn Dialog
4. **Bulk Actions Toolbar** → Custom shadcn component
5. **Main table structure** → shadcn Table components
6. **Enhanced Pagination** → shadcn component with row count display
7. **Sticky Table Wrapper** → Custom CSS + shadcn Table

### **Priority 2: Shipments-Specific Styling (No New Components)**
8. **CarrierImage**: Minimal styling updates for consistency
9. **Table layout and structure**: Bulma to Tailwind conversion

### **Priority 3: Shared Components (Defer Until Draft Order PR Merges)**
10. **StatusBadge** → shadcn Badge (shared with draft order)
11. **Spinner** → shadcn Skeleton (shared with draft order)
12. **AppLink** → shadcn Button styling (shared with draft order)
13. **ConfirmModal** → shadcn AlertDialog (shared with draft order)

### **No Migration Needed ✅**
- **ShipmentMenu**: Already uses shadcn DropdownMenu
- **useLoader**: Hook usage, no component migration needed

## **New Features Implementation**

### **1. Rows Count + Pagination Controls**
- **Bottom left**: "Viewing 1–20 of 50 results" format
- **Bottom right**: "Prev" and "Next" buttons  
- **Data source**: GraphQL `page_info.count` for accuracy
- **Component**: Create enhanced `ShipmentPagination` component

### **2. Card-Style Filters**
- **Convert tabs** → Card-based filter components
- **Reference**: Provided card filter screenshot
- **Implementation**: Individual clickable cards instead of tabs
- **Component**: Create `ShipmentFiltersCard` component

### **3. Sticky Columns**  
- **Left column**: Checkbox remains sticky during horizontal scroll
- **Right column**: Three-dot edit menu remains sticky  
- **Reference**: Provided sticky columns screenshot
- **Implementation**: CSS `position: sticky` with proper z-index

### **4. Mobile Responsiveness + Scrolling**
- **Consistent sizing**: Icons, text, row heights
- **Dual scrolling**: Both vertical and horizontal
- **Space optimization**: Minimize empty space without squashing content
- **Reference**: Provided scrolling screenshot

## **Migration Steps**

### **Phase 1: Environment Setup**
- [x] Review current Shadcn components available
- [x] Analyze shipments-specific components and requirements
- [x] Plan new component structure in `/packages/ui/components`

### **Phase 2: Shipments-Specific Components (Priority 1)**  
- [x] Replace Bulma header layout with Tailwind flex ✅ COMPLETED
- [ ] Migrate ShipmentsFilter to Shadcn Popover + Form components
- [x] Convert tab navigation to card-style filters ✅ COMPLETED (ShipmentFiltersCard)
- [ ] Create Bulk Actions Toolbar component
- [ ] Update ShipmentPreview to use Shadcn Dialog
- [ ] Convert basic Bulma classes (columns, containers, etc.)

### **Phase 3: Table Structure & Enhanced Features**
- [x] Replace `<table className="table is-fullwidth">` with Shadcn Table ✅ COMPLETED
- [x] Implement TableHeader, TableBody, TableRow, TableCell components ✅ COMPLETED
- [ ] Add sticky positioning for checkbox and actions columns
- [x] Create enhanced pagination with row count display ✅ COMPLETED (ShipmentPagination)
- [ ] Implement sticky column behavior with StickyTableWrapper
- [x] Maintain existing click handlers and selection logic ✅ COMPLETED
- [ ] Preserve row hover and selection states

### **Phase 4: Shipments-Specific Styling (Priority 2)**
- [ ] Update CarrierImage styling for consistency
- [ ] Convert remaining Bulma table layout to Tailwind
- [ ] Add mobile responsiveness improvements
- [ ] Optimize scrolling experience
- [ ] Test horizontal scroll with sticky columns

### **Phase 5: Integration & Testing (Shipments-Specific)**
- [ ] Verify all shipments-specific functionality preserved
- [ ] Test bulk selection and actions
- [ ] Validate responsive behavior across devices
- [ ] Check loading states and error handling
- [ ] Performance testing with large datasets

### **Phase 6: Shared Components (Deferred Until Draft Order PR Merges)**
- [ ] Replace StatusBadge with shadcn Badge (when available from draft order)
- [ ] Replace Spinner with Shadcn Skeleton (when available from draft order)  
- [ ] Update AppLink styling to use Shadcn Button patterns (when available from draft order)
- [ ] Convert ConfirmModal to Shadcn AlertDialog (when available from draft order)

### **Phase 7: Final Integration & Testing**
- [ ] Verify all existing functionality preserved
- [ ] Test bulk selection and actions
- [ ] Validate responsive behavior across devices
- [ ] Check loading states and error handling
- [ ] Performance testing with large datasets

## **New Components to Create**

### **1. ShipmentFiltersCard** ✅ COMPLETED
**Location**: `/packages/ui/components/shipment-filters-card.tsx`
```typescript
interface ShipmentFiltersCardProps {
  filters: FilterOption[];
  activeFilter: string[];
  onFilterChange: (filter: string[]) => void;
}
```

### **2. ShipmentTable**
**Location**: `/packages/ui/components/shipment-table.tsx`  
```typescript
interface ShipmentTableProps {
  shipments: ShipmentType[];
  selection: string[];
  onSelection: (selection: string[]) => void;
  onRowClick: (shipmentId: string) => void;
}
```

### **3. BulkActionsToolbar**
**Location**: `/packages/ui/components/bulk-actions-toolbar.tsx`
```typescript
interface BulkActionsToolbarProps {
  selection: string[];
  shipments: ShipmentType[];
  documentTemplates: DocumentTemplateType[];
}
```

### **4. ShipmentPagination** ✅ COMPLETED
**Location**: `/packages/ui/components/shipment-pagination.tsx`
```typescript
interface ShipmentPaginationProps {
  currentOffset: number;
  pageSize: number;
  totalCount: number;
  hasNextPage: boolean;
  onPageChange: (offset: number) => void;
}
```

### **5. StickyTableWrapper**
**Location**: `/packages/ui/components/sticky-table-wrapper.tsx`
```typescript
interface StickyTableWrapperProps {
  children: React.ReactNode;
  leftStickyColumns: number;
  rightStickyColumns: number;
}
```

## **Key Technical Considerations**

### **Data Preservation**
- Maintain all existing GraphQL query logic
- Preserve URL parameter synchronization  
- Keep existing mutation handlers intact
- Maintain selection state management

### **Performance**
- Minimize re-renders during bulk selection
- Optimize table rendering for large datasets
- Maintain preloadNextPage functionality
- Efficient sticky column implementation

### **Accessibility**  
- Preserve keyboard navigation
- Maintain screen reader compatibility
- Ensure proper focus management
- Keep semantic HTML structure

### **Browser Compatibility**
- Test sticky positioning across browsers
- Ensure horizontal scroll works on mobile
- Validate touch interactions on tablets
- Check responsive breakpoints

## **QA Checklist**

### **Functionality Verification**
- [ ] All existing features work identically
- [ ] Bulk selection/deselection functions correctly
- [ ] Individual shipment actions work via dropdown
- [ ] Pagination navigates properly
- [ ] Filters apply correctly and maintain URL state
- [ ] Loading states display appropriately
- [ ] Empty states show proper messaging

### **New Features Validation**  
- [ ] Row count displays accurate format "Viewing X–Y of Z results"
- [ ] Card-style filters match reference design
- [ ] Sticky columns remain positioned during horizontal scroll
- [ ] Mobile responsiveness meets requirements
- [ ] Enhanced scrolling works smoothly

### **Visual Consistency**
- [ ] Design matches existing Karrio design system
- [ ] Colors, fonts, and spacing are consistent
- [ ] Hover states and interactions feel natural  
- [ ] Loading animations are smooth
- [ ] Mobile layout is optimized

### **Performance Testing**
- [ ] Large datasets (100+ shipments) render smoothly
- [ ] Horizontal scrolling doesn't lag
- [ ] Selection changes are responsive
- [ ] Page navigation is fast

## **Success Criteria**
✅ **Zero functionality loss** from current implementation  
✅ **All new features** implemented per specifications  
✅ **Clean, maintainable** Shadcn + Tailwind code  
✅ **Improved mobile experience** with better scrolling  
✅ **Better visual consistency** with design system  
✅ **Enhanced user experience** with sticky columns and better pagination

## **Rollback Plan**
- Maintain git branch with current Bulma implementation
- Feature flags for A/B testing if needed  
- Database/API calls remain unchanged for easy rollback
- Component-level rollback capability for individual features

---

## **Implementation Notes**

### **⚠️ Draft Order PR Strategy**
- The draft order migration PR is not merged yet, so we cannot reference its components
- We start with shipments-specific components to avoid duplicating work
- Shared components (StatusBadge, Spinner, AppLink, ConfirmModal) are deferred to Phase 6
- Once draft order PR merges, we can reuse those migrated components
- This strategy ensures efficient development and avoids conflicts

### **Reference Screenshots Analysis**
1. **rows count feature.png**: Shows "Viewing 1–20 of 42 results" at bottom left with Previous/Next buttons at bottom right
2. **sticky left select column and right edit column.png**: Demonstrates checkbox column staying fixed on left and three-dot menu column staying fixed on right during horizontal scroll
3. **card filter.png**: Shows filter options as individual card components instead of traditional tabs
4. **scrolling.png**: Demonstrates mobile-optimized scrolling with consistent row sizing

### **Current File Locations**
- **Main shipments page**: `/packages/core/modules/Shipments/index.tsx`
- **Shadcn components**: `/packages/ui/components/ui/`
- **Custom components**: `/packages/ui/components/`
- **Status badge**: `/packages/ui/core/components/status-badge.tsx`
- **Carrier image**: `/packages/ui/core/components/carrier-image.tsx`
- **Shipment menu**: `/packages/ui/components/shipment-menu.tsx` (Already Shadcn ✅)

### **Migration Timeline**
- **Phase 1**: 1 hour (Environment setup)
- **Phase 2**: 3-4 hours (Shipments-specific components)
- **Phase 3**: 3-4 hours (Table structure & enhanced features)  
- **Phase 4**: 2-3 hours (Shipments-specific styling)
- **Phase 5**: 2-3 hours (Integration & testing - shipments-specific)
- **Phase 6**: 1-2 hours (Shared components - when draft order PR merges)
- **Phase 7**: 1-2 hours (Final integration & testing)
- **Total Estimated Time**: 13-19 hours (11-15 hours before draft order PR merge)

This plan ensures a systematic, feature-complete migration from Bulma to Shadcn + Tailwind while adding the requested enhancements and maintaining full functionality.