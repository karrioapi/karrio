"use client";
import { useShippingRules, useShippingRuleMutation } from "@karrio/hooks/shipping-rules";
import { Sheet, SheetContent, SheetTrigger } from "@karrio/ui/components/ui/sheet";
import { ShippingRuleForm } from "@karrio/core/components/shipping-rule-form";
import { MoreHorizontal, Plus, Settings, Trash2, Edit, Info, Target, Shield, Truck, HelpCircle } from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@karrio/ui/components/ui/alert-dialog";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { Button } from "@karrio/ui/components/ui/button";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Badge } from "@karrio/ui/components/ui/badge";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/core/components";
import { useState, useEffect } from "react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { ShippingRuleTemplatePicker } from "@karrio/core/components/shipping-rule-template-picker";
import { ShippingRuleTemplate } from "@karrio/hooks/shipping-rule-templates";

const ContextProviders = bundleContexts([ModalProvider]);



export default function Page(pageProps: any) {
  const Component = (): JSX.Element => {
    const { user_connections } = useCarrierConnections();
    const [deletingId, setDeletingId] = useState<string | null>(null);
    const [editingId, setEditingId] = useState<string | null>(null);
    const [isCreating, setIsCreating] = useState(false);
    const [selectedTemplate, setSelectedTemplate] = useState<ShippingRuleTemplate | null>(null);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [ruleToDelete, setRuleToDelete] = useState<{ id: string; name: string } | null>(null);
    const mutation = useShippingRuleMutation();
    const {
      query: { data: { shipping_rules } = {}, ...query },
    } = useShippingRules();

    // Add CSS to hide sheet overlay
    useEffect(() => {
      const style = document.createElement('style');
      style.textContent = `
        [data-radix-dialog-overlay] {
          display: none !important;
        }
        .bg-black\\/80 {
          display: none !important;
        }
      `;
      document.head.appendChild(style);

      return () => {
        document.head.removeChild(style);
      };
    }, []);

    const handleDeleteClick = (id: string, name: string) => {
      setRuleToDelete({ id, name });
      setDeleteDialogOpen(true);
    };

    const handleDeleteConfirm = async () => {
      if (ruleToDelete) {
        setDeletingId(ruleToDelete.id);
        try {
          await mutation.deleteShippingRule.mutateAsync({ id: ruleToDelete.id });
        } catch (error) {
          console.error("Failed to delete shipping rule:", error);
        } finally {
          setDeletingId(null);
          setRuleToDelete(null);
          setDeleteDialogOpen(false);
        }
      }
    };

    const handleFormSave = () => {
      query.refetch();
    };

    const handleToggleActive = async (id: string, isActive: boolean) => {
      try {
        // Find the current rule to get its data
        const currentRule = (shipping_rules?.edges || []).find(({ node }) => node.id === id)?.node;
        if (!currentRule) return;

        await mutation.updateShippingRule.mutateAsync({
          id,
          name: currentRule.name,
          description: currentRule.description,
          priority: currentRule.priority,
          is_active: isActive,
          conditions: currentRule.conditions,
          actions: currentRule.actions,
          metadata: currentRule.metadata
        });
        query.refetch();
      } catch (error) {
        console.error("Failed to toggle shipping rule:", error);
      }
    };

    const getConditionsSummary = (rule: any) => {
      const conditions = rule.conditions || {};
      const summary: string[] = [];

      if (conditions.destination?.country_code) {
        summary.push(`Country: ${conditions.destination.country_code}`);
      }
      if (conditions.weight) {
        const { min, max, unit = "lb" } = conditions.weight;
        if (min && max) {
          summary.push(`Weight: ${min}-${max}${unit}`);
        } else if (min) {
          summary.push(`Weight: ≥${min}${unit}`);
        } else if (max) {
          summary.push(`Weight: ≤${max}${unit}`);
        }
      }
      if (conditions.carrier_id) {
        const conn = user_connections?.find((c) => c.id === conditions.carrier_id);
        const name = conn?.display_name || conn?.custom_carrier_name || conn?.carrier_name || conditions.carrier_id;
        summary.push(`Carrier: ${name}`);
      }
      if (conditions.service) {
        summary.push(`Service: ${conditions.service}`);
      }

      return summary.length > 0 ? summary : ["No specific conditions"];
    };

    const getActionsSummary = (rule: any) => {
      const actions = rule.actions || {};
      const summary: string[] = [];

      if (actions.select_service) {
        const { strategy, carrier_code } = actions.select_service;
        if (strategy === "cheapest") summary.push("Select cheapest option");
        if (strategy === "fastest") summary.push("Select fastest option");
        if (strategy === "preferred" && carrier_code) summary.push(`Prefer ${carrier_code.toUpperCase()}`);
      }

      if (actions.block_service) {
        summary.push("Block automatic selection");
      }

      return summary.length > 0 ? summary : ["No specific actions"];
    };

    return (
      <>
        {/* Header */}
        <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 px-0 pb-0 pt-4">
          <span className="text-2xl font-semibold">Shipping Rules</span>
          <ShippingRuleTemplatePicker
            onSelectTemplate={(template) => {
              setSelectedTemplate(template);
              setIsCreating(true);
            }}
          >
            <Button size="sm">
              <Plus className="h-4 w-4 mr-2" />
              New Rule
            </Button>
          </ShippingRuleTemplatePicker>
        </header>

        <div className="py-4">
          {/* Shipping Rules Info Banner */}
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-4 mb-6">
            <div className="flex flex-col sm:flex-row items-start gap-3">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Info className="h-4 w-4 text-green-600" />
              </div>
              <div className="space-y-2 flex-1">
                <h3 className="text-sm font-semibold text-green-900">How Shipping Rules Work</h3>
                <p className="text-sm text-green-700">
                  Shipping rules automatically select the best carrier and service based on your criteria.
                  Rules are evaluated by priority order, with higher numbers taking precedence.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-3">
                  <div className="flex items-start gap-2">
                    <Target className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-xs font-medium text-green-800">Conditions</p>
                      <p className="text-xs text-green-600">Define when the rule applies (weight, destination, etc.)</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-2">
                    <Shield className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-xs font-medium text-blue-800">Actions</p>
                      <p className="text-xs text-blue-600">What to do when conditions match (select carrier, block service)</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-2">
                    <Truck className="h-4 w-4 text-purple-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-xs font-medium text-purple-800">Priority</p>
                      <p className="text-xs text-purple-600">Higher priority rules override lower ones</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {!query.isFetched && (
            <div className="flex justify-center py-8">
              <Spinner />
            </div>
          )}

          {query.isFetched && (shipping_rules?.edges || []).length > 0 && (
            <div className="grid gap-4 max-w-2xl">
              {(shipping_rules?.edges || []).map(({ node: rule }) => (
                <Card key={rule.id} className="border border-slate-200 hover:border-slate-300 transition-colors rounded-lg shadow-sm hover:shadow-md">
                  <CardContent className="p-4">
                    <div className="flex flex-col space-y-4">
                      {/* Header Section */}
                      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-slate-900 mb-1">{rule.name}</h3>
                          {rule.description && (
                            <p className="text-sm text-slate-600">{rule.description}</p>
                          )}
                        </div>
                        <div className="flex flex-wrap items-center gap-2">
                          <div className="group relative">
                            <Badge variant="outline" className="text-xs cursor-help">
                              Priority {rule.priority}
                            </Badge>
                            <div className="absolute right-0 bottom-full mb-1 w-56 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                              Higher priority rules (larger numbers) are evaluated first and can override lower priority rules.
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Switch
                              checked={rule.is_active || false}
                              onCheckedChange={(checked) => handleToggleActive(rule.id, checked)}
                              className="h-4 w-7"
                            />
                            <span className="text-xs text-slate-600">
                              {rule.is_active ? "Active" : "Inactive"}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Conditions and Actions Grid */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                        <div>
                          <div className="flex items-center gap-1 mb-3">
                            <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                            <h4 className="text-sm font-medium text-slate-700">Conditions</h4>
                            <div className="group relative">
                              <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                              <div className="absolute left-0 bottom-full mb-1 w-48 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                                Conditions determine when this rule applies. If all conditions match, the actions will be executed.
                              </div>
                            </div>
                          </div>
                          <div className="space-y-2 pl-4">
                            {getConditionsSummary(rule).map((condition, index) => (
                              <div key={index} className="text-sm text-slate-600">
                                {condition}
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <div className="flex items-center gap-1 mb-3">
                            <span className="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
                            <h4 className="text-sm font-medium text-slate-700">Actions</h4>
                            <div className="group relative">
                              <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                              <div className="absolute left-0 bottom-full mb-1 w-48 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                                Actions define what happens when the rule conditions are met (e.g., select cheapest carrier, block certain services).
                              </div>
                            </div>
                          </div>
                          <div className="space-y-2 pl-4">
                            {getActionsSummary(rule).map((action, index) => (
                              <div key={index} className="text-sm text-slate-600">
                                {action}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex items-center justify-end gap-2 pt-2 border-t">
                        {/* Copyable ID */}
                        {rule.id && (
                          <button
                            className="text-xs px-2 py-1 border rounded hover:bg-slate-50"
                            title="Copy rule ID"
                            onClick={() => navigator.clipboard?.writeText(rule.id)}
                          >
                            ID
                          </button>
                        )}
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" className="w-40">
                            <Sheet open={editingId === rule.id} onOpenChange={(open) => !open && setEditingId(null)}>
                              <SheetTrigger asChild>
                                <DropdownMenuItem
                                  onClick={() => setEditingId(rule.id)}
                                  onSelect={(e) => e.preventDefault()}
                                >
                                  <Edit className="h-4 w-4 mr-2" />
                                  Edit
                                </DropdownMenuItem>
                              </SheetTrigger>
                              <SheetContent className="w-full sm:w-[800px] sm:max-w-[800px] p-0 shadow-none">
                                <ShippingRuleForm
                                  ruleId={rule.id}
                                  onClose={() => setEditingId(null)}
                                  onSave={handleFormSave}
                                />
                              </SheetContent>
                            </Sheet>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                              onClick={() => handleDeleteClick(rule.id, rule.name)}
                              disabled={deletingId === rule.id}
                              className="text-destructive"
                            >
                              <Trash2 className="h-4 w-4 mr-2" />
                              {deletingId === rule.id ? "Deleting..." : "Delete"}
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {query.isFetched && (shipping_rules?.edges || []).length === 0 && (
            <Card className="rounded-lg shadow-sm">
              <CardContent className="flex flex-col items-center justify-center py-16">
                <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-6">
                  <Settings className="h-8 w-8 text-slate-500" />
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2">No shipping rules found</h3>
                <p className="text-slate-600 text-center mb-6 max-w-md">
                  Automate your shipping process by creating rules that automatically select the best carrier and service based on your criteria.
                </p>
                <ShippingRuleTemplatePicker
                  onSelectTemplate={(template) => {
                    setSelectedTemplate(template);
                    setIsCreating(true);
                  }}
                >
                  <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                    <Plus className="h-4 w-4 mr-2" />
                    Create Your First Rule
                  </Button>
                </ShippingRuleTemplatePicker>
              </CardContent>
            </Card>
          )}

          {/* Delete Confirmation Dialog */}
          <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Delete Shipping Rule</AlertDialogTitle>
                <AlertDialogDescription>
                  Are you sure you want to delete "{ruleToDelete?.name}"? This action cannot be undone.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter className="flex justify-end gap-3">
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction
                  onClick={handleDeleteConfirm}
                  className="bg-red-600 hover:bg-red-700"
                >
                  Delete
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>

          {/* Create Rule Sheet */}
          <Sheet open={isCreating} onOpenChange={(open) => {
            if (!open) {
              setIsCreating(false);
              setSelectedTemplate(null);
            }
          }}>
            <SheetContent className="w-full sm:w-[800px] sm:max-w-[800px] p-0 shadow-none">
              <ShippingRuleForm
                templateData={selectedTemplate}
                onClose={() => {
                  setIsCreating(false);
                  setSelectedTemplate(null);
                }}
                onSave={handleFormSave}
              />
            </SheetContent>
          </Sheet>
        </div>
      </>
    );
  };

  return (
    <>
      <ContextProviders>
        <Component />
      </ContextProviders>
    </>
  );
}
