"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
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
import { CURRENCY_OPTIONS, DIMENSION_UNITS, WEIGHT_UNITS } from "@karrio/types";
import { isEqual } from "@karrio/lib";
import { Cross2Icon } from "@radix-ui/react-icons";
import React from "react";

// Surcharge type for linking
interface Surcharge {
  id: string;
  name?: string | null;
  amount?: number | null;
  surcharge_type?: string | null;
  active?: boolean | null;
}

interface ServiceEditorModalProps {
  service?: any;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (service: any) => void;
  trigger?: React.ReactElement;
  availableSurcharges?: Surcharge[];
}

const DEFAULT_SERVICE = {
  service_name: "",
  service_code: "",
  carrier_service_code: "",
  description: "",
  active: true,
  currency: "USD",
  transit_days: null,
  transit_time: null,
  max_width: null,
  max_height: null,
  max_length: null,
  dimension_unit: "CM",
  min_weight: null,
  max_weight: null,
  weight_unit: "KG",
  domicile: true,
  international: false,
  zones: [],
  surcharge_ids: [],
};

export const ServiceEditorModal = ({
  service,
  isOpen,
  onClose,
  onSubmit,
  trigger,
  availableSurcharges = [],
}: ServiceEditorModalProps) => {
  const [formData, setFormData] = React.useState(service || DEFAULT_SERVICE);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    if (service) {
      setFormData({
        ...DEFAULT_SERVICE,
        ...service,
        surcharge_ids: service.surcharge_ids || [],
      });
    } else {
      setFormData(DEFAULT_SERVICE);
    }
  }, [service]);

  const handleChange = (field: string, value: any) => {
    setFormData((prev: any) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await onSubmit(formData);
      onClose();
    } catch (error) {
      console.error("Failed to save service:", error);
    } finally {
      setLoading(false);
    }
  };

  const isEditing = !!service?.id;
  const hasChanges = !isEqual(formData, service || DEFAULT_SERVICE);

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="p-4 border-b sticky top-0 bg-background z-10">
          <DialogTitle>
            {isEditing ? "Edit Service" : "Add Service"}
          </DialogTitle>
        </DialogHeader>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto p-4">
          <form onSubmit={handleSubmit} className="space-y-4 pb-16">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="service_name">Service Name</Label>
                <Input
                  id="service_name"
                  value={formData.service_name}
                  onChange={(e) => handleChange("service_name", e.target.value)}
                  placeholder="Standard Service"
                  required
                />
              </div>

              <div>
                <Label htmlFor="service_code">Service Code</Label>
                <Input
                  id="service_code"
                  value={formData.service_code}
                  onChange={(e) => handleChange("service_code", e.target.value)}
                  placeholder="standard_service"
                  pattern="^[a-z0-9_]+$"
                  title="Only lowercase letters, numbers, and underscores allowed"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="carrier_service_code">
                  Carrier Service Code
                </Label>
                <Input
                  id="carrier_service_code"
                  value={formData.carrier_service_code || ""}
                  onChange={(e) =>
                    handleChange("carrier_service_code", e.target.value)
                  }
                  placeholder="Optional"
                />
              </div>

              <div>
                <Label htmlFor="currency">Currency</Label>
                <Select
                  value={formData.currency}
                  onValueChange={(value) => handleChange("currency", value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {CURRENCY_OPTIONS.map((currency) => (
                      <SelectItem key={currency} value={currency}>
                        {currency}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div>
              <Label htmlFor="description">Description</Label>
              <Input
                id="description"
                value={formData.description || ""}
                onChange={(e) => handleChange("description", e.target.value)}
                placeholder="Service description"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="transit_days">Transit Days</Label>
                <Input
                  id="transit_days"
                  type="number"
                  min="0"
                  value={formData.transit_days || ""}
                  onChange={(e) =>
                    handleChange(
                      "transit_days",
                      e.target.value ? parseInt(e.target.value) : null
                    )
                  }
                  placeholder="1"
                />
              </div>

              <div>
                <Label htmlFor="transit_time">Transit Time (hours)</Label>
                <Input
                  id="transit_time"
                  type="number"
                  step="0.1"
                  min="0"
                  value={formData.transit_time || ""}
                  onChange={(e) =>
                    handleChange(
                      "transit_time",
                      e.target.value ? parseFloat(e.target.value) : null
                    )
                  }
                  placeholder="24.0"
                />
              </div>
            </div>

            <div className="space-y-3">
              <Label>Service Type</Label>
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="domicile"
                    checked={formData.domicile}
                    onCheckedChange={(checked) =>
                      handleChange("domicile", checked)
                    }
                  />
                  <Label htmlFor="domicile">National/Domestic</Label>
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="international"
                    checked={formData.international}
                    onCheckedChange={(checked) =>
                      handleChange("international", checked)
                    }
                  />
                  <Label htmlFor="international">International</Label>
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="active"
                    checked={formData.active}
                    onCheckedChange={(checked) =>
                      handleChange("active", checked)
                    }
                  />
                  <Label htmlFor="active">Active</Label>
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
                    const isSelected = (formData.surcharge_ids || []).includes(
                      surcharge.id
                    );
                    return (
                      <div
                        key={surcharge.id}
                        className="flex items-center justify-between gap-2 py-1"
                      >
                        <div className="flex items-center gap-2 min-w-0">
                          <Checkbox
                            id={`surcharge-${surcharge.id}`}
                            checked={isSelected}
                            onCheckedChange={(checked) => {
                              const newSurchargeIds = checked
                                ? [...(formData.surcharge_ids || []), surcharge.id]
                                : (formData.surcharge_ids || []).filter(
                                    (id: string) => id !== surcharge.id
                                  );
                              handleChange("surcharge_ids", newSurchargeIds);
                            }}
                          />
                          <Label
                            htmlFor={`surcharge-${surcharge.id}`}
                            className="text-sm font-medium text-foreground cursor-pointer truncate"
                          >
                            {surcharge.name || "Unnamed surcharge"}
                          </Label>
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
                {(formData.surcharge_ids || []).length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {(formData.surcharge_ids || []).map((surchargeId: string) => {
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
                                (formData.surcharge_ids || []).filter(
                                  (id: string) => id !== surchargeId
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

            <div className="space-y-3">
              <Label>Weight Limits</Label>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="min_weight">Min Weight</Label>
                  <Input
                    id="min_weight"
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.min_weight || ""}
                    onChange={(e) =>
                      handleChange(
                        "min_weight",
                        e.target.value ? parseFloat(e.target.value) : null
                      )
                    }
                  />
                </div>

                <div>
                  <Label htmlFor="max_weight">Max Weight</Label>
                  <Input
                    id="max_weight"
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.max_weight || ""}
                    onChange={(e) =>
                      handleChange(
                        "max_weight",
                        e.target.value ? parseFloat(e.target.value) : null
                      )
                    }
                  />
                </div>

                <div>
                  <Label htmlFor="weight_unit">Unit</Label>
                  <Select
                    value={formData.weight_unit}
                    onValueChange={(value) => handleChange("weight_unit", value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
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

            <div className="space-y-3">
              <Label>Dimension Limits</Label>
              <div className="grid grid-cols-4 gap-4">
                <div>
                  <Label htmlFor="max_length">Max Length</Label>
                  <Input
                    id="max_length"
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.max_length || ""}
                    onChange={(e) =>
                      handleChange(
                        "max_length",
                        e.target.value ? parseFloat(e.target.value) : null
                      )
                    }
                  />
                </div>

                <div>
                  <Label htmlFor="max_width">Max Width</Label>
                  <Input
                    id="max_width"
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.max_width || ""}
                    onChange={(e) =>
                      handleChange(
                        "max_width",
                        e.target.value ? parseFloat(e.target.value) : null
                      )
                    }
                  />
                </div>

                <div>
                  <Label htmlFor="max_height">Max Height</Label>
                  <Input
                    id="max_height"
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.max_height || ""}
                    onChange={(e) =>
                      handleChange(
                        "max_height",
                        e.target.value ? parseFloat(e.target.value) : null
                      )
                    }
                  />
                </div>

                <div>
                  <Label htmlFor="dimension_unit">Unit</Label>
                  <Select
                    value={formData.dimension_unit}
                    onValueChange={(value) =>
                      handleChange("dimension_unit", value)
                    }
                  >
                    <SelectTrigger>
                      <SelectValue />
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

          {/* Sticky Footer */}
          <DialogFooter className="px-6 py-4 border-t sticky bottom-0 bg-background">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={
                loading ||
                !hasChanges ||
                !formData.service_name ||
                !formData.service_code
              }
              onClick={(e) => (e.preventDefault(), handleSubmit(e as any))}
            >
              {loading ? "Saving..." : isEditing ? "Update" : "Add"} Service
            </Button>
          </DialogFooter>
        </div>
      </DialogContent>
    </Dialog>
  );
};
