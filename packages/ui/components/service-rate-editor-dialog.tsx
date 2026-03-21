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
  SharedSurcharge,
} from "@karrio/ui/components/rate-sheet-editor";
import type { MarkupType } from "@karrio/hooks/admin-markups";

interface ServiceRateEditorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  serviceRate: ServiceRate | null;
  onSave: (updated: ServiceRate) => void;
  services: ServiceLevelWithZones[];
  sharedZones: EmbeddedZone[];
  weightUnit: string;
  markups?: MarkupType[];
  surcharges?: SharedSurcharge[];
}

export function ServiceRateEditorDialog({
  open,
  onOpenChange,
  serviceRate,
  onSave,
  services,
  sharedZones,
  weightUnit,
  markups,
  surcharges,
}: ServiceRateEditorDialogProps) {
  const [rate, setRate] = useState("");
  const [transitDays, setTransitDays] = useState("");
  const [transitTime, setTransitTime] = useState("");
  const [excludedMarkupIds, setExcludedMarkupIds] = useState<string[]>([]);
  const [excludedSurchargeIds, setExcludedSurchargeIds] = useState<string[]>([]);
  const [planCosts, setPlanCosts] = useState<Record<string, string>>({});
  const [planCostTypes, setPlanCostTypes] = useState<Record<string, "PERCENTAGE" | "AMOUNT">>({});

  // Plan markups are markups with meta.plan set
  const planMarkups = (markups || []).filter((m) => m.active && m.meta?.plan);

  useEffect(() => {
    if (serviceRate && open) {
      setRate(serviceRate.rate?.toString() || "0");
      setTransitDays(serviceRate.transit_days?.toString() || "");
      setTransitTime(serviceRate.transit_time?.toString() || "");
      const meta = serviceRate.meta || {};
      setExcludedMarkupIds(meta.excluded_markup_ids || []);
      setExcludedSurchargeIds(meta.excluded_surcharge_ids || []);
      // Initialize per-plan costs and types from meta
      const existingPlanCosts = meta.plan_costs || {};
      const existingPlanCostTypes = meta.plan_cost_types || {};
      const costState: Record<string, string> = {};
      const typeState: Record<string, "PERCENTAGE" | "AMOUNT"> = {};
      planMarkups.forEach((m) => {
        costState[m.id] = existingPlanCosts[m.id]?.toString() || "";
        typeState[m.id] = existingPlanCostTypes[m.id] || "AMOUNT";
      });
      setPlanCosts(costState);
      setPlanCostTypes(typeState);
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

  const activeMarkups = (markups || []).filter((m) => m.active);
  // Non-plan markups for exclusion section
  const nonPlanMarkups = activeMarkups.filter((m) => !m.meta?.plan);
  const activeSurcharges = (surcharges || []).filter((s) => s.active);

  const toggleMarkupExclusion = (markupId: string) => {
    setExcludedMarkupIds((prev) =>
      prev.includes(markupId)
        ? prev.filter((id) => id !== markupId)
        : [...prev, markupId]
    );
  };

  const toggleSurchargeExclusion = (surchargeId: string) => {
    setExcludedSurchargeIds((prev) =>
      prev.includes(surchargeId)
        ? prev.filter((id) => id !== surchargeId)
        : [...prev, surchargeId]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!serviceRate) return;

    const parsedTransitDays = transitDays ? parseInt(transitDays, 10) : null;
    const parsedTransitTime = transitTime ? parseFloat(transitTime) : null;

    // Build meta with exclusions and plan costs merged into existing meta
    const existingMeta = serviceRate.meta || {};
    const newMeta: Record<string, any> = { ...existingMeta };
    if (excludedMarkupIds.length > 0) {
      newMeta.excluded_markup_ids = excludedMarkupIds;
    } else {
      delete newMeta.excluded_markup_ids;
    }
    if (excludedSurchargeIds.length > 0) {
      newMeta.excluded_surcharge_ids = excludedSurchargeIds;
    } else {
      delete newMeta.excluded_surcharge_ids;
    }

    // Build plan_costs: { [markup_id]: cost_value }
    // Build plan_cost_types: { [markup_id]: "PERCENTAGE" | "AMOUNT" }
    const parsedPlanCosts: Record<string, number> = {};
    const parsedPlanCostTypes: Record<string, string> = {};
    for (const [markupId, value] of Object.entries(planCosts)) {
      if (value && !isNaN(parseFloat(value))) {
        parsedPlanCosts[markupId] = parseFloat(value);
        parsedPlanCostTypes[markupId] = planCostTypes[markupId] || "AMOUNT";
      }
    }
    if (Object.keys(parsedPlanCosts).length > 0) {
      newMeta.plan_costs = parsedPlanCosts;
      newMeta.plan_cost_types = parsedPlanCostTypes;
    } else {
      delete newMeta.plan_costs;
      delete newMeta.plan_cost_types;
    }

    onSave({
      ...serviceRate,
      rate: parseFloat(rate) || 0,
      cost: null, // cost is now per-plan, clear legacy single cost
      transit_days:
        parsedTransitDays !== null && !isNaN(parsedTransitDays)
          ? parsedTransitDays
          : null,
      transit_time:
        parsedTransitTime !== null && !isNaN(parsedTransitTime)
          ? parsedTransitTime
          : null,
      meta: Object.keys(newMeta).length > 0 ? newMeta : null,
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

            {/* Rate + Transit */}
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-1.5">
                <Label className="text-xs">Base Rate</Label>
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

            {/* Per-Plan Custom Margin + Exclusion table */}
            {planMarkups.length > 0 && (
              <div className="space-y-2">
                <Label className="text-xs font-medium">Plans</Label>
                <p className="text-[11px] text-muted-foreground">
                  Set a custom margin per plan that overrides the standard tier margin for this weight bucket.
                </p>
                <div className="border border-border rounded-md overflow-hidden">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-muted/50 text-xs text-muted-foreground">
                        <th className="text-left px-3 py-1.5 font-medium">Plan</th>
                        <th className="text-left px-3 py-1.5 font-medium w-36">Custom Margin</th>
                        <th className="text-center px-3 py-1.5 font-medium w-16">Exclude</th>
                      </tr>
                    </thead>
                    <tbody>
                      {planMarkups.map((markup) => (
                        <tr key={markup.id} className="border-t border-border">
                          <td className="px-3 py-1.5">
                            <div className="text-sm text-foreground">{markup.name}</div>
                            <div className="text-[10px] text-muted-foreground">
                              {markup.markup_type === "PERCENTAGE"
                                ? `${markup.amount}%`
                                : markup.amount}
                            </div>
                          </td>
                          <td className="px-3 py-1.5">
                            <div className="flex items-center gap-1">
                              <div className="relative flex-1 min-w-[9rem]">
                                <span className="absolute left-2 top-1/2 -translate-y-1/2 text-xs text-muted-foreground pointer-events-none">€</span>
                                <Input
                                  type="number"
                                  step="0.01"
                                  value={planCosts[markup.id] || ""}
                                  onChange={(e) =>
                                    setPlanCosts((prev) => ({
                                      ...prev,
                                      [markup.id]: e.target.value,
                                    }))
                                  }
                                  placeholder="0.00"
                                  className="h-7 text-xs pl-6"
                                  disabled={excludedMarkupIds.includes(markup.id)}
                                />
                              </div>
                              <button
                                type="button"
                                className="h-7 px-1.5 text-[10px] font-medium border border-border rounded hover:bg-muted/50 shrink-0 min-w-[28px]"
                                disabled={excludedMarkupIds.includes(markup.id)}
                                onClick={() =>
                                  setPlanCostTypes((prev) => ({
                                    ...prev,
                                    [markup.id]: prev[markup.id] === "PERCENTAGE" ? "AMOUNT" : "PERCENTAGE",
                                  }))
                                }
                                title={planCostTypes[markup.id] === "PERCENTAGE" ? "Percentage" : "Fixed amount"}
                              >
                                {planCostTypes[markup.id] === "PERCENTAGE" ? "%" : "$"}
                              </button>
                            </div>
                          </td>
                          <td className="px-3 py-1.5 text-center">
                            <input
                              type="checkbox"
                              checked={excludedMarkupIds.includes(markup.id)}
                              onChange={() => toggleMarkupExclusion(markup.id)}
                              className="h-3.5 w-3.5 rounded border-border"
                            />
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Excluded Markups (non-plan markups only) */}
            {nonPlanMarkups.length > 0 && (
              <div className="space-y-2">
                <Label className="text-xs font-medium">Excluded Markups</Label>
                <p className="text-[11px] text-muted-foreground">
                  Checked markups will NOT apply to this specific rate
                </p>
                <div className="space-y-1.5 max-h-32 overflow-y-auto">
                  {nonPlanMarkups.map((markup) => (
                    <label
                      key={markup.id}
                      className="flex items-center gap-2 px-2 py-1 rounded hover:bg-muted/50 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        checked={excludedMarkupIds.includes(markup.id)}
                        onChange={() => toggleMarkupExclusion(markup.id)}
                        className="h-3.5 w-3.5 rounded border-border"
                      />
                      <span className="text-sm text-foreground">{markup.name}</span>
                      <span className="text-xs text-muted-foreground ml-auto">
                        {markup.markup_type === "PERCENTAGE"
                          ? `${markup.amount}%`
                          : markup.amount}
                      </span>
                    </label>
                  ))}
                </div>
              </div>
            )}

            {/* Excluded Surcharges */}
            {activeSurcharges.length > 0 && (
              <div className="space-y-2">
                <Label className="text-xs font-medium">Excluded Surcharges</Label>
                <p className="text-[11px] text-muted-foreground">
                  Checked surcharges will NOT apply to this specific rate
                </p>
                <div className="space-y-1.5 max-h-32 overflow-y-auto">
                  {activeSurcharges.map((surcharge) => (
                    <label
                      key={surcharge.id}
                      className="flex items-center gap-2 px-2 py-1 rounded hover:bg-muted/50 cursor-pointer"
                    >
                      <input
                        type="checkbox"
                        checked={excludedSurchargeIds.includes(surcharge.id)}
                        onChange={() => toggleSurchargeExclusion(surcharge.id)}
                        className="h-3.5 w-3.5 rounded border-border"
                      />
                      <span className="text-sm text-foreground">{surcharge.name}</span>
                      <span className="text-xs text-muted-foreground ml-auto">
                        {surcharge.amount}
                      </span>
                    </label>
                  ))}
                </div>
              </div>
            )}
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
