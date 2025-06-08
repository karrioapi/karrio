"use client";
import { useWorkflows, useWorkflowMutation } from "@karrio/hooks/workflows";
import { Sheet, SheetContent, SheetTrigger } from "@karrio/ui/components/ui/sheet";
import { MoreHorizontal, Plus, Settings, Trash2, Edit } from "lucide-react";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { Switch } from "@karrio/ui/components/ui/switch";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/core/components";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useState, useEffect } from "react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

const ContextProviders = bundleContexts([ModalProvider]);

export default function Page(pageProps: any) {
  const Component = (): JSX.Element => {
    const { metadata } = useAPIMetadata();
    const [deletingId, setDeletingId] = useState<string | null>(null);
    const mutation = useWorkflowMutation();
    const {
      query: { data: { workflows } = {}, ...query },
    } = useWorkflows();

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
      if (confirm("Are you sure you want to delete this workflow?")) {
        setDeletingId(id);
        try {
          await mutation.deleteWorkflow.mutateAsync({ id });
        } catch (error) {
          console.error("Failed to delete workflow:", error);
        } finally {
          setDeletingId(null);
        }
      }
    };

    const handleFormSave = () => {
      query.refetch();
    };

    const getTriggerSummary = (workflow: any) => {
      const trigger = workflow.trigger || {};
      const summary: string[] = [];

      if (trigger.trigger_type) {
        summary.push(`Type: ${trigger.trigger_type}`);
      }
      if (trigger.schedule && trigger.trigger_type === 'scheduled') {
        summary.push(`Schedule: ${trigger.schedule}`);
      }
      if (trigger.trigger_type === 'webhook') {
        summary.push("Webhook trigger");
      }
      if (trigger.trigger_type === 'manual') {
        summary.push("Manual execution");
      }

      return summary.length > 0 ? summary : ["No trigger configured"];
    };

    const getActionsSummary = (workflow: any) => {
      const actions = workflow.actions || [];
      const summary: string[] = [];

      if (actions.length > 0) {
        actions.forEach((action: any) => {
          if (action.name && action.action_type) {
            summary.push(`${action.name} - ${action.action_type}`);
          } else if (action.action_type) {
            summary.push(`${action.action_type}`);
          }
        });
      }

      return summary.length > 0 ? summary : ["No actions configured"];
    };

    return (
      <>
        {/* Header */}
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <div className="title is-4">
            <span>Automation</span>
            <span className="tag is-warning is-size-7 has-text-weight-bold mx-2">
              PREVIEW
            </span>
          </div>
          <AppLink href={`/workflows/new`} className="button is-small">
            <Plus className="h-4 w-4 mr-2" />
            <span>New Workflow</span>
          </AppLink>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold ${metadata?.SHIPPING_RULES ? "" : "is-disabled"}`}
              onClick={() => {
                if (!metadata?.SHIPPING_RULES) {
                  alert("Shipping rules are not enabled in your API configuration.");
                }
              }}
            >
              <AppLink href="/shipping-rules" shallow={false} prefetch={false}>
                <span>Shipping Rules</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/workflows" shallow={false} prefetch={false}>
                <span>Workflows</span>
              </AppLink>
            </li>
          </ul>
        </div>

        <div className="py-4">
          {!query.isFetched && (
            <div className="flex justify-center py-8">
              <Spinner />
            </div>
          )}

          {query.isFetched && (workflows?.edges || []).length > 0 && (
            <div className="grid gap-4 max-w-2xl">
              {(workflows?.edges || []).map(({ node: workflow }) => (
                <Card key={workflow.id} className="border border-slate-200 hover:border-slate-300 transition-colors rounded-md shadow-none h-[280px]">
                  <CardContent className="p-4 h-full flex flex-col">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-3 mb-3">
                          <div className="flex-1 min-w-0">
                            <h3 className="text-lg font-semibold text-slate-900 truncate">{workflow.name}</h3>
                            {workflow.description && (
                              <p className="text-base text-slate-600 mt-1 line-clamp-2">{workflow.description}</p>
                            )}
                          </div>
                          <div className="flex items-center gap-2 flex-shrink-0">
                            <Badge variant="outline" className="text-xs">
                              {workflow.action_nodes?.length || 0} action{(workflow.action_nodes?.length || 0) !== 1 ? 's' : ''}
                            </Badge>
                          </div>
                        </div>
                      </div>

                      <div className="ml-4 flex-shrink-0">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="h-9 w-9 p-0">
                              <MoreHorizontal className="h-5 w-5" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem asChild>
                              <AppLink href={`/workflows/${workflow.id}`} className="flex items-center w-full">
                                <Edit className="h-4 w-4 mr-2" />
                                Edit
                              </AppLink>
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                              onClick={() => handleDelete(workflow.id)}
                              disabled={deletingId === workflow.id}
                              className="text-destructive"
                            >
                              <Trash2 className="h-4 w-4 mr-2" />
                              {deletingId === workflow.id ? "Deleting..." : "Delete"}
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1 overflow-hidden">
                      <div className="flex flex-col min-h-0">
                        <h4 className="text-base font-medium text-slate-700 mb-2">Trigger</h4>
                        <div className="space-y-1 overflow-y-auto flex-1">
                          {getTriggerSummary(workflow).map((trigger, index) => (
                            <div key={index} className="text-slate-600 text-sm flex items-center">
                              <span className="w-1 h-1 bg-slate-400 rounded-full mr-2 flex-shrink-0"></span>
                              <span className="break-words">{trigger}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="flex flex-col min-h-0">
                        <h4 className="text-base font-medium text-slate-700 mb-2">Actions</h4>
                        <div className="space-y-1 overflow-y-auto flex-1">
                          {getActionsSummary(workflow).map((action, index) => (
                            <div key={index} className="text-slate-600 text-sm flex items-center">
                              <span className="w-1 h-1 bg-slate-400 rounded-full mr-2 flex-shrink-0"></span>
                              <span className="break-words">{action}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {query.isFetched && (workflows?.edges || []).length === 0 && (
            <Card className="rounded-md shadow-none">
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Settings className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium mb-2">No workflows found</h3>
                <p className="text-muted-foreground text-center mb-4 max-w-md">
                  Automate your business processes by creating workflows that execute actions based on triggers and conditions.
                </p>
                <AppLink href={`/workflows/new`} className="button">
                  <Plus className="h-4 w-4 mr-2" />
                  Create Your First Workflow
                </AppLink>
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
