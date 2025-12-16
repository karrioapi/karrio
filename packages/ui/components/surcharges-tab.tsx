"use client";

import React from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import { PlusIcon, TrashIcon, Link2Icon } from "@radix-ui/react-icons";
import type {
  SharedSurcharge,
  ServiceLevelWithZones,
} from "@karrio/ui/components/rate-sheet-editor";

interface SurchargesTabProps {
  surcharges: SharedSurcharge[];
  services: ServiceLevelWithZones[];
  onUpdateSurcharge: (
    surchargeId: string,
    updates: Partial<SharedSurcharge>
  ) => void;
  onAddSurcharge: () => void;
  onRemoveSurcharge: (surchargeId: string) => void;
  onToggleServiceSurcharge: (
    serviceId: string,
    surchargeId: string,
    linked: boolean
  ) => void;
}

const SURCHARGE_TYPES = [
  { value: "fixed", label: "Fixed Amount" },
  { value: "percentage", label: "Percentage" },
];

export function SurchargesTab({
  surcharges,
  services,
  onUpdateSurcharge,
  onAddSurcharge,
  onRemoveSurcharge,
  onToggleServiceSurcharge,
}: SurchargesTabProps) {
  // Helper to check if a service has a surcharge linked
  const isServiceLinked = (serviceId: string, surchargeId: string): boolean => {
    const service = services.find((s) => s.id === serviceId);
    return service?.surcharge_ids?.includes(surchargeId) ?? false;
  };

  // Get linked services count for a surcharge
  const getLinkedServicesCount = (surchargeId: string): number => {
    return services.filter((s) => s.surcharge_ids?.includes(surchargeId)).length;
  };

  if (surcharges.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-muted-foreground p-8">
        <p className="mb-4">No surcharges configured yet.</p>
        <Button onClick={onAddSurcharge}>
          <PlusIcon className="h-4 w-4 mr-2" />
          Add Surcharge
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6 h-full overflow-y-auto pr-2">
      <div className="flex items-center justify-between sticky top-0 bg-background z-10 py-2">
        <h3 className="text-lg font-medium">Surcharge Configuration</h3>
        <Button onClick={onAddSurcharge}>
          <PlusIcon className="h-4 w-4 mr-2" />
          Add Surcharge
        </Button>
      </div>

      <div className="grid gap-4 grid-cols-1 pb-6">
        {surcharges.map((surcharge, index) => (
          <div
            key={surcharge.id}
            className="p-4 bg-card border border-border rounded-lg shadow-sm space-y-4 relative group"
          >
            <div className="flex items-center justify-between gap-2">
              <h4 className="text-base font-semibold text-foreground">
                {surcharge.name || `Surcharge ${index + 1}`}
              </h4>
              <div className="flex items-center gap-2">
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={surcharge.active ?? false}
                    onChange={(e) =>
                      onUpdateSurcharge(surcharge.id, {
                        active: e.target.checked,
                      })
                    }
                    className="rounded border-border"
                  />
                  Active
                </label>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onRemoveSurcharge(surcharge.id)}
                  className="text-muted-foreground hover:text-destructive hover:bg-destructive/10"
                  title="Remove Surcharge"
                >
                  <TrashIcon className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-6 gap-y-3">
              <div>
                <Label className="text-xs mb-1 block">Name</Label>
                <Input
                  value={surcharge.name || ""}
                  onChange={(e) =>
                    onUpdateSurcharge(surcharge.id, { name: e.target.value })
                  }
                  placeholder="Fuel Surcharge"
                />
              </div>

              <div>
                <Label className="text-xs mb-1 block">Type</Label>
                <Select
                  value={surcharge.surcharge_type || "fixed"}
                  onValueChange={(val) =>
                    onUpdateSurcharge(surcharge.id, { surcharge_type: val })
                  }
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    {SURCHARGE_TYPES.map((type) => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label className="text-xs mb-1 block">
                  Amount {surcharge.surcharge_type === "percentage" ? "(%)" : ""}
                </Label>
                <Input
                  type="number"
                  step="0.01"
                  value={surcharge.amount?.toString() || "0"}
                  onChange={(e) =>
                    onUpdateSurcharge(surcharge.id, {
                      amount: parseFloat(e.target.value) || 0,
                    })
                  }
                  placeholder="0.00"
                />
              </div>

              <div>
                <Label className="text-xs mb-1 block">Cost (COGS)</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={surcharge.cost?.toString() || ""}
                  onChange={(e) =>
                    onUpdateSurcharge(surcharge.id, {
                      cost: e.target.value ? parseFloat(e.target.value) : null,
                    })
                  }
                  placeholder="0.00"
                />
              </div>
            </div>

            {/* Service Linking Section */}
            {services.length > 0 && (
              <div className="pt-3 border-t border-border">
                <div className="flex items-center gap-2 mb-2">
                  <Link2Icon className="h-4 w-4 text-muted-foreground" />
                  <Label className="text-xs">
                    Linked Services ({getLinkedServicesCount(surcharge.id)} of{" "}
                    {services.length})
                  </Label>
                </div>
                <div className="flex flex-wrap gap-2">
                  {services.map((service) => {
                    const isLinked = isServiceLinked(service.id, surcharge.id);
                    return (
                      <button
                        key={service.id}
                        onClick={() =>
                          onToggleServiceSurcharge(
                            service.id,
                            surcharge.id,
                            !isLinked
                          )
                        }
                        className={`px-3 py-1.5 text-xs font-medium rounded-full border transition-colors ${
                          isLinked
                            ? "bg-primary text-primary-foreground border-primary hover:bg-primary/90"
                            : "bg-background text-muted-foreground border-border hover:bg-accent hover:text-foreground"
                        }`}
                        title={
                          isLinked
                            ? `Unlink from ${service.service_name}`
                            : `Link to ${service.service_name}`
                        }
                      >
                        {service.service_name || service.service_code}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SurchargesTab;
