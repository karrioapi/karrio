"use client";

import React from "react";
import { PlusIcon, Pencil1Icon, TrashIcon } from "@radix-ui/react-icons";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import type { ServiceLevelWithZones } from "@karrio/ui/components/rate-sheet-editor";

function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(" ");
}

interface ServicePreset {
  code: string;
  name: string;
}

interface ServicesTabProps {
  services: ServiceLevelWithZones[];
  onEditService: (service: ServiceLevelWithZones) => void;
  onDeleteService: (service: ServiceLevelWithZones) => void;
  onAddService: () => void;
  servicePresets?: ServicePreset[];
  onAddServiceFromPreset?: (serviceCode: string) => void;
  onCloneService?: (service: ServiceLevelWithZones) => void;
}

export function ServicesTab({
  services,
  onEditService,
  onDeleteService,
  onAddService,
  servicePresets,
  onAddServiceFromPreset,
  onCloneService,
}: ServicesTabProps) {
  const AddServicePopover = ({ align = "end" }: { align?: "start" | "end" | "center" }) => (
    <Popover>
      <PopoverTrigger asChild>
        <button className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md transition-colors">
          <PlusIcon className="h-4 w-4" />
          Add Service
        </button>
      </PopoverTrigger>
      <PopoverContent align={align} className="w-56 p-2" sideOffset={8}>
        <div className="space-y-1">
          <p className="text-xs font-medium text-muted-foreground px-2 py-1">Add service</p>

          {servicePresets && servicePresets.length > 0 && onAddServiceFromPreset && (
            <>
              <div className="max-h-48 overflow-y-auto space-y-0.5">
                {servicePresets.map((preset) => (
                  <button
                    key={preset.code}
                    onClick={() => onAddServiceFromPreset(preset.code)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate"
                    title={preset.name}
                  >
                    {preset.name || preset.code}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          {services.length > 0 && onCloneService && (
            <>
              <p className="text-xs text-muted-foreground px-2 py-0.5">Clone existing</p>
              <div className="max-h-32 overflow-y-auto space-y-0.5">
                {services.map((service) => (
                  <button
                    key={service.id}
                    onClick={() => onCloneService(service)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate text-muted-foreground"
                    title={`Clone ${service.service_name}`}
                  >
                    {service.service_name || service.service_code}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          <button
            onClick={onAddService}
            className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors flex items-center gap-1.5 text-primary font-medium"
          >
            <PlusIcon className="h-3.5 w-3.5" />
            Create new service
          </button>
        </div>
      </PopoverContent>
    </Popover>
  );

  if (services.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-muted-foreground p-8">
        <p className="mb-4">No services added yet.</p>
        <AddServicePopover align="center" />
      </div>
    );
  }

  return (
    <div className="space-y-4 h-full overflow-y-auto pr-2">
      <div className="flex items-center justify-between sticky top-0 bg-background z-10 py-2">
        <h3 className="text-lg font-medium">Service Configuration</h3>
        <AddServicePopover />
      </div>
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
                <button
                  onClick={() => onEditService(service)}
                  className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-accent rounded transition-colors"
                  title="Edit Service"
                >
                  <Pencil1Icon className="h-4 w-4" />
                </button>
                <button
                  onClick={() => onDeleteService(service)}
                  className="p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded transition-colors"
                  title="Delete Service"
                >
                  <TrashIcon className="h-4 w-4" />
                </button>
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
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Transit Days:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {service.transit_days ? `${service.transit_days} Days` : "N/A"}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                  Max Weight:
                </div>
                <div className="text-sm font-semibold text-foreground">
                  {service.max_weight
                    ? `${service.max_weight} ${service.weight_unit || "KG"}`
                    : "N/A"}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
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
