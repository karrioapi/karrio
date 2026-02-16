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
import { MultiSelect } from "@karrio/ui/components/multi-select";
import { CURRENCY_OPTIONS, DIMENSION_UNITS, WEIGHT_UNITS } from "@karrio/types";
import { isEqual } from "@karrio/lib";
import { cn } from "@karrio/ui/lib/utils";
import { Cross2Icon } from "@radix-ui/react-icons";
import React from "react";

// =============================================================================
// CONSTANTS
// =============================================================================

// Common feature options for service levels (boolean features only)
const SERVICE_FEATURES = [
  { value: "tracked", label: "Tracked" },
  { value: "b2c", label: "B2C" },
  { value: "b2b", label: "B2B" },
  { value: "signature", label: "Signature Required" },
  { value: "insurance", label: "Insurance" },
  { value: "express", label: "Express" },
  { value: "dangerous_goods", label: "Dangerous Goods" },
  { value: "saturday_delivery", label: "Saturday Delivery" },
  { value: "sunday_delivery", label: "Sunday Delivery" },
  { value: "multicollo", label: "Multicollo" },
  { value: "neighbor_delivery", label: "Neighbor Delivery" },
  { value: "labelless", label: "Labelless" },
  { value: "notification", label: "Notification" },
  { value: "address_validation", label: "Address Validation" },
];

// Placeholder value for "not specified" options (SelectItem can't use empty string)
const NONE_VALUE = "__none__";

// Transit label options (customer-facing)
const TRANSIT_LABEL_OPTIONS = [
  { value: NONE_VALUE, label: "Not specified" },
  { value: "best_effort", label: "Best effort" },
  { value: "next_day", label: "Next day" },
  { value: "within_24h", label: "Within 24h" },
  { value: "within_48h", label: "Within 48h" },
];

// Shipment type options
const SHIPMENT_TYPE_OPTIONS = [
  { value: NONE_VALUE, label: "Not specified" },
  { value: "outbound", label: "Outbound" },
  { value: "returns", label: "Returns" },
];

// Age check options (string enum, not boolean)
const AGE_CHECK_OPTIONS = [
  { value: NONE_VALUE, label: "Not required" },
  { value: "16", label: "16+" },
  { value: "18", label: "18+" },
];

// First mile options
const FIRST_MILE_OPTIONS = [
  { value: NONE_VALUE, label: "Not specified" },
  { value: "pick_up", label: "Pick Up" },
  { value: "drop_off", label: "Drop Off" },
  { value: "pick_up_and_drop_off", label: "Pick Up & Drop Off" },
];

// Last mile options
const LAST_MILE_OPTIONS = [
  { value: NONE_VALUE, label: "Not specified" },
  { value: "home_delivery", label: "Home Delivery" },
  { value: "service_point", label: "Service Point" },
  { value: "mailbox", label: "Mailbox" },
];

// Form factor options
const FORM_FACTOR_OPTIONS = [
  { value: NONE_VALUE, label: "Not specified" },
  { value: "parcel", label: "Parcel" },
  { value: "mailbox", label: "Mailbox" },
  { value: "pallet", label: "Pallet" },
];

// Helper to convert empty/null to NONE_VALUE for Select display
const toSelectValue = (val: string | null | undefined): string => {
  return val && val.trim() !== "" ? val : NONE_VALUE;
};

// Helper to convert NONE_VALUE back to empty string for storage
const fromSelectValue = (val: string | null | undefined): string => {
  if (!val || val === NONE_VALUE || val.trim() === "") return "";
  return val.trim();
};

// =============================================================================
// TYPES
// =============================================================================

type ServiceEditorTab = "general" | "transit" | "features" | "logistics" | "limits" | "surcharges";

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
  servicePresets?: Array<{ code: string; name: string }>;
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
  features: [] as string[],
  first_mile: "",
  last_mile: "",
  form_factor: "",
  age_check: "",
  transit_label: "",
  shipment_type: "",
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function extractFeaturesArray(features: any): string[] {
  if (!features) return [];
  if (Array.isArray(features)) return features;
  return SERVICE_FEATURES
    .filter((f) => features[f.value] === true)
    .map((f) => f.value);
}

function mergeServiceWithDefaults(service: any) {
  const features = service?.features;
  const featuresArray = extractFeaturesArray(features);

  const first_mile = (features && typeof features === "object" && !Array.isArray(features))
    ? (features.first_mile || "")
    : (service?.first_mile || "");
  const last_mile = (features && typeof features === "object" && !Array.isArray(features))
    ? (features.last_mile || "")
    : (service?.last_mile || "");
  const form_factor = (features && typeof features === "object" && !Array.isArray(features))
    ? (features.form_factor || "")
    : (service?.form_factor || "");
  const age_check = (features && typeof features === "object" && !Array.isArray(features))
    ? (features.age_check || "")
    : (service?.age_check || "");
  const transit_label = (features && typeof features === "object" && !Array.isArray(features))
    ? (features.transit_label || "")
    : (service?.transit_label || "");
  const shipment_type = (features && typeof features === "object" && !Array.isArray(features))
    ? (features.shipment_type || "")
    : (service?.shipment_type || "");

  return {
    ...DEFAULT_SERVICE,
    ...service,
    surcharge_ids: service?.surcharge_ids || [],
    features: featuresArray,
    first_mile,
    last_mile,
    form_factor,
    age_check,
    transit_label,
    shipment_type,
  };
}

// =============================================================================
// MAIN COMPONENT
// =============================================================================

export const ServiceEditorModal = ({
  service,
  isOpen,
  onClose,
  onSubmit,
  trigger,
  availableSurcharges = [],
  servicePresets = [],
}: ServiceEditorModalProps) => {
  const [formData, setFormData] = React.useState(service || DEFAULT_SERVICE);
  const [loading, setLoading] = React.useState(false);
  const [activeTab, setActiveTab] = React.useState<ServiceEditorTab>("general");
  const [errors, setErrors] = React.useState<Record<string, string>>({});

  const tabs = React.useMemo(() => {
    const base: { id: ServiceEditorTab; label: string }[] = [
      { id: "general", label: "General" },
      { id: "transit", label: "Transit" },
      { id: "features", label: "Features" },
      { id: "logistics", label: "Logistics" },
      { id: "limits", label: "Limits" },
    ];
    if (availableSurcharges.length > 0) base.push({ id: "surcharges", label: "Surcharges" });
    return base;
  }, [availableSurcharges.length]);

  React.useEffect(() => {
    if (service) {
      setFormData(mergeServiceWithDefaults(service));
    } else {
      setFormData(DEFAULT_SERVICE);
    }
    setActiveTab("general");
    setErrors({});
  }, [service]);

  const handleChange = (field: string, value: any) => {
    setFormData((prev: any) => ({ ...prev, [field]: value }));
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
    if (!formData.service_name?.trim()) newErrors.service_name = "Required";
    if (!formData.service_code?.trim()) newErrors.service_code = "Required";
    else if (!/^[a-z0-9_]+$/.test(formData.service_code))
      newErrors.service_code = "Only lowercase letters, numbers, and underscores";
    setErrors(newErrors);
    if (Object.keys(newErrors).length > 0) {
      setActiveTab("general");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;

    setLoading(true);

    try {
      const serviceData = { ...formData };

      const toNullIfEmpty = (val: string | undefined | null): string | null => {
        if (!val || val.trim() === "") return null;
        return val.trim();
      };

      serviceData.features = {
        tracked: formData.features.includes("tracked"),
        b2c: formData.features.includes("b2c"),
        b2b: formData.features.includes("b2b"),
        signature: formData.features.includes("signature"),
        insurance: formData.features.includes("insurance"),
        express: formData.features.includes("express"),
        dangerous_goods: formData.features.includes("dangerous_goods"),
        saturday_delivery: formData.features.includes("saturday_delivery"),
        sunday_delivery: formData.features.includes("sunday_delivery"),
        multicollo: formData.features.includes("multicollo"),
        neighbor_delivery: formData.features.includes("neighbor_delivery"),
        labelless: formData.features.includes("labelless"),
        age_check: toNullIfEmpty(formData.age_check),
        first_mile: toNullIfEmpty(formData.first_mile),
        last_mile: toNullIfEmpty(formData.last_mile),
        form_factor: toNullIfEmpty(formData.form_factor),
        shipment_type: toNullIfEmpty(formData.shipment_type),
        transit_label: toNullIfEmpty(formData.transit_label),
      } as any;

      delete serviceData.first_mile;
      delete serviceData.last_mile;
      delete serviceData.form_factor;
      delete serviceData.age_check;
      delete serviceData.transit_label;
      delete serviceData.shipment_type;

      await onSubmit(serviceData);
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
      <DialogContent className="max-w-xl max-h-[90vh] p-0 flex flex-col">
        {/* Header */}
        <DialogHeader className="px-4 py-3 border-b bg-background shrink-0">
          <DialogTitle className="text-base">
            {isEditing ? "Edit Service" : "Add Service"}
          </DialogTitle>
          <p className="text-xs text-muted-foreground">Configure service details and settings</p>
        </DialogHeader>

        {/* Tab Bar */}
        <div className="border-b border-border px-4 shrink-0">
          <div className="flex">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
                className={cn(
                  "flex-1 py-2 text-xs font-medium border-b-2 transition-colors",
                  activeTab === tab.id
                    ? "border-primary text-primary"
                    : "border-transparent text-muted-foreground hover:text-foreground"
                )}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto px-4 py-3 min-h-0">
          <form onSubmit={handleSubmit} className="space-y-3">

            {/* General Tab */}
            {activeTab === "general" && (
              <div className="space-y-3">
                {!isEditing && servicePresets.length > 0 && (
                  <div className="space-y-1.5">
                    <Label className="text-xs">Prefill from carrier service</Label>
                    <Select
                      value=""
                      onValueChange={(code) => {
                        const preset = servicePresets.find(p => p.code === code);
                        if (preset) {
                          handleChange("service_name", preset.name);
                          handleChange("service_code", code);
                          handleChange("carrier_service_code", code);
                        }
                      }}
                    >
                      <SelectTrigger className="h-9">
                        <SelectValue placeholder="Select a preset..." />
                      </SelectTrigger>
                      <SelectContent>
                        {servicePresets.map(p => (
                          <SelectItem key={p.code} value={p.code}>{p.name}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}

                <div className="space-y-1.5">
                  <Label htmlFor="service_name" className="text-xs">Service Name <span className="text-destructive">*</span></Label>
                  <Input
                    id="service_name"
                    value={formData.service_name}
                    onChange={(e) => handleChange("service_name", e.target.value)}
                    placeholder="Standard Service"
                    className={cn("h-9", errors.service_name && "border-destructive")}
                  />
                  {errors.service_name && <p className="text-xs text-destructive">{errors.service_name}</p>}
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="service_code" className="text-xs">Service Code <span className="text-destructive">*</span></Label>
                  <Input
                    id="service_code"
                    value={formData.service_code}
                    onChange={(e) => handleChange("service_code", e.target.value)}
                    placeholder="standard_service"
                    className={cn("h-9", errors.service_code && "border-destructive")}
                  />
                  {errors.service_code && <p className="text-xs text-destructive">{errors.service_code}</p>}
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="carrier_service_code" className="text-xs">Carrier Service Code</Label>
                  <Input
                    id="carrier_service_code"
                    value={formData.carrier_service_code || ""}
                    onChange={(e) => handleChange("carrier_service_code", e.target.value)}
                    placeholder="Optional"
                    className="h-9"
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="currency" className="text-xs">Currency <span className="text-destructive">*</span></Label>
                  <Select
                    value={formData.currency}
                    onValueChange={(value) => handleChange("currency", value)}
                  >
                    <SelectTrigger className="h-9">
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

                <div className="space-y-1.5">
                  <Label htmlFor="description" className="text-xs">Description</Label>
                  <Input
                    id="description"
                    value={formData.description || ""}
                    onChange={(e) => handleChange("description", e.target.value)}
                    placeholder="Optional service description"
                    className="h-9"
                  />
                </div>

                {/* Service Type & Active - Horizontal */}
                <div className="flex flex-wrap items-center gap-4 pt-1">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="domicile"
                      checked={formData.domicile}
                      onCheckedChange={(checked) => handleChange("domicile", checked)}
                    />
                    <Label htmlFor="domicile" className="text-xs cursor-pointer">National/Domestic</Label>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="international"
                      checked={formData.international}
                      onCheckedChange={(checked) => handleChange("international", checked)}
                    />
                    <Label htmlFor="international" className="text-xs cursor-pointer">International</Label>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="active"
                      checked={formData.active}
                      onCheckedChange={(checked) => handleChange("active", checked)}
                    />
                    <Label htmlFor="active" className="text-xs cursor-pointer">Active</Label>
                  </div>
                </div>
              </div>
            )}

            {/* Transit Tab */}
            {activeTab === "transit" && (
              <div className="space-y-3">
                <div className="space-y-1.5">
                  <Label htmlFor="transit_days" className="text-xs">Transit Days</Label>
                  <Input
                    id="transit_days"
                    type="number"
                    min="0"
                    value={formData.transit_days || ""}
                    onChange={(e) => handleChange("transit_days", e.target.value ? parseInt(e.target.value) : null)}
                    placeholder="e.g., 3"
                    className="h-9"
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="transit_time" className="text-xs">Transit Time (hours)</Label>
                  <Input
                    id="transit_time"
                    type="number"
                    step="0.1"
                    min="0"
                    value={formData.transit_time || ""}
                    onChange={(e) => handleChange("transit_time", e.target.value ? parseFloat(e.target.value) : null)}
                    placeholder="e.g., 72"
                    className="h-9"
                  />
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="transit_label" className="text-xs">Transit Label</Label>
                  <Select
                    value={toSelectValue(formData.transit_label)}
                    onValueChange={(value) => handleChange("transit_label", fromSelectValue(value))}
                  >
                    <SelectTrigger className="h-9">
                      <SelectValue placeholder="Not specified" />
                    </SelectTrigger>
                    <SelectContent>
                      {TRANSIT_LABEL_OPTIONS.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <p className="text-xs text-muted-foreground">Displayed to customers in shipping rates</p>
                </div>
              </div>
            )}

            {/* Features Tab */}
            {activeTab === "features" && (
              <div className="space-y-4 py-2">
                <div className="space-y-1.5">
                  <Label className="text-xs">Service Features</Label>
                  <p className="text-xs text-muted-foreground">Select the capabilities this service supports</p>
                  <MultiSelect
                    options={SERVICE_FEATURES}
                    value={formData.features || []}
                    onValueChange={(values) => handleChange("features", values)}
                    placeholder="Select features..."
                  />
                </div>
              </div>
            )}

            {/* Logistics Tab */}
            {activeTab === "logistics" && (
              <div className="space-y-3">
                  <div className="space-y-1.5">
                    <Label htmlFor="shipment_type" className="text-xs">Shipment Type</Label>
                    <Select
                      value={toSelectValue(formData.shipment_type)}
                      onValueChange={(value) => handleChange("shipment_type", fromSelectValue(value))}
                    >
                      <SelectTrigger className="h-9">
                        <SelectValue placeholder="Not specified" />
                      </SelectTrigger>
                      <SelectContent>
                        {SHIPMENT_TYPE_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="first_mile" className="text-xs">First Mile</Label>
                    <Select
                      value={toSelectValue(formData.first_mile)}
                      onValueChange={(value) => handleChange("first_mile", fromSelectValue(value))}
                    >
                      <SelectTrigger className="h-9">
                        <SelectValue placeholder="Not specified" />
                      </SelectTrigger>
                      <SelectContent>
                        {FIRST_MILE_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="last_mile" className="text-xs">Last Mile</Label>
                    <Select
                      value={toSelectValue(formData.last_mile)}
                      onValueChange={(value) => handleChange("last_mile", fromSelectValue(value))}
                    >
                      <SelectTrigger className="h-9">
                        <SelectValue placeholder="Not specified" />
                      </SelectTrigger>
                      <SelectContent>
                        {LAST_MILE_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="form_factor" className="text-xs">Form Factor</Label>
                    <Select
                      value={toSelectValue(formData.form_factor)}
                      onValueChange={(value) => handleChange("form_factor", fromSelectValue(value))}
                    >
                      <SelectTrigger className="h-9">
                        <SelectValue placeholder="Not specified" />
                      </SelectTrigger>
                      <SelectContent>
                        {FORM_FACTOR_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="age_check" className="text-xs">Age Check</Label>
                    <Select
                      value={toSelectValue(formData.age_check)}
                      onValueChange={(value) => handleChange("age_check", fromSelectValue(value))}
                    >
                      <SelectTrigger className="h-9">
                        <SelectValue placeholder="Not required" />
                      </SelectTrigger>
                      <SelectContent>
                        {AGE_CHECK_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
              </div>
            )}

            {/* Limits Tab (merged Weight + Dimensions) */}
            {activeTab === "limits" && (
              <div className="space-y-4">
                <div className="space-y-3">
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Weight</h4>
                  <div className="space-y-1.5">
                    <Label htmlFor="min_weight" className="text-xs">Min Weight</Label>
                    <Input
                      id="min_weight"
                      type="number"
                      step="0.1"
                      min="0"
                      value={formData.min_weight || ""}
                      onChange={(e) => handleChange("min_weight", e.target.value ? parseFloat(e.target.value) : null)}
                      placeholder="0"
                      className="h-9"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="max_weight" className="text-xs">Max Weight</Label>
                    <Input
                      id="max_weight"
                      type="number"
                      step="0.1"
                      min="0"
                      value={formData.max_weight || ""}
                      onChange={(e) => handleChange("max_weight", e.target.value ? parseFloat(e.target.value) : null)}
                      placeholder="No limit"
                      className="h-9"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="weight_unit" className="text-xs">Weight Unit</Label>
                    <Select
                      value={formData.weight_unit}
                      onValueChange={(value) => handleChange("weight_unit", value)}
                    >
                      <SelectTrigger className="h-9">
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

                <div className="border-t border-border pt-4 space-y-3">
                  <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Dimensions</h4>
                  <div className="space-y-1.5">
                    <Label htmlFor="max_length" className="text-xs">Max Length</Label>
                      <Input
                        id="max_length"
                        type="number"
                        step="0.1"
                        min="0"
                        value={formData.max_length || ""}
                        onChange={(e) => handleChange("max_length", e.target.value ? parseFloat(e.target.value) : null)}
                        placeholder="No limit"
                        className="h-9"
                      />
                    </div>

                    <div className="space-y-1.5">
                      <Label htmlFor="max_width" className="text-xs">Max Width</Label>
                      <Input
                        id="max_width"
                        type="number"
                        step="0.1"
                        min="0"
                        value={formData.max_width || ""}
                        onChange={(e) => handleChange("max_width", e.target.value ? parseFloat(e.target.value) : null)}
                        placeholder="No limit"
                        className="h-9"
                      />
                    </div>

                    <div className="space-y-1.5">
                      <Label htmlFor="max_height" className="text-xs">Max Height</Label>
                      <Input
                        id="max_height"
                        type="number"
                        step="0.1"
                        min="0"
                        value={formData.max_height || ""}
                        onChange={(e) => handleChange("max_height", e.target.value ? parseFloat(e.target.value) : null)}
                        placeholder="No limit"
                        className="h-9"
                      />
                    </div>

                    <div className="space-y-1.5">
                      <Label htmlFor="dimension_unit" className="text-xs">Dimension Unit</Label>
                      <Select
                        value={formData.dimension_unit}
                        onValueChange={(value) => handleChange("dimension_unit", value)}
                      >
                        <SelectTrigger className="h-9">
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
            )}

            {/* Surcharges Tab (conditional) */}
            {activeTab === "surcharges" && availableSurcharges.length > 0 && (
              <div className="space-y-3">
                <div className="border border-border rounded-md p-2 space-y-1.5 max-h-32 overflow-y-auto">
                  {availableSurcharges.map((surcharge) => {
                    const isSelected = (formData.surcharge_ids || []).includes(surcharge.id);
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
                                : (formData.surcharge_ids || []).filter((id: string) => id !== surcharge.id);
                              handleChange("surcharge_ids", newSurchargeIds);
                            }}
                          />
                          <Label
                            htmlFor={`surcharge-${surcharge.id}`}
                            className="text-xs font-medium text-foreground cursor-pointer truncate"
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
                {(formData.surcharge_ids || []).length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {(formData.surcharge_ids || []).map((surchargeId: string) => {
                      const surcharge = availableSurcharges.find((s) => s.id === surchargeId);
                      if (!surcharge) return null;
                      return (
                        <span
                          key={surchargeId}
                          className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium bg-primary/10 text-primary rounded-full"
                        >
                          {surcharge.name || "Unnamed"}
                          <button
                            type="button"
                            onClick={() => handleChange("surcharge_ids", (formData.surcharge_ids || []).filter((id: string) => id !== surchargeId))}
                            className="hover:bg-primary/20 rounded-full p-0.5"
                          >
                            <Cross2Icon className="h-2.5 w-2.5" />
                          </button>
                        </span>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </form>
        </div>

        {/* Footer */}
        <DialogFooter className="px-4 py-3 border-t bg-background shrink-0">
          <Button type="button" variant="outline" size="sm" onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="submit"
            size="sm"
            disabled={loading || !hasChanges || !formData.service_name || !formData.service_code}
            onClick={(e) => (e.preventDefault(), handleSubmit(e as any))}
          >
            {loading ? "Saving..." : isEditing ? "Update" : "Add"} Service
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
