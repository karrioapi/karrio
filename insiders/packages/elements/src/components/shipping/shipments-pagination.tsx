import * as React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@karrio/ui/components/ui/button";

export interface PaginationProps {
  currentPage: number;
  totalItems: number;
  pageSize: number;
  siblingCount?: number;
  onPageChange: (page: number) => void;
}

export function ShipmentsPagination({
  currentPage,
  totalItems,
  pageSize,
  siblingCount = 1,
  onPageChange,
}: PaginationProps) {
  const totalPages = Math.ceil(totalItems / pageSize);

  // Generate page numbers
  const getPageNumbers = () => {
    const totalPageNumbers = siblingCount * 2 + 3; // siblings on each side + current + first + last

    // If total pages are less than the total page numbers we want to show
    if (totalPages <= totalPageNumbers) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    const leftSiblingIndex = Math.max(currentPage - siblingCount, 1);
    const rightSiblingIndex = Math.min(currentPage + siblingCount, totalPages);

    const shouldShowLeftDots = leftSiblingIndex > 2;
    const shouldShowRightDots = rightSiblingIndex < totalPages - 1;

    // Case 1: Show left dots but not right dots
    if (shouldShowLeftDots && !shouldShowRightDots) {
      const rightItemCount = 3 + 2 * siblingCount;
      const rightRange = Array.from(
        { length: rightItemCount },
        (_, i) => totalPages - rightItemCount + i + 1
      );
      return [1, "...", ...rightRange];
    }

    // Case 2: Show right dots but not left dots
    if (!shouldShowLeftDots && shouldShowRightDots) {
      const leftItemCount = 3 + 2 * siblingCount;
      const leftRange = Array.from(
        { length: leftItemCount },
        (_, i) => i + 1
      );
      return [...leftRange, "...", totalPages];
    }

    // Case 3: Show both left and right dots
    if (shouldShowLeftDots && shouldShowRightDots) {
      const middleRange = Array.from(
        { length: rightSiblingIndex - leftSiblingIndex + 1 },
        (_, i) => leftSiblingIndex + i
      );
      return [1, "...", ...middleRange, "...", totalPages];
    }

    // This shouldn't happen, but just in case
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="flex items-center justify-between px-2 py-4">
      <div className="text-sm text-gray-500">
        Showing {Math.min((currentPage - 1) * pageSize + 1, totalItems)} to{" "}
        {Math.min(currentPage * pageSize, totalItems)} of {totalItems} shipments
      </div>

      <div className="flex items-center space-x-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          <ChevronLeft className="h-4 w-4" />
          <span className="sr-only">Previous page</span>
        </Button>

        {pageNumbers.map((pageNumber, i) => (
          <React.Fragment key={i}>
            {pageNumber === "..." ? (
              <span className="px-2">...</span>
            ) : (
              <Button
                variant={pageNumber === currentPage ? "default" : "outline"}
                size="sm"
                onClick={() => onPageChange(pageNumber as number)}
              >
                {pageNumber}
              </Button>
            )}
          </React.Fragment>
        ))}

        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages || totalPages === 0}
        >
          <ChevronRight className="h-4 w-4" />
          <span className="sr-only">Next page</span>
        </Button>
      </div>
    </div>
  );
}
