"use client";

import React from "react";
import { PlusIcon, Pencil1Icon, TrashIcon } from "@radix-ui/react-icons";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@karrio/ui/components/ui/popover";
import type {
  SharedSurcharge,
  ServiceLevelWithZones,
} from "@karrio/ui/components/rate-sheet-editor";

function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(" ");
}

interface SurchargePreset {
  id: string;
  name: string;
  amount: number;
  surcharge_type: string;
}

interface SurchargesTabProps {
  surcharges: SharedSurcharge[];
  services: ServiceLevelWithZones[];
  onEditSurcharge: (surcharge: SharedSurcharge) => void;
  onAddSurcharge: () => void;
  onRemoveSurcharge: (surchargeId: string) => void;
  surchargePresets?: SurchargePreset[];
  onAddSurchargeFromPreset?: (presetSurchargeId: string) => void;
  onCloneSurcharge?: (surcharge: SharedSurcharge) => void;
}

export function SurchargesTab({
  surcharges,
  services,
  onEditSurcharge,
  onAddSurcharge,
  onRemoveSurcharge,
  surchargePresets,
  onAddSurchargeFromPreset,
  onCloneSurcharge,
}: SurchargesTabProps) {
  const getLinkedServicesCount = (surchargeId: string): number => {
    return services.filter((s) => s.surcharge_ids?.includes(surchargeId)).length;
  };

  const formatAmount = (surcharge: SharedSurcharge): string => {
    if (surcharge.surcharge_type === "percentage") {
      return `${surcharge.amount ?? 0}%`;
    }
    return `${surcharge.amount ?? 0}`;
  };

  const formatType = (surcharge: SharedSurcharge): string => {
    return surcharge.surcharge_type === "percentage" ? "Percentage" : "Fixed Amount";
  };

  const AddSurchargePopover = ({ align = "end" }: { align?: "start" | "end" | "center" }) => (
    <Popover>
      <PopoverTrigger asChild>
        <button className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary-foreground bg-primary hover:bg-primary/90 rounded-md transition-colors">
          <PlusIcon className="h-4 w-4" />
          Add Surcharge
        </button>
      </PopoverTrigger>
      <PopoverContent align={align} className="w-56 p-2" sideOffset={8}>
        <div className="space-y-1">
          <p className="text-xs font-medium text-muted-foreground px-2 py-1">Add surcharge</p>

          {surchargePresets && surchargePresets.length > 0 && (
            <>
              <div className="max-h-48 overflow-y-auto space-y-0.5">
                {surchargePresets.map((preset) => (
                  <button
                    key={preset.id}
                    onClick={() => onAddSurchargeFromPreset?.(preset.id)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate"
                    title={`${preset.name} (${preset.surcharge_type === "percentage" ? `${preset.amount}%` : preset.amount})`}
                  >
                    {preset.name}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          {surcharges.length > 0 && onCloneSurcharge && (
            <>
              <p className="text-xs text-muted-foreground px-2 py-0.5">Clone existing</p>
              <div className="max-h-32 overflow-y-auto space-y-0.5">
                {surcharges.map((surcharge) => (
                  <button
                    key={surcharge.id}
                    onClick={() => onCloneSurcharge(surcharge)}
                    className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors truncate text-muted-foreground"
                    title={`Clone ${surcharge.name}`}
                  >
                    {surcharge.name || "Unnamed"}
                  </button>
                ))}
              </div>
              <div className="border-t border-border my-1" />
            </>
          )}

          <button
            onClick={onAddSurcharge}
            className="w-full text-left px-2 py-1.5 text-sm rounded-md hover:bg-accent transition-colors flex items-center gap-1.5 text-primary font-medium"
          >
            <PlusIcon className="h-3.5 w-3.5" />
            Create new surcharge
          </button>
        </div>
      </PopoverContent>
    </Popover>
  );

  if (surcharges.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-muted-foreground p-8">
        <p className="mb-4">No surcharges configured yet.</p>
        <AddSurchargePopover align="center" />
      </div>
    );
  }

  return (
    <div className="space-y-4 h-full overflow-y-auto pr-2">
      <div className="flex items-center justify-between sticky top-0 bg-background z-10 py-2">
        <h3 className="text-lg font-medium">Surcharge Configuration</h3>
        <AddSurchargePopover />
      </div>

      {surcharges.map((surcharge, index) => {
        const linkedCount = getLinkedServicesCount(surcharge.id);

        return (
          <div
            key={surcharge.id}
            className="bg-card border border-border rounded-lg shadow-sm hover:border-primary/50 transition-colors"
          >
            <div className="px-6 py-4 space-y-4">
              {/* Header with name, active badge, and actions */}
              <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <h4 className="font-semibold text-foreground text-base">
                    {surcharge.name || `Surcharge ${index + 1}`}
                  </h4>
                  <span
                    className={cn(
                      "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold",
                      surcharge.active
                        ? "bg-green-500 text-white dark:bg-green-600 dark:text-white"
                        : "bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300"
                    )}
                  >
                    {surcharge.active ? "Active" : "Inactive"}
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => onEditSurcharge(surcharge)}
                    className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-accent rounded transition-colors"
                    title="Edit Surcharge"
                  >
                    <Pencil1Icon className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => onRemoveSurcharge(surcharge.id)}
                    className="p-1.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded transition-colors"
                    title="Delete Surcharge"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {/* Surcharge details grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Type:
                  </div>
                  <div className="text-sm font-semibold text-foreground">
                    {formatType(surcharge)}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Amount:
                  </div>
                  <div className="text-sm font-semibold text-foreground">
                    {formatAmount(surcharge)}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Cost (COGS):
                  </div>
                  <div className="text-sm font-semibold text-foreground">
                    {surcharge.cost != null ? surcharge.cost : "\u2014"}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <div className="text-sm font-medium text-muted-foreground whitespace-nowrap">
                    Linked Services:
                  </div>
                  <div className="text-sm font-semibold text-foreground">
                    {linkedCount} of {services.length}
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default SurchargesTab;
