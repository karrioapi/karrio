"use client";

import React from "react";
import { Card } from "@karrio/ui/components/ui/card";
import { cn } from "@karrio/ui/lib/utils";

interface FilterOption {
  label: string;
  value: string[];
}

interface ShipmentFiltersCardProps {
  filters: FilterOption[];
  activeFilter: string[];
  onFilterChange: (filter: string[]) => void;
  className?: string;
}

export const ShipmentFiltersCard: React.FC<ShipmentFiltersCardProps> = ({
  filters,
  activeFilter,
  onFilterChange,
  className
}) => {
  const isActive = (filterValue: string[]) => {
    return JSON.stringify(filterValue.sort()) === JSON.stringify(activeFilter.sort());
  };

  return (
    <div className={cn("grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6", className)}>
      {filters.map((filter, index) => (
        <Card
          key={index}
          className={cn(
            "cursor-pointer transition-all duration-200 hover:shadow-sm border",
            "p-3 text-center min-h-[60px] flex flex-col justify-center",
            isActive(filter.value)
              ? "border-blue-500 bg-blue-50 shadow-sm"
              : "border-gray-200 hover:border-gray-300 bg-white"
          )}
          onClick={() => onFilterChange(filter.value)}
        >
          <div className={cn(
            "text-sm font-medium capitalize",
            isActive(filter.value) ? "text-blue-700" : "text-gray-700"
          )}>
            {filter.label}
          </div>
        </Card>
      ))}
    </div>
  );
};