"use client";

import React, { useEffect, useState } from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@karrio/ui/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import { Cross2Icon } from "@radix-ui/react-icons";
import type {
  ServiceLevelWithZones,
  SharedSurcharge,
} from "@karrio/ui/components/rate-sheet-editor";

// Enums - inline for simplicity; can also be imported from @karrio/types
const DIMENSION_UNITS = ["CM", "IN"];
const WEIGHT_UNITS = ["KG", "LB", "OZ", "G"];
const CURRENCIES = [
  "USD",
  "EUR",
  "GBP",
  "CAD",
  "AUD",
  "CHF",
  "CNY",
  "JPY",
  "INR",
  "BRL",
  "MXN",
  "PLN",
  "HKD",
  "SGD",
  "NZD",
  "SEK",
  "NOK",
  "DKK",
  "ZAR",
  "MYR",
  "THB",
];

// Default service values - ensures all fields have proper defaults
const DEFAULT_SERVICE = {
  service_name: "",
  service_code: "",
  currency: "USD",
  carrier_service_code: "",
  description: "",
  active: true,
  domicile: true,
  international: false,
  transit_days: null as number | null,
  transit_time: null as number | null,
  max_width: null as number | null,
  max_height: null as number | null,
  max_length: null as number | null,
  dimension_unit: "CM" as string | null,
  max_weight: null as number | null,
  weight_unit: "KG" as string | null,
  surcharge_ids: [] as string[],
};

type ServiceFormData = typeof DEFAULT_SERVICE;

interface ServiceEditorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  service?: ServiceLevelWithZones | null;
  onSave: (serviceData: Partial<ServiceLevelWithZones>) => void;
  availableSurcharges?: SharedSurcharge[];
}

// Helper to merge service into defaults, handling null values properly
function mergeServiceWithDefaults(
  service: ServiceLevelWithZones | null | undefined
): ServiceFormData {
  if (!service) return DEFAULT_SERVICE;

  return {
    service_name: service.service_name ?? DEFAULT_SERVICE.service_name,
    service_code: service.service_code ?? DEFAULT_SERVICE.service_code,
    currency: service.currency ?? DEFAULT_SERVICE.currency,
    carrier_service_code:
      service.carrier_service_code ?? DEFAULT_SERVICE.carrier_service_code,
    description: service.description ?? DEFAULT_SERVICE.description,
    active: service.active ?? DEFAULT_SERVICE.active,
    domicile: service.domicile ?? DEFAULT_SERVICE.domicile,
    international: service.international ?? DEFAULT_SERVICE.international,
    transit_days: service.transit_days ?? DEFAULT_SERVICE.transit_days,
    transit_time: service.transit_time ?? DEFAULT_SERVICE.transit_time,
    max_width: service.max_width ?? DEFAULT_SERVICE.max_width,
    max_height: service.max_height ?? DEFAULT_SERVICE.max_height,
    max_length: service.max_length ?? DEFAULT_SERVICE.max_length,
    dimension_unit: service.dimension_unit ?? DEFAULT_SERVICE.dimension_unit,
    max_weight: service.max_weight ?? DEFAULT_SERVICE.max_weight,
    weight_unit: service.weight_unit ?? DEFAULT_SERVICE.weight_unit,
    surcharge_ids: service.surcharge_ids ?? DEFAULT_SERVICE.surcharge_ids,
  };
}

export function ServiceEditorDialog({
  open,
  onOpenChange,
  service,
  onSave,
  availableSurcharges = [],
}: ServiceEditorDialogProps) {
  const isEditMode = !!service;

  // Initialize with service data immediately using lazy initialization
  const [formData, setFormData] = useState<ServiceFormData>(() =>
    mergeServiceWithDefaults(service)
  );
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Reset form when service changes OR when dialog opens
  useEffect(() => {
    setFormData(mergeServiceWithDefaults(service));
  }, [service, open]);

  const handleChange = (field: keyof ServiceFormData, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    // Clear error when field changes
    if (errors[field]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.service_name || !formData.service_name.trim()) {
      newErrors.service_name = "Service name is required";
    }

    if (!formData.service_code || !formData.service_code.trim()) {
      newErrors.service_code = "Service code is required";
    } else if (!/^[a-z0-9_]+$/.test(formData.service_code)) {
      newErrors.service_code =
        "Only lowercase letters, numbers, and underscores allowed";
    }

    if (!formData.currency) {
      newErrors.currency = "Currency is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Build serviceData, only including fields that have actual values
      const serviceData: Partial<ServiceLevelWithZones> = {
        service_name: formData.service_name,
        service_code: formData.service_code,
        currency: formData.currency as any,
        active: formData.active,
        domicile: formData.domicile,
        international: formData.international,
      };

      // Only include optional fields if they have values
      if (formData.carrier_service_code) {
        serviceData.carrier_service_code = formData.carrier_service_code;
      }
      if (formData.description) {
        serviceData.description = formData.description;
      }
      if (formData.transit_days !== null && formData.transit_days !== undefined) {
        serviceData.transit_days = Number(formData.transit_days);
      }
      if (formData.transit_time !== null && formData.transit_time !== undefined) {
        serviceData.transit_time = Number(formData.transit_time);
      }
      if (formData.max_width !== null && formData.max_width !== undefined) {
        serviceData.max_width = Number(formData.max_width);
      }
      if (formData.max_height !== null && formData.max_height !== undefined) {
        serviceData.max_height = Number(formData.max_height);
      }
      if (formData.max_length !== null && formData.max_length !== undefined) {
        serviceData.max_length = Number(formData.max_length);
      }
      if (formData.dimension_unit) {
        serviceData.dimension_unit = formData.dimension_unit as any;
      }
      if (formData.max_weight !== null && formData.max_weight !== undefined) {
        serviceData.max_weight = Number(formData.max_weight);
      }
      if (formData.weight_unit) {
        serviceData.weight_unit = formData.weight_unit as any;
      }

      // Always include surcharge_ids (even if empty array)
      serviceData.surcharge_ids = formData.surcharge_ids;

      onSave(serviceData);
      onOpenChange(false);
    } catch (error) {
      console.error("Failed to save service:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {isEditMode ? "Edit Service" : "Add Service"}
          </DialogTitle>
          <DialogDescription>
            Configure service details and settings
          </DialogDescription>
        </DialogHeader>

        <form id="service-form" onSubmit={handleSubmit} className="space-y-4">
          {/* Basic Information - 2 Column Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Service Name */}
            <div>
              <Label htmlFor="service_name">
                Service Name <span className="text-destructive">*</span>
              </Label>
              <Input
                id="service_name"
                value={formData.service_name}
                onChange={(e) => handleChange("service_name", e.target.value)}
                placeholder="e.g., Express Shipping"
              />
              {errors.service_name && (
                <p className="text-sm text-destructive mt-1">
                  {errors.service_name}
                </p>
              )}
            </div>

            {/* Service Code */}
            <div>
              <Label htmlFor="service_code">
                Service Code <span className="text-destructive">*</span>
              </Label>
              <Input
                id="service_code"
                value={formData.service_code}
                onChange={(e) => handleChange("service_code", e.target.value)}
                placeholder="e.g., express_shipping"
              />
              {errors.service_code && (
                <p className="text-sm text-destructive mt-1">
                  {errors.service_code}
                </p>
              )}
            </div>
          </div>

          <p className="text-xs text-muted-foreground -mt-2">
            Service code: only lowercase letters, numbers, and underscores
          </p>

          <div className="grid grid-cols-2 gap-4">
            {/* Carrier Service Code */}
            <div>
              <Label htmlFor="carrier_service_code">Carrier Service Code</Label>
              <Input
                id="carrier_service_code"
                value={formData.carrier_service_code || ""}
                onChange={(e) =>
                  handleChange("carrier_service_code", e.target.value)
                }
                placeholder="Optional"
              />
            </div>

            {/* Currency */}
            <div>
              <Label htmlFor="currency">
                Currency <span className="text-destructive">*</span>
              </Label>
              <Select
                value={formData.currency}
                onValueChange={(value) => handleChange("currency", value)}
              >
                <SelectTrigger id="currency" className="w-full">
                  <SelectValue placeholder="Select currency" />
                </SelectTrigger>
                <SelectContent>
                  {CURRENCIES.map((code) => (
                    <SelectItem key={code} value={code}>
                      {code}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.currency && (
                <p className="text-sm text-destructive mt-1">
                  {errors.currency}
                </p>
              )}
            </div>
          </div>

          {/* Description - Full Width */}
          <div>
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={formData.description || ""}
              onChange={(e) => handleChange("description", e.target.value)}
              placeholder="Optional service description"
            />
          </div>

          {/* Transit & Timing - 2 Column Grid */}
          <div className="grid grid-cols-2 gap-4">
            {/* Transit Days */}
            <div>
              <Label htmlFor="transit_days">Transit Days</Label>
              <Input
                id="transit_days"
                type="number"
                min={0}
                step={1}
                value={formData.transit_days ?? ""}
                onChange={(e) => {
                  const val = e.target.value;
                  handleChange("transit_days", val === "" ? null : Number(val));
                }}
                placeholder="e.g., 3"
              />
            </div>

            {/* Transit Time */}
            <div>
              <Label htmlFor="transit_time">Transit Time (hours)</Label>
              <Input
                id="transit_time"
                type="number"
                min={0}
                step={0.1}
                value={formData.transit_time ?? ""}
                onChange={(e) => {
                  const val = e.target.value;
                  handleChange("transit_time", val === "" ? null : Number(val));
                }}
                placeholder="e.g., 72.5"
              />
            </div>
          </div>

          {/* Service Type - Horizontal Checkboxes */}
          <div className="space-y-3">
            <Label>Service Type</Label>
            <div className="flex flex-wrap items-center gap-4 sm:gap-6">
              {/* Domicile Checkbox */}
              <div className="flex items-center gap-2">
                <input
                  id="domicile"
                  type="checkbox"
                  checked={formData.domicile}
                  onChange={(e) => handleChange("domicile", e.target.checked)}
                  className="h-4 w-4 rounded border-border text-primary focus:ring-2 focus:ring-ring focus:ring-offset-2"
                />
                <label
                  htmlFor="domicile"
                  className="text-sm font-medium text-foreground cursor-pointer"
                >
                  National/Domestic
                </label>
              </div>

              {/* International Checkbox */}
              <div className="flex items-center gap-2">
                <input
                  id="international"
                  type="checkbox"
                  checked={formData.international}
                  onChange={(e) =>
                    handleChange("international", e.target.checked)
                  }
                  className="h-4 w-4 rounded border-border text-primary focus:ring-2 focus:ring-ring focus:ring-offset-2"
                />
                <label
                  htmlFor="international"
                  className="text-sm font-medium text-foreground cursor-pointer"
                >
                  International
                </label>
              </div>

              {/* Active Checkbox */}
              <div className="flex items-center gap-2">
                <input
                  id="active"
                  type="checkbox"
                  checked={formData.active}
                  onChange={(e) => handleChange("active", e.target.checked)}
                  className="h-4 w-4 rounded border-border text-primary focus:ring-2 focus:ring-ring focus:ring-offset-2"
                />
                <label
                  htmlFor="active"
                  className="text-sm font-medium text-foreground cursor-pointer"
                >
                  Active
                </label>
              </div>
            </div>
          </div>

          {/* Surcharges Selection */}
          {availableSurcharges.length > 0 && (
            <div className="space-y-3">
              <Label>Applied Surcharges</Label>
              <p className="text-xs text-muted-foreground -mt-2">
                Select surcharges that apply to this service
              </p>
              <div className="border border-border rounded-md p-3 space-y-2 max-h-40 overflow-y-auto">
                {availableSurcharges.map((surcharge) => {
                  const isSelected = formData.surcharge_ids.includes(
                    surcharge.id
                  );
                  return (
                    <div
                      key={surcharge.id}
                      className="flex items-center justify-between gap-2 py-1"
                    >
                      <div className="flex items-center gap-2 min-w-0">
                        <input
                          type="checkbox"
                          id={`surcharge-${surcharge.id}`}
                          checked={isSelected}
                          onChange={(e) => {
                            const newSurchargeIds = e.target.checked
                              ? [...formData.surcharge_ids, surcharge.id]
                              : formData.surcharge_ids.filter(
                                  (id) => id !== surcharge.id
                                );
                            handleChange("surcharge_ids", newSurchargeIds);
                          }}
                          className="h-4 w-4 rounded border-border text-primary focus:ring-2 focus:ring-ring focus:ring-offset-2"
                        />
                        <label
                          htmlFor={`surcharge-${surcharge.id}`}
                          className="text-sm font-medium text-foreground cursor-pointer truncate"
                        >
                          {surcharge.name || "Unnamed surcharge"}
                        </label>
                      </div>
                      <span className="text-xs text-muted-foreground whitespace-nowrap">
                        {surcharge.surcharge_type === "percentage"
                          ? `${surcharge.amount}%`
                          : `${surcharge.amount}`}
                      </span>
                    </div>
                  );
                })}
              </div>
              {/* Show selected surcharges as chips */}
              {formData.surcharge_ids.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {formData.surcharge_ids.map((surchargeId) => {
                    const surcharge = availableSurcharges.find(
                      (s) => s.id === surchargeId
                    );
                    if (!surcharge) return null;
                    return (
                      <span
                        key={surchargeId}
                        className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium bg-primary/10 text-primary rounded-full"
                      >
                        {surcharge.name || "Unnamed"}
                        <button
                          type="button"
                          onClick={() => {
                            handleChange(
                              "surcharge_ids",
                              formData.surcharge_ids.filter(
                                (id) => id !== surchargeId
                              )
                            );
                          }}
                          className="hover:bg-primary/20 rounded-full p-0.5"
                        >
                          <Cross2Icon className="h-3 w-3" />
                        </button>
                      </span>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* Weight Limits */}
          <div className="space-y-3">
            <Label>Weight Limits</Label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              {/* Max Weight */}
              <div className="col-span-1">
                <Label htmlFor="max_weight" className="text-xs">
                  Max Weight
                </Label>
                <Input
                  id="max_weight"
                  type="number"
                  min={0}
                  step={0.1}
                  value={formData.max_weight ?? ""}
                  onChange={(e) => {
                    const val = e.target.value;
                    handleChange("max_weight", val === "" ? null : Number(val));
                  }}
                  placeholder="Max Weight"
                />
              </div>

              {/* Weight Unit */}
              <div className="col-span-1 sm:col-span-2">
                <Label htmlFor="weight_unit" className="text-xs">
                  Unit
                </Label>
                <Select
                  value={formData.weight_unit ?? "KG"}
                  onValueChange={(value) => handleChange("weight_unit", value)}
                >
                  <SelectTrigger id="weight_unit" className="w-full">
                    <SelectValue placeholder="Unit" />
                  </SelectTrigger>
                  <SelectContent>
                    {WEIGHT_UNITS.map((unit) => (
                      <SelectItem key={unit} value={unit}>
                        {unit}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>

          {/* Dimension Limits */}
          <div className="space-y-3">
            <Label>Dimension Limits</Label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {/* Max Length */}
              <div>
                <Label htmlFor="max_length" className="text-xs">
                  Max Length
                </Label>
                <Input
                  id="max_length"
                  type="number"
                  min={0}
                  step={0.1}
                  value={formData.max_length ?? ""}
                  onChange={(e) => {
                    const val = e.target.value;
                    handleChange("max_length", val === "" ? null : Number(val));
                  }}
                  placeholder="Length"
                />
              </div>

              {/* Max Width */}
              <div>
                <Label htmlFor="max_width" className="text-xs">
                  Max Width
                </Label>
                <Input
                  id="max_width"
                  type="number"
                  min={0}
                  step={0.1}
                  value={formData.max_width ?? ""}
                  onChange={(e) => {
                    const val = e.target.value;
                    handleChange("max_width", val === "" ? null : Number(val));
                  }}
                  placeholder="Width"
                />
              </div>

              {/* Max Height */}
              <div>
                <Label htmlFor="max_height" className="text-xs">
                  Max Height
                </Label>
                <Input
                  id="max_height"
                  type="number"
                  min={0}
                  step={0.1}
                  value={formData.max_height ?? ""}
                  onChange={(e) => {
                    const val = e.target.value;
                    handleChange("max_height", val === "" ? null : Number(val));
                  }}
                  placeholder="Height"
                />
              </div>

              {/* Dimension Unit */}
              <div>
                <Label htmlFor="dimension_unit" className="text-xs">
                  Unit
                </Label>
                <Select
                  value={formData.dimension_unit ?? "CM"}
                  onValueChange={(value) =>
                    handleChange("dimension_unit", value)
                  }
                >
                  <SelectTrigger id="dimension_unit" className="w-full">
                    <SelectValue placeholder="Unit" />
                  </SelectTrigger>
                  <SelectContent>
                    {DIMENSION_UNITS.map((unit) => (
                      <SelectItem key={unit} value={unit}>
                        {unit}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        </form>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={loading}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            form="service-form"
            disabled={loading}
          >
            {loading ? "Saving..." : "Save"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default ServiceEditorDialog;
