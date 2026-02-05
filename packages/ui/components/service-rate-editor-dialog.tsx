"use client";

import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogBody,
  DialogTitle,
  DialogDescription,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import type { ServiceRate } from "@karrio/ui/components/weight-rate-grid";
import type {
  ServiceLevelWithZones,
  EmbeddedZone,
} from "@karrio/ui/components/rate-sheet-editor";

interface ServiceRateEditorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  serviceRate: ServiceRate | null;
  onSave: (updated: ServiceRate) => void;
  services: ServiceLevelWithZones[];
  sharedZones: EmbeddedZone[];
  weightUnit: string;
}

export function ServiceRateEditorDialog({
  open,
  onOpenChange,
  serviceRate,
  onSave,
  services,
  sharedZones,
  weightUnit,
}: ServiceRateEditorDialogProps) {
  const [rate, setRate] = useState("");
  const [cost, setCost] = useState("");
  const [transitDays, setTransitDays] = useState("");
  const [transitTime, setTransitTime] = useState("");

  useEffect(() => {
    if (serviceRate && open) {
      setRate(serviceRate.rate?.toString() || "0");
      setCost(serviceRate.cost?.toString() || "");
      setTransitDays(serviceRate.transit_days?.toString() || "");
      setTransitTime(serviceRate.transit_time?.toString() || "");
    }
  }, [serviceRate, open]);

  const serviceName = serviceRate
    ? services.find((s) => s.id === serviceRate.service_id)?.service_name ||
      serviceRate.service_id
    : "";

  const zoneName = serviceRate
    ? sharedZones.find((z) => z.id === serviceRate.zone_id)?.label ||
      serviceRate.zone_id
    : "";

  const weightLabel = serviceRate
    ? serviceRate.min_weight === 0 && serviceRate.max_weight === 0
      ? "Flat rate"
      : serviceRate.min_weight === 0
        ? `Up to ${serviceRate.max_weight} ${weightUnit}`
        : `${serviceRate.min_weight} \u2013 ${serviceRate.max_weight} ${weightUnit}`
    : "";

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!serviceRate) return;

    const parsedTransitDays = transitDays ? parseInt(transitDays, 10) : null;
    const parsedTransitTime = transitTime ? parseFloat(transitTime) : null;

    onSave({
      ...serviceRate,
      rate: parseFloat(rate) || 0,
      cost: cost ? parseFloat(cost) : null,
      transit_days:
        parsedTransitDays !== null && !isNaN(parsedTransitDays)
          ? parsedTransitDays
          : null,
      transit_time:
        parsedTransitTime !== null && !isNaN(parsedTransitTime)
          ? parsedTransitTime
          : null,
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Edit Service Rate</DialogTitle>
          <DialogDescription>
            Update rate details for this service-zone-weight combination
          </DialogDescription>
        </DialogHeader>

        <DialogBody>
          <form id="service-rate-form" onSubmit={handleSubmit} className="space-y-4">
            {/* Read-only context fields */}
            <div className="grid grid-cols-1 gap-3 p-3 bg-muted/50 rounded-lg">
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-muted-foreground w-20">Service:</span>
                <span className="text-sm font-medium text-foreground">{serviceName}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-muted-foreground w-20">Zone:</span>
                <span className="text-sm font-medium text-foreground">{zoneName}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-muted-foreground w-20">Weight:</span>
                <span className="text-sm font-medium text-foreground">{weightLabel}</span>
              </div>
            </div>

            {/* Editable fields */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label className="text-xs">Rate (Sell Price)</Label>
                <Input
                  type="number"
                  step="0.01"
                  value={rate}
                  onChange={(e) => setRate(e.target.value)}
                  placeholder="0.00"
                  className="h-9"
                  autoFocus
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
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label className="text-xs">Transit Days</Label>
                <Input
                  type="number"
                  min={0}
                  step="1"
                  value={transitDays}
                  onChange={(e) => setTransitDays(e.target.value)}
                  placeholder="e.g., 3"
                  className="h-9"
                />
              </div>
              <div className="space-y-1.5">
                <Label className="text-xs">Transit Time (hours)</Label>
                <Input
                  type="number"
                  min={0}
                  step="0.5"
                  value={transitTime}
                  onChange={(e) => setTransitTime(e.target.value)}
                  placeholder="e.g., 48"
                  className="h-9"
                />
              </div>
            </div>
          </form>
        </DialogBody>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => onOpenChange(false)}
          >
            Cancel
          </Button>
          <Button type="submit" size="sm" form="service-rate-form">
            Save
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default ServiceRateEditorDialog;
