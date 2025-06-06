"use client";
import { useShippingRules, useShippingRuleMutation } from "@karrio/hooks/shipping-rules";
import { Sheet, SheetContent, SheetTrigger, SheetPortal } from "@karrio/ui/components/ui/sheet";
import { ShippingRuleForm } from "@karrio/core/components/shipping-rule-form";
import { MoreHorizontal, Plus, Settings, Trash2, Edit } from "lucide-react";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Switch } from "@karrio/ui/components/ui/switch";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { Button } from "@karrio/ui/components/ui/button";
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

const ContextProviders = bundleContexts([ModalProvider]);



export default function Page(pageProps: any) {
  const Component = (): JSX.Element => {
    const [deletingId, setDeletingId] = useState<string | null>(null);
    const [editingId, setEditingId] = useState<string | null>(null);
    const [isCreating, setIsCreating] = useState(false);
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

    const handleDelete = async (id: string) => {
      if (confirm("Are you sure you want to delete this shipping rule?")) {
        setDeletingId(id);
        try {
          await mutation.deleteShippingRule.mutateAsync({ id });
        } catch (error) {
          console.error("Failed to delete shipping rule:", error);
        } finally {
          setDeletingId(null);
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
        summary.push(`Carrier: ${conditions.carrier_id}`);
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
        <header className="flex items-center justify-between py-4">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-semibold">Shipping Rules</h1>
            <Badge variant="secondary" className="text-xs font-bold">
              PREVIEW
            </Badge>
          </div>
          <Sheet open={isCreating} onOpenChange={setIsCreating}>
            <SheetTrigger asChild>
              <Button size="sm">
                <Plus className="h-4 w-4 mr-2" />
                Add Rule
              </Button>
            </SheetTrigger>
            <SheetContent className="w-[800px] min-w-[800px] sm:max-w-[800px] p-0 shadow-none">
              <ShippingRuleForm
                ruleId="new"
                onClose={() => setIsCreating(false)}
                onSave={handleFormSave}
              />
            </SheetContent>
          </Sheet>
        </header>

        <div className="py-6">
          {!query.isFetched && (
            <div className="flex justify-center py-8">
              <Spinner />
            </div>
          )}

          {query.isFetched && (shipping_rules?.edges || []).length > 0 && (
            <div className="grid gap-4 max-w-2xl">
              {(shipping_rules?.edges || []).map(({ node: rule }) => (
                <Card key={rule.id} className="border border-slate-200 hover:border-slate-300 transition-colors rounded-md shadow-none">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                          <div>
                            <h3 className="text-lg font-semibold text-slate-900">{rule.name}</h3>
                            {rule.description && (
                              <p className="text-base text-slate-600 mt-1">{rule.description}</p>
                            )}
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className="text-xs">
                              Priority {rule.priority}
                            </Badge>
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

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <h4 className="text-base font-medium text-slate-700 mb-2">Conditions</h4>
                            <div className="space-y-1">
                              {getConditionsSummary(rule).map((condition, index) => (
                                <div key={index} className="text-slate-600 text-sm flex items-center">
                                  <span className="w-1 h-1 bg-slate-400 rounded-full mr-2"></span>
                                  {condition}
                                </div>
                              ))}
                            </div>
                          </div>

                          <div>
                            <h4 className="text-base font-medium text-slate-700 mb-2">Actions</h4>
                            <div className="space-y-1">
                              {getActionsSummary(rule).map((action, index) => (
                                <div key={index} className="text-slate-600 text-sm flex items-center">
                                  <span className="w-1 h-1 bg-slate-400 rounded-full mr-2"></span>
                                  {action}
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="ml-4">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="h-9 w-9 p-0">
                              <MoreHorizontal className="h-5 w-5" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
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
                              <SheetContent className="w-[800px] min-w-[800px] sm:max-w-[800px] p-0 shadow-none">
                                <ShippingRuleForm
                                  ruleId={rule.id}
                                  onClose={() => setEditingId(null)}
                                  onSave={handleFormSave}
                                />
                              </SheetContent>
                            </Sheet>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                              onClick={() => handleDelete(rule.id)}
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
            <Card className="rounded-md shadow-none">
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Settings className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium mb-2">No shipping rules found</h3>
                <p className="text-muted-foreground text-center mb-4 max-w-md">
                  Automate your shipping process by creating rules that automatically select the best carrier and service based on your criteria.
                </p>
                <Sheet open={isCreating} onOpenChange={setIsCreating}>
                  <SheetTrigger asChild>
                    <Button>
                      <Plus className="h-4 w-4 mr-2" />
                      Create Your First Rule
                    </Button>
                  </SheetTrigger>
                  <SheetContent className="w-[800px] min-w-[800px] sm:max-w-[800px] p-0 shadow-none">
                    <ShippingRuleForm
                      ruleId="new"
                      onClose={() => setIsCreating(false)}
                      onSave={handleFormSave}
                    />
                  </SheetContent>
                </Sheet>
              </CardContent>
            </Card>
          )}
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
