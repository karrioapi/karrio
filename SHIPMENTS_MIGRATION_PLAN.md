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

### **Priority 1: Core UI Components**
1. **StatusBadge** → shadcn Badge ✅ (Already available)
2. **Spinner** → shadcn Skeleton
3. **AppLink** → shadcn Button styling
4. **Main table structure** → shadcn Table components

### **Priority 2: Complex Components**  
5. **ShipmentsFilter** → shadcn Popover + Form + Checkbox + Input + Button
6. **Tab filters** → Custom Card-style components (per reference images)
7. **Pagination** → Enhanced shadcn component with row count display

### **Priority 3: Modal Components**
8. **ShipmentPreview** → shadcn Dialog
9. **ConfirmModal** → shadcn AlertDialog

### **No Migration Needed ✅**
- **ShipmentMenu**: Already uses shadcn DropdownMenu
- **CarrierImage**: Minimal changes needed

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
- [x] Identify reusable patterns from draft_order.tsx migration
- [x] Plan new component structure in `/packages/ui/components`

### **Phase 2: Basic Component Migration**  
- [ ] Replace Bulma header layout with Tailwind flex
- [ ] Convert StatusBadge if needed (check current implementation)
- [ ] Replace Spinner with Shadcn Skeleton  
- [ ] Update AppLink styling to use Shadcn Button patterns
- [ ] Convert basic Bulma classes (columns, containers, etc.)

### **Phase 3: Table Structure Overhaul**
- [ ] Replace `<table className="table is-fullwidth">` with Shadcn Table
- [ ] Implement TableHeader, TableBody, TableRow, TableCell components
- [ ] Add sticky positioning for checkbox and actions columns
- [ ] Maintain existing click handlers and selection logic
- [ ] Preserve row hover and selection states

### **Phase 4: Filter System Migration**
- [ ] Convert tab navigation to card-style filters
- [ ] Migrate ShipmentsFilter to Shadcn Popover + Form components
- [ ] Maintain existing filter logic and URL synchronization
- [ ] Ensure proper active state styling

### **Phase 5: Enhanced Features**
- [ ] Create enhanced pagination with row count display
- [ ] Implement sticky column behavior
- [ ] Add mobile responsiveness improvements
- [ ] Optimize scrolling experience
- [ ] Test horizontal scroll with sticky columns

### **Phase 6: Modal System Migration**
- [ ] Update ShipmentPreview to use Shadcn Dialog
- [ ] Convert ConfirmModal to Shadcn AlertDialog  
- [ ] Maintain existing modal trigger logic
- [ ] Test modal interactions and state management

### **Phase 7: Integration & Testing**
- [ ] Verify all existing functionality preserved
- [ ] Test bulk selection and actions
- [ ] Validate responsive behavior across devices
- [ ] Check loading states and error handling
- [ ] Performance testing with large datasets

## **New Components to Create**

### **1. ShipmentFiltersCard** 
**Location**: `/packages/ui/components/shipment-filters-card.tsx`
```typescript
interface ShipmentFiltersCardProps {
  filters: FilterOption[];
  activeFilter: string;
  onFilterChange: (filter: string) => void;
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

### **4. ShipmentPagination**
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
- **Phase 1-2**: 1-2 hours (Basic component migration)
- **Phase 3**: 2-3 hours (Table structure overhaul)  
- **Phase 4**: 2-3 hours (Filter system migration)
- **Phase 5**: 2-3 hours (Enhanced features)
- **Phase 6**: 1-2 hours (Modal system migration)
- **Phase 7**: 2-3 hours (Integration & testing)
- **Total Estimated Time**: 10-16 hours

This plan ensures a systematic, feature-complete migration from Bulma to Shadcn + Tailwind while adding the requested enhancements and maintaining full functionality.