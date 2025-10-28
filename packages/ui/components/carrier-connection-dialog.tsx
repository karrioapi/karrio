import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "./ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "./ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "./ui/tabs";
import { CountrySelect } from "./country-select";
import { GetSystemConnections_system_carrier_connections_edges_node } from "@karrio/types/graphql/admin/types";
import { IntegrationStatusBadge } from "@karrio/ui/core/components/integration-status-badge";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { EnhancedMetadataEditor } from "./enhanced-metadata-editor";
import { zodResolver } from "@hookform/resolvers/zod";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useState, useEffect } from "react";
import { References } from "@karrio/types";
import { useForm } from "react-hook-form";
import { isEqual } from "@karrio/lib";
import { Button } from "./ui/button";
import { Switch } from "./ui/switch";
import { Input } from "./ui/input";
import * as z from "zod";


type Connection = Omit<GetSystemConnections_system_carrier_connections_edges_node, 'credentials' | 'config' | 'metadata'> & {
  credentials?: Record<string, any>;
  config?: Record<string, any>;
  metadata?: Record<string, any>;
};

const formSchema = z.object({
  // Use string instead of enum to avoid runtime enum issues when admin types are not generated yet
  carrier_name: z.string().min(1, { message: "Carrier is required" }),
  carrier_id: z.string().min(1, { message: "Carrier ID is required" }),
  active: z.boolean(),
  capabilities: z.array(z.string()),
  credentials: z.record(z.any()),
  config: z.record(z.any()),
  metadata: z.record(z.any()),
});

type FormData = z.infer<typeof formSchema>;

interface CarrierConnectionDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  selectedConnection: Connection | null;
  references?: References;
  title?: string;
  description?: string;
  disableCarrierSelection?: boolean;
  onSuccess?: () => void;
  onSubmit?: (values: FormData, connection: Connection | null) => Promise<void>;
}

export function CarrierConnectionDialog({
  open,
  onOpenChange,
  selectedConnection,
  references,
  title,
  description,
  disableCarrierSelection = false,
  onSuccess,
  onSubmit,
}: CarrierConnectionDialogProps) {
  const [initialValues, setInitialValues] = useState<FormData | null>(null);
  const { toast } = useToast();

  const defaultValues: FormData = {
    carrier_name: "",
    carrier_id: "",
    active: false,
    capabilities: [],
    credentials: {},
    config: {},
    metadata: {},
  };

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues,
  });

  const handleSubmit = async (values: FormData) => {
    if (!onSubmit) {
      toast({
        title: "Error",
        description: "No submit handler provided",
        variant: "destructive",
      });
      return;
    }

    try {
      // Keep carrier_name as-is (should be "generic" for custom carriers)
      // The custom_carrier_name stays in credentials where backend expects it
      await onSubmit(values, selectedConnection);

      toast({
        title: "Success",
        description: `Carrier connection ${selectedConnection ? 'updated' : 'created'} successfully!`,
      });

      onSuccess?.();
      onOpenChange(false);
    } catch (error: any) {
      toast({
        title: "Error",
        description: error?.message || error?.data?.message || `Failed to ${selectedConnection ? 'update' : 'create'} carrier connection`,
        variant: "destructive",
      });
    }
  };

  const { watch, setValue } = form;

  const formValues = watch();
  const isDirty = initialValues ? !isEqual(formValues, initialValues) : true; // Allow saving for new connections

  const areCredentialsValid = () => {
    const carrierName = watch("carrier_name");
    const carrierId = watch("carrier_id");

    // Basic validation - must have carrier and carrier_id
    if (!carrierName || !carrierId) return false;

    const credentials = watch("credentials");
    const fields = references?.connection_fields?.[carrierName] || {};

    // For generic (custom) carriers, display_name and custom_carrier_name are always required
    if (carrierName === "generic") {
      const displayName = credentials?.display_name;
      const customCarrierName = credentials?.custom_carrier_name;

      if (!displayName || displayName.trim() === "") {
        return false;
      }

      if (!customCarrierName || customCarrierName.trim() === "") {
        return false;
      }
    }

    // Check account_country_code separately if required
    const accountCountryCodeField = fields["account_country_code"];
    if (accountCountryCodeField?.required) {
      const accountCountryCode = credentials?.account_country_code;
      if (!accountCountryCode || accountCountryCode === "") {
        return false;
      }
    }

    // Check only required credential fields (excluding the ones we've filtered out)
    return Object.entries(fields)
      .filter(([key]) => ![
        "display_name",
        "custom_carrier_name",
        "account_country_code", // This is handled by CountrySelect component
        "metadata",
        "config",
        "label_template",
        "services"
      ].includes(key))
      .every(([key, field]: [string, any]) => {
        if (field.required) {
          const value = credentials?.[key];
          return value !== undefined && value !== "" && value !== null;
        }
        return true;
      });
  };

  const isValid = areCredentialsValid();

  useEffect(() => {
    if (open) {
      const initial = selectedConnection
        ? {
          // If the connection has a custom_carrier_name in credentials, it's a generic carrier
          carrier_name: selectedConnection.credentials?.custom_carrier_name ? "generic" : selectedConnection.carrier_name || "",
          carrier_id: selectedConnection.carrier_id || "",
          active: selectedConnection.active || false,
          capabilities: selectedConnection.capabilities || [],
          credentials: selectedConnection.credentials || {},
          config: selectedConnection.config || {},
          metadata: selectedConnection.metadata || {},
        }
        : {
          ...defaultValues,
          active: true, // Set active by default for new connections
        };

      form.reset(initial);
      setInitialValues(initial);

      // Force re-render of the Select component
      setTimeout(() => {
        if (initial.carrier_name) {
          form.setValue('carrier_name', initial.carrier_name, { shouldDirty: false });
        }
      }, 0);
    }
  }, [open, selectedConnection?.id, selectedConnection?.carrier_name]);


  useEffect(() => {
    const subscription = watch((value, { name, type }) => {
      if (name === 'carrier_name' && type === 'change' && !selectedConnection) {
        const carrierName = value.carrier_name as string;
        const fields = references?.connection_fields?.[carrierName] || {};
        const defaultCredentials = Object.entries(fields).reduce(
          (acc, [key, field]: [string, any]) => ({
            ...acc,
            [key]: field.default || "",
          }),
          {}
        );
        setValue("credentials", defaultCredentials);

        // Set all capabilities as checked by default
        const capabilities = references?.carrier_capabilities?.[carrierName] || [];
        setValue("capabilities", capabilities);
      }
    });
    return () => subscription.unsubscribe();
  }, [watch, setValue, selectedConnection, references]);


  const handleModalClose = () => {
    onOpenChange(false);
  };

  const formatLabel = (label: string) => {
    return label
      .split(/[\s_-]/)
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(" ");
  };

  const renderCredentialFields = () => {
    const carrierName = watch("carrier_name");
    if (!carrierName) return null;
    const fields = references?.connection_fields?.[carrierName] || {};

    // First render display_name and custom_carrier_name if they exist
    const specialFields = Object.entries(fields)
      .filter(([key]) => ["display_name", "custom_carrier_name"].includes(key))
      .map(([key, field]: [string, any]) => (
        <FormField
          key={key}
          control={form.control}
          name={`credentials.${key}`}
          render={({ field: formField }) => (
            <FormItem>
              <FormLabel>
                {key === "display_name" ? "Display Name" : "Slug"}
                {(field.required || carrierName === "generic") && <span className="text-destructive">*</span>}
              </FormLabel>
              <FormControl>
                <Input
                  {...formField}
                  value={formField.value || ""}
                  autoComplete="off"
                  pattern={key === "custom_carrier_name" ? "^[a-z0-9_]+$" : undefined}
                  title={key === "custom_carrier_name" ? "Please enter a valid slug (lowercase letters, numbers, and underscores only)" : undefined}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      ));

    // Then render other fields
    const otherFields = Object.entries(fields)
      .filter(([key]) => ![
        "display_name",
        "custom_carrier_name",
        "metadata",
        "config",
        "label_template",
        "services"
      ].includes(key))
      .map(([key, field]: [string, any]) => (
        <FormField
          key={key}
          control={form.control}
          name={`credentials.${key}`}
          render={({ field: formField }) => (
            <FormItem>
              <FormLabel>
                {formatLabel(field.name)}
                {field.required && <span className="text-destructive">*</span>}
              </FormLabel>
              <FormControl>
                {key === "account_country_code" ? (
                  <CountrySelect
                    value={formField.value || ""}
                    onValueChange={formField.onChange}
                    placeholder="Select a country"
                  />
                ) : field.type === "string" && !field.enum ? (
                  <Input {...formField} value={formField.value || ""} autoComplete="off" />
                ) : field.type === "string" && field.enum ? (
                  <Select
                    onValueChange={formField.onChange}
                    value={formField.value || ""}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select..." />
                    </SelectTrigger>
                    <SelectContent>
                      {field.enum.map((option: string) => (
                        <SelectItem key={option} value={option}>
                          {formatLabel(option)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                ) : field.type === "boolean" ? (
                  <div className="flex items-center gap-2 pt-2">
                    <Switch
                      checked={formField.value || false}
                      onCheckedChange={formField.onChange}
                    />
                    <span className="text-sm">{formatLabel(field.name)}</span>
                  </div>
                ) : null}
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      ));

    return [...specialFields, ...otherFields];
  };

  const renderConfigFields = () => {
    const carrierName = watch("carrier_name");
    if (!carrierName) return null;
    const configs = references?.connection_configs?.[carrierName] || {};

    return (
      <div className="grid grid-cols-2 gap-4">
        {Object.entries(configs)
          .filter(
            ([key, _]) =>
              ![
                "brand_color",
                "text_color",
                "shipping_services",
                "shipping_options",
              ].includes(key),
          )
          .map(([key, config]: [string, any]) => (
            <FormField
              key={key}
              control={form.control}
              name={`config.${key}`}
              render={({ field: formField }) => (
                <FormItem className={config.type === "boolean" ? "col-span-2" : ""}>
                  <FormLabel>{formatLabel(config.name)}</FormLabel>
                  <FormControl>
                    {config.type === "string" && !config.enum ? (
                      <Input {...formField} value={formField.value || ''} />
                    ) : config.type === "string" && config.enum ? (
                      <Select
                        onValueChange={formField.onChange}
                        value={formField.value}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select..." />
                        </SelectTrigger>
                        <SelectContent>
                          {config.enum.map((option: string) => (
                            <SelectItem key={option} value={option}>
                              {formatLabel(option)}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    ) : config.type === "boolean" ? (
                      <div className="flex items-center gap-2 pt-2">
                        <Switch
                          checked={formField.value}
                          onCheckedChange={formField.onChange}
                        />
                        <span className="text-sm">{formatLabel(config.name)}</span>
                      </div>
                    ) : null}
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          ))}

        {configs["brand_color"] && (
          <FormField
            control={form.control}
            name="config.brand_color"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Brand Color</FormLabel>
                <FormControl>
                  <Input type="color" {...field} value={field.value || '#000000'} className="h-10 p-1" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        {configs["text_color"] && (
          <FormField
            control={form.control}
            name="config.text_color"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Text Color</FormLabel>
                <FormControl>
                  <Input type="color" {...field} value={field.value || '#000000'} className="h-10 p-1" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        {configs["shipping_services"] && (
          <FormField
            control={form.control}
            name="config.shipping_services"
            render={({ field }) => {
              const allServices = Object.keys(references?.service_names?.[carrierName] || {});
              const selectedServices = field.value || [];
              const isAllSelected = allServices.length > 0 && allServices.every(service => selectedServices.includes(service));
              const isPartiallySelected = selectedServices.length > 0 && selectedServices.length < allServices.length;

              return (
                <FormItem className="col-span-2">
                  <div className="flex items-center justify-between">
                    <FormLabel>Preferred Shipping Services</FormLabel>
                    {allServices.length > 0 && (
                      <div className="flex items-center gap-2">
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          className="h-6 px-2 text-xs"
                          onClick={() => {
                            if (isAllSelected) {
                              field.onChange([]);
                            } else {
                              field.onChange(allServices);
                            }
                          }}
                        >
                          {isAllSelected ? 'Uncheck All' : 'Check All'}
                        </Button>
                        {isPartiallySelected && (
                          <span className="text-xs text-muted-foreground">
                            {selectedServices.length} of {allServices.length} selected
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                  <FormControl>
                    <div className="rounded-md border max-h-[160px] overflow-y-auto">
                      <div className="p-3 space-y-1.5">
                        {Object.entries(
                          references?.service_names?.[carrierName] || {},
                        ).map(([value, label]) => (
                          <div key={value} className="flex items-center space-x-2">
                            <Switch
                              id={`service-${value}`}
                              checked={(field.value || []).includes(value)}
                              onCheckedChange={(checked) => {
                                const values = field.value || [];
                                if (checked) {
                                  field.onChange([...values, value]);
                                } else {
                                  field.onChange(values.filter((v: string) => v !== value));
                                }
                              }}
                            />
                            <label htmlFor={`service-${value}`} className="text-sm font-medium">
                              {formatLabel(label as string)}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              );
            }}
          />
        )}

        {configs["shipping_options"] && (
          <FormField
            control={form.control}
            name="config.shipping_options"
            render={({ field }) => {
              const allOptions = Object.keys(references?.option_names?.[carrierName] || {});
              const selectedOptions = field.value || [];
              const isAllSelected = allOptions.length > 0 && allOptions.every(option => selectedOptions.includes(option));
              const isPartiallySelected = selectedOptions.length > 0 && selectedOptions.length < allOptions.length;

              return (
                <FormItem className="col-span-2">
                  <div className="flex items-center justify-between">
                    <FormLabel>Enable Carrier Specific Shipping Options</FormLabel>
                    {allOptions.length > 0 && (
                      <div className="flex items-center gap-2">
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          className="h-6 px-2 text-xs"
                          onClick={() => {
                            if (isAllSelected) {
                              field.onChange([]);
                            } else {
                              field.onChange(allOptions);
                            }
                          }}
                        >
                          {isAllSelected ? 'Uncheck All' : 'Check All'}
                        </Button>
                        {isPartiallySelected && (
                          <span className="text-xs text-muted-foreground">
                            {selectedOptions.length} of {allOptions.length} selected
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                  <FormControl>
                    <div className="rounded-md border max-h-[160px] overflow-y-auto">
                      <div className="p-3 space-y-1.5">
                        {Object.entries(
                          references?.option_names?.[carrierName] || {},
                        ).map(([value, label]) => (
                          <div key={value} className="flex items-center space-x-2">
                            <Switch
                              id={`option-${value}`}
                              checked={(field.value || []).includes(value)}
                              onCheckedChange={(checked) => {
                                const values = field.value || [];
                                if (checked) {
                                  field.onChange([...values, value]);
                                } else {
                                  field.onChange(values.filter((v: string) => v !== value));
                                }
                              }}
                            />
                            <label htmlFor={`option-${value}`} className="text-sm font-medium">
                              {formatLabel(label as string)}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              );
            }}
          />
        )}
      </div>
    );
  };

  const renderCapabilityFields = () => {
    const carrierName = watch("carrier_name");
    if (!carrierName) return null;
    const capabilities = references?.carrier_capabilities?.[carrierName] || [];

    if (capabilities.length === 0) {
      return <p className="text-sm text-muted-foreground">No capabilities for this carrier.</p>;
    }

    return (
      <div className="space-y-2">
        {capabilities.map((capability: string) => (
          <FormField
            key={capability}
            control={form.control}
            name="capabilities"
            render={({ field }) => {
              const isChecked = (field.value || []).includes(capability);
              return (
                <FormItem className="flex flex-row items-center space-x-3 space-y-0 rounded-md border p-4">
                  <FormControl>
                    <Switch
                      checked={isChecked}
                      onCheckedChange={(checked) => {
                        const currentCapabilities = field.value || [];
                        if (checked) {
                          field.onChange([...currentCapabilities, capability]);
                        } else {
                          field.onChange(currentCapabilities.filter(c => c !== capability));
                        }
                      }}
                    />
                  </FormControl>
                  <FormLabel className="font-normal">
                    {formatLabel(capability)}
                  </FormLabel>
                </FormItem>
              );
            }}
          />
        ))}
      </div>
    );
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>
            {title || (selectedConnection ? "Edit Connection" : "Add Connection")}
          </DialogTitle>
          <DialogDescription>
            {description || (selectedConnection
              ? `Update ${selectedConnection.carrier_name} connection details.`
              : "Register a new carrier account.")}
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="flex flex-col flex-1 min-h-0">
            {/* Scrollable Body */}
            <div className="flex-1 overflow-y-auto px-4 py-3">
              <div className="space-y-6">
                <div className="space-y-4">
                  <FormField
                    control={form.control}
                    name="carrier_name"
                    key={`carrier-${selectedConnection?.id || 'new'}`}
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>
                          Carrier <span className="text-destructive">*</span>
                        </FormLabel>
                        <Select
                          onValueChange={field.onChange}
                          value={field.value || ""}
                          disabled={!!selectedConnection || disableCarrierSelection}
                        >
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select a carrier" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {references?.connection_fields && (
                              <>
                                {/* Generic carrier first */}
                                {Object.keys(references.connection_fields)
                                  .filter((carrier) => carrier === "generic")
                                  .map((carrier) => (
                                    <SelectItem key={carrier} value={carrier}>
                                      <div className="flex items-center gap-2">
                                        <CarrierImage
                                          carrier_name={carrier}
                                          width={20}
                                          height={20}
                                          className="grayscale"
                                        />
                                        <span>{references.carriers[carrier] as string}</span>
                                      </div>
                                    </SelectItem>
                                  ))}

                                {/* Separator */}
                                {references.carriers.generic && (
                                  <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground">
                                    Shipping Carriers
                                  </div>
                                )}

                                {/* Other carriers */}
                                {Object.keys(references.connection_fields)
                                  .filter((carrier) => carrier !== "generic")
                                  .sort()
                                  .map((carrier) => (
                                    <SelectItem key={carrier} value={carrier}>
                                      <div className="flex items-center gap-2">
                                        <CarrierImage
                                          carrier_name={carrier}
                                          width={20}
                                          height={20}
                                          className="grayscale"
                                        />
                                        <span>{references.carriers[carrier] as string}</span>
                                      </div>
                                    </SelectItem>
                                  ))}
                              </>
                            )}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  {watch("carrier_name") &&
                    <>
                      {/* Integration Status */}
                      {references?.integration_status && (
                        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
                          <span className="font-semibold">Integration status:</span>
                          <IntegrationStatusBadge
                            status={references.integration_status[watch("carrier_name")] || 'in-development'}
                            showPrefix={false}
                          />
                        </div>
                      )}

                      <FormField
                        control={form.control}
                        name="carrier_id"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>
                              Carrier ID <span className="text-destructive">*</span>
                            </FormLabel>
                            <FormControl>
                              <Input {...field} autoComplete="off" />
                            </FormControl>
                            <div className="text-xs text-muted-foreground mt-1">
                              Friendly tag. e.g: <strong>dhl-express-us, ups-ca-test...</strong>
                            </div>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name="active"
                        render={({ field }) => (
                          <FormItem className="flex items-center gap-2 pt-2">
                            <FormControl>
                              <Switch
                                checked={field.value}
                                onCheckedChange={field.onChange}
                              />
                            </FormControl>
                            <FormLabel className="!m-0">Active</FormLabel>
                          </FormItem>
                        )}
                      />
                    </>
                  }
                </div>

                {watch("carrier_name") && (
                  <Tabs defaultValue="credentials" className="w-full">
                    <TabsList className="grid w-full grid-cols-4">
                      <TabsTrigger value="credentials">Credentials</TabsTrigger>
                      <TabsTrigger
                        value="config"
                        disabled={Object.keys(references?.connection_configs?.[watch("carrier_name")] || {}).length === 0}
                      >
                        Config
                      </TabsTrigger>
                      <TabsTrigger value="capabilities">Capabilities</TabsTrigger>
                      <TabsTrigger value="metadata">Metadata</TabsTrigger>
                    </TabsList>
                    <TabsContent value="credentials" className="pt-6">
                      <div className="space-y-4">
                        {renderCredentialFields()}
                      </div>
                    </TabsContent>
                    <TabsContent value="config" className="pt-6">
                      <div className="space-y-4">
                        {renderConfigFields()}
                      </div>
                    </TabsContent>
                    <TabsContent value="capabilities" className="pt-6">
                      <div className="space-y-4">
                        {renderCapabilityFields()}
                      </div>
                    </TabsContent>
                    <TabsContent value="metadata" className="pt-6">
                      <EnhancedMetadataEditor
                        value={watch("metadata") || {}}
                        onChange={(metadata) => {
                          form.setValue("metadata", metadata, { shouldDirty: true });
                        }}
                      />
                    </TabsContent>
                  </Tabs>
                )}
              </div>
            </div>

            {/* Sticky Footer */}
            <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background">
              <Button type="button" variant="outline" onClick={handleModalClose}>
                Cancel
              </Button>
              <Button type="submit" disabled={!isValid}>
                Save
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
