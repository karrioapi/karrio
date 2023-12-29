import { ShipmentStatusEnum } from '@karrio/types';
import { formatRef } from '@karrio/lib';
import React from 'react';

interface StatusBadgeComponent extends React.AllHTMLAttributes<HTMLSpanElement> {
  status?: string | ShipmentStatusEnum;
}

export const StatusBadge: React.FC<StatusBadgeComponent> = ({ status, className, ...props }) => {
  const color = {
    "draft": "is-primary is-light",
    "unfulfilled": "is-primary is-light",
    "cancelled": "is-light",
    "partial": "is-info is-light",
    "purchased": "is-info is-light",
    "in_transit": "is-info is-light",
    "unknown": "is-light",
    "transit": "is-info is-light",
    "pending": "is-primary is-light",
    "fulfilled": "is-success is-light",
    "delivered": "is-success is-light",
    "shipped": "is-success is-light",
    "out_for_delivery": "is-info",
    "ready_for_pickup": "is-info",
    "on_hold": "is-warning is-light",
    "delivery_delayed": "is-warning is-light",
    "needs_attention": "is-warning is-light",
    "delivery_failed": "is-danger is-light",
    "success": "is-success is-light",
    "failed": "is-danger is-light",
    "running": "is-info is-light",
  }[status || ""] || "is-light";

  return (
    <span className={`tag is-size-7 has-text-weight-semibold ${color} ${className}`} {...props}>
      {formatRef(status || "").toLocaleLowerCase()}
    </span>
  )
};
