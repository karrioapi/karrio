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
import { GetSystemConnections_system_carrier_connections_edges_node, CarrierNameEnum } from "@karrio/types/graphql/admin/types";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { ChevronDown, ChevronUp } from "lucide-react";
import { MetadataEditor } from "./ui/metadata-editor";
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
  carrier_name: z.nativeEnum(CarrierNameEnum),
  carrier_id: z.string(),
  active: z.boolean(),
  capabilities: z.array(z.string()),
  credentials: z.record(z.any()).refine(
    (credentials) => true, // Will be validated in areCredentialsValid
    { message: "Please fill in all required fields" }
  ),
  config: z.record(z.any()),
  metadata: z.record(z.any()),
});

type FormData = z.infer<typeof formSchema>;

interface CarrierConnectionDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  selectedConnection: Connection | null;
  onSubmit: (values: FormData) => void;
}

export function CarrierConnectionDialog({
  open,
  onOpenChange,
  selectedConnection,
  onSubmit,
}: CarrierConnectionDialogProps) {
  const { references } = useAPIMetadata();
  const [isConfigOpen, setIsConfigOpen] = useState(false);
  const [isMetadataOpen, setIsMetadataOpen] = useState(false);
  const [initialValues, setInitialValues] = useState<FormData | null>(null);

  const defaultValues: FormData = {
    carrier_name: "" as CarrierNameEnum,
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

  // Track form changes
  const carrierName = form.watch("carrier_name");
  const formState = form.formState;
  const formValues = form.watch();
  const isDirty = initialValues ? !isEqual(formValues, initialValues) : false;

  // Check if required credentials are filled
  const areCredentialsValid = () => {
    const carrierName = form.getValues("carrier_name");
    const credentials = form.getValues("credentials");
    const fields = references?.connection_fields?.[carrierName] || {};

    return Object.entries(fields).every(([key, field]) => {
      if (field.required) {
        const value = credentials?.[key];
        return value !== undefined && value !== "" && value !== null;
      }
      return true;
    });
  };

  const isValid = formState.isValid && areCredentialsValid();

  // Initialize form values
  useEffect(() => {
    if (!open) {
      form.reset(defaultValues);
      setInitialValues(null);
      setIsConfigOpen(false);
      setIsMetadataOpen(false);
      return;
    }

    if (selectedConnection) {
      const values: FormData = {
        carrier_name: selectedConnection.carrier_name as CarrierNameEnum,
        carrier_id: selectedConnection.carrier_id,
        active: selectedConnection.active,
        capabilities: selectedConnection.capabilities || [],
        credentials: selectedConnection.credentials || {},
        config: selectedConnection.config || {},
        metadata: selectedConnection.metadata || {},
      };
      form.reset(values);
      setInitialValues(values);
    } else {
      form.reset(defaultValues);
      setInitialValues(defaultValues);
    }
  }, [open, selectedConnection]);

  // Handle carrier change
  useEffect(() => {
    if (!carrierName || selectedConnection || !open) return;

    const fields = references?.connection_fields?.[carrierName] || {};
    const defaultCredentials = Object.entries(fields).reduce(
      (acc, [key, field]) => ({
        ...acc,
        [key]: field.default || "",
      }),
      {}
    );
    form.setValue("credentials", defaultCredentials);
  }, [carrierName, selectedConnection, open]);

  const handleModalClose = () => {
    // Reset form first
    form.reset(defaultValues);
    // Close modal in next frame
    requestAnimationFrame(() => {
      onOpenChange(false);
    });
  };

  const formatLabel = (label: string) => {
    return label
      .split(/[\s_-]/)
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(" ");
  };

  const renderCredentialFields = () => {
    const carrierName = form.watch("carrier_name");
    const fields = references?.connection_fields?.[carrierName] || {};
    const credentials = form.watch("credentials");

    return Object.entries(fields)
      .filter(([key]) => key !== "display_name")
      .map(([key, field]) => {
        const fieldValue = credentials?.[key] || "";
        return (
          <FormField
            key={key}
            control={form.control}
            name={`credentials.${key}`}
            defaultValue={fieldValue}
            render={({ field: formField }) => (
              <FormItem>
                <FormLabel>
                  {formatLabel(field.name)}
                  {field.required && <span className="text-destructive">*</span>}
                </FormLabel>
                <FormControl>
                  {field.type === "string" && !field.enum ? (
                    <Input {...formField} value={formField.value || ""} />
                  ) : field.type === "string" && field.enum ? (
                    <Select
                      onValueChange={formField.onChange}
                      value={formField.value || ""}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select..." />
                      </SelectTrigger>
                      <SelectContent>
                        {field.enum.map((option) => (
                          <SelectItem key={option} value={option}>
                            {formatLabel(option)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  ) : field.type === "boolean" ? (
                    <div className="flex items-center gap-2">
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
        );
      });
  };

  const renderConfigFields = () => {
    const carrierName = form.watch("carrier_name");
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
          .map(([key, config]) => (
            <FormField
              key={key}
              control={form.control}
              name={`config.${key}`}
              render={({ field: formField }) => (
                <FormItem className={config.type === "boolean" ? "col-span-2" : undefined}>
                  <FormLabel>{formatLabel(config.name)}</FormLabel>
                  <FormControl>
                    {config.type === "string" && !config.enum ? (
                      <Input {...formField} />
                    ) : config.type === "string" && config.enum ? (
                      <Select
                        onValueChange={formField.onChange}
                        value={formField.value}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select..." />
                        </SelectTrigger>
                        <SelectContent>
                          {config.enum.map((option) => (
                            <SelectItem key={option} value={option}>
                              {formatLabel(option)}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    ) : config.type === "boolean" ? (
                      <div className="flex items-center gap-2">
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
                  <Input type="color" {...field} className="h-10" />
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
                  <Input type="color" {...field} className="h-10" />
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
                  <div className="rounded-md border">
                    <div className="p-3 space-y-1.5 max-h-[160px] overflow-y-auto">
                      {Object.entries(
                        references?.service_names?.[carrierName] || {},
                      ).map(([value, label]) => (
                        <div
                          key={value}
                          className="flex items-center space-x-2 py-0.5 px-1 hover:bg-gray-50 rounded"
                        >
                          <input
                            type="checkbox"
                            id={`service-${value}`}
                            checked={(field.value || []).includes(value)}
                            onChange={(e) => {
                              const values = field.value || [];
                              if (e.target.checked) {
                                field.onChange([...values, value]);
                              } else {
                                field.onChange(
                                  values.filter((v: string) => v !== value),
                                );
                              }
                            }}
                            className="h-4 w-4 rounded border-gray-300"
                          />
                          <label
                            htmlFor={`service-${value}`}
                            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                          >
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

        {configs["shipping_options"] && (
          <FormField
            control={form.control}
            name="config.shipping_options"
            render={({ field }) => (
              <FormItem className="col-span-2">
                <FormLabel>Carrier Specific Shipping Options</FormLabel>
                <FormControl>
                  <div className="rounded-md border">
                    <div className="p-3 space-y-1.5 max-h-[160px] overflow-y-auto">
                      {Object.entries(
                        references?.option_names?.[carrierName] || {},
                      ).map(([value, label]) => (
                        <div
                          key={value}
                          className="flex items-center space-x-2 py-0.5 px-1 hover:bg-gray-50 rounded"
                        >
                          <input
                            type="checkbox"
                            id={`option-${value}`}
                            checked={(field.value || []).includes(value)}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                              const values = field.value || [];
                              if (e.target.checked) {
                                field.onChange([...values, value]);
                              } else {
                                field.onChange(
                                  values.filter((v: string) => v !== value),
                                );
                              }
                            }}
                            className="h-4 w-4 rounded border-gray-300"
                          />
                          <label
                            htmlFor={`option-${value}`}
                            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                          >
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

  const handleSubmit = (values: FormData) => {
    // Create base data
    const baseData = {
      carrier_name: values.carrier_name,
      carrier_id: values.carrier_id,
      active: values.active,
      capabilities: values.capabilities,
      credentials: values.credentials,
      config: values.config || {},
      metadata: values.metadata || {},
    };

    // Call onSubmit with the appropriate data
    onSubmit(baseData);
  };

  return (
    <Dialog
      open={open}
      onOpenChange={(value) => {
        if (!value) {
          handleModalClose();
        } else {
          onOpenChange(true);
        }
      }}
    >
      <DialogContent
        className="max-w-2xl max-h-[90vh] flex flex-col p-4 pb-8"
        onEscapeKeyDown={() => handleModalClose()}
        onInteractOutside={() => handleModalClose()}
      >
        <DialogHeader className="shrink-0 p-6 border-b">
          <DialogTitle>
            {selectedConnection ? "Edit Connection" : "Add Connection"}
          </DialogTitle>
          <DialogDescription>
            Update carrier connection details and credentials.
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className="flex flex-col flex-1 min-h-0"
          >
            <div className="flex-1 overflow-y-auto p-4 pb-8">
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
                        <FormControl>
                          <Select
                            onValueChange={(value) => {
                              field.onChange(value as CarrierNameEnum);
                              form.setValue("carrier_id", value.toLowerCase());
                            }}
                            value={field.value}
                            disabled={!!selectedConnection}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Select a carrier" />
                            </SelectTrigger>
                            <SelectContent>
                              {references?.carriers &&
                                Object.entries(references.carriers)
                                  .sort()
                                  .map(([carrier, label]) => (
                                    <SelectItem key={carrier} value={carrier}>
                                      {label}
                                    </SelectItem>
                                  ))}
                            </SelectContent>
                          </Select>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="carrier_id"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>
                          Carrier ID <span className="text-destructive">*</span>
                        </FormLabel>
                        <FormControl>
                          <Input {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="flex gap-4">
                    <FormField
                      control={form.control}
                      name="active"
                      render={({ field }) => (
                        <FormItem className="flex items-center gap-2">
                          <FormControl>
                            <Switch
                              checked={field.value}
                              onCheckedChange={field.onChange}
                            />
                          </FormControl>
                          <FormLabel className="!m-0">Active</FormLabel>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                </div>

                {form.watch("carrier_name") && (
                  <>
                    <div className="space-y-4">{renderCredentialFields()}</div>

                    {Object.keys(
                      references?.connection_configs?.[
                      form.watch("carrier_name")
                      ] || {},
                    ).length > 0 && (
                        <div className="space-y-4">
                          <button
                            type="button"
                            className="flex w-full items-center justify-between rounded-lg border p-4 text-left text-sm font-medium hover:bg-gray-100"
                            onClick={() => setIsConfigOpen(!isConfigOpen)}
                          >
                            <span>Connection Config</span>
                            {isConfigOpen ? (
                              <ChevronUp className="h-4 w-4" />
                            ) : (
                              <ChevronDown className="h-4 w-4" />
                            )}
                          </button>
                          {isConfigOpen && (
                            <div className="space-y-4 rounded-lg border p-4">
                              {renderConfigFields()}
                            </div>
                          )}
                        </div>
                      )}

                    <div className="space-y-4">
                      <button
                        type="button"
                        className="flex w-full items-center justify-between rounded-lg border p-4 text-left text-sm font-medium hover:bg-gray-100"
                        onClick={() => setIsMetadataOpen(!isMetadataOpen)}
                      >
                        <span>Metadata</span>
                        {isMetadataOpen ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </button>
                      {isMetadataOpen && (
                        <div className="space-y-4 rounded-lg border p-4">
                          <MetadataEditor
                            value={form.watch("config.metadata") || {}}
                            onChange={(metadata) => {
                              form.setValue("config.metadata", metadata);
                            }}
                          />
                        </div>
                      )}
                    </div>
                  </>
                )}
              </div>
            </div>

            <DialogFooter className="shrink-0 p-6 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={handleModalClose}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={!isDirty || !isValid}
              >
                Save
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
