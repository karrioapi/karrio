"use client";

import React from "react";
import { ShipmentStatusEnum } from "@karrio/types";
import { formatRef } from "@karrio/lib";
import { cn } from "@karrio/ui/lib/utils";

interface ShipmentsStatusBadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  status?: string | ShipmentStatusEnum;
}

export const ShipmentsStatusBadge = ({
  status,
  className,
  ...props
}: ShipmentsStatusBadgeProps): JSX.Element => {
  const getStatusStyles = (status: string) => {
    const styles = {
      draft: "bg-violet-50 text-violet-500",
      unfulfilled: "bg-violet-50 text-violet-500", 
      pending: "bg-violet-50 text-violet-500",
      cancelled: "bg-gray-50 text-gray-500",
      unknown: "bg-gray-50 text-gray-500",
      partial: "bg-cyan-50 text-cyan-500",
      purchased: "bg-blue-50 text-blue-500",
      in_transit: "bg-cyan-50 text-cyan-500",
      transit: "bg-cyan-50 text-cyan-500", 
      running: "bg-cyan-50 text-cyan-500",
      fulfilled: "bg-green-50 text-green-500",
      delivered: "bg-green-50 text-green-500",
      shipped: "bg-green-50 text-green-500",
      success: "bg-green-50 text-green-500",
      out_for_delivery: "bg-cyan-500 text-white",
      ready_for_pickup: "bg-cyan-500 text-white",
      on_hold: "bg-yellow-50 text-yellow-500",
      delivery_delayed: "bg-yellow-50 text-yellow-500",
      needs_attention: "bg-yellow-50 text-yellow-500", 
      delivery_failed: "bg-red-50 text-red-500",
      failed: "bg-red-50 text-red-500",
    };
    
    return styles[status as keyof typeof styles] || "bg-gray-50 text-gray-500";
  };

  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-1 rounded text-xs font-semibold",
        getStatusStyles(status || ""),
        className
      )}
      {...props}
    >
      {formatRef(status || "").toLocaleLowerCase()}
    </span>
  );
};