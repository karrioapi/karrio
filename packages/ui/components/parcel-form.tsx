import React from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Checkbox } from "./ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { ParcelType, DEFAULT_PARCEL_CONTENT, WeightUnitEnum } from "@karrio/types";
import { isEqual, formatRef } from "@karrio/lib";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useParcelTemplates } from "@karrio/hooks/parcel";

const WEIGHT_UNITS = ["KG", "LB"];
const DIMENSION_UNITS = ["CM", "IN"];

interface ParcelFormProps {
  value?: Partial<ParcelType>;
  onChange?: (parcel: Partial<ParcelType>) => void;
  onSubmit?: (parcel: Partial<ParcelType>) => Promise<void>;
  showSubmitButton?: boolean;
  submitButtonText?: string;
  disabled?: boolean;
  className?: string;
  showTemplateSelector?: boolean;
}

export interface ParcelFormRef {
  submit: () => Promise<void>;
}

export const ParcelForm = React.forwardRef<ParcelFormRef, ParcelFormProps>(({
  value = DEFAULT_PARCEL_CONTENT,
  onChange,
  onSubmit,
  showSubmitButton = true,
  submitButtonText = "Save Parcel",
  disabled = false,
  className = "",
  showTemplateSelector = true,
}, ref) => {
  const { references: { packaging_types, package_presets } } = useAPIMetadata();
  const { query } = useParcelTemplates();
  const [parcel, setParcel] = React.useState<Partial<ParcelType>>(value || DEFAULT_PARCEL_CONTENT);
  const [parcelType, setParcelType] = React.useState<string>("custom");
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  React.useEffect(() => {
    setParcel(value || DEFAULT_PARCEL_CONTENT);
  }, [value]);

  const handleChange = (field: string, fieldValue: string | boolean | number) => {
    const updatedParcel = { ...parcel, [field]: fieldValue };
    setParcel(updatedParcel);
    onChange?.(updatedParcel);
  };

  const handleParcelTypeChange = (newType: string) => {
    setParcelType(newType);

    if (newType === "custom") {
      // Reset to custom parcel
      const customParcel = {
        ...parcel,
        package_preset: undefined,
      };
      setParcel(customParcel);
      onChange?.(customParcel);
    } else if (newType === "preset") {
      // Keep current parcel but clear preset
      const presetParcel = {
        ...parcel,
        package_preset: "",
      };
      setParcel(presetParcel);
      onChange?.(presetParcel);
    } else {
      // Load template
      const template = (query.data?.parcel_templates.edges || []).find(
        (p) => p.node.id === newType,
      )?.node?.parcel;

      if (template) {
        const templateParcel = {
          ...parcel,
          weight: template.weight,
          weight_unit: template.weight_unit,
          length: template.length,
          width: template.width,
          height: template.height,
          dimension_unit: template.dimension_unit,
          packaging_type: template.packaging_type,
          package_preset: template.package_preset,
          is_document: template.is_document,
        };
        setParcel(templateParcel);
        onChange?.(templateParcel);
      }
    }
  };

  const handlePackagePresetChange = (preset: string) => {
    // Find preset data and apply it
    let presetData = null;
    Object.values(package_presets || {}).forEach((carrierPresets: any) => {
      if (carrierPresets[preset]) {
        presetData = carrierPresets[preset];
      }
    });

    if (presetData) {
      const presetParcel = { ...parcel, ...(presetData as object), package_preset: preset };
      setParcel(presetParcel);
      onChange?.(presetParcel);
    } else {
      handleChange("package_preset", preset);
    }
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!onSubmit) return;

    setIsSubmitting(true);
    try {
      await onSubmit(parcel);
    } finally {
      setIsSubmitting(false);
    }
  };

  React.useImperativeHandle(ref, () => ({
    submit: () => handleSubmit(),
  }));

  const isDimensionRequired = (parcel: Partial<ParcelType>) => {
    return !!(parcel.width || parcel.height || parcel.length);
  };

  const shouldShowDimensions = () => {
    if (parcelType === "custom") return true;
    if (parcelType === "preset" && parcel.package_preset) return true;
    return parcelType !== "custom" && parcelType !== "preset";
  };

  const getDimensionDisplay = () => {
    if (!parcel.length && !parcel.width && !parcel.height) return "";
    return `${parcel.length || 0} × ${parcel.width || 0} × ${parcel.height || 0} ${parcel.dimension_unit || "CM"}`;
  };

  const hasChanges = !isEqual(value, parcel);

  return (
    <form onSubmit={handleSubmit} className={`space-y-3 ${className}`}>
      {/* Document Only Checkbox */}
      <div className="flex items-center space-x-2">
        <Checkbox
          id="is_document"
          checked={parcel.is_document || false}
          onCheckedChange={(checked) => handleChange("is_document", !!checked)}
          disabled={disabled}
        />
        <Label htmlFor="is_document" className="text-xs text-slate-700">Document Only</Label>
      </div>

      {/* Parcel Type Selector */}
      {showTemplateSelector && (
        <div className="space-y-1">
          <Label htmlFor="parcel_type" className="text-xs text-slate-700">Parcel Type</Label>
          <Select
            value={parcelType}
            onValueChange={handleParcelTypeChange}
            disabled={disabled}
          >
            <SelectTrigger className="h-8">
              <SelectValue placeholder="Select parcel type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="custom">Custom Measurements</SelectItem>
              <SelectItem value="preset">Carrier Parcel Presets</SelectItem>
              {(query.data?.parcel_templates.edges || []).length > 0 && (
                <>
                  {(query.data?.parcel_templates.edges || []).map(({ node: template }) => (
                    <SelectItem key={template.id} value={template.id}>
                      {template.label}
                    </SelectItem>
                  ))}
                </>
              )}
            </SelectContent>
          </Select>
        </div>
      )}

      {/* Package Preset Selector */}
      {parcelType === "preset" && (
        <div className="space-y-2">
          <Label htmlFor="package_preset">Package Preset</Label>
          <Select
            value={parcel.package_preset || ""}
            onValueChange={handlePackagePresetChange}
            disabled={disabled}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select a carrier provided parcel" />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(package_presets || {}).map(([carrier, presets]) => (
                <React.Fragment key={carrier}>
                  {Object.keys(presets as object).map((preset) => (
                    <SelectItem key={preset} value={preset}>
                      {formatRef(carrier)} - {formatRef(preset)}
                    </SelectItem>
                  ))}
                </React.Fragment>
              ))}
            </SelectContent>
          </Select>
        </div>
      )}

      {/* Dimension Display for Presets */}
      {shouldShowDimensions() && getDimensionDisplay() && (
        <div className="text-sm text-muted-foreground">
          Dimensions: {getDimensionDisplay()}
        </div>
      )}

      {/* Custom Dimensions */}
      {parcelType === "custom" && (
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="packaging_type">
              Packaging Type <span className="text-red-500">*</span>
            </Label>
            <Select
              value={parcel.packaging_type || ""}
              onValueChange={(value) => handleChange("packaging_type", value)}
              disabled={disabled}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select packaging type" />
              </SelectTrigger>
              <SelectContent>
                {packaging_types &&
                  Object.entries(packaging_types).map(([carrier, types]) => (
                    <React.Fragment key={carrier}>
                      {Object.keys(types as object).map((type) => (
                        <SelectItem key={type} value={type}>
                          {formatRef(carrier)} - {formatRef(type)}
                        </SelectItem>
                      ))}
                    </React.Fragment>
                  ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Dimensions</Label>
            <div className="grid grid-cols-4 gap-4">
              <div className="space-y-2">
                <Label htmlFor="length" className="text-xs">Length</Label>
                <Input
                  id="length"
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder="0.0"
                  value={parcel.length?.toString() || ""}
                  onChange={(e) => handleChange("length", parseFloat(e.target.value) || 0)}
                  required={isDimensionRequired(parcel)}
                  disabled={disabled}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="width" className="text-xs">Width</Label>
                <Input
                  id="width"
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder="0.0"
                  value={parcel.width?.toString() || ""}
                  onChange={(e) => handleChange("width", parseFloat(e.target.value) || 0)}
                  required={isDimensionRequired(parcel)}
                  disabled={disabled}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="height" className="text-xs">Height</Label>
                <Input
                  id="height"
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder="0.0"
                  value={parcel.height?.toString() || ""}
                  onChange={(e) => handleChange("height", parseFloat(e.target.value) || 0)}
                  required={isDimensionRequired(parcel)}
                  disabled={disabled}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="dimension_unit" className="text-xs">Unit</Label>
                <Select
                  value={parcel.dimension_unit || "CM"}
                  onValueChange={(value) => handleChange("dimension_unit", value)}
                  disabled={disabled}
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
        </div>
      )}

      {/* Weight */}
      <div className="space-y-2">
        <Label>
          Weight <span className="text-red-500">*</span>
        </Label>
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Input
              type="number"
              step="0.01"
              min="0"
              placeholder="0.0"
              value={parcel.weight?.toString() || ""}
              onChange={(e) => handleChange("weight", parseFloat(e.target.value) || 0)}
              required
              disabled={disabled}
            />
          </div>
          <div className="space-y-2">
            <Select
              value={parcel.weight_unit || WeightUnitEnum.KG}
              onValueChange={(value) => handleChange("weight_unit", value)}
              disabled={disabled}
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

      {/* Submit Button */}
      {showSubmitButton && (
        <div className="flex justify-end pt-4">
          <Button
            type="submit"
            disabled={disabled || isSubmitting || !hasChanges}
            className="min-w-[120px]"
          >
            {isSubmitting ? "Saving..." : submitButtonText}
          </Button>
        </div>
      )}
    </form>
  );
});

ParcelForm.displayName = "ParcelForm";
