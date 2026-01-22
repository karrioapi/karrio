import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Checkbox } from "./ui/checkbox";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "./ui/form";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { ParcelType, DEFAULT_PARCEL_CONTENT, WeightUnitEnum } from "@karrio/types";
import { isEqual, formatRef } from "@karrio/lib";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useParcels } from "@karrio/hooks/parcel";
import { useToast } from "@karrio/ui/hooks/use-toast";

/**
 * ParcelForm - React Hook Form Implementation
 *
 * This form uses react-hook-form for performance optimization, avoiding
 * re-renders on every keystroke. Key features:
 *
 * - Zod schema validation with conditional required fields
 * - Parcel type selector: custom, carrier preset, or saved templates
 * - Package preset selector for carrier-specific presets
 * - Custom dimensions with L×W×H inputs
 * - Weight fields (always required)
 * - Document checkbox for document-only shipments
 * - Imperative handle for external form submission
 *
 * The form uses uncontrolled inputs where possible to minimize re-renders,
 * with controlled components only where necessary (selects, checkboxes).
 */

const WEIGHT_UNITS = ["KG", "LB"];
const DIMENSION_UNITS = ["CM", "IN"];

// Zod schema for parcel validation
const parcelSchema = z.object({
  is_document: z.boolean().optional(),
  packaging_type: z.string().optional(),
  package_preset: z.string().optional(),
  weight: z.number().min(0.01, "Weight must be greater than 0"),
  weight_unit: z.string().min(1, "Weight unit is required"),
  length: z.number().optional(),
  width: z.number().optional(),
  height: z.number().optional(),
  dimension_unit: z.string().optional(),
});

type ParcelFormValues = z.infer<typeof parcelSchema>;

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
  const { query } = useParcels();
  const [parcelType, setParcelType] = React.useState<string>("custom");
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const { toast } = useToast();

  // Initialize form with react-hook-form
  const form = useForm<ParcelFormValues>({
    resolver: zodResolver(parcelSchema),
    defaultValues: {
      is_document: value?.is_document || false,
      packaging_type: value?.packaging_type || "",
      package_preset: value?.package_preset || "",
      weight: value?.weight || 0,
      weight_unit: value?.weight_unit || WeightUnitEnum.KG,
      length: value?.length || undefined,
      width: value?.width || undefined,
      height: value?.height || undefined,
      dimension_unit: value?.dimension_unit || "CM",
    },
    mode: "onBlur",
  });

  const formValues = form.watch();

  // Reset form when value prop changes (e.g., edit mode)
  React.useEffect(() => {
    if (value) {
      form.reset({
        is_document: value.is_document || false,
        packaging_type: value.packaging_type || "",
        package_preset: value.package_preset || "",
        weight: value.weight || 0,
        weight_unit: value.weight_unit || WeightUnitEnum.KG,
        length: value.length || undefined,
        width: value.width || undefined,
        height: value.height || undefined,
        dimension_unit: value.dimension_unit || "CM",
      });
      // Determine initial parcel type based on value
      if (value.package_preset) {
        setParcelType("preset");
      }
    }
  }, [value, form]);

  // Notify parent of changes
  React.useEffect(() => {
    const subscription = form.watch((data) => {
      onChange?.(data as Partial<ParcelType>);
    });
    return () => subscription.unsubscribe();
  }, [form, onChange]);

  // Handle parcel type selection
  const handleParcelTypeChange = (newType: string) => {
    setParcelType(newType);

    if (newType === "custom") {
      form.setValue("package_preset", undefined);
    } else if (newType === "preset") {
      form.setValue("package_preset", "");
    } else {
      // Load template
      const template = (query.data?.parcels.edges || []).find(
        (p) => p.node.id === newType,
      )?.node;

      if (template) {
        form.reset({
          is_document: template.is_document || false,
          packaging_type: template.packaging_type || "",
          package_preset: template.package_preset || "",
          weight: template.weight || 0,
          weight_unit: template.weight_unit || WeightUnitEnum.KG,
          length: template.length || undefined,
          width: template.width || undefined,
          height: template.height || undefined,
          dimension_unit: template.dimension_unit || "CM",
        });
      }
    }
  };

  // Handle package preset selection
  const handlePackagePresetChange = (preset: string) => {
    let presetData: any = null;
    Object.values(package_presets || {}).forEach((carrierPresets: any) => {
      if (carrierPresets[preset]) {
        presetData = carrierPresets[preset];
      }
    });

    if (presetData) {
      form.setValue("package_preset", preset);
      if (presetData.length) form.setValue("length", presetData.length);
      if (presetData.width) form.setValue("width", presetData.width);
      if (presetData.height) form.setValue("height", presetData.height);
      if (presetData.dimension_unit) form.setValue("dimension_unit", presetData.dimension_unit);
      if (presetData.weight) form.setValue("weight", presetData.weight);
      if (presetData.weight_unit) form.setValue("weight_unit", presetData.weight_unit);
    } else {
      form.setValue("package_preset", preset);
    }
  };

  // Handle form submission
  const handleSubmit = async (data: ParcelFormValues) => {
    if (!onSubmit) return;

    // Additional validation for custom parcels
    if (parcelType === "custom" && !data.packaging_type) {
      toast({
        variant: "destructive",
        title: "Missing required fields",
        description: "Packaging type is required for custom parcels",
      });
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(data as Partial<ParcelType>);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Expose submit method via ref
  React.useImperativeHandle(ref, () => ({
    submit: async () => {
      const isValid = await form.trigger();
      if (isValid) {
        const data = form.getValues();
        await handleSubmit(data);
      }
    },
  }));

  // Helper functions
  const isDimensionRequired = () => {
    return !!(formValues.width || formValues.height || formValues.length);
  };

  const shouldShowDimensions = () => {
    if (parcelType === "custom") return true;
    if (parcelType === "preset" && formValues.package_preset) return true;
    return parcelType !== "custom" && parcelType !== "preset";
  };

  const getDimensionDisplay = () => {
    if (!formValues.length && !formValues.width && !formValues.height) return "";
    return `${formValues.length || 0} × ${formValues.width || 0} × ${formValues.height || 0} ${formValues.dimension_unit || "CM"}`;
  };

  const hasChanges = !isEqual(value, formValues);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className={`space-y-3 ${className}`}>
        {/* Document Only Checkbox */}
        <FormField
          control={form.control}
          name="is_document"
          render={({ field }) => (
            <FormItem className="flex items-center space-x-2">
              <FormControl>
                <Checkbox
                  id="is_document"
                  checked={field.value}
                  onCheckedChange={field.onChange}
                  disabled={disabled}
                />
              </FormControl>
              <Label htmlFor="is_document" className="text-xs text-slate-700">Document Only</Label>
            </FormItem>
          )}
        />

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
                {(query.data?.parcels.edges || []).length > 0 && (
                  <>
                    {(query.data?.parcels.edges || []).map(({ node: template }) => (
                      <SelectItem key={template.id} value={template.id}>
                        {template.meta?.label}
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
          <FormField
            control={form.control}
            name="package_preset"
            render={({ field }) => (
              <FormItem className="space-y-1">
                <FormLabel className="text-xs">Package Preset</FormLabel>
                <Select
                  value={field.value || ""}
                  onValueChange={handlePackagePresetChange}
                  disabled={disabled}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select a carrier provided parcel" />
                    </SelectTrigger>
                  </FormControl>
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
                <FormMessage className="text-xs" />
              </FormItem>
            )}
          />
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
            <FormField
              control={form.control}
              name="packaging_type"
              render={({ field }) => (
                <FormItem className="space-y-1">
                  <FormLabel className="text-xs">
                    Packaging Type <span className="text-red-500">*</span>
                  </FormLabel>
                  <Select
                    value={field.value || ""}
                    onValueChange={field.onChange}
                    disabled={disabled}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select packaging type" />
                      </SelectTrigger>
                    </FormControl>
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
                  <FormMessage className="text-xs" />
                </FormItem>
              )}
            />

            <div className="space-y-1">
              <Label className="text-xs">Dimensions</Label>
              <div className="grid grid-cols-4 gap-4">
                <FormField
                  control={form.control}
                  name="length"
                  render={({ field }) => (
                    <FormItem className="space-y-1">
                      <FormLabel className="text-xs">Length</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.01"
                          min="0"
                          placeholder="0.0"
                          value={field.value?.toString() || ""}
                          onChange={(e) => field.onChange(parseFloat(e.target.value) || undefined)}
                          required={isDimensionRequired()}
                          disabled={disabled}
                        />
                      </FormControl>
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="width"
                  render={({ field }) => (
                    <FormItem className="space-y-1">
                      <FormLabel className="text-xs">Width</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.01"
                          min="0"
                          placeholder="0.0"
                          value={field.value?.toString() || ""}
                          onChange={(e) => field.onChange(parseFloat(e.target.value) || undefined)}
                          required={isDimensionRequired()}
                          disabled={disabled}
                        />
                      </FormControl>
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="height"
                  render={({ field }) => (
                    <FormItem className="space-y-1">
                      <FormLabel className="text-xs">Height</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.01"
                          min="0"
                          placeholder="0.0"
                          value={field.value?.toString() || ""}
                          onChange={(e) => field.onChange(parseFloat(e.target.value) || undefined)}
                          required={isDimensionRequired()}
                          disabled={disabled}
                        />
                      </FormControl>
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="dimension_unit"
                  render={({ field }) => (
                    <FormItem className="space-y-1">
                      <FormLabel className="text-xs">Unit</FormLabel>
                      <Select
                        value={field.value || "CM"}
                        onValueChange={field.onChange}
                        disabled={disabled}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {DIMENSION_UNITS.map((unit) => (
                            <SelectItem key={unit} value={unit}>
                              {unit}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage className="text-xs" />
                    </FormItem>
                  )}
                />
              </div>
            </div>
          </div>
        )}

        {/* Weight */}
        <div className="space-y-1">
          <Label className="text-xs">
            Weight <span className="text-red-500">*</span>
          </Label>
          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="weight"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.0"
                      value={field.value?.toString() || ""}
                      onChange={(e) => field.onChange(parseFloat(e.target.value) || 0)}
                      required
                      disabled={disabled}
                    />
                  </FormControl>
                  <FormMessage className="text-xs" />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="weight_unit"
              render={({ field }) => (
                <FormItem>
                  <Select
                    value={field.value || WeightUnitEnum.KG}
                    onValueChange={field.onChange}
                    disabled={disabled}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {WEIGHT_UNITS.map((unit) => (
                        <SelectItem key={unit} value={unit}>
                          {unit}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage className="text-xs" />
                </FormItem>
              )}
            />
          </div>
        </div>

        {/* Submit Button */}
        {showSubmitButton && (
          <div className="flex justify-end pt-4">
            <Button
              type="submit"
              disabled={
                disabled ||
                isSubmitting ||
                !hasChanges ||
                !formValues.weight ||
                !formValues.weight_unit ||
                (parcelType === "custom" && !formValues.packaging_type)
              }
              className="min-w-[120px]"
            >
              {isSubmitting ? "Saving..." : submitButtonText}
            </Button>
          </div>
        )}
      </form>
    </Form>
  );
});

ParcelForm.displayName = "ParcelForm";
