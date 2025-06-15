"use client";
import React, { useState } from "react";
import { useWorkflowForm } from "@karrio/hooks/workflows";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import { Separator } from "@karrio/ui/components/ui/separator";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@karrio/ui/components/ui/collapsible";
import { ChevronDown, X, Save, ArrowDown, Edit, Trash2, Plus, Play, Copy, Clock, Link, Zap, HelpCircle, Info, CheckCircle, XCircle, AlertCircle, Loader } from "lucide-react";
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
import { AutomationTriggerType, AutomationEventStatus, AutomationActionType, AutomationAuthType } from "@karrio/types/graphql/ee";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { NotificationType } from "@karrio/types";
import { ActionModalEditor } from "./workflow-action-editor";
import { ConnectionModalEditor } from "./workflow-connection-editor";
import { ActionTemplatePicker } from "./action-template-picker";
import { ConnectionTemplatePicker } from "./connection-template-picker";

import { CopiableLink } from "@karrio/ui/core/components/copiable-link";
import { WorkflowActionType } from "@karrio/hooks/workflow-actions";
import { parseWorkflowEventRecordData } from "../modules/Workflows/event";
import { WorkflowEventList } from "../modules/Workflows/events";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { isEqual, isNone, isNoneOrEmpty, url$ } from "@karrio/lib";
import { useLoader } from "@karrio/ui/core/components/loader";
import CodeMirror from "@uiw/react-codemirror";
import { jsonLanguage } from "@codemirror/lang-json";
import { htmlLanguage } from "@codemirror/lang-html";
import hljs from "highlight.js";
import django from "highlight.js/lib/languages/django";
import json from "highlight.js/lib/languages/json";
import moment from "moment";

// Register syntax highlighting languages
hljs.registerLanguage("django", django);
hljs.registerLanguage("json", json);

interface WorkflowEditorProps {
  workflowId: string;
  templateSlug?: string;
  onClose: () => void;
  onSave: () => void;
}

export function WorkflowEditor({ workflowId, templateSlug, onClose, onSave }: WorkflowEditorProps) {
  const loader = useLoader();
  const notifier = useNotifier();
  const { references } = useAPIMetadata();
  const [selectedTab, setSelectedTab] = useState("editor");

  // Confirmation dialog states
  const [deleteActionDialogOpen, setDeleteActionDialogOpen] = useState(false);
  const [deleteConnectionDialogOpen, setDeleteConnectionDialogOpen] = useState(false);
  const [actionToDelete, setActionToDelete] = useState<{ index: number; id?: string } | null>(null);
  const [connectionToDelete, setConnectionToDelete] = useState<{ index: number; actionId?: string; connectionId?: string } | null>(null);
  const {
    workflow,
    current,
    isNew,
    DEFAULT_STATE,
    query,
    zipActionWithNode,
    debug_event,
    ...mutation
  } = useWorkflowForm({ id: workflowId, templateSlug });

  const handleChange = async (changes: Partial<typeof workflow>) => {
    if (changes === undefined) return;
    // For new workflows or immediate UI updates, update local state directly
    await mutation.updateWorkflow(changes, { forcelocalUpdate: true });
  };

  const handleSave = async () => {
    // Basic validation before saving
    if (!workflow.name?.trim()) {
      notifier.notify({
        type: "error" as NotificationType,
        message: "Workflow name is required"
      });
      return;
    }

    try {
      await mutation.save();
      onSave();
    } catch (error) {
      console.error("Save error:", error);
    }
  };

  const handleRunWorkflow = async () => {
    await mutation.runWorkflow();
  };

  // Confirmation handlers
  const handleDeleteActionClick = (index: number, actionId?: string | null) => {
    setActionToDelete({ index, id: actionId || undefined });
    setDeleteActionDialogOpen(true);
  };

  const handleDeleteActionConfirm = async () => {
    if (actionToDelete) {
      await mutation.deleteAction(actionToDelete.index, actionToDelete.id)();
      setActionToDelete(null);
      setDeleteActionDialogOpen(false);
    }
  };

  const handleDeleteConnectionClick = (index: number, actionId?: string | null, connectionId?: string | null) => {
    setConnectionToDelete({ index, actionId: actionId || undefined, connectionId: connectionId || undefined });
    setDeleteConnectionDialogOpen(true);
  };

  const handleDeleteConnectionConfirm = async () => {
    if (connectionToDelete) {
      await mutation.deleteActionConnection(
        connectionToDelete.index,
        connectionToDelete.actionId,
        connectionToDelete.connectionId,
      )();
      setConnectionToDelete(null);
      setDeleteConnectionDialogOpen(false);
    }
  };

  const NextIndicator = () => (
    <div className="flex justify-center py-4">
      <ArrowDown className="h-5 w-5 text-slate-400" />
    </div>
  );

  const TriggerIcon = ({ type }: { type: string }) => {
    switch (type) {
      case AutomationTriggerType.scheduled:
        return <Clock className="h-5 w-5" />;
      case AutomationTriggerType.webhook:
        return <Link className="h-5 w-5" />;
      case AutomationTriggerType.manual:
        return <Zap className="h-5 w-5" />;
      default:
        return <Zap className="h-5 w-5" />;
    }
  };

  // Helper functions to determine action status from debug_event
  const getActionStatus = (action: any) => {
    if (!debug_event?.records) return null;

    const actionRecords = debug_event.records.filter(
      record => record.meta.workflow_action_slug === action.slug || record.meta.workflow_action_id === action.id
    );

    if (actionRecords.length === 0) return null;

    // Check for output records to determine final status
    const outputRecord = actionRecords.find(record => record.key === "action-output");
    if (outputRecord) {
      const status = outputRecord.record?.status;
      return status === "success" ? "success" : status === "failed" ? "failed" : "completed";
    }

    // Check if action has input but no output (running)
    const inputRecord = actionRecords.find(record => record.key === "action-input");
    if (inputRecord && !outputRecord) {
      return "running";
    }

    return null;
  };

  const getActionStatusIcon = (status: string | null) => {
    switch (status) {
      case "success":
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case "failed":
        return <XCircle className="h-4 w-4 text-red-600" />;
      case "running":
        return <Loader className="h-4 w-4 text-blue-600 animate-spin" />;
      case "completed":
        return <CheckCircle className="h-4 w-4 text-blue-600" />;
      default:
        return null;
    }
  };

  const getActionStatusBadge = (status: string | null) => {
    if (!status) return null;

    const badgeStyles = {
      success: "bg-green-100 text-green-800 border-green-200",
      failed: "bg-red-100 text-red-800 border-red-200",
      running: "bg-blue-100 text-blue-800 border-blue-200",
      completed: "bg-blue-100 text-blue-800 border-blue-200"
    };

    return (
      <Badge className={`${badgeStyles[status]} text-xs font-medium`}>
        {status}
      </Badge>
    );
  };

  return (
    <div className="tailwind-only h-screen flex flex-col bg-slate-50 overflow-hidden">
      {/* Sticky Header */}
      <header className="bg-white border-b border-slate-200 px-3 lg:px-4 py-3 flex items-center justify-between sticky top-0 z-10 shadow-sm flex-shrink-0">
        <div className="flex items-center gap-2 lg:gap-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="h-8 w-8 lg:h-10 lg:w-10 rounded-md p-0 hover:bg-slate-100"
          >
            <X className="h-4 w-4 lg:h-5 lg:w-5" />
          </Button>
          <Separator orientation="vertical" className="h-4 lg:h-6" />
          <div>
            <h1 className="text-base lg:text-lg font-semibold text-slate-900">
              {isNew ? "Create workflow" : "Edit workflow"}
            </h1>
          </div>
        </div>
        <div className="flex items-center gap-2 lg:gap-3">
          <Button
            onClick={handleRunWorkflow}
            disabled={[AutomationEventStatus.running, AutomationEventStatus.pending].includes(
              debug_event?.status as any
            )}
            variant="outline"
            size="sm"
            className="flex items-center gap-1 lg:gap-2 h-8 lg:h-10 px-2 lg:px-4 text-xs lg:text-sm"
          >
            <Play className="h-3 w-3 lg:h-4 lg:w-4" />
            <span className="hidden sm:inline">Execute workflow</span>
            <span className="sm:hidden">Execute</span>
          </Button>
          <Button
            onClick={handleSave}
            disabled={loader.loading || isEqual(workflow, current || DEFAULT_STATE)}
            className="flex items-center gap-1 lg:gap-2 h-8 lg:h-10 px-2 lg:px-4 text-xs lg:text-sm"
            size="sm"
          >
            <Save className="h-3 w-3 lg:h-4 lg:w-4" />
            <span className="hidden sm:inline">Save</span>
            <span className="sm:hidden">Save</span>
          </Button>
        </div>
      </header>

      {/* Tab Navigation */}
      <Tabs value={selectedTab} onValueChange={setSelectedTab} className="flex-1 flex flex-col overflow-hidden">
        <div className="bg-white border-b border-slate-200 flex-shrink-0">
          <TabsList className="bg-transparent h-auto p-0 mx-3 lg:mx-4">
            <TabsTrigger
              value="editor"
              className="px-3 lg:px-4 py-3 data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-blue-500 rounded-none text-sm"
            >
              Editor
            </TabsTrigger>
            <TabsTrigger
              value="executions"
              className="px-3 lg:px-4 py-3 data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-blue-500 rounded-none text-sm"
            >
              Executions
            </TabsTrigger>
          </TabsList>
        </div>

        <TabsContent value="editor" className="flex-1 m-0 overflow-hidden">
          {query.isFetched && !!workflow.actions && (
            <div className="flex flex-col lg:flex-row h-full overflow-hidden">
              {/* Left Sidebar - Form Fields */}
              <div className="w-full lg:w-80 bg-white border-b lg:border-b-0 lg:border-r border-slate-200 p-4 space-y-4 overflow-y-auto flex-shrink-0 max-h-96 lg:max-h-none">
                {/* Workflow Info Admonition */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
                  <div className="flex items-start gap-2">
                    <Info className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                    <div className="space-y-1">
                      <p className="text-xs font-medium text-blue-900">How Workflows Work</p>
                      <p className="text-xs text-blue-700">
                        Workflows automate tasks by combining triggers (when to run) with actions (what to do).
                        Configure the trigger below, then add actions.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900 mb-4">Basic Information</h3>
                    <div className="space-y-3">
                      <div className="space-y-1">
                        <div className="flex items-center gap-1">
                          <Label htmlFor="name" className="text-sm text-slate-700">
                            Name *
                          </Label>
                          <div className="group relative">
                            <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                            <div className="absolute left-0 bottom-full mb-1 w-48 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                              Give your workflow a clear, descriptive name like "Order Fulfillment" or "Inventory Sync"
                            </div>
                          </div>
                        </div>
                        <Input
                          id="name"
                          value={workflow.name || ""}
                          onChange={(e) => handleChange({ name: e.target.value })}
                          placeholder="ERP orders sync"
                          className="h-9"
                          required
                        />
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center gap-1">
                          <Label htmlFor="description" className="text-sm text-slate-700">
                            Description
                          </Label>
                          <div className="group relative">
                            <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                            <div className="absolute left-0 bottom-full mb-1 w-48 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                              Explain what this workflow accomplishes and when it should be used
                            </div>
                          </div>
                        </div>
                        <Textarea
                          id="description"
                          value={workflow.description || ""}
                          onChange={(e) => handleChange({ description: e.target.value })}
                          placeholder="Automate ERP orders syncing for fulfillment"
                          className="min-h-[100px] text-sm"
                          rows={4}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Canvas - Workflow Visualization */}
              <div className="flex-1 flex flex-col bg-slate-50 overflow-hidden">
                <div className="flex-1 overflow-y-auto">
                  <div className="max-w-4xl mx-auto p-4 lg:p-6 space-y-6 pb-8 min-h-full">

                    {/* Trigger Section */}
                    <Collapsible defaultOpen className="w-full">
                      <Card className="border-slate-200 rounded-lg shadow-sm">
                        <CollapsibleTrigger asChild>
                          <CardHeader className="cursor-pointer hover:bg-slate-50 transition-colors p-3 lg:p-4">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-3">
                                <TriggerIcon type={workflow.trigger?.trigger_type || ""} />
                                <div>
                                  <CardTitle className="text-base font-semibold">Trigger</CardTitle>
                                  <p className="text-sm text-slate-600 mt-1">
                                    How the workflow is triggered
                                  </p>
                                </div>
                              </div>
                              <ChevronDown className="h-5 w-5 text-slate-400" />
                            </div>
                          </CardHeader>
                        </CollapsibleTrigger>
                        <CollapsibleContent>
                          <CardContent className="pt-0 p-3 lg:p-4 space-y-4">
                            <Separator />

                            {/* Trigger Type Selection */}
                            <div className="space-y-2">
                              <div className="flex items-center gap-1">
                                <Label className="text-sm text-slate-700">
                                  Trigger Type *
                                </Label>
                                <div className="group relative">
                                  <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                                  <div className="absolute left-0 bottom-full mb-1 w-56 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                                    <div className="space-y-1">
                                      <p><strong>Manual:</strong> Run by clicking a button</p>
                                      <p><strong>Scheduled:</strong> Run automatically on a schedule</p>
                                      <p><strong>Webhook:</strong> Run when called by external systems</p>
                                    </div>
                                  </div>
                                </div>
                              </div>
                              <select
                                value={workflow.trigger?.trigger_type || ""}
                                onChange={(e) =>
                                  handleChange({
                                    trigger: {
                                      ...workflow.trigger,
                                      trigger_type: e.target.value as AutomationTriggerType,
                                    },
                                  })
                                }
                                className="w-full mt-1 px-3 py-2 border border-slate-300 rounded-md bg-white h-10 text-sm"
                              >
                                <option value={AutomationTriggerType.manual}>Manual</option>
                                <option value={AutomationTriggerType.scheduled}>Scheduled</option>
                                <option value={AutomationTriggerType.webhook}>Webhook</option>
                              </select>
                            </div>

                            {/* Conditional Fields Based on Trigger Type */}
                            {workflow.trigger?.trigger_type === AutomationTriggerType.scheduled && (
                              <div className="space-y-2">
                                <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 mb-3">
                                  <div className="flex items-start gap-2">
                                    <Clock className="h-4 w-4 text-amber-600 mt-0.5 flex-shrink-0" />
                                    <div className="space-y-1">
                                      <p className="text-xs font-medium text-amber-900">Cron Expression Format</p>
                                      <p className="text-xs text-amber-700">
                                        Format: minute hour day month weekday
                                      </p>
                                      <p className="text-xs text-amber-700">
                                        Common examples:
                                        <br />• "0 9 * * 1-5" = 9 AM weekdays
                                        <br />• "0 */2 * * *" = Every 2 hours
                                        <br />• "0 0 1 * *" = 1st of each month
                                      </p>
                                    </div>
                                  </div>
                                </div>
                                <div className="flex items-center gap-1">
                                  <Label className="text-sm text-slate-700">
                                    Schedule (Cron Expression) *
                                  </Label>
                                  <div className="group relative">
                                    <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                                    <div className="absolute left-0 bottom-full mb-1 w-56 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                                      Use cron syntax to specify when the workflow runs. The format is: minute hour day month weekday
                                    </div>
                                  </div>
                                </div>
                                <Input
                                  value={workflow.trigger?.schedule || ""}
                                  onChange={(e) =>
                                    handleChange({
                                      trigger: {
                                        ...workflow.trigger,
                                        schedule: e.target.value,
                                      },
                                    })
                                  }
                                  placeholder="0 9 * * 1-5"
                                  className="font-mono h-9"
                                />
                              </div>
                            )}

                            {workflow.trigger?.trigger_type === AutomationTriggerType.webhook && (
                              <div className="space-y-4">
                                <div className="bg-green-50 border border-green-200 rounded-lg p-3 mb-3">
                                  <div className="flex items-start gap-2">
                                    <Link className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                                    <div className="space-y-1">
                                      <p className="text-xs font-medium text-green-900">Webhook Security</p>
                                      <p className="text-xs text-green-700">
                                        Add a secret to verify webhook authenticity. The secret will be compared against the specified header from incoming requests.
                                      </p>
                                    </div>
                                  </div>
                                </div>
                                <div className="space-y-2">
                                  <div className="flex items-center gap-1">
                                    <Label className="text-sm text-slate-700">
                                      Webhook Secret (Optional)
                                    </Label>
                                    <div className="group relative">
                                      <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                                      <div className="absolute left-0 bottom-full mb-1 w-56 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                                        A secret value that must match the header value in incoming webhook requests for security
                                      </div>
                                    </div>
                                  </div>
                                  <Input
                                    value={workflow.trigger?.secret || ""}
                                    onChange={(e) =>
                                      handleChange({
                                        trigger: {
                                          ...workflow.trigger,
                                          secret: e.target.value,
                                        },
                                      })
                                    }
                                    placeholder="your-secret-key"
                                    className="h-9"
                                  />
                                </div>
                                <div className="space-y-2">
                                  <div className="flex items-center gap-1">
                                    <Label className="text-sm text-slate-700">
                                      Secret Key Header (Optional)
                                    </Label>
                                    <div className="group relative">
                                      <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                                      <div className="absolute left-0 bottom-full mb-1 w-56 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                                        The HTTP header name where the secret will be sent (e.g., "X-Webhook-Secret", "Authorization")
                                      </div>
                                    </div>
                                  </div>
                                  <Input
                                    value={workflow.trigger?.secret_key || ""}
                                    onChange={(e) =>
                                      handleChange({
                                        trigger: {
                                          ...workflow.trigger,
                                          secret_key: e.target.value,
                                        },
                                      })
                                    }
                                    placeholder="X-Webhook-Secret"
                                    className="h-9"
                                  />
                                </div>
                              </div>
                            )}

                            {/* Webhook URL Display */}
                            <div className="space-y-2">
                              <div className="flex items-center gap-1">
                                <Label className="text-sm text-slate-700">
                                  Webhook URL
                                </Label>
                                <div className="group relative">
                                  <HelpCircle className="h-3 w-3 text-slate-400 cursor-help" />
                                  <div className="absolute left-0 bottom-full mb-1 w-56 bg-slate-900 text-white text-xs rounded p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity z-50">
                                    Use this URL to trigger the workflow from external systems. Available after saving the workflow.
                                  </div>
                                </div>
                              </div>
                              <div className="relative">
                                <Input
                                  value={
                                    !!workflow.id && workflow.id !== "new"
                                      ? url$`${references.HOST}/v1/workflows/${workflow.id}/trigger`
                                      : ""
                                  }
                                  readOnly
                                  className="pr-16 bg-slate-50 h-9"
                                />
                                <CopiableLink
                                  text="COPY"
                                  value={
                                    !!workflow.id && workflow.id !== "new"
                                      ? url$`${references.HOST}/v1/workflows/${workflow.id}/trigger`
                                      : ""
                                  }
                                  className="absolute right-2 top-1/2 transform -translate-y-1/2 text-xs hover:bg-slate-100 rounded px-2 py-1"
                                />
                              </div>
                            </div>
                          </CardContent>
                        </CollapsibleContent>
                      </Card>
                    </Collapsible>

                    <NextIndicator />

                    {/* Actions Section */}
                    {zipActionWithNode(
                      workflow.actions as WorkflowActionType[],
                      workflow.action_nodes as any[],
                    ).map(([action, node], index) => (
                      <React.Fragment key={index}>
                        <Collapsible className="w-full">
                          <Card className="border-slate-200 rounded-lg shadow-sm">
                            <CollapsibleTrigger asChild>
                              <CardHeader className="cursor-pointer hover:bg-slate-50 transition-colors p-3 lg:p-4">
                                <div className="flex items-center justify-between">
                                  <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-sm font-medium">
                                      {index + 1}
                                    </div>
                                    <div className="flex-1 min-w-0">
                                      <div className="flex items-center gap-2">
                                        <CardTitle className="text-base font-semibold">Action</CardTitle>
                                        {getActionStatusIcon(getActionStatus(action))}
                                        {getActionStatusBadge(getActionStatus(action))}
                                      </div>
                                      <p className="text-sm text-slate-600 mt-1 truncate">
                                        {action.name || "An action to perform"}
                                      </p>
                                    </div>
                                  </div>
                                  <div className="flex items-center gap-1 lg:gap-2 flex-shrink-0">
                                    <ActionModalEditor
                                      action={action}
                                      onSubmit={mutation.updateAction(index, action?.id)}
                                      trigger={
                                        <Button variant="ghost" size="sm" className="h-8 w-8 lg:h-9 lg:w-9 p-0 hover:bg-slate-100">
                                          <Edit className="h-3 w-3 lg:h-4 lg:w-4" />
                                        </Button>
                                      }
                                    />
                                    <AlertDialog>
                                      <AlertDialogTrigger asChild>
                                        <Button
                                          variant="ghost"
                                          size="sm"
                                          disabled={index === 0}
                                          className="text-red-600 hover:text-red-700 hover:bg-red-50 h-8 w-8 lg:h-9 lg:w-9 p-0"
                                          onClick={() => handleDeleteActionClick(index, action?.id)}
                                        >
                                          <Trash2 className="h-3 w-3 lg:h-4 lg:w-4" />
                                        </Button>
                                      </AlertDialogTrigger>
                                      <AlertDialogContent>
                                        <AlertDialogHeader>
                                          <AlertDialogTitle>Delete Action</AlertDialogTitle>
                                          <AlertDialogDescription>
                                            Are you sure you want to delete this action? This action cannot be undone.
                                          </AlertDialogDescription>
                                        </AlertDialogHeader>
                                        <AlertDialogFooter className="flex justify-end gap-3">
                                          <AlertDialogCancel>Cancel</AlertDialogCancel>
                                          <AlertDialogAction
                                            onClick={handleDeleteActionConfirm}
                                            className="bg-red-600 hover:bg-red-700"
                                          >
                                            Delete
                                          </AlertDialogAction>
                                        </AlertDialogFooter>
                                      </AlertDialogContent>
                                    </AlertDialog>
                                    <ChevronDown className="h-4 w-4 text-slate-400" />
                                  </div>
                                </div>
                              </CardHeader>
                            </CollapsibleTrigger>
                            <CollapsibleContent>
                              <CardContent className="pt-0 p-3 lg:p-4">
                                <Separator className="mb-4" />

                                {/* Action Detail Tabs */}
                                <Tabs defaultValue="template" className="w-full">
                                  <TabsList className="grid w-full grid-cols-2 lg:grid-cols-4 h-9">
                                    <TabsTrigger value="template" className="text-xs lg:text-sm">Template</TabsTrigger>
                                    <TabsTrigger value="inputs" className="text-xs lg:text-sm">Inputs</TabsTrigger>
                                    <TabsTrigger value="outputs" className="text-xs lg:text-sm">Outputs</TabsTrigger>
                                    <TabsTrigger value="details" className="text-xs lg:text-sm">Details</TabsTrigger>
                                  </TabsList>

                                  <TabsContent value="template" className="mt-3">
                                    <div className="border rounded-lg overflow-hidden">
                                      <CodeMirror
                                        height="300px"
                                        extensions={[htmlLanguage]}
                                        value={action.parameters_template || ""}
                                        onChange={(value) =>
                                          mutation.updateAction(index, action?.id)({
                                            parameters_template: value
                                          })
                                        }
                                      />
                                    </div>
                                  </TabsContent>

                                  <TabsContent value="inputs" className="mt-3">
                                    {(debug_event?.records || []).filter(
                                      (_) =>
                                        _.meta.workflow_action_slug === action.slug &&
                                        _.key === "action-input",
                                    ).length === 0 ? (
                                      <div className="bg-slate-50 border rounded-lg p-6 text-center">
                                        <p className="text-slate-600 text-sm">No input data sample...</p>
                                      </div>
                                    ) : (
                                      <div className="space-y-3">
                                        {debug_event!.records
                                          .filter(
                                            (_) =>
                                              _.meta.workflow_action_slug === action.slug &&
                                              _.key === "action-input",
                                          )
                                          .map((trace) => (
                                            <div key={trace.id} className="border rounded-lg overflow-hidden">
                                              <CodeMirror
                                                height="300px"
                                                extensions={[jsonLanguage]}
                                                value={
                                                  parseWorkflowEventRecordData(
                                                    trace.record.output || trace.record,
                                                  ) || "{}"
                                                }
                                                readOnly={true}
                                              />
                                            </div>
                                          ))}
                                      </div>
                                    )}
                                  </TabsContent>

                                  <TabsContent value="outputs" className="mt-3">
                                    {(debug_event?.records || []).filter(
                                      (_) =>
                                        _.meta.workflow_action_slug === action.slug &&
                                        _.key === "action-output",
                                    ).length === 0 ? (
                                      <div className="bg-slate-50 border rounded-lg p-6 text-center">
                                        <p className="text-slate-600 text-sm">No output data sample...</p>
                                      </div>
                                    ) : (
                                      <div className="space-y-3">
                                        {debug_event!.records
                                          .filter(
                                            (_) =>
                                              _.meta.workflow_action_slug === action.slug &&
                                              _.key === "action-output",
                                          )
                                          .map((trace) => (
                                            <div key={trace.id} className="border rounded-lg overflow-hidden">
                                              <CodeMirror
                                                height="300px"
                                                extensions={[jsonLanguage]}
                                                value={
                                                  parseWorkflowEventRecordData(
                                                    trace.record.output || trace.record,
                                                  ) || "{}"
                                                }
                                                readOnly={true}
                                              />
                                            </div>
                                          ))}
                                      </div>
                                    )}
                                  </TabsContent>

                                  <TabsContent value="details" className="mt-3">
                                    <div className="bg-white border rounded-lg p-3 lg:p-5 space-y-5">
                                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
                                        <div className="space-y-4">
                                          <div>
                                            <Label className="text-sm text-slate-700 font-medium">Action Type</Label>
                                            <div className="text-sm mt-1">
                                              <Badge variant="outline">{action.action_type}</Badge>
                                            </div>
                                          </div>
                                          {action.description && (
                                            <div>
                                              <Label className="text-sm text-slate-700 font-medium">Description</Label>
                                              <p className="text-sm text-slate-600 mt-1">{action.description}</p>
                                            </div>
                                          )}
                                        </div>

                                        {action.action_type === AutomationActionType.http_request && (
                                          <div className="space-y-4">
                                            <div>
                                              <Label className="text-sm text-slate-700 font-medium">Method</Label>
                                              <div className="text-sm mt-1">
                                                <Badge variant="outline">{action.method?.toUpperCase()}</Badge>
                                              </div>
                                            </div>
                                            <div>
                                              <Label className="text-sm text-slate-700 font-medium">Host</Label>
                                              <p className="text-sm text-slate-600 mt-1 font-mono">{action.host}</p>
                                            </div>
                                            {!isNone(action.port) && (
                                              <div>
                                                <Label className="text-sm text-slate-700 font-medium">Port</Label>
                                                <p className="text-sm text-slate-600 mt-1">{action.port}</p>
                                              </div>
                                            )}
                                            {!isNoneOrEmpty(action.endpoint) && (
                                              <div>
                                                <Label className="text-sm text-slate-700 font-medium">Endpoint</Label>
                                                <p className="text-sm text-slate-600 mt-1 font-mono">{action.endpoint}</p>
                                              </div>
                                            )}
                                            <div>
                                              <Label className="text-sm text-slate-700 font-medium">Content Type</Label>
                                              <div className="text-sm mt-1">
                                                <Badge variant="outline">{action.content_type}</Badge>
                                              </div>
                                            </div>
                                          </div>
                                        )}

                                        {action.action_type === AutomationActionType.data_mapping && (
                                          <div>
                                            <Label className="text-sm text-slate-700 font-medium">Format</Label>
                                            <div className="text-sm mt-1">
                                              <Badge variant="outline">{action.content_type}</Badge>
                                            </div>
                                          </div>
                                        )}
                                      </div>

                                      {/* Connection Section */}
                                      <div className="border-t pt-5">
                                        <Collapsible className="w-full">
                                          <Card className="border-slate-200 rounded-md shadow-sm">
                                            <CollapsibleTrigger asChild>
                                              <CardHeader className="cursor-pointer hover:bg-slate-50 transition-colors p-3 lg:p-4">
                                                <div className="flex items-center justify-between">
                                                  <div className="flex items-center gap-3">
                                                    <div className="flex-1 min-w-0">
                                                      <CardTitle className="text-base font-semibold">Connection</CardTitle>
                                                      <p className="text-sm text-slate-600 mt-1 truncate">
                                                        {action.connection?.name || "A connection for the action"}
                                                      </p>
                                                    </div>
                                                  </div>
                                                  <div className="flex items-center gap-1 lg:gap-2 flex-shrink-0">
                                                    {action.connection ? (
                                                      <ConnectionModalEditor
                                                        connection={action.connection}
                                                        onSubmit={mutation.updateActionConnection(index, action?.id)}
                                                        trigger={
                                                          <Button variant="ghost" size="sm" className="h-8 w-8 lg:h-9 lg:w-9 p-0 hover:bg-slate-100">
                                                            <Edit className="h-3 w-3 lg:h-4 lg:w-4" />
                                                          </Button>
                                                        }
                                                      />
                                                    ) : (
                                                      <ConnectionTemplatePicker
                                                        onSelectTemplate={(template) => {
                                                          if (template) {
                                                            // Use template to create connection
                                                            mutation.updateActionConnection(index, action?.id)({
                                                              ...template,
                                                              name: template.name || "New Connection",
                                                              id: undefined, // New connection
                                                            });
                                                          } else {
                                                            // Create blank connection
                                                            mutation.updateActionConnection(index, action?.id)({
                                                              auth_type: "basic" as any,
                                                              name: "New Connection",
                                                            });
                                                          }
                                                        }}
                                                      >
                                                        <Button variant="ghost" size="sm" className="h-8 w-8 lg:h-9 lg:w-9 p-0 hover:bg-slate-100">
                                                          <Plus className="h-3 w-3 lg:h-4 lg:w-4" />
                                                        </Button>
                                                      </ConnectionTemplatePicker>
                                                    )}
                                                    <AlertDialog>
                                                      <AlertDialogTrigger asChild>
                                                        <Button
                                                          variant="ghost"
                                                          size="sm"
                                                          disabled={!action.connection}
                                                          className="text-red-600 hover:text-red-700 hover:bg-red-50 h-8 w-8 lg:h-9 lg:w-9 p-0"
                                                          onClick={() => handleDeleteConnectionClick(index, action?.id, action.connection?.id)}
                                                        >
                                                          <Trash2 className="h-3 w-3 lg:h-4 lg:w-4" />
                                                        </Button>
                                                      </AlertDialogTrigger>
                                                      <AlertDialogContent>
                                                        <AlertDialogHeader>
                                                          <AlertDialogTitle>Delete Connection</AlertDialogTitle>
                                                          <AlertDialogDescription>
                                                            Are you sure you want to delete this connection? This action cannot be undone.
                                                          </AlertDialogDescription>
                                                        </AlertDialogHeader>
                                                        <AlertDialogFooter className="flex justify-end gap-3">
                                                          <AlertDialogCancel>Cancel</AlertDialogCancel>
                                                          <AlertDialogAction
                                                            onClick={handleDeleteConnectionConfirm}
                                                            className="bg-red-600 hover:bg-red-700"
                                                          >
                                                            Delete
                                                          </AlertDialogAction>
                                                        </AlertDialogFooter>
                                                      </AlertDialogContent>
                                                    </AlertDialog>
                                                    <ChevronDown className="h-4 w-4 text-slate-400" />
                                                  </div>
                                                </div>
                                              </CardHeader>
                                            </CollapsibleTrigger>
                                            <CollapsibleContent>
                                              <CardContent className="pt-0 p-3 lg:p-4">
                                                <Separator className="mb-4" />

                                                {!action.connection ? (
                                                  <div className="bg-amber-50 border border-amber-200 rounded-md p-4 text-center">
                                                    <p className="text-sm text-amber-800 font-medium">
                                                      No connection defined
                                                    </p>
                                                    <p className="text-sm text-amber-700 mt-1">
                                                      Add a connection to authenticate this action
                                                    </p>
                                                  </div>
                                                ) : (
                                                  <div className="space-y-4">
                                                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                                      <div>
                                                        <Label className="text-sm text-slate-700 font-medium">Auth Type</Label>
                                                        <div className="text-sm mt-1">
                                                          <Badge variant="outline">{action.connection.auth_type}</Badge>
                                                        </div>
                                                      </div>
                                                      {action.connection.description && (
                                                        <div>
                                                          <Label className="text-sm text-slate-700 font-medium">Description</Label>
                                                          <p className="text-sm text-slate-600 mt-1">{action.connection.description}</p>
                                                        </div>
                                                      )}
                                                    </div>

                                                    {[AutomationAuthType.oauth2, AutomationAuthType.jwt].includes(
                                                      action.connection.auth_type as any,
                                                    ) && (
                                                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                                          <div>
                                                            <Label className="text-sm text-slate-700 font-medium">Host</Label>
                                                            <p className="text-sm text-slate-600 mt-1 font-mono break-all">{action.connection.host}</p>
                                                          </div>
                                                          {!isNone(action.connection.port) && (
                                                            <div>
                                                              <Label className="text-sm text-slate-700 font-medium">Port</Label>
                                                              <p className="text-sm text-slate-600 mt-1">{action.connection.port}</p>
                                                            </div>
                                                          )}
                                                          {!isNoneOrEmpty(action.connection.endpoint) && (
                                                            <div className="lg:col-span-2">
                                                              <Label className="text-sm text-slate-700 font-medium">Endpoint</Label>
                                                              <p className="text-sm text-slate-600 mt-1 font-mono break-all">{action.connection.endpoint}</p>
                                                            </div>
                                                          )}
                                                        </div>
                                                      )}

                                                    <div>
                                                      <Label className="text-sm text-slate-700 font-medium">Auth Template</Label>
                                                      <div className="bg-slate-50 border rounded mt-2 p-3 max-h-40 overflow-auto">
                                                        <pre className="text-sm">
                                                          <code
                                                            dangerouslySetInnerHTML={{
                                                              __html: hljs.highlight(
                                                                (action.connection.auth_template || "") as string,
                                                                { language: "django" },
                                                              ).value,
                                                            }}
                                                          />
                                                        </pre>
                                                      </div>
                                                    </div>

                                                    {[AutomationAuthType.oauth2, AutomationAuthType.jwt].includes(
                                                      action.connection.auth_type as any,
                                                    ) && (
                                                        <div>
                                                          <Label className="text-sm text-slate-700 font-medium">Parameters Template</Label>
                                                          <div className="bg-slate-50 border rounded mt-2 p-3 max-h-40 overflow-auto">
                                                            <pre className="text-sm">
                                                              <code
                                                                dangerouslySetInnerHTML={{
                                                                  __html: hljs.highlight(
                                                                    (action.connection.parameters_template || "{}") as string,
                                                                    { language: "django" },
                                                                  ).value,
                                                                }}
                                                              />
                                                            </pre>
                                                          </div>
                                                        </div>
                                                      )}
                                                  </div>
                                                )}
                                              </CardContent>
                                            </CollapsibleContent>
                                          </Card>
                                        </Collapsible>
                                      </div>
                                    </div>
                                  </TabsContent>
                                </Tabs>
                              </CardContent>
                            </CollapsibleContent>
                          </Card>
                        </Collapsible>

                        {index < workflow.actions.length - 1 && <NextIndicator />}
                      </React.Fragment>
                    ))}

                    {/* Add Action Button */}
                    <div className="flex justify-center py-4 lg:py-6">
                      <ActionTemplatePicker
                        onSelectTemplate={(template) => {
                          if (template) {
                            // Use template to create action
                            mutation.addAction({
                              ...template,
                              name: template.name || "New Action",
                              slug: undefined, // Let the server generate a new slug
                              id: undefined, // New action
                            });
                          } else {
                            // Create blank action
                            mutation.addAction((DEFAULT_STATE.actions || [])[0] as any);
                          }
                        }}
                      >
                        <Button variant="outline" className="flex items-center gap-2 h-9 lg:h-10 px-3 lg:px-4 text-sm">
                          <Plus className="h-3 w-3 lg:h-4 lg:w-4" />
                          Add action
                        </Button>
                      </ActionTemplatePicker>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </TabsContent>

        <TabsContent value="executions" className="flex-1 m-0">
          {!!workflowId && workflowId !== "new" && (
            <div className="h-full">
              <WorkflowEventList defaultFilter={{ keyword: workflowId }} />
            </div>
          )}
          {(!workflowId || workflowId === "new") && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <p className="text-slate-600 text-sm">Save the workflow first to view executions</p>
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
