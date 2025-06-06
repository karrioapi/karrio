"use client";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { SheetHeader, SheetTitle } from "@karrio/ui/components/ui/sheet";
import { useShippingRuleForm } from "@karrio/hooks/shipping-rules";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Trash2, Plus, X } from "lucide-react";
import React from "react";

interface ShippingRuleFormProps {
  ruleId?: string;
  onClose: () => void;
  onSave: () => void;
}

export function ShippingRuleForm({ ruleId, onClose, onSave }: ShippingRuleFormProps) {
  const loader = useLoader();
  const { references } = useAPIMetadata();
  const {
    form,
    shippingRule,
    isNew,
    save,
    deleteShippingRule,
    handleChange,
    handleConditionChange,
    handleActionChange,
    handleWeightChange,
    handleSelectServiceChange,
    handleDestinationChange,
    handleRateComparisonChange,
    current,
    query,
  } = useShippingRuleForm({ id: ruleId });

  // Use current data when available for editing, otherwise use form state
  const ruleData = current || shippingRule;

  // State for dynamic conditions and actions
  const [activeConditions, setActiveConditions] = React.useState<string[]>([]);
  const [activeActions, setActiveActions] = React.useState<string[]>([]);

  // Initialize active conditions and actions based on existing data
  React.useEffect(() => {
    const conditions: string[] = [];
    const actions: string[] = [];

    if (ruleData.conditions?.destination?.country_code) {
      conditions.push('destination');
    }
    if (ruleData.conditions?.weight?.min || ruleData.conditions?.weight?.max) {
      conditions.push('weight');
    }
    if (ruleData.conditions?.carrier_id || ruleData.conditions?.service) {
      conditions.push('carrier_service');
    }
    if (ruleData.conditions?.rate_comparison?.compare) {
      conditions.push('rate_comparison');
    }

    if (ruleData.actions?.select_service?.strategy) {
      actions.push('service_selection');
    }
    if (ruleData.actions?.block_service) {
      actions.push('service_blocking');
    }

    setActiveConditions(conditions);
    setActiveActions(actions);
  }, [ruleData]);

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
    }
  };

  const removeCondition = (conditionType: string) => {
    setActiveConditions(activeConditions.filter(c => c !== conditionType));
    // Clear the condition data
    switch (conditionType) {
      case 'destination':
        handleDestinationChange('country_code', '');
        break;
      case 'weight':
        handleWeightChange('min', null);
        handleWeightChange('max', null);
        handleWeightChange('unit', 'lb');
        break;
      case 'carrier_service':
        handleConditionChange('carrier_id', '');
        handleConditionChange('service', '');
        break;
      case 'rate_comparison':
        handleRateComparisonChange('compare', '');
        handleRateComparisonChange('operator', '');
        handleRateComparisonChange('value', null);
        break;
    }
  };

  const addAction = (actionType: string) => {
    if (!activeActions.includes(actionType)) {
      setActiveActions([...activeActions, actionType]);
    }
  };

  const removeAction = (actionType: string) => {
    setActiveActions(activeActions.filter(a => a !== actionType));
    // Clear the action data
    switch (actionType) {
      case 'service_selection':
        handleSelectServiceChange('strategy', '');
        handleSelectServiceChange('carrier_code', '');
        handleSelectServiceChange('carrier_id', '');
        handleSelectServiceChange('service_code', '');
        break;
      case 'service_blocking':
        handleActionChange('block_service', false);
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
                className="h-6 w-6 p-0 text-slate-500 hover:text-red-600"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-2">
              <Label className="text-xs text-slate-700">Country Code</Label>
              <Input
                value={ruleData.conditions?.destination?.country_code || ""}
                onChange={(e) => handleDestinationChange("country_code", e.target.value)}
                placeholder="CA, US, GB..."
                className="h-8"
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
                className="h-6 w-6 p-0 text-slate-500 hover:text-red-600"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Min</Label>
                <Input
                  type="number"
                  value={ruleData.conditions?.weight?.min || ""}
                  onChange={(e) => handleWeightChange("min", parseFloat(e.target.value) || null)}
                  placeholder="0"
                  className="h-8"
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Max</Label>
                <Input
                  type="number"
                  value={ruleData.conditions?.weight?.max || ""}
                  onChange={(e) => handleWeightChange("max", parseFloat(e.target.value) || null)}
                  placeholder="100"
                  className="h-8"
                />
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Unit</Label>
                <Select
                  value={ruleData.conditions?.weight?.unit || "lb"}
                  onValueChange={(value) => handleWeightChange("unit", value)}
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
                className="h-6 w-6 p-0 text-slate-500 hover:text-red-600"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Carrier</Label>
                <Select
                  value={ruleData.conditions?.carrier_id || "any"}
                  onValueChange={(value) => handleConditionChange("carrier_id", value === "any" ? null : value)}
                >
                  <SelectTrigger className="h-8">
                    <SelectValue placeholder="Select carrier" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="any">Any carrier</SelectItem>
                    {references?.carriers && Object.entries(references.carriers).map(([key, name]) => (
                      <SelectItem key={key} value={key}>
                        {name as string}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Service</Label>
                <Input
                  value={ruleData.conditions?.service || ""}
                  onChange={(e) => handleConditionChange("service", e.target.value)}
                  placeholder="ground, express..."
                  className="h-8"
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
                className="h-6 w-6 p-0 text-slate-500 hover:text-red-600"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Field</Label>
                <Select
                  value={ruleData.conditions?.rate_comparison?.compare || "total_charge"}
                  onValueChange={(value) => handleRateComparisonChange("compare", value)}
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
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Operator</Label>
                <Select
                  value={ruleData.conditions?.rate_comparison?.operator || "eq"}
                  onValueChange={(value) => handleRateComparisonChange("operator", value)}
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
              </div>
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Value</Label>
                <Input
                  type="number"
                  value={ruleData.conditions?.rate_comparison?.value || ""}
                  onChange={(e) => handleRateComparisonChange("value", parseFloat(e.target.value) || null)}
                  placeholder="0.00"
                  className="h-8"
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
                className="h-6 w-6 p-0 text-slate-500 hover:text-red-600"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Strategy</Label>
                <Select
                  value={shippingRule.actions?.select_service?.strategy || "cheapest"}
                  onValueChange={(value) => handleSelectServiceChange("strategy", value)}
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
              </div>

              {shippingRule.actions?.select_service?.strategy === "preferred" && (
                <>
                  <div className="space-y-1">
                    <Label className="text-xs text-slate-700">Preferred Carrier</Label>
                    <Select
                      value={shippingRule.actions?.select_service?.carrier_code || "none"}
                      onValueChange={(value) => handleSelectServiceChange("carrier_code", value === "none" ? null : value)}
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
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Carrier ID</Label>
                      <Input
                        value={shippingRule.actions?.select_service?.carrier_id || ""}
                        onChange={(e) => handleSelectServiceChange("carrier_id", e.target.value)}
                        placeholder="Optional"
                        className="h-8"
                      />
                    </div>
                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Service Code</Label>
                      <Input
                        value={shippingRule.actions?.select_service?.service_code || ""}
                        onChange={(e) => handleSelectServiceChange("service_code", e.target.value)}
                        placeholder="Optional"
                        className="h-8"
                      />
                    </div>
                  </div>
                </>
              )}
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
                className="h-6 w-6 p-0 text-slate-500 hover:text-red-600"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex items-center justify-between p-3 bg-white rounded-md border">
              <div>
                <Label className="text-xs text-slate-700">Block automatic selection</Label>
                <p className="text-xs text-slate-500">Prevent auto service selection</p>
              </div>
              <Switch
                checked={ruleData.actions?.block_service || false}
                onCheckedChange={(checked) => handleActionChange("block_service", checked)}
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
                <Input
                  value={ruleData.name || ""}
                  onChange={(e) => handleChange({ name: e.target.value })}
                  placeholder="e.g., Canada Express Rule"
                  className={`h-8 ${!ruleData.name ? "border-red-300" : ""}`}
                />
                {!ruleData.name && (
                  <p className="text-xs text-red-600">Rule name is required</p>
                )}
              </div>

              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Priority</Label>
                <Input
                  type="number"
                  value={ruleData.priority || 1}
                  onChange={(e) => handleChange({ priority: parseInt(e.target.value) || 1 })}
                  min="0"
                  max="100"
                  className="h-8"
                />
                <p className="text-xs text-slate-500">Lower numbers = higher priority</p>
              </div>

              <div className="space-y-1">
                <Label className="text-xs text-slate-700">Description</Label>
                <Textarea
                  value={ruleData.description || ""}
                  onChange={(e) => handleChange({ description: e.target.value })}
                  placeholder="Describe when this rule should be applied..."
                  rows={2}
                  className="text-xs"
                />
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-50 rounded-md border my-4">
                <div>
                  <Label className="text-xs text-slate-700">Enable Rule</Label>
                  <p className="text-xs text-slate-500">Activate this shipping rule</p>
                </div>
                <Switch
                  checked={ruleData.is_active || false}
                  onCheckedChange={(checked) => handleChange({ is_active: checked })}
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
                  <Select onValueChange={addCondition}>
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
                  <Select onValueChange={addAction}>
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
            <Button
              onClick={handleSave}
              disabled={loader.loading || (!form.state.isDirty && !isNew)}
              size="sm"
            >
              {loader.loading ? "Saving..." : "Save rule"}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
