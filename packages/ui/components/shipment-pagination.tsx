"use client";

import React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { cn } from "@karrio/ui/lib/utils";

interface ShipmentPaginationProps {
  currentOffset: number;
  pageSize: number;
  totalCount: number;
  hasNextPage: boolean;
  onPageChange: (offset: number) => void;
  className?: string;
}

export const ShipmentPagination: React.FC<ShipmentPaginationProps> = ({
  currentOffset,
  pageSize,
  totalCount,
  hasNextPage,
  onPageChange,
  className
}) => {
  const currentPage = Math.floor(currentOffset / pageSize) + 1;
  const startItem = currentOffset + 1;
  const endItem = Math.min(currentOffset + pageSize, totalCount);
  
  const handlePrevious = () => {
    if (currentOffset > 0) {
      onPageChange(Math.max(0, currentOffset - pageSize));
    }
  };

  const handleNext = () => {
    if (hasNextPage) {
      onPageChange(currentOffset + pageSize);
    }
  };

  return (
    <div className={cn("flex items-center justify-between px-2 py-2", className)}>
      {/* Results count - left side */}
      <div className="text-sm font-medium text-gray-700">
        {totalCount > 0 ? (
          <span>Viewing {startItem}–{endItem} of {totalCount} results</span>
        ) : (
          <span>0 results</span>
        )}
      </div>

      {/* Navigation buttons - right side */}
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={handlePrevious}
          disabled={currentOffset === 0}
          className="px-3"
        >
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={handleNext}
          disabled={!hasNextPage}
          className="px-3"
        >
          Next
        </Button>
      </div>
    </div>
  );
};