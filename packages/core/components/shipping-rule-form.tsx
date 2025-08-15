"use client";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { ShippingRuleTemplate } from "@karrio/hooks/shipping-rule-templates";
import { SheetHeader, SheetTitle } from "@karrio/ui/components/ui/sheet";
import { useShippingRuleForm } from "@karrio/hooks/shipping-rules";
import { useLoader } from "@karrio/ui/core/components/loader";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { Button } from "@karrio/ui/components/ui/button";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Trash2, Plus, X } from "lucide-react";
import React from "react";

interface ShippingRuleFormProps {
  ruleId?: string;
  templateData?: ShippingRuleTemplate | null;
  onClose: () => void;
  onSave: () => void;
}

export function ShippingRuleForm({ ruleId, templateData, onClose, onSave }: ShippingRuleFormProps) {
  const loader = useLoader();
  const { references } = useAPIMetadata();
  const { query: carrierQuery, user_carrier_connections: userConnections } = useCarrierConnections();
  const {
    form,
    isNew,
    save,
    deleteShippingRule,
    current,
    query,
  } = useShippingRuleForm({ id: ruleId });

  // State for dynamic conditions and actions
  const [activeConditions, setActiveConditions] = React.useState<string[]>([]);
  const [activeActions, setActiveActions] = React.useState<string[]>([]);
  const [conditionSelectValue, setConditionSelectValue] = React.useState<string>("");
  const [actionSelectValue, setActionSelectValue] = React.useState<string>("");

  // Initialize form with template data for new rules
  React.useEffect(() => {
    if (isNew && templateData && !current) {
      form.setFieldValue("name", templateData.name);
      form.setFieldValue("description", templateData.description);
      form.setFieldValue("priority", templateData.priority);
      form.setFieldValue("conditions", templateData.conditions || {});
      form.setFieldValue("actions", templateData.actions || {});
    }
  }, [isNew, templateData, current, form]);

  // Initialize active conditions and actions based on form state
  React.useEffect(() => {
    const formValues = form.state.values as any;
    const conditions: string[] = [];
    const actions: string[] = [];

    const hasValue = (v: any) => v !== undefined && v !== null && !(typeof v === 'object' && Object.keys(v || {}).length === 0);

    if (hasValue(formValues?.conditions?.destination)) conditions.push('destination');
    if (hasValue(formValues?.conditions?.weight)) conditions.push('weight');
    if (hasValue(formValues?.conditions?.carrier_id) || hasValue(formValues?.conditions?.service)) conditions.push('carrier_service');
    if (hasValue(formValues?.conditions?.rate_comparison)) conditions.push('rate_comparison');

    if (hasValue(formValues?.actions?.select_service)) actions.push('service_selection');
    // Only show blocking action when explicitly true
    if (formValues?.actions?.block_service === true) actions.push('service_blocking');

    setActiveConditions(conditions);
    setActiveActions(actions);
  }, [form.state.values]);

  const conditionTypes = [
    { id: 'destination', label: 'Destination', description: 'Filter by destination country' },
    { id: 'weight', label: 'Weight Range', description: 'Filter by package weight' },
    { id: 'carrier_service', label: 'Carrier & Service', description: 'Filter by specific carrier or service' },
    { id: 'rate_comparison', label: 'Rate Comparison', description: 'Compare rates or transit times' },
  ];

  const actionTypes = [
    { id: 'service_selection', label: 'Service Selection', description: 'Automatically select best service' },
    { id: 'service_blocking', label: 'Service Blocking', description: 'Block automatic service selection' },
  ];

  const addCondition = (conditionType: string) => {
    if (!activeConditions.includes(conditionType)) {
      setActiveConditions([...activeConditions, conditionType]);

      // Initialize condition data based on type
      const currentConditions = form.getFieldValue("conditions") || {};
      switch (conditionType) {
        case 'destination':
          form.setFieldValue("conditions", {
            ...currentConditions,
            destination: { country_code: "" }
          });
          break;
        case 'weight':
          form.setFieldValue("conditions", {
            ...currentConditions,
            weight: { min: null, max: null, unit: "lb" }
          });
          break;
        case 'carrier_service':
          form.setFieldValue("conditions", {
            ...currentConditions,
            carrier_id: "",
            service: ""
          });
          break;
        case 'rate_comparison':
          form.setFieldValue("conditions", {
            ...currentConditions,
            rate_comparison: { compare: "total_charge", operator: "eq", value: null }
          });
          break;
      }
    }
    // Reset the select dropdown
    setConditionSelectValue("");
  };

  const removeCondition = (conditionType: string) => {
    setActiveConditions(activeConditions.filter(c => c !== conditionType));

    // Clear the condition data
    const currentConditions = form.getFieldValue("conditions") || {};
    switch (conditionType) {
      case 'destination':
        const { destination, ...restConditions1 } = currentConditions;
        form.setFieldValue("conditions", restConditions1);
        break;
      case 'weight':
        const { weight, ...restConditions2 } = currentConditions;
        form.setFieldValue("conditions", restConditions2);
        break;
      case 'carrier_service':
        const { carrier_id, service, ...restConditions3 } = currentConditions;
        form.setFieldValue("conditions", restConditions3);
        break;
      case 'rate_comparison':
        const { rate_comparison, ...restConditions4 } = currentConditions;
        form.setFieldValue("conditions", restConditions4);
        break;
    }
  };

  const addAction = (actionType: string) => {
    if (!activeActions.includes(actionType)) {
      setActiveActions([...activeActions, actionType]);

      // Initialize action data based on type
      const currentActions = form.getFieldValue("actions") || {};
      switch (actionType) {
        case 'service_selection':
          form.setFieldValue("actions", {
            ...currentActions,
            select_service: { strategy: "cheapest" }
          });
          break;
        case 'service_blocking':
          form.setFieldValue("actions", {
            ...currentActions,
            block_service: true
          });
          break;
      }
    }
    // Reset the select dropdown
    setActionSelectValue("");
  };

  const removeAction = (actionType: string) => {
    setActiveActions(activeActions.filter(a => a !== actionType));

    // Clear the action data
    const currentActions = form.getFieldValue("actions") || {};
    switch (actionType) {
      case 'service_selection':
        const { select_service, ...restActions1 } = currentActions;
        form.setFieldValue("actions", restActions1);
        break;
      case 'service_blocking':
        const { block_service, ...restActions2 } = currentActions;
        form.setFieldValue("actions", restActions2);
        break;
    }
  };

  const handleSave = async () => {
    await save();
    onSave();
    onClose();
  };

  const handleDelete = async () => {
    if (confirm("Are you sure you want to delete this shipping rule?")) {
      await deleteShippingRule();
      onSave();
      onClose();
    }
  };

  const renderCondition = (conditionType: string) => {
    switch (conditionType) {
      case 'destination':
        return (
          <div key="destination" className="bg-blue-50 rounded-md border border-blue-200 p-3 my-2">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-slate-900">Destination</h4>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeCondition('destination')}
                className="h-8 w-8 p-0 text-slate-500 hover:text-red-600 hover:bg-red-50"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-2">
              <Label className="text-xs text-slate-700">Country Code</Label>
              <form.Field
                name="conditions.destination.country_code"
                children={(field) => {
                  const CountrySelect = require("@karrio/ui/components/country-select").CountrySelect;
                  return (
                    <CountrySelect
                      value={field.state.value || ""}
                      onValueChange={(val: string) => field.handleChange(val || null)}
                      placeholder="Select country"
                      fieldClass="m-0"
                      wrapperClass="m-0"
                    />
                  );
                }}
              />
              <p className="text-xs text-slate-500">ISO 2-letter country code</p>
            </div>
          </div>
        );

      case 'weight':
        return (
          <div key="weight" className="bg-green-50 rounded-md border border-green-200 p-3 my-2">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-slate-900">Weight Range</h4>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeCondition('weight')}
                className="h-8 w-8 p-0 text-slate-500 hover:text-red-600 hover:bg-red-50"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Min</Label>
                <form.Field
                  name="conditions.weight.min"
                  children={(field) => (
                    <Input
                      type="number"
                      value={field.state.value || ""}
                      onChange={(e) => field.handleChange(parseFloat(e.target.value) || null)}
                      placeholder="0"
                      className="h-8"
                    />
                  )}
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Max</Label>
                <form.Field
                  name="conditions.weight.max"
                  children={(field) => (
                    <Input
                      type="number"
                      value={field.state.value || ""}
                      onChange={(e) => field.handleChange(parseFloat(e.target.value) || null)}
                      placeholder="100"
                      className="h-8"
                    />
                  )}
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Unit</Label>
                <form.Field
                  name="conditions.weight.unit"
                  children={(field) => (
                    <Select
                      value={field.state.value || "lb"}
                      onValueChange={(value) => field.handleChange(value)}
                    >
                      <SelectTrigger className="h-8">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="lb">lb</SelectItem>
                        <SelectItem value="oz">oz</SelectItem>
                        <SelectItem value="kg">kg</SelectItem>
                        <SelectItem value="g">g</SelectItem>
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>
            </div>
          </div>
        );

      case 'carrier_service':
        return (
          <div key="carrier_service" className="bg-orange-50 rounded-md border border-orange-200 p-3 my-2">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-slate-900">Carrier & Service</h4>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeCondition('carrier_service')}
                className="h-8 w-8 p-0 text-slate-500 hover:text-red-600 hover:bg-red-50"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Carrier Connection</Label>
                <form.Field
                  name="conditions.carrier_id"
                  children={(field) => (
                    <Select
                      value={field.state.value || "any"}
                      onValueChange={(value) => {
                        field.handleChange(value === "any" ? null : value);
                        // If carrier changes, clear service to avoid mismatches
                        form.setFieldValue("conditions.service" as any, null as any);
                      }}
                    >
                      <SelectTrigger className="h-8">
                        <SelectValue placeholder="Select connection" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="any">Any connection</SelectItem>
                        {(userConnections || []).map((c: any) => (
                          <SelectItem key={c.id} value={c.id}>
                            {(c.display_name || c.custom_carrier_name || c.carrier_name)}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Service</Label>
                <form.Subscribe
                  selector={(state) => state.values.conditions?.carrier_id}
                  children={(carrierId) => (
                    <form.Field
                      name="conditions.service"
                      children={(field) => {
                        // Resolve carrier_name from selected connection to list relevant services
                        const connection = (userConnections || []).find((c: any) => c.id === carrierId);
                        const carrierName = connection?.carrier_name;
                        const serviceMap = references?.services || {};
                        const servicesForCarrier = carrierName ? Object.keys(serviceMap[carrierName] || {}) : [];
                        return (
                          <Select
                            value={field.state.value || ""}
                            onValueChange={(value) => field.handleChange(value === "any" ? null : value)}
                          >
                            <SelectTrigger className="h-8">
                              <SelectValue placeholder={carrierId ? "Select service" : "Select a connection first"} />
                            </SelectTrigger>
                            <SelectContent>
                              {carrierId && servicesForCarrier.length > 0 ? (
                                servicesForCarrier.map((svc) => (
                                  <SelectItem key={svc} value={svc}>{svc}</SelectItem>
                                ))
                              ) : (
                                <SelectItem value="any">Any</SelectItem>
                              )}
                            </SelectContent>
                          </Select>
                        );
                      }}
                    />
                  )}
                />
              </div>
            </div>
          </div>
        );

      case 'rate_comparison':
        return (
          <div key="rate_comparison" className="bg-purple-50 rounded-md border border-purple-200 p-3">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-slate-900">Rate Comparison</h4>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeCondition('rate_comparison')}
                className="h-8 w-8 p-0 text-slate-500 hover:text-red-600 hover:bg-red-50"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Field</Label>
                <form.Field
                  name="conditions.rate_comparison.compare"
                  children={(field) => (
                    <Select
                      value={field.state.value || "total_charge"}
                      onValueChange={(value) => field.handleChange(value)}
                    >
                      <SelectTrigger className="h-8">
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="total_charge">Total Charge</SelectItem>
                        <SelectItem value="transit_days">Transit Days</SelectItem>
                        <SelectItem value="insurance_charge">Insurance</SelectItem>
                        <SelectItem value="fuel_surcharge">Fuel</SelectItem>
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Operator</Label>
                <form.Field
                  name="conditions.rate_comparison.operator"
                  children={(field) => (
                    <Select
                      value={field.state.value || "eq"}
                      onValueChange={(value) => field.handleChange(value)}
                    >
                      <SelectTrigger className="h-8">
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="eq">=</SelectItem>
                        <SelectItem value="gt">&gt;</SelectItem>
                        <SelectItem value="gte">≥</SelectItem>
                        <SelectItem value="lt">&lt;</SelectItem>
                        <SelectItem value="lte">≤</SelectItem>
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Value</Label>
                <form.Field
                  name="conditions.rate_comparison.value"
                  children={(field) => (
                    <Input
                      type="number"
                      value={field.state.value || ""}
                      onChange={(e) => field.handleChange(parseFloat(e.target.value) || null)}
                      placeholder="0.00"
                      className="h-8"
                    />
                  )}
                />
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  const renderAction = (actionType: string) => {
    switch (actionType) {
      case 'service_selection':
        return (
          <div key="service_selection" className="bg-blue-50 rounded-md border border-blue-200 p-3">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-slate-900">Service Selection</h4>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeAction('service_selection')}
                className="h-8 w-8 p-0 text-slate-500 hover:text-red-600 hover:bg-red-50"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Strategy</Label>
                <form.Field
                  name="actions.select_service.strategy"
                  children={(field) => (
                    <Select
                      value={field.state.value || "cheapest"}
                      onValueChange={(value) => field.handleChange(value)}
                    >
                      <SelectTrigger className="h-8">
                        <SelectValue placeholder="Select strategy" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="cheapest">Select Cheapest</SelectItem>
                        <SelectItem value="fastest">Select Fastest</SelectItem>
                        <SelectItem value="preferred">Prefer Specific Carrier</SelectItem>
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>

              <form.Field
                name="actions.select_service.strategy"
                children={(strategyField) => {
                  if (strategyField.state.value === "preferred") {
                    return (
                      <>
                        <div className="space-y-1">
                          <Label className="text-xs text-slate-700">Preferred Carrier</Label>
                          <form.Field
                            name="actions.select_service.carrier_code"
                            children={(field) => (
                              <Select
                                value={field.state.value || "none"}
                                onValueChange={(value) => {
                                  field.handleChange(value === "none" ? null : value);
                                  // Reset dependent fields when carrier changes
                                  form.setFieldValue("actions.select_service.service_code" as any, null as any);
                                }}
                              >
                                <SelectTrigger className="h-8">
                                  <SelectValue placeholder="Select carrier" />
                                </SelectTrigger>
                                <SelectContent>
                                  <SelectItem value="none">Select carrier</SelectItem>
                                  {references?.carriers && Object.entries(references.carriers).map(([key, name]) => (
                                    <SelectItem key={key} value={key}>
                                      {name as string}
                                    </SelectItem>
                                  ))}
                                </SelectContent>
                              </Select>
                            )}
                          />
                        </div>
                        <div className="grid grid-cols-2 gap-2">
                          <div className="space-y-1">
                            <Label className="text-xs text-slate-700">Carrier ID</Label>
                            <form.Field
                              name="actions.select_service.carrier_id"
                              children={(field) => (
                                <Input
                                  value={field.state.value || ""}
                                  onChange={(e) => field.handleChange(e.target.value)}
                                  placeholder="Optional"
                                  className="h-8"
                                />
                              )}
                            />
                          </div>
                          <div className="space-y-1">
                            <Label className="text-xs text-slate-700">Service Code</Label>
                            <form.Subscribe
                              selector={(state) => state.values.actions?.select_service?.carrier_code}
                              children={(carrierCode) => (
                                <form.Field
                                  name="actions.select_service.service_code"
                                  children={(field) => {
                                    const serviceMap = references?.services || {};
                                    const servicesForCarrier = carrierCode ? Object.keys(serviceMap[carrierCode] || {}) : [];
                                    return (
                                      <Select
                                        value={field.state.value || ""}
                                        onValueChange={(value) => field.handleChange(value === "any" ? null : value)}
                                      >
                                        <SelectTrigger className="h-8">
                                          <SelectValue placeholder={carrierCode ? "Select service" : "Select carrier first"} />
                                        </SelectTrigger>
                                        <SelectContent>
                                          {carrierCode && servicesForCarrier.length > 0 ? (
                                            servicesForCarrier.map((svc) => (
                                              <SelectItem key={svc} value={svc}>{svc}</SelectItem>
                                            ))
                                          ) : (
                                            <SelectItem value="any">Any</SelectItem>
                                          )}
                                        </SelectContent>
                                      </Select>
                                    );
                                  }}
                                />
                              )}
                            />
                          </div>
                        </div>
                      </>
                    );
                  }
                  return null;
                }}
              />
            </div>
          </div>
        );

      case 'service_blocking':
        return (
          <div key="service_blocking" className="bg-red-50 rounded-md border border-red-200 p-3">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-sm font-semibold text-slate-900">Service Blocking</h4>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeAction('service_blocking')}
                className="h-8 w-8 p-0 text-slate-500 hover:text-red-600 hover:bg-red-50"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex items-center justify-between p-3 bg-white rounded-md border">
              <div>
                <Label className="text-xs text-slate-700">Block automatic selection</Label>
                <p className="text-xs text-slate-500">Prevent auto service selection</p>
              </div>
              <form.Field
                name="actions.block_service"
                children={(field) => (
                  <Switch
                    checked={field.state.value || false}
                    onCheckedChange={(checked) => field.handleChange(checked)}
                  />
                )}
              />
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  const availableConditions = conditionTypes.filter(ct => !activeConditions.includes(ct.id));
  const availableActions = actionTypes.filter(at => !activeActions.includes(at.id));

  return (
    <div className="h-full flex flex-col">
      <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
        <div className="flex items-center justify-between">
          <SheetTitle className="text-lg font-semibold">
            {isNew ? "Create shipping rule" : "Edit shipping rule"}
          </SheetTitle>
          {!isNew && current?.id && (
            <button
              className="text-xs px-2 py-1 border rounded hover:bg-slate-50"
              title="Copy rule ID"
              onClick={() => navigator.clipboard?.writeText(current.id)}
            >
              Copy ID
            </button>
          )}
        </div>
      </SheetHeader>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-8 pb-32">
        {/* Basic Information */}
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-4">Basic Information</h3>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Rule Name *</Label>
                <form.Field
                  name="name"
                  validators={{
                    onChange: ({ value }) => !value ? 'Rule name is required' : undefined,
                  }}
                  children={(field) => (
                    <>
                      <Input
                        value={field.state.value || ""}
                        onChange={(e) => field.handleChange(e.target.value)}
                        placeholder="e.g., Canada Express Rule"
                        className={`h-8 ${field.state.meta.errors.length ? "border-red-300" : ""}`}
                      />
                      {field.state.meta.errors.map((error, index) => (
                        <p key={index} className="text-xs text-red-600">{error}</p>
                      ))}
                    </>
                  )}
                />
              </div>

              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Priority</Label>
                <form.Field
                  name="priority"
                  children={(field) => (
                    <Input
                      type="number"
                      value={field.state.value || 1}
                      onChange={(e) => field.handleChange(parseInt(e.target.value) || 1)}
                      min="0"
                      max="100"
                      className="h-8"
                    />
                  )}
                />
                <p className="text-xs text-slate-500">Lower numbers = higher priority</p>
              </div>

              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Description</Label>
                <form.Field
                  name="description"
                  children={(field) => (
                    <Textarea
                      value={field.state.value || ""}
                      onChange={(e) => field.handleChange(e.target.value)}
                      placeholder="Describe when this rule should be applied..."
                      rows={2}
                      className="text-xs"
                    />
                  )}
                />
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border my-4">
                <div>
                  <Label className="text-xs text-slate-700">Enable Rule</Label>
                  <p className="text-xs text-slate-500">Activate this shipping rule</p>
                </div>
                <form.Field
                  name="is_active"
                  children={(field) => (
                    <Switch
                      checked={field.state.value || false}
                      onCheckedChange={(checked) => field.handleChange(checked)}
                    />
                  )}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Conditions */}
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-2">Conditions</h3>
            <p className="text-xs text-slate-600 mb-4">When to apply this rule</p>

            <div className="space-y-3">
              {activeConditions.map(conditionType => renderCondition(conditionType))}

              {availableConditions.length > 0 && (
                <div className="border-2 border-dashed border-slate-200 rounded-md p-3 my-2">
                  <Select value={conditionSelectValue} onValueChange={addCondition}>
                    <SelectTrigger className="h-9">
                      <div className="flex items-center">
                        <Plus className="h-4 w-4 mr-2 text-slate-500" />
                        <SelectValue placeholder="Add a condition..." />
                      </div>
                    </SelectTrigger>
                    <SelectContent>
                      {availableConditions.map(condition => (
                        <SelectItem key={condition.id} value={condition.id}>
                          <div className="flex flex-col">
                            <span className="font-medium text-xs">{condition.label}</span>
                            <span className="text-xs text-slate-500">{condition.description}</span>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}

              {activeConditions.length === 0 && (
                <div className="text-center py-6 text-slate-500">
                  <div className="text-xs">No conditions added</div>
                  <div className="text-xs mt-1">Add conditions to control when this rule applies</div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-2">Actions</h3>
            <p className="text-xs text-slate-600 mb-4">What to do when conditions match</p>

            <div className="space-y-3">
              {activeActions.map(actionType => renderAction(actionType))}

              {availableActions.length > 0 && (
                <div className="border-2 border-dashed border-slate-200 rounded-md p-3 my-2">
                  <Select value={actionSelectValue} onValueChange={addAction}>
                    <SelectTrigger className="h-9">
                      <div className="flex items-center">
                        <Plus className="h-4 w-4 mr-2 text-slate-500" />
                        <SelectValue placeholder="Add an action..." />
                      </div>
                    </SelectTrigger>
                    <SelectContent>
                      {availableActions.map(action => (
                        <SelectItem key={action.id} value={action.id}>
                          <div className="flex flex-col">
                            <span className="font-medium text-xs">{action.label}</span>
                            <span className="text-xs text-slate-500">{action.description}</span>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}

              {activeActions.length === 0 && (
                <div className="text-center py-6 text-slate-500">
                  <div className="text-xs">No actions added</div>
                  <div className="text-xs mt-1">Add actions to define what happens when conditions match</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Floating Action Buttons */}
      <div className="sticky bottom-0 z-10 bg-white border-t px-4 py-4">
        <div className="flex items-center justify-between">
          <div>
            {!isNew && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleDelete}
                disabled={loader.loading}
                className="text-red-600 border-red-200 hover:bg-red-50"
              >
                <Trash2 className="h-4 w-4 mr-1" />
                Delete
              </Button>
            )}
          </div>
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={onClose}
              disabled={loader.loading}
            >
              Cancel
            </Button>
            <form.Subscribe
              selector={(state) => [state.canSubmit, state.isSubmitting]}
              children={([canSubmit, isSubmitting]) => (
                <Button
                  onClick={handleSave}
                  disabled={!canSubmit || isSubmitting || loader.loading}
                  size="sm"
                >
                  {loader.loading || isSubmitting ? "Saving..." : "Save rule"}
                </Button>
              )}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
