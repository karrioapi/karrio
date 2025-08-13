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
import { GetSystemConnections_system_carrier_connections_edges_node } from "@karrio/types/graphql/admin/types";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import { MetadataEditor } from "./ui/metadata-editor";
import { References } from "@karrio/types";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState, useEffect } from "react";
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
  onSubmit: (values: FormData) => void;
  references?: References;
  title?: string;
  description?: string;
  disableCarrierSelection?: boolean;
}

export function CarrierConnectionDialog({
  open,
  onOpenChange,
  selectedConnection,
  onSubmit,
  references,
  title,
  description,
  disableCarrierSelection = false,
}: CarrierConnectionDialogProps) {
  const [initialValues, setInitialValues] = useState<FormData | null>(null);

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

  const { watch, setValue } = form;

  const formValues = watch();
  const isDirty = initialValues ? !isEqual(formValues, initialValues) : false;

  const areCredentialsValid = () => {
    const carrierName = watch("carrier_name");
    if (!carrierName) return false;

    const credentials = watch("credentials");
    const fields = references?.connection_fields?.[carrierName] || {};

    return Object.entries(fields).every(([key, field]: [string, any]) => {
      if (field.required) {
        const value = credentials?.[key];
        return value !== undefined && value !== "" && value !== null;
      }
      return true;
    });
  };

  const isValid = form.formState.isValid && areCredentialsValid();

  useEffect(() => {
    if (open) {
      const initial = selectedConnection
        ? {
          carrier_name: selectedConnection.carrier_name,
          carrier_id: selectedConnection.carrier_id,
          active: selectedConnection.active,
          capabilities: selectedConnection.capabilities || [],
          credentials: selectedConnection.credentials || {},
          config: selectedConnection.config || {},
          metadata: selectedConnection.metadata || {},
        }
        : defaultValues;
      form.reset(initial);
      setInitialValues(initial);
    }
  }, [open, selectedConnection]);


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

    return Object.entries(fields)
      .filter(([key]) => key !== "display_name")
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
                {field.type === "string" && !field.enum ? (
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
            render={({ field }) => (
              <FormItem className="col-span-2">
                <FormLabel>Preferred Shipping Services</FormLabel>
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
            )}
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
          <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col flex-1 min-h-0">
            {/* Scrollable Body */}
            <div className="flex-1 overflow-y-auto px-4 py-3">
              <div className="space-y-6">
                <div className="space-y-4">
                  <FormField
                    control={form.control}
                    name="carrier_name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>
                          Carrier <span className="text-destructive">*</span>
                        </FormLabel>
                        <Select
                          onValueChange={(value) => field.onChange(value)}
                          value={field.value}
                          disabled={!!selectedConnection || disableCarrierSelection}
                        >
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select a carrier" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {references?.carriers &&
                              Object.entries(references.carriers)
                                .sort()
                                .map(([carrier, label]) => (
                                  <SelectItem key={carrier} value={carrier}>
                                    <div className="flex items-center gap-2">
                                      <CarrierImage
                                        carrier_name={carrier}
                                        width={20}
                                        height={20}
                                        className="grayscale"
                                      />
                                      <span>{label as string}</span>
                                    </div>
                                  </SelectItem>
                                ))}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  {watch("carrier_name") &&
                    <>
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
                      <MetadataEditor
                        value={watch("metadata") || {}}
                        onChange={(metadata) => {
                          form.setValue("metadata", metadata);
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
              <Button type="submit" disabled={!isDirty || !isValid}>
                Save
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
