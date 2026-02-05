"use client";

import * as React from "react";
import { Badge } from "@karrio/ui/components/ui/badge";
import { cn } from "@karrio/ui/lib/utils";
import { formatRef } from "@karrio/lib";

interface StatusBadgeProps {
  status: string;
  variant?: "default" | "secondary" | "destructive" | "outline";
  className?: string;
}

const statusVariants = {
  // Shipment statuses
  draft: "bg-purple-100 text-purple-800 border-purple-200",
  unfulfilled: "bg-purple-100 text-purple-800 border-purple-200", 
  cancelled: "bg-gray-100 text-gray-800 border-gray-200",
  partial: "bg-blue-100 text-blue-800 border-blue-200",
  purchased: "bg-purple-100 text-purple-800 border-purple-200",
  in_transit: "bg-blue-100 text-blue-800 border-blue-200",
  transit: "bg-blue-100 text-blue-800 border-blue-200",
  pending: "bg-yellow-100 text-yellow-800 border-yellow-200",
  fulfilled: "bg-green-100 text-green-800 border-green-200",
  delivered: "bg-green-100 text-green-800 border-green-200",
  shipped: "bg-blue-100 text-blue-800 border-blue-200",
  out_for_delivery: "bg-orange-100 text-orange-800 border-orange-200",
  ready_for_pickup: "bg-purple-100 text-purple-800 border-purple-200",
  on_hold: "bg-yellow-100 text-yellow-800 border-yellow-200",
  delivery_delayed: "bg-yellow-100 text-yellow-800 border-yellow-200",
  needs_attention: "bg-red-100 text-red-800 border-red-200",
  delivery_failed: "bg-red-100 text-red-800 border-red-200",
  exception: "bg-red-100 text-red-800 border-red-200",
  
  // Pickup statuses
  scheduled: "bg-purple-100 text-purple-800 border-purple-200",
  picked_up: "bg-green-100 text-green-800 border-green-200",
  closed: "bg-blue-100 text-blue-800 border-blue-200",

  // Connection statuses
  active: "bg-green-100 text-green-800 border-green-200",
  inactive: "bg-gray-100 text-gray-800 border-gray-200",
  enabled: "bg-green-100 text-green-800 border-green-200",
  disabled: "bg-gray-100 text-gray-800 border-gray-200",
  
  // Test mode
  test: "bg-orange-100 text-orange-800 border-orange-200",
  live: "bg-green-100 text-green-800 border-green-200",
  
  // Generic statuses
  success: "bg-green-100 text-green-800 border-green-200",
  failed: "bg-red-100 text-red-800 border-red-200",
  running: "bg-blue-100 text-blue-800 border-blue-200",
  unknown: "bg-gray-100 text-gray-800 border-gray-200",
} as const;

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  variant = "secondary",  
  className,
}) => {
  const normalizedStatus = status?.toLowerCase().replace(/\s+/g, '_');
  const statusClass = statusVariants[normalizedStatus as keyof typeof statusVariants];
  
  return (
    <Badge 
      variant={variant}
      className={cn(
        "text-xs px-2 py-1",
        statusClass,
        className
      )}
    >
      {formatRef(status || "").replace(/_/g, ' ')}
    </Badge>
  );
};