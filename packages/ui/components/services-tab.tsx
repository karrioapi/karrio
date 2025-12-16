"use client";

import React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Pencil1Icon, TrashIcon } from "@radix-ui/react-icons";
import type { ServiceLevelWithZones } from "@karrio/ui/components/rate-sheet-editor";

function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(" ");
}

interface ServicesTabProps {
  services: ServiceLevelWithZones[];
  onEditService: (service: ServiceLevelWithZones) => void;
  onDeleteService: (service: ServiceLevelWithZones) => void;
}

export function ServicesTab({
  services,
  onEditService,
  onDeleteService,
}: ServicesTabProps) {
  if (services.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-muted-foreground p-8">
        <p>
          No services added yet. Add a service from the sidebar to get started.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4 h-full overflow-y-auto pr-2">
      {services.map((service) => (
        <div
          key={service.id || service.service_code}
          className="bg-card border border-border rounded-lg shadow-sm hover:border-primary/50 transition-colors"
        >
          {/* Service details */}
          <div className="px-6 py-4 space-y-4">
            {/* Header with service name and actions */}
            <div className="flex items-center justify-between gap-4">
              <h4 className="font-semibold text-foreground text-base">
                {service.service_name}
              </h4>
              <div className="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onEditService(service)}
                  title="Edit Service"
                  className="h-8 w-8"
                >
                  <Pencil1Icon className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onDeleteService(service)}
                  title="Delete Service"
                  className="h-8 w-8 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                >
                  <TrashIcon className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Service details grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Service Code:
                </div>
                <div className="text-sm font-mono text-foreground bg-muted/50 dark:bg-muted/20 px-2 py-1 rounded">
                  {service.service_code}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Currency:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {service.currency || "N/A"}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap flex items-center gap-1.5">
                  <svg
                    className="h-3.5 w-3.5"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12,6 12,12 16,14" />
                  </svg>
                  Transit Days:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {service.transit_days ? `${service.transit_days} Days` : "N/A"}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap flex items-center gap-1.5">
                  <svg
                    className="h-3.5 w-3.5"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" />
                    <line x1="3" y1="6" x2="21" y2="6" />
                  </svg>
                  Max Weight:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {service.max_weight
                    ? `${service.max_weight} ${service.weight_unit || "KG"}`
                    : "N/A"}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap flex items-center gap-1.5">
                  <svg
                    className="h-3.5 w-3.5"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                  </svg>
                  Zones:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {service.zone_ids?.length || 0}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Active:
                </div>
                <span
                  className={cn(
                    "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold",
                    service.active
                      ? "bg-green-500 text-white dark:bg-green-600 dark:text-white"
                      : "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
                  )}
                >
                  {service.active ? "Yes" : "No"}
                </span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ServicesTab;
