"use client";
import React, { useState, useEffect } from "react";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@karrio/ui/components/ui/sheet";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import { Settings, AlertCircle, Save, X } from "lucide-react";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAppMutations } from "@karrio/hooks";
import { MetafieldTypeEnum } from "@karrio/types/graphql/ee/types";
import type { MetafieldSchema } from "../types";

interface AppConfigureSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  app: {
    id: string;
    manifest: {
      name: string;
      description: string;
      metafields?: MetafieldSchema[];
    };
    installation?: {
      id: string;
      metafields: Array<{
        id: string;
        key: string;
        value: string;
        type: string;
        is_required: boolean;
      }>;
    };
  };
}

export function AppConfigureSheet({ open, onOpenChange, app }: AppConfigureSheetProps) {
  const [configValues, setConfigValues] = useState<Record<string, any>>({});
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  const { updateAppInstallation } = useAppMutations();

  // Initialize form values from existing installation metafields or defaults
  useEffect(() => {
    if (!app.manifest.metafields) return;

    const initialValues: Record<string, any> = {};

    app.manifest.metafields.forEach((field) => {
      // Check if there's an existing value from installation
      const existingValue = app.installation?.metafields?.find(
        (mf) => mf.key === field.key
      )?.value;

      if (existingValue !== undefined) {
        // Parse the existing value based on field type
        if (field.type === "boolean") {
          initialValues[field.key] = existingValue === "true" || existingValue === "1" || Boolean(existingValue);
        } else if (field.type === "number") {
          initialValues[field.key] = parseFloat(existingValue) || 0;
        } else {
          initialValues[field.key] = existingValue;
        }
      } else if (field.default_value !== undefined) {
        initialValues[field.key] = field.default_value;
      } else {
        // Set appropriate empty values based on type
        if (field.type === "boolean") {
          initialValues[field.key] = false;
        } else if (field.type === "number") {
          initialValues[field.key] = 0;
        } else {
          initialValues[field.key] = "";
        }
      }
    });

    setConfigValues(initialValues);
  }, [app.manifest.metafields, app.installation?.metafields]);

  const handleValueChange = (key: string, value: any) => {
    setConfigValues(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSave = async () => {
    if (!app.installation?.id) {
      toast({
        title: "Error",
        description: "App installation not found",
        variant: "destructive",
      });
      return;
    }

    try {
      setIsLoading(true);

      // Convert form values to metafields format
      const metafields = app.manifest.metafields?.map((field) => {
        // Map all frontend types to backend enum values (only text, number, boolean supported)
        let backendType: MetafieldTypeEnum = MetafieldTypeEnum.text;
        if (field.type === "number") {
          backendType = MetafieldTypeEnum.number;
        } else if (field.type === "boolean") {
          backendType = MetafieldTypeEnum.boolean;
        } else {
          // All other types (password, url, multiselect, select, etc.) are stored as text
          backendType = MetafieldTypeEnum.text;
        }

        return {
          key: field.key,
          value: String(configValues[field.key] || ""),
          type: backendType,
          is_required: field.is_required || false,
        };
      }) || [];

      const result = await updateAppInstallation.mutateAsync({
        id: app.installation.id,
        metafields: metafields,
      });

      if (result.update_app_installation?.errors?.length) {
        const error = result.update_app_installation.errors[0];
        toast({
          title: "Error saving configuration",
          description: error.messages?.join(", "),
          variant: "destructive",
        });
      } else {
        toast({
          title: "Configuration saved",
          description: `${app.manifest.name} has been configured successfully`,
        });
        onOpenChange(false);
      }
    } catch (error: any) {
      toast({
        title: "Error saving configuration",
        description: error.message || "An unexpected error occurred",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const renderField = (field: MetafieldSchema) => {
    const value = configValues[field.key];

    // Text field with options = Select dropdown
    if (field.type === "text" && field.options && field.options.length > 0) {
      return (
        <Select
          value={value || ""}
          onValueChange={(newValue) => handleValueChange(field.key, newValue)}
        >
          <SelectTrigger>
            <SelectValue placeholder={field.placeholder || `Select ${field.label.toLowerCase()}`} />
          </SelectTrigger>
          <SelectContent>
            {field.options.map((option) => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      );
    }

    // Boolean field = Switch
    if (field.type === "boolean") {
      return (
        <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border">
          <div className="flex items-center space-x-3">
            <Switch
              id={field.key}
              checked={value || false}
              onCheckedChange={(checked) => handleValueChange(field.key, checked)}
            />
            <Label htmlFor={field.key} className="text-sm text-slate-700">
              {value ? "Enabled" : "Disabled"}
            </Label>
          </div>
        </div>
      );
    }

    // Number field = Number input
    if (field.type === "number") {
      return (
        <Input
          type="number"
          value={value || ""}
          onChange={(e) => handleValueChange(field.key, parseFloat(e.target.value) || 0)}
          placeholder={field.placeholder}
          min={field.validation?.min}
          max={field.validation?.max}
          step={field.validation?.step || 1}
        />
      );
    }

    // Password field = Password input
    if (field.type === "password" || field.sensitive) {
      return (
        <Input
          type="password"
          value={value || ""}
          onChange={(e) => handleValueChange(field.key, e.target.value)}
          placeholder={field.placeholder || "Enter password"}
        />
      );
    }

    // Multiselect = Textarea with comma-separated values (when field has multiple options but is text type)
    if (field.options && field.options.length > 1 && field.type === "text" && field.description?.includes("comma-separated")) {
      const displayValue = Array.isArray(value) ? value.join(", ") : value || "";
      return (
        <div className="space-y-3">
          <Textarea
            value={displayValue}
            onChange={(e) => {
              const values = e.target.value.split(",").map(v => v.trim()).filter(Boolean);
              handleValueChange(field.key, values);
            }}
            placeholder={field.options ?
              `Available: ${field.options.map(o => o.label).join(", ")}` :
              "Enter comma-separated values"
            }
            rows={3}
            className="resize-none"
          />
          {field.options && (
            <div className="p-3 bg-slate-50 rounded-md border">
              <Label className="text-xs text-slate-700 mb-2 block">Available Options:</Label>
              <div className="flex flex-wrap gap-2">
                {field.options.map((option) => (
                  <Badge
                    key={option.value}
                    variant="outline"
                    className="text-xs cursor-pointer hover:bg-slate-100 transition-colors"
                    onClick={() => {
                      const currentValues = Array.isArray(value) ? value : [];
                      const newValues = currentValues.includes(option.value)
                        ? currentValues.filter(v => v !== option.value)
                        : [...currentValues, option.value];
                      handleValueChange(field.key, newValues);
                    }}
                  >
                    {option.label}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }

    // Default: Text input
    return (
      <Input
        type={field.type === "url" ? "url" : "text"}
        value={value || ""}
        onChange={(e) => handleValueChange(field.key, e.target.value)}
        placeholder={field.placeholder}
      />
    );
  };

  if (!app.manifest.metafields || app.manifest.metafields.length === 0) {
    return (
      <Sheet open={open} onOpenChange={onOpenChange}>
        <SheetContent className="w-full sm:max-w-2xl">
          <div className="h-full flex flex-col">
            <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
              <div className="flex items-center justify-between">
                <SheetTitle className="text-lg font-semibold">
                  {app.manifest.name} Configuration
                </SheetTitle>
              </div>
              <SheetDescription className="sr-only">
                Configure your {app.manifest.name} installation settings.
              </SheetDescription>
            </SheetHeader>
            <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6 pb-32">
              <div className="flex items-center justify-center py-8">
                <div className="text-center">
                  <AlertCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-sm text-muted-foreground">
                    This app has no configurable settings.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </SheetContent>
      </Sheet>
    );
  }

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="w-full sm:max-w-2xl">
        <div className="h-full flex flex-col">
          <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
            <div className="flex items-center justify-between">
              <SheetTitle className="text-lg font-semibold">
                {app.manifest.name} Configuration
              </SheetTitle>
            </div>
            <SheetDescription className="sr-only">
              Configure your {app.manifest.name} installation settings.
            </SheetDescription>
          </SheetHeader>

          <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6 pb-32">
            {app.manifest.metafields.map((field) => (
              <div key={field.key} className="space-y-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-sm font-semibold text-slate-900">
                      {field.label}
                    </h3>
                    {field.is_required && (
                      <Badge variant="destructive" className="text-xs">Required</Badge>
                    )}
                    {field.sensitive && (
                      <Badge variant="outline" className="text-xs">Sensitive</Badge>
                    )}
                  </div>

                  {field.description && (
                    <p className="text-xs text-slate-500 mb-3">{field.description}</p>
                  )}

                  <div className="space-y-2">
                    {renderField(field)}

                    {/* Validation info */}
                    {field.validation && (
                      <div className="text-xs text-slate-500">
                        {field.validation.min !== undefined && field.validation.max !== undefined && (
                          <span>Range: {field.validation.min} - {field.validation.max}</span>
                        )}
                        {field.validation.format && (
                          <span>Format: {field.validation.format}</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Floating Action Buttons */}
          <div className="sticky bottom-0 z-10 bg-white border-t px-4 py-4">
            <div className="flex items-center justify-between">
              <div></div>
              <div className="flex items-center gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onOpenChange(false)}
                  disabled={isLoading}
                >
                  Cancel
                </Button>
                <Button
                  size="sm"
                  onClick={handleSave}
                  disabled={isLoading}
                >
                  <Save className="h-4 w-4 mr-1" />
                  {isLoading ? "Saving..." : "Save Configuration"}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
