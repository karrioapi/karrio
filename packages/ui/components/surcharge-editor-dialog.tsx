"use client";

import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
  DialogBody,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import type {
  SharedSurcharge,
  ServiceLevelWithZones,
} from "@karrio/ui/components/rate-sheet-editor";

interface SurchargeEditorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  surcharge: SharedSurcharge | null;
  onSave: (surchargeId: string, updates: Partial<SharedSurcharge>) => void;
  services: ServiceLevelWithZones[];
  onToggleServiceSurcharge: (serviceId: string, surchargeId: string, linked: boolean) => void;
}

const SURCHARGE_TYPES = [
  { value: "fixed", label: "Fixed Amount" },
  { value: "percentage", label: "Percentage" },
];

export function SurchargeEditorDialog({
  open,
  onOpenChange,
  surcharge,
  onSave,
  services,
  onToggleServiceSurcharge,
}: SurchargeEditorDialogProps) {
  const [name, setName] = useState("");
  const [surchargeType, setSurchargeType] = useState("fixed");
  const [amount, setAmount] = useState("0");
  const [cost, setCost] = useState("");
  const [active, setActive] = useState(true);

  useEffect(() => {
    if (surcharge && open) {
      setName(surcharge.name || "");
      setSurchargeType(surcharge.surcharge_type || "fixed");
      setAmount(surcharge.amount?.toString() || "0");
      setCost(surcharge.cost?.toString() || "");
      setActive(surcharge.active ?? true);
    }
  }, [surcharge, open]);

  const isServiceLinked = (serviceId: string): boolean => {
    if (!surcharge) return false;
    const service = services.find((s) => s.id === serviceId);
    return service?.surcharge_ids?.includes(surcharge.id) ?? false;
  };

  const getLinkedServicesCount = (): number => {
    if (!surcharge) return 0;
    return services.filter((s) => s.surcharge_ids?.includes(surcharge.id)).length;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!surcharge) return;

    onSave(surcharge.id, {
      name,
      surcharge_type: surchargeType,
      amount: parseFloat(amount) || 0,
      cost: cost ? parseFloat(cost) : null,
      active,
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Edit Surcharge</DialogTitle>
          <DialogDescription>
            Configure surcharge details and linked services
          </DialogDescription>
        </DialogHeader>

        <DialogBody>
          <form id="surcharge-form" onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <Label className="text-xs">Name</Label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Fuel Surcharge"
                className="h-9"
              />
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">Type</Label>
              <Select value={surchargeType} onValueChange={setSurchargeType}>
                <SelectTrigger className="w-full h-9">
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

            <div className="space-y-1.5">
              <Label className="text-xs">
                Amount {surchargeType === "percentage" ? "(%)" : ""}
              </Label>
              <Input
                type="number"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                className="h-9"
              />
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">Cost (COGS)</Label>
              <Input
                type="number"
                step="0.01"
                value={cost}
                onChange={(e) => setCost(e.target.value)}
                placeholder="0.00"
                className="h-9"
              />
            </div>

            <div className="flex items-center space-x-2 pt-1">
              <Checkbox
                id="surcharge-active"
                checked={active}
                onCheckedChange={(checked) => setActive(checked === true)}
              />
              <Label htmlFor="surcharge-active" className="text-xs cursor-pointer">
                Active
              </Label>
            </div>

            {/* Service Linking Section */}
            {services.length > 0 && surcharge && (
              <div className="pt-3 border-t border-border">
                <div className="flex items-center justify-between mb-2">
                  <Label className="text-xs text-muted-foreground">
                    Linked Services ({getLinkedServicesCount()} of {services.length})
                  </Label>
                  <button
                    type="button"
                    onClick={() => {
                      const allLinked = getLinkedServicesCount() === services.length;
                      services.forEach((s) => {
                        const linked = isServiceLinked(s.id);
                        if (allLinked && linked) {
                          onToggleServiceSurcharge(s.id, surcharge.id, false);
                        } else if (!allLinked && !linked) {
                          onToggleServiceSurcharge(s.id, surcharge.id, true);
                        }
                      });
                    }}
                    className="text-xs text-primary hover:text-primary/80 font-medium"
                  >
                    {getLinkedServicesCount() === services.length ? "Deselect All" : "Select All"}
                  </button>
                </div>
                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {services.map((service) => {
                    const linked = isServiceLinked(service.id);
                    const checkId = `surch-svc-${service.id}`;
                    return (
                      <label
                        key={service.id}
                        htmlFor={checkId}
                        className="flex items-center gap-2.5 px-2 py-1.5 rounded-md hover:bg-accent cursor-pointer transition-colors"
                      >
                        <Checkbox
                          id={checkId}
                          checked={linked}
                          onCheckedChange={(checked) =>
                            onToggleServiceSurcharge(service.id, surcharge.id, checked === true)
                          }
                        />
                        <span className="text-sm text-foreground">
                          {service.service_name || service.service_code}
                        </span>
                      </label>
                    );
                  })}
                </div>
              </div>
            )}
          </form>
        </DialogBody>

        <DialogFooter>
          <Button type="button" variant="outline" size="sm" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button type="submit" size="sm" form="surcharge-form">
            Save
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default SurchargeEditorDialog;
