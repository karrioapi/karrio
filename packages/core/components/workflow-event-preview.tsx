"use client";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger, SheetClose } from "@karrio/ui/components/ui/sheet";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Button } from "@karrio/ui/components/ui/button";
import { Separator } from "@karrio/ui/components/ui/separator";
import { Label } from "@karrio/ui/components/ui/label";
import { formatDateTimeLong, jsonify, isNone } from "@karrio/lib";
import { useWorkflowEvent } from "@karrio/hooks/workflow-events";
import { Copy, ExternalLink, Clock, Code, Play, Database, AlertCircle, CheckCircle, XCircle, X } from "lucide-react";
import { AutomationEventStatus } from "@karrio/types/graphql/ee";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Spinner } from "@karrio/ui/core/components";
import json from "highlight.js/lib/languages/json";
import hljs from "highlight.js";
import moment from "moment";
import React from "react";

hljs.registerLanguage("json", json);

type WorkflowEventPreviewModalProps = {
  eventId: string;
  trigger: React.ReactElement;
};

export const WorkflowPreviewModal = ({
  eventId,
  trigger,
}: WorkflowEventPreviewModalProps): JSX.Element => {
  const [open, setOpen] = React.useState(false);
  const {
    query: { data: { workflow_event } = {}, ...query },
  } = useWorkflowEvent(eventId);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case AutomationEventStatus.success:
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case AutomationEventStatus.failed:
        return <XCircle className="h-4 w-4 text-red-600" />;
      case AutomationEventStatus.running:
      case AutomationEventStatus.pending:
        return <Play className="h-4 w-4 text-blue-600" />;
      default:
        return <AlertCircle className="h-4 w-4 text-slate-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case AutomationEventStatus.success:
        return "bg-green-100 text-green-800 border-green-200";
      case AutomationEventStatus.failed:
        return "bg-red-100 text-red-800 border-red-200";
      case AutomationEventStatus.running:
        return "bg-blue-100 text-blue-800 border-blue-200";
      case AutomationEventStatus.pending:
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      default:
        return "bg-slate-100 text-slate-800 border-slate-200";
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(typeof text === 'string' ? text : JSON.stringify(text, null, 2));
  };

  const parseWorkflowEventRecordData = (record: any) => {
    try {
      if (typeof record === 'string') return record;
      return JSON.stringify(record, null, 2);
    } catch {
      return String(record);
    }
  };

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        {React.cloneElement(trigger, {
          onClick: () => setOpen(true),
        })}
      </SheetTrigger>
      <SheetContent className="w-[800px] min-w-[800px] sm:max-w-[800px] p-0 shadow-none">
        <div className="h-full flex flex-col">
          <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3 flex-1 min-w-0">
                <div className="flex items-center space-x-2 min-w-0">
                  {getStatusIcon(workflow_event?.status as string)}
                  <SheetTitle className="text-lg font-semibold text-slate-900 truncate">
                    Workflow Event
                  </SheetTitle>
                </div>
                <Badge className={`${getStatusColor(workflow_event?.status as string)} text-xs font-medium flex-shrink-0`}>
                  {workflow_event?.status}
                </Badge>
              </div>
              <div className="flex items-center space-x-2 flex-shrink-0">
                <AppLink
                  href={`/workflows/events/${eventId}`}
                  target="_blank"
                  className="hidden sm:inline-flex"
                >
                  <Button variant="outline" size="sm" className="h-8 text-xs">
                    <ExternalLink className="h-3 w-3 mr-1" />
                    <span className="hidden md:inline">View Full Page</span>
                    <span className="md:hidden">View</span>
                  </Button>
                </AppLink>
                <SheetClose asChild>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-slate-100">
                    <X className="h-4 w-4" />
                    <span className="sr-only">Close</span>
                  </Button>
                </SheetClose>
              </div>
            </div>
            <div className="text-sm text-slate-600 mt-1 pr-10">
              <span className="block truncate">
                {workflow_event?.event_type} trigger of "{workflow_event?.workflow?.name}"
              </span>
            </div>
            {/* Mobile-only view full page link */}
            <div className="sm:hidden mt-2">
              <AppLink
                href={`/workflows/events/${eventId}`}
                target="_blank"
                className="inline-flex"
              >
                <Button variant="outline" size="sm" className="h-7 text-xs w-full">
                  <ExternalLink className="h-3 w-3 mr-1" />
                  View Full Page
                </Button>
              </AppLink>
            </div>
          </SheetHeader>

          {query.isFetching ? (
            <div className="flex items-center justify-center py-12">
              <Spinner />
            </div>
          ) : workflow_event ? (
            <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4 pb-32">
              <Tabs defaultValue="overview" className="w-full">
                <TabsList className="grid w-full grid-cols-3 mb-4">
                  <TabsTrigger value="overview" className="flex items-center gap-2 text-xs">
                    <Database className="h-4 w-4" />
                    Overview
                  </TabsTrigger>
                  <TabsTrigger value="parameters" className="flex items-center gap-2 text-xs">
                    <Code className="h-4 w-4" />
                    Parameters
                  </TabsTrigger>
                  <TabsTrigger value="timeline" className="flex items-center gap-2 text-xs">
                    <Clock className="h-4 w-4" />
                    Timeline
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="overview" className="space-y-4 m-0">
                  <div className="bg-white border rounded-lg">
                    <div className="px-4 py-3 border-b">
                      <h3 className="text-sm font-semibold text-slate-900">Event Details</h3>
                    </div>
                    <div className="p-4 space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                        <div className="space-y-3">
                          <div>
                            <Label className="text-xs text-slate-600 font-medium">Event ID</Label>
                            <div className="flex items-center space-x-2 mt-1">
                              <code className="text-xs bg-slate-100 px-2 py-1 rounded font-mono text-slate-800">
                                {workflow_event.id}
                              </code>
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-6 w-6 p-0 hover:bg-slate-100"
                                onClick={() => copyToClipboard(workflow_event.id)}
                              >
                                <Copy className="h-3 w-3" />
                              </Button>
                            </div>
                          </div>
                          <div>
                            <Label className="text-xs text-slate-600 font-medium">Event Type</Label>
                            <div className="mt-1">
                              <Badge variant="outline" className="text-xs">{workflow_event.event_type}</Badge>
                            </div>
                          </div>
                          <div>
                            <Label className="text-xs text-slate-600 font-medium">Test Mode</Label>
                            <div className="mt-1">
                              <Badge variant={workflow_event.test_mode ? "secondary" : "outline"} className="text-xs">
                                {workflow_event.test_mode ? "Yes" : "No"}
                              </Badge>
                            </div>
                          </div>
                        </div>
                        <div className="space-y-3">
                          <div>
                            <Label className="text-xs text-slate-600 font-medium">Workflow</Label>
                            <div className="mt-1">
                              <p className="text-xs font-medium text-slate-900">{workflow_event.workflow.name}</p>
                              <code className="text-xs text-slate-600 bg-slate-100 px-2 py-1 rounded font-mono mt-1 inline-block">
                                {workflow_event.workflow.id}
                              </code>
                            </div>
                          </div>
                          <div>
                            <Label className="text-xs text-slate-600 font-medium">Started At</Label>
                            <p className="text-xs text-slate-900 mt-1">
                              {formatDateTimeLong(workflow_event.created_at)}
                            </p>
                          </div>
                          <div>
                            <Label className="text-xs text-slate-600 font-medium">Last Updated</Label>
                            <p className="text-xs text-slate-900 mt-1">
                              {formatDateTimeLong(workflow_event.updated_at)}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {workflow_event.workflow.description && (
                    <div className="bg-white border rounded-lg">
                      <div className="px-4 py-3 border-b">
                        <h3 className="text-sm font-semibold text-slate-900">Workflow Description</h3>
                      </div>
                      <div className="p-4">
                        <p className="text-xs text-slate-700">{workflow_event.workflow.description}</p>
                      </div>
                    </div>
                  )}
                </TabsContent>

                <TabsContent value="parameters" className="space-y-4 m-0">
                  <div className="bg-white border rounded-lg">
                    <div className="px-4 py-3 border-b">
                      <div className="flex items-center justify-between">
                        <h3 className="text-sm font-semibold text-slate-900">Event Parameters</h3>
                        {workflow_event.parameters && Object.keys(workflow_event.parameters).length > 0 && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => copyToClipboard(workflow_event.parameters)}
                            className="h-7 text-xs"
                          >
                            <Copy className="h-3 w-3 mr-1" />
                            Copy
                          </Button>
                        )}
                      </div>
                    </div>
                    <div className="p-4">
                      {!workflow_event.parameters || Object.keys(workflow_event.parameters).length === 0 ? (
                        <div className="bg-slate-50 border border-slate-200 rounded-lg p-6 text-center">
                          <Code className="h-6 w-6 text-slate-400 mx-auto mb-2" />
                          <p className="text-xs text-slate-600">No parameters provided for this event</p>
                        </div>
                      ) : (
                        <div className="bg-slate-50 border rounded-lg p-3 max-h-80 overflow-auto">
                          <pre className="text-xs">
                            <code
                              dangerouslySetInnerHTML={{
                                __html: hljs.highlight(
                                  jsonify(workflow_event.parameters) as string,
                                  { language: "json" },
                                ).value,
                              }}
                            />
                          </pre>
                        </div>
                      )}
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="timeline" className="space-y-4 m-0">
                  <div className="p-0">
                    {!workflow_event.records || workflow_event.records.length === 0 ? (
                      <div className="bg-slate-50 border border-slate-200 rounded-lg p-6 text-center">
                        <Clock className="h-6 w-6 text-slate-400 mx-auto mb-2" />
                        <p className="text-xs text-slate-600">No execution records available</p>
                      </div>
                    ) : (
                      <div className="space-y-3 h-full overflow-auto">
                        {workflow_event.records.map((record, index) => (
                          <div key={record.id || index} className="bg-slate-50 border border-slate-200 rounded-lg">
                            <div className="px-3 py-2 border-b border-slate-200">
                              <div className="flex items-center justify-between">
                                <div className="flex items-center space-x-2">
                                  <Badge variant="outline" className="text-xs font-medium">
                                    {record.key}
                                  </Badge>
                                  {record.timestamp && (
                                    <span className="text-xs text-slate-500">
                                      {moment(record.timestamp * 1000).format("HH:mm:ss")}
                                    </span>
                                  )}
                                </div>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="h-6 w-6 p-0 hover:bg-slate-200"
                                  onClick={() => copyToClipboard(record.record)}
                                >
                                  <Copy className="h-3 w-3" />
                                </Button>
                              </div>
                            </div>
                            <div className="p-3">
                              {record.record?.url && (
                                <div className="mb-2">
                                  <Label className="text-xs text-slate-600 font-medium">URL:</Label>
                                  <p className="text-xs font-mono text-slate-800 mt-1">{record.record.url}</p>
                                </div>
                              )}
                              {record.record?.request_id && (
                                <div className="mb-2">
                                  <Label className="text-xs text-slate-600 font-medium">Request ID:</Label>
                                  <p className="text-xs font-mono text-slate-800 mt-1">{record.record.request_id}</p>
                                </div>
                              )}
                              {record.record?.action_name && (
                                <div className="mb-2">
                                  <Label className="text-xs text-slate-600 font-medium">Action:</Label>
                                  <p className="text-xs font-mono text-slate-800 mt-1">{record.record.action_name}</p>
                                </div>
                              )}
                              {(record.record?.url || record.record?.request_id || record.record?.action_name) && (
                                <Separator className="my-2" />
                              )}
                              <div className="bg-white border rounded p-2 max-h-40 overflow-auto">
                                <pre className="text-xs">
                                  <code
                                    dangerouslySetInnerHTML={{
                                      __html: hljs.highlight(
                                        parseWorkflowEventRecordData(record.record),
                                        { language: record.record?.format || "json" },
                                      ).value,
                                    }}
                                  />
                                </pre>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          ) : (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <p className="text-sm text-slate-600">No event data available</p>
              </div>
            </div>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
};
