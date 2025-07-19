"use client";
import { MoreHorizontal, Plus, Settings, Trash2, Edit, Play, Info, Clock, Link, Zap } from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@karrio/ui/components/ui/alert-dialog";
import { useWorkflows, useWorkflowMutation } from "@karrio/hooks/workflows";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/core/components";
import { useState } from "react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@karrio/ui/components/ui/dropdown-menu";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";

import { Dialog, DialogContent, DialogTitle } from "@karrio/ui/components/ui/dialog";
import { WorkflowEditor } from "@karrio/core/components/workflow-editor";
import { WorkflowTemplatePicker } from "@karrio/core/components/workflow-template-picker";

const ContextProviders = bundleContexts([]);

export default function Page(pageProps: any) {
  const Component = (): JSX.Element => {
    const { metadata } = useAPIMetadata();
    const [deletingId, setDeletingId] = useState<string | null>(null);
    const [editingId, setEditingId] = useState<string | null>(null);
    const [isCreating, setIsCreating] = useState(false);
    const [selectedTemplate, setSelectedTemplate] = useState<any>(null);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [workflowToDelete, setWorkflowToDelete] = useState<{ id: string; name: string } | null>(null);
    const mutation = useWorkflowMutation();
    const {
      query: { data: { workflows } = {}, ...query },
    } = useWorkflows();



    const handleDeleteClick = (id: string, name: string) => {
      setWorkflowToDelete({ id, name });
      setDeleteDialogOpen(true);
    };

    const handleDeleteConfirm = async () => {
      if (workflowToDelete) {
        setDeletingId(workflowToDelete.id);
        try {
          await mutation.deleteWorkflow.mutateAsync({ id: workflowToDelete.id });
        } catch (error) {
          console.error("Failed to delete workflow:", error);
        } finally {
          setDeletingId(null);
          setWorkflowToDelete(null);
          setDeleteDialogOpen(false);
        }
      }
    };

    const handleFormSave = () => {
      query.refetch();
      setIsCreating(false);
      setSelectedTemplate(null);
    };

    const getTriggerSummary = (workflow: any) => {
      const trigger = workflow.trigger;
      const summary: string[] = [];

      if (!trigger || !trigger.trigger_type) {
        return ["No trigger configured"];
      }

      switch (trigger.trigger_type) {
        case 'scheduled':
          summary.push("Scheduled");
          if (trigger.schedule) {
            summary.push(`Schedule: ${trigger.schedule}`);
          }
          if (trigger.next_run_description) {
            summary.push(`Next: ${trigger.next_run_description}`);
          }
          break;
        case 'webhook':
          summary.push("Webhook");
          if (trigger.secret) {
            summary.push("Secret configured");
          }
          break;
        case 'manual':
          summary.push("Manual");
          break;
        default:
          summary.push("Unknown trigger type");
      }

      return summary;
    };

    const getActionsSummary = (workflow: any) => {
      const actions = workflow.actions || [];
      const summary: string[] = [];

      if (actions.length > 0) {
        actions.forEach((action: any, index: number) => {
          if (action.name) {
            summary.push(`${index + 1}. ${action.name}`);
          } else if (action.action_type) {
            summary.push(`${index + 1}. ${action.action_type.replace('_', ' ')}`);
          } else {
            summary.push(`${index + 1}. Unnamed action`);
          }
        });
      }

      return summary.length > 0 ? summary : ["No actions configured"];
    };

    const handleTriggerWorkflow = async (triggerId: string) => {
      try {
        await mutation.triggerScheduledWorkflow.mutateAsync(triggerId);
        query.refetch();
      } catch (error) {
        console.error("Failed to trigger workflow:", error);
      }
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
          <WorkflowTemplatePicker
            onSelectTemplate={(template) => {
              setSelectedTemplate(template);
              setIsCreating(true);
            }}
          >
            <Button size="sm">
              <Plus className="h-4 w-4 mr-2" />
              New Workflow
            </Button>
          </WorkflowTemplatePicker>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold ${metadata?.WORKFLOW_MANAGEMENT ? "" : "is-disabled"}`}
              onClick={() => {
                if (!metadata?.WORKFLOW_MANAGEMENT) {
                  alert("Workflow management is not enabled in your API configuration.");
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
          {/* Workflow Info Banner */}
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex flex-col sm:flex-row items-start gap-3">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Info className="h-4 w-4 text-blue-600" />
              </div>
              <div className="space-y-2 flex-1">
                <h3 className="text-sm font-semibold text-blue-900">Getting Started with Workflows</h3>
                <p className="text-sm text-blue-700">
                  Workflows automate business processes by combining triggers (when to run) with actions (what to do).
                  Start with a template or create from scratch.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-3">
                  <div className="flex items-start gap-2">
                    <Clock className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-xs font-medium text-blue-800">Scheduled</p>
                      <p className="text-xs text-blue-600">Run automatically on a schedule</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-2">
                    <Link className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-xs font-medium text-green-800">Webhook</p>
                      <p className="text-xs text-green-600">Triggered by external systems</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-2">
                    <Zap className="h-4 w-4 text-purple-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-xs font-medium text-purple-800">Manual</p>
                      <p className="text-xs text-purple-600">Run on-demand with a button</p>
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

          {query.isFetched && (workflows?.edges || []).length > 0 && (
            <div className="grid gap-4 w-full max-w-none lg:max-w-4xl">
              {(workflows?.edges || []).map(({ node: workflow }) => (
                <Card key={workflow.id} className="border border-slate-200 hover:border-slate-300 transition-colors rounded-lg shadow-sm hover:shadow-md">
                  <CardContent className="p-4">
                    <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="mb-4">
                          <div className="flex flex-col sm:flex-row sm:items-start justify-between mb-2 gap-2">
                            <div className="flex-1">
                              <h3 className="text-lg font-semibold text-slate-900 mb-1">{workflow.name}</h3>
                              {workflow.description && (
                                <p className="text-sm text-slate-600">{workflow.description}</p>
                              )}
                            </div>
                            <div className="flex items-center gap-2">
                              {workflow.trigger?.is_due && (
                                <Badge variant="default" className="text-xs bg-green-100 text-green-800 border-green-200">
                                  Due
                                </Badge>
                              )}
                            </div>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                          <div>
                            <h4 className="text-sm font-medium text-slate-700 mb-3 flex items-center">
                              <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                              Trigger
                            </h4>
                            <div className="space-y-2 pl-4">
                              {getTriggerSummary(workflow).map((trigger, index) => (
                                <div key={index} className="text-sm text-slate-600">
                                  {trigger}
                                </div>
                              ))}
                            </div>
                          </div>

                          <div>
                            <h4 className="text-sm font-medium text-slate-700 mb-3 flex items-center">
                              <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                              Actions
                              <Badge variant="outline" className="text-xs ml-2">
                                {workflow.actions?.length || 0}
                              </Badge>
                            </h4>
                            <div className="space-y-2 pl-4">
                              {getActionsSummary(workflow).slice(0, 3).map((action, index) => (
                                <div key={index} className="text-sm text-slate-600 break-words">
                                  {action}
                                </div>
                              ))}
                              {(workflow.actions?.length || 0) > 3 && (
                                <div className="text-xs text-slate-500 italic">
                                  +{(workflow.actions?.length || 0) - 3} more actions...
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="lg:ml-6 flex justify-end lg:justify-start">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" className="w-40">
                            <DropdownMenuItem onClick={() => setEditingId(workflow.id)}>
                              <Edit className="h-4 w-4 mr-2" />
                              Edit
                            </DropdownMenuItem>
                            {workflow.trigger?.id && (
                              <DropdownMenuItem onClick={() => handleTriggerWorkflow(workflow.trigger!.id)}>
                                <Play className="h-4 w-4 mr-2" />
                                Trigger Now
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                              onClick={() => handleDeleteClick(workflow.id, workflow.name)}
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
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {query.isFetched && (workflows?.edges || []).length === 0 && (
            <Card className="rounded-lg shadow-sm">
              <CardContent className="flex flex-col items-center justify-center py-16 px-4">
                <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-6">
                  <Settings className="h-8 w-8 text-slate-500" />
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2 text-center">No workflows found</h3>
                <p className="text-slate-600 text-center mb-6 max-w-md">
                  Automate your business processes by creating workflows that execute actions based on triggers.
                </p>
                <WorkflowTemplatePicker
                  onSelectTemplate={(template) => {
                    setSelectedTemplate(template);
                    setIsCreating(true);
                  }}
                >
                  <Button size="lg" className="bg-blue-600 hover:bg-blue-700 w-full sm:w-auto">
                    <Plus className="h-4 w-4 mr-2" />
                    Create Your First Workflow
                  </Button>
                </WorkflowTemplatePicker>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Delete Confirmation Dialog */}
        <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Delete Workflow</AlertDialogTitle>
              <AlertDialogDescription>
                Are you sure you want to delete "{workflowToDelete?.name}"? This action cannot be undone.
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

        {/* Editor Dialog */}
        <Dialog open={isCreating || !!editingId} onOpenChange={(open) => {
          if (!open) {
            setIsCreating(false);
            setEditingId(null);
            setSelectedTemplate(null);
          }
        }}>
          <DialogContent className="max-w-none w-screen h-screen m-0">
            <DialogTitle className="sr-only">
              {isCreating ? "Create Workflow" : "Edit Workflow"}
            </DialogTitle>
            <WorkflowEditor
              workflowId={editingId || "new"}
              templateSlug={isCreating ? selectedTemplate?.slug : undefined}
              onClose={() => {
                setIsCreating(false);
                setEditingId(null);
                setSelectedTemplate(null);
              }}
              onSave={handleFormSave}
            />
          </DialogContent>
        </Dialog>
      </>
    );
  };

  return (
    <ContextProviders>
      <Component />
    </ContextProviders>
  );
}
