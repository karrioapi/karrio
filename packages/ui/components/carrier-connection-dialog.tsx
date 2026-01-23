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
import { useOAuthConnection, supportsOAuth, useCarrierWebhook, supportsWebhook } from "@karrio/hooks/carrier-connections";
import { zodResolver } from "@hookform/resolvers/zod";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useState, useEffect } from "react";
import { References } from "@karrio/types";
import { useForm } from "react-hook-form";
import { isEqual, KARRIO_API } from "@karrio/lib";
import { Button } from "./ui/button";
import { Switch } from "./ui/switch";
import { Input } from "./ui/input";
import { Zap, Loader2, Webhook, Check, X, Copy, Plus, Trash2 } from "lucide-react";
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
  const [oauthCredentials, setOauthCredentials] = useState<Record<string, any> | null>(null);
  const { toast } = useToast();

  // OAuth connection hook
  const {
    initiateOAuth,
    cancelOAuth,
    isLoading: isOAuthLoading,
  } = useOAuthConnection({
    onSuccess: (result) => {
      if (result.credentials) {
        // Store OAuth credentials to prefill form
        setOauthCredentials(result.credentials);
        toast({
          title: "Authorization Successful",
          description: "Your account has been authorized. Please complete the connection details.",
        });
      }
    },
    onError: (error) => {
      toast({
        title: "Authorization Failed",
        description: error instanceof Error ? error.message : "OAuth authorization failed",
        variant: "destructive",
      });
    },
  });

  // Carrier webhook hook
  const {
    registerWebhook,
    deregisterWebhook,
    disconnectWebhook,
    isLoading: isWebhookLoading,
  } = useCarrierWebhook();

  const defaultValues: FormData = {
    carrier_name: "",
    carrier_id: "",
    active: false,
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
          // Generic carriers have carrier_name === "generic"
          carrier_name: selectedConnection.carrier_name || "",
          carrier_id: selectedConnection.carrier_id || "",
          active: selectedConnection.active || false,
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
      }
    });
    return () => subscription.unsubscribe();
  }, [watch, setValue, selectedConnection, references]);

  // Apply OAuth credentials when received
  useEffect(() => {
    if (oauthCredentials) {
      const currentCredentials = form.getValues("credentials") || {};
      // Merge OAuth credentials with existing credentials
      form.setValue("credentials", {
        ...currentCredentials,
        ...oauthCredentials,
      }, { shouldDirty: true });
    }
  }, [oauthCredentials, form]);

  // Reset OAuth state when dialog closes
  useEffect(() => {
    if (!open) {
      setOauthCredentials(null);
      cancelOAuth();
    }
  }, [open, cancelOAuth]);

  const handleModalClose = () => {
    onOpenChange(false);
  };

  // Handle OAuth connect button click
  const handleOAuthConnect = async () => {
    const carrierName = watch("carrier_name");
    if (!carrierName) return;

    try {
      await initiateOAuth(carrierName);
    } catch (error) {
      // Error is already handled by the hook's onError callback
    }
  };

  // Check if current carrier supports OAuth
  const currentCarrierSupportsOAuth = supportsOAuth(
    watch("carrier_name"),
    references?.carrier_capabilities
  );

  // Check if current carrier supports webhook registration
  const currentCarrierSupportsWebhook = supportsWebhook(
    watch("carrier_name"),
    references?.carrier_capabilities
  );

  // Check if webhook is currently registered (from connection config)
  const webhookId = watch("config.webhook_id");
  const webhookUrl = watch("config.webhook_url");
  const webhookSecret = watch("config.webhook_secret");

  // Webhook is considered enabled if webhook_id OR webhook_secret is set
  // (users may manually configure webhook_secret without auto-registration)
  const isWebhookEnabled = !!(webhookId || webhookSecret);

  // Webhook operation handler - reduces repetition across register/deregister/disconnect
  const handleWebhookOperation = async (
    operation: () => Promise<any>,
    successTitle: string,
    successDescription: string,
    errorTitle: string,
    clearConfig: boolean = false,
  ) => {
    if (!selectedConnection?.id) return;

    try {
      const result = await operation();
      if (!result.success) return;

      if (clearConfig) {
        ["webhook_id", "webhook_secret", "webhook_url"].forEach((key) =>
          form.setValue(`config.${key}` as any, "", { shouldDirty: false })
        );
      }

      toast({ title: successTitle, description: successDescription });
    } catch (error: any) {
      toast({
        title: errorTitle,
        description: error?.message || `${errorTitle.toLowerCase()}.`,
        variant: "destructive",
      });
    }
  };

  const handleRegisterWebhook = () =>
    handleWebhookOperation(
      () => registerWebhook(selectedConnection!.id),
      "Webhook Registered",
      "Webhook has been successfully registered with the carrier. Close and reopen to see updated configuration.",
      "Registration Failed",
    );

  const handleDeregisterWebhook = () =>
    handleWebhookOperation(
      () => deregisterWebhook(selectedConnection!.id),
      "Webhook Deregistered",
      "Webhook has been successfully removed from the carrier.",
      "Deregistration Failed",
      true,
    );

  const handleDisconnectWebhook = () =>
    handleWebhookOperation(
      () => disconnectWebhook(selectedConnection!.id),
      "Webhook Disconnected",
      "Webhook configuration has been cleared locally.",
      "Disconnect Failed",
      true,
    );

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

    // Identify object array configs (type "list" with nested "fields")
    const objectArrayConfigs = Object.entries(configs).filter(
      ([_, config]: [string, any]) => config.type === "list" && config.fields
    );

    return (
      <div className="grid grid-cols-2 gap-4">
        {Object.entries(configs)
          .filter(
            ([key, config]: [string, any]) =>
              ![
                "brand_color",
                "text_color",
                "shipping_services",
                "shipping_options",
              ].includes(key) &&
              // Exclude object array configs - they are rendered separately
              !(config.type === "list" && config.fields),
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

        {/* Object Array Config Fields (e.g., service_billing_numbers) */}
        {objectArrayConfigs.map(([key, config]: [string, any]) => (
          <FormField
            key={key}
            control={form.control}
            name={`config.${key}`}
            render={({ field }) => {
              const items: any[] = field.value || [];
              const fieldDefs = config.fields || {};
              // Sort fields: required first, then enums, then plain fields
              const fieldKeys = Object.keys(fieldDefs).sort((a, b) => {
                const aRequired = fieldDefs[a]?.required ? 0 : 2;
                const bRequired = fieldDefs[b]?.required ? 0 : 2;
                const aEnum = fieldDefs[a]?.enum ? 0 : 1;
                const bEnum = fieldDefs[b]?.enum ? 0 : 1;
                // Primary sort by required, secondary by enum
                return (aRequired + aEnum) - (bRequired + bEnum);
              });

              // Default values for service_billing_numbers (DHL Parcel DE sandbox)
              const defaultServiceBillingNumbers: Record<string, any>[] = [
                { service: "dhl_parcel_de_paket", billing_number: "33333333330102", name: "" },
                { service: "dhl_parcel_de_paket_international", billing_number: "33333333335301", name: "" },
                { service: "dhl_parcel_de_europaket", billing_number: "33333333335401", name: "" },
                { service: "dhl_parcel_de_kleinpaket", billing_number: "33333333336201", name: "" },
                { service: "dhl_parcel_de_warenpost_international", billing_number: "33333333336601", name: "" },
              ];

              // Auto-prefill defaults for service_billing_numbers when empty
              if (key === "service_billing_numbers" && items.length === 0 && field.value === undefined) {
                // Use setTimeout to avoid updating state during render
                setTimeout(() => field.onChange(defaultServiceBillingNumbers), 0);
              }

              const addItem = () => {
                const newItem: Record<string, any> = {};
                Object.entries(fieldDefs).forEach(([fieldKey, fieldDef]: [string, any]) => {
                  newItem[fieldKey] = fieldDef.default || "";
                });
                field.onChange([...items, newItem]);
              };

              const removeItem = (index: number) => {
                const newItems = items.filter((_, i) => i !== index);
                field.onChange(newItems);
              };

              const updateItem = (index: number, fieldKey: string, value: any) => {
                const newItems = [...items];
                newItems[index] = { ...newItems[index], [fieldKey]: value };
                field.onChange(newItems);
              };

              return (
                <FormItem className="col-span-2">
                  <div className="flex items-center justify-between mb-2">
                    <FormLabel>{formatLabel(config.name)}</FormLabel>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={addItem}
                      className="h-7 px-2"
                    >
                      <Plus className="h-4 w-4 mr-1" />
                      Add
                    </Button>
                  </div>
                  <FormControl>
                    <div className="rounded-md border overflow-hidden">
                      {/* Table Header */}
                      <div className="bg-muted/50 border-b">
                        <div className="grid gap-2 p-2 text-xs font-medium text-muted-foreground" style={{
                          gridTemplateColumns: `repeat(${fieldKeys.length}, minmax(0, 1fr)) 40px`
                        }}>
                          {fieldKeys.map((fieldKey) => {
                            const fieldDef = fieldDefs[fieldKey];
                            return (
                              <div key={fieldKey} className="px-1">
                                {formatLabel(fieldDef.name || fieldKey)}
                                {fieldDef.required && <span className="text-destructive ml-0.5">*</span>}
                              </div>
                            );
                          })}
                          <div className="px-1"></div>
                        </div>
                      </div>

                      {/* Table Body */}
                      {items.length === 0 ? (
                        <div className="p-4 text-center text-sm text-muted-foreground">
                          No items configured. Click "Add" to create one.
                        </div>
                      ) : (
                        <div className="divide-y max-h-[240px] overflow-y-auto">
                          {items.map((item, index) => (
                            <div
                              key={index}
                              className="grid gap-2 p-2 items-center hover:bg-muted/30"
                              style={{
                                gridTemplateColumns: `repeat(${fieldKeys.length}, minmax(0, 1fr)) 40px`
                              }}
                            >
                              {fieldKeys.map((fieldKey) => {
                                const fieldDef = fieldDefs[fieldKey];
                                const hasEnum = fieldDef.enum;
                                const isServiceField = fieldKey === "service" || fieldKey.includes("service");
                                const serviceNames = references?.service_names?.[carrierName] || {};

                                return (
                                  <div key={fieldKey} className="w-full min-w-0">
                                    {/* Enum field */}
                                    {hasEnum ? (
                                      <Select
                                        value={item[fieldKey] || ""}
                                        onValueChange={(value) => updateItem(index, fieldKey, value)}
                                      >
                                        <SelectTrigger className="h-8 text-sm w-full">
                                          <SelectValue placeholder="Select..." className="truncate" />
                                        </SelectTrigger>
                                        <SelectContent>
                                          {fieldDef.enum.map((option: string) => (
                                            <SelectItem key={option} value={option}>
                                              {formatLabel(option)}
                                            </SelectItem>
                                          ))}
                                        </SelectContent>
                                      </Select>
                                    ) : isServiceField && Object.keys(serviceNames).length > 0 ? (
                                      /* Service field - use carrier service_names */
                                      <Select
                                        value={item[fieldKey] || ""}
                                        onValueChange={(value) => updateItem(index, fieldKey, value)}
                                      >
                                        <SelectTrigger className="h-8 text-sm w-full">
                                          <SelectValue placeholder="Select service..." className="truncate" />
                                        </SelectTrigger>
                                        <SelectContent>
                                          {Object.entries(serviceNames).map(([serviceKey, serviceLabel]) => (
                                            <SelectItem key={serviceKey} value={serviceKey}>
                                              {formatLabel(serviceLabel as string)}
                                            </SelectItem>
                                          ))}
                                        </SelectContent>
                                      </Select>
                                    ) : (
                                      /* Text input */
                                      <Input
                                        value={item[fieldKey] || ""}
                                        onChange={(e) => updateItem(index, fieldKey, e.target.value)}
                                        placeholder={fieldDef.name || fieldKey}
                                        className="h-8 text-sm w-full"
                                      />
                                    )}
                                  </div>
                                );
                              })}
                              <div className="flex justify-center">
                                <Button
                                  type="button"
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => removeItem(index)}
                                  className="h-8 w-8 p-0 text-muted-foreground hover:text-destructive"
                                >
                                  <Trash2 className="h-4 w-4" />
                                </Button>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              );
            }}
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
                    <TabsList className={`grid w-full ${currentCarrierSupportsWebhook ? 'grid-cols-4' : 'grid-cols-3'}`}>
                      <TabsTrigger value="credentials">Credentials</TabsTrigger>
                      <TabsTrigger
                        value="config"
                        disabled={Object.keys(references?.connection_configs?.[watch("carrier_name")] || {}).length === 0}
                      >
                        Config
                      </TabsTrigger>
                      {currentCarrierSupportsWebhook && (
                        <TabsTrigger value="webhook">Webhook</TabsTrigger>
                      )}
                      <TabsTrigger value="metadata">Metadata</TabsTrigger>
                    </TabsList>
                    <TabsContent value="credentials" className="pt-6">
                      <div className="space-y-4">
                        {/* OAuth Quick Connect Banner - only show for new connections with OAuth support */}
                        {!selectedConnection && currentCarrierSupportsOAuth && (
                          <>
                            <div className="rounded-lg border border-purple-200 bg-gradient-to-r from-purple-50 to-indigo-50 p-4">
                              <div className="flex items-start gap-3">
                                <div className="flex-shrink-0">
                                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100">
                                    <Zap className="h-5 w-5 text-purple-600" />
                                  </div>
                                </div>
                                <div className="flex-1 min-w-0">
                                  <h4 className="text-sm font-semibold text-purple-900">
                                    Quick Connect
                                  </h4>
                                  <p className="mt-1 text-sm text-purple-700">
                                    Connect your {references?.carriers?.[watch("carrier_name")] || watch("carrier_name")} account instantly with secure OAuth authorization.
                                  </p>
                                  <Button
                                    type="button"
                                    onClick={handleOAuthConnect}
                                    disabled={isOAuthLoading}
                                    className="mt-3 bg-purple-600 hover:bg-purple-700 text-white"
                                    size="sm"
                                  >
                                    {isOAuthLoading ? (
                                      <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Connecting...
                                      </>
                                    ) : (
                                      <>
                                        <Zap className="mr-2 h-4 w-4" />
                                        Connect with {references?.carriers?.[watch("carrier_name")] || watch("carrier_name")}
                                      </>
                                    )}
                                  </Button>
                                </div>
                              </div>
                              {oauthCredentials && (
                                <div className="mt-3 rounded-md bg-green-50 border border-green-200 p-2">
                                  <p className="text-xs text-green-700 flex items-center gap-1">
                                    <span className="inline-block h-2 w-2 rounded-full bg-green-500"></span>
                                    Authorization successful! Credentials have been prefilled below.
                                  </p>
                                </div>
                              )}
                            </div>
                            <div className="relative">
                              <div className="absolute inset-0 flex items-center">
                                <span className="w-full border-t" />
                              </div>
                              <div className="relative flex justify-center text-xs uppercase">
                                <span className="bg-background px-2 text-muted-foreground">
                                  Or enter credentials manually
                                </span>
                              </div>
                            </div>
                          </>
                        )}
                        {renderCredentialFields()}
                      </div>
                    </TabsContent>
                    <TabsContent value="config" className="pt-6">
                      <div className="space-y-4">
                        {renderConfigFields()}
                      </div>
                    </TabsContent>
                    {currentCarrierSupportsWebhook && (
                      <TabsContent value="webhook" className="pt-6">
                        <div className="space-y-6">
                          {/* Inbound Webhook URL Section */}
                          <div className="rounded-lg border bg-muted/50 p-4">
                            <h4 className="text-sm font-medium mb-2">Inbound Webhook URL</h4>
                            <p className="text-xs text-muted-foreground mb-3">
                              Use this URL to receive tracking updates and shipment events from {references?.carriers?.[watch("carrier_name")] || watch("carrier_name")}.
                            </p>
                            {selectedConnection?.id ? (
                              <div className="flex items-center gap-2">
                                <code className="flex-1 text-xs bg-background border rounded px-3 py-2 overflow-x-auto whitespace-nowrap">
                                  {KARRIO_API}/v1/connections/webhook/{selectedConnection.id}/events
                                </code>
                                <Button
                                  type="button"
                                  variant="outline"
                                  size="sm"
                                  onClick={() => {
                                    navigator.clipboard.writeText(
                                      `${KARRIO_API}/v1/connections/webhook/${selectedConnection.id}/events`
                                    );
                                    toast({
                                      title: "Copied!",
                                      description: "Webhook URL copied to clipboard.",
                                    });
                                  }}
                                >
                                  <Copy className="h-4 w-4" />
                                </Button>
                              </div>
                            ) : (
                              <p className="text-xs text-muted-foreground italic">
                                Save the connection first to generate the webhook URL.
                              </p>
                            )}
                          </div>

                          {/* Auto Registration Section - only for existing connections */}
                          {selectedConnection ? (
                            <>
                              <div className="border-t pt-4">
                                <h4 className="text-sm font-medium mb-3">Auto Registration</h4>
                                <p className="text-xs text-muted-foreground mb-4">
                                  Automatically register a webhook with the carrier to receive events at your Karrio endpoint.
                                </p>

                                {isWebhookEnabled ? (
                                  // Webhook is enabled (either auto-registered or manually configured)
                                  <div className="rounded-lg border border-green-200 bg-green-50 p-4">
                                    <div className="flex items-start gap-3">
                                      <div className="flex-shrink-0">
                                        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100">
                                          <Check className="h-4 w-4 text-green-600" />
                                        </div>
                                      </div>
                                      <div className="flex-1 min-w-0">
                                        <h5 className="text-sm font-medium text-green-900">
                                          Webhook {webhookId ? "Active" : "Configured"}
                                        </h5>
                                        <p className="mt-1 text-xs text-green-700 break-all">
                                          {webhookUrl || (webhookId ? "Webhook registered with carrier" : "Webhook manually configured")}
                                        </p>
                                        {webhookSecret && (
                                          <p className="mt-1 text-xs text-green-600">
                                            Secret configured for signature verification
                                          </p>
                                        )}
                                        <div className="flex gap-2 mt-3">
                                          {/* Only show Deregister if we have a webhook_id (auto-registered) */}
                                          {webhookId && (
                                            <Button
                                              type="button"
                                              variant="outline"
                                              size="sm"
                                              onClick={handleDeregisterWebhook}
                                              disabled={isWebhookLoading}
                                              className="border-red-200 text-red-600 hover:bg-red-50"
                                            >
                                              {isWebhookLoading ? (
                                                <>
                                                  <Loader2 className="mr-2 h-3 w-3 animate-spin" />
                                                  Processing...
                                                </>
                                              ) : (
                                                <>
                                                  <X className="mr-2 h-3 w-3" />
                                                  Deregister
                                                </>
                                              )}
                                            </Button>
                                          )}
                                          <Button
                                            type="button"
                                            variant="ghost"
                                            size="sm"
                                            onClick={handleDisconnectWebhook}
                                            disabled={isWebhookLoading}
                                            className="text-muted-foreground hover:text-foreground"
                                            title="Clear local webhook config without notifying the carrier"
                                          >
                                            {isWebhookLoading ? (
                                              <>
                                                <Loader2 className="mr-2 h-3 w-3 animate-spin" />
                                                Processing...
                                              </>
                                            ) : (
                                              <>
                                                Disconnect
                                              </>
                                            )}
                                          </Button>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                ) : (
                                  // Webhook is not registered
                                  <div className="rounded-lg border border-blue-200 bg-blue-50 p-4">
                                    <div className="flex items-start gap-3">
                                      <div className="flex-shrink-0">
                                        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
                                          <Webhook className="h-4 w-4 text-blue-600" />
                                        </div>
                                      </div>
                                      <div className="flex-1 min-w-0">
                                        <h5 className="text-sm font-medium text-blue-900">
                                          Enable Carrier Webhooks
                                        </h5>
                                        <p className="mt-1 text-xs text-blue-700">
                                          Register a webhook to receive real-time tracking updates and shipment events from the carrier.
                                        </p>
                                        <Button
                                          type="button"
                                          size="sm"
                                          onClick={handleRegisterWebhook}
                                          disabled={isWebhookLoading}
                                          className="mt-3 bg-blue-600 hover:bg-blue-700 text-white"
                                        >
                                          {isWebhookLoading ? (
                                            <>
                                              <Loader2 className="mr-2 h-3 w-3 animate-spin" />
                                              Registering...
                                            </>
                                          ) : (
                                            <>
                                              <Webhook className="mr-2 h-3 w-3" />
                                              Register Webhook
                                            </>
                                          )}
                                        </Button>
                                      </div>
                                    </div>
                                  </div>
                                )}
                              </div>
                            </>
                          ) : (
                            <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
                              <p className="text-xs text-amber-700">
                                Save the connection first to enable automatic webhook registration.
                              </p>
                            </div>
                          )}

                          {/* Manual webhook secret input */}
                          <div className="border-t pt-4">
                            <FormField
                              control={form.control}
                              name="config.webhook_secret"
                              render={({ field }) => (
                                <FormItem>
                                  <FormLabel>Webhook Secret</FormLabel>
                                  <FormControl>
                                    <Input
                                      {...field}
                                      value={field.value || ""}
                                      type="password"
                                      placeholder="Enter webhook secret for signature verification"
                                    />
                                  </FormControl>
                                  <p className="text-xs text-muted-foreground">
                                    Used to verify webhook signatures. Auto-populated when using the register button, or enter manually if you registered the webhook externally.
                                  </p>
                                </FormItem>
                              )}
                            />
                          </div>
                        </div>
                      </TabsContent>
                    )}
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
