"use client";

import React from "react";
import { Card } from "@karrio/ui/components/ui/card";
import { cn } from "@karrio/ui/lib/utils";

interface FilterOption {
  label: string;
  value: string[];
}

interface FiltersCardProps {
  filters: FilterOption[];
  activeFilter: string[];
  onFilterChange: (filter: string[]) => void;
  className?: string;
}

export const FiltersCard: React.FC<FiltersCardProps> = ({
  filters,
  activeFilter,
  onFilterChange,
  className
}) => {
  const isActive = (filterValue: string[]) => {
    return JSON.stringify(filterValue.sort()) === JSON.stringify(activeFilter.sort());
  };

  return (
    <div className={cn("flex gap-2 overflow-x-auto pb-2 sm:grid sm:grid-cols-3 lg:grid-cols-6 sm:gap-3 mb-5 mt-4", className)}>
      {filters.map((filter, index) => (
        <Card
          key={index}
          className={cn(
            "cursor-pointer transition-all duration-200 hover:border-gray-300 hover:shadow-sm border shadow-none",
            "text-center min-h-[60px] flex flex-col justify-center",
            "px-2 py-3 flex-shrink-0 min-w-[80px] sm:p-3 sm:flex-shrink sm:min-w-0",
            isActive(filter.value)
              ? "border-blue-500 bg-blue-50 shadow-sm"
              : "border-gray-200 bg-white"
          )}
          onClick={() => onFilterChange(filter.value)}
        >
          <div className={cn(
            "text-sm font-medium capitalize whitespace-nowrap sm:whitespace-normal",
            isActive(filter.value) ? "text-blue-700" : "text-gray-700"
          )}>
            {filter.label}
          </div>
        </Card>
      ))}
    </div>
  );
};