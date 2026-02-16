"use client";

import React, { useState } from "react";
import { RefreshCw, Calendar, Package, Truck, Webhook, AlertCircle, X, Filter, Copy, Check, Activity, Clock, Server, Terminal, Play } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Card, CardContent, CardHeader } from "@karrio/ui/components/ui/card";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { formatDateTimeLong, groupBy, failsafe } from "@karrio/lib";
import { useWebhooks, useWebhookMutation } from "@karrio/hooks/webhook";
import { useWorkerActions } from "@karrio/hooks/admin-worker";
import { useEvents } from "@karrio/hooks/event";
import { useLogs } from "@karrio/hooks/log";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";
import { xml } from "@codemirror/lang-xml";
import { EventTypes, EVENT_TYPES } from "@karrio/types";
import { cn } from "@karrio/ui/lib/utils";
import moment from "moment";

const EVENT_TYPE_COLORS = {
  [EventTypes.order_created]: "bg-indigo-900/30 text-indigo-200",
  [EventTypes.order_updated]: "bg-cyan-900/30 text-cyan-200",
  [EventTypes.order_fulfilled]: "bg-emerald-900/30 text-emerald-200",
  [EventTypes.order_cancelled]: "bg-red-900/30 text-red-200",
  [EventTypes.shipment_purchased]: "bg-blue-900/30 text-blue-200",
  [EventTypes.shipment_cancelled]: "bg-red-900/30 text-red-200",
  [EventTypes.shipment_fulfilled]: "bg-purple-900/30 text-purple-200",
  [EventTypes.tracker_created]: "bg-orange-900/30 text-orange-200",
  [EventTypes.tracker_updated]: "bg-yellow-900/30 text-yellow-200",
  default: "bg-slate-900/30 text-slate-200",
};

const EVENT_TYPE_ICONS = {
  shipment: <Package className="h-4 w-4 text-primary" />,
  tracker: <Truck className="h-4 w-4 text-primary" />,
  order: <Calendar className="h-4 w-4 text-primary" />,
  webhook: <Webhook className="h-4 w-4 text-primary" />,
  default: <AlertCircle className="h-4 w-4 text-primary" />,
};

const parseRecordData = (record: any) => {
  if (!record) return null;

  const rawData = record.data || record.response || record.error;
  if (!rawData) return null;

  if (record?.format === "xml") {
    if (typeof rawData === 'string') {
      return rawData.replace(/></g, '>\n<');
    }
    return rawData;
  }

  if (record?.format === "json" || !record?.format) {
    if (typeof rawData === 'object') {
      return JSON.stringify(rawData, null, 2);
    }

    if (typeof rawData === 'string') {
      try {
        const parsed = JSON.parse(rawData);
        return JSON.stringify(parsed, null, 2);
      } catch {
        return rawData;
      }
    }
  }

  return rawData;
};

// Generate cURL command from a carrier tracing record
const generateTracingCurlCommand = (request: any): string | null => {
  if (!request?.record) return null;

  const record = request.record;
  const url = record.url;
  if (!url) return null;

  const format = record.format || "json";
  const contentType = format === "xml"
    ? "application/xml"
    : "application/json";

  const parts: string[] = [`curl -X POST`];
  parts.push(`  '${url}'`);
  parts.push(`  -H 'Content-Type: ${contentType}'`);

  const rawData = record.data;
  if (rawData) {
    const body = typeof rawData === "object"
      ? JSON.stringify(rawData)
      : String(rawData);
    if (body && body !== "{}" && body !== "null") {
      parts.push(`  -d '${body.replace(/'/g, "'\\''")}'`);
    }
  }

  return parts.join(" \\\n");
};

// Timeline tab showing tracing records from associated API logs
const EventTimelineTab = ({ entityId }: { entityId: string | undefined }) => {
  const { query: logsQuery } = useLogs({ entity_id: entityId });
  const logs = logsQuery.data?.logs?.edges || [];

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  if (!entityId) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
        <p>No associated entity activity</p>
        <p className="text-xs mt-1">This event does not reference a specific entity</p>
      </div>
    );
  }

  if (logsQuery.isFetching) {
    return (
      <div className="flex items-center justify-center py-8">
        <RefreshCw className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  // Collect all tracing records from all logs
  const allRecords = logs.flatMap(({ node: log }) => (log.records || []).map((r: any) => ({ ...r, _log: log })));

  if (allRecords.length === 0 && logs.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <Clock className="h-8 w-8 mx-auto mb-2 opacity-50" />
        <p>No API logs found for this entity</p>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      {/* API Logs summary */}
      {logs.length > 0 && (
        <div className="mb-2">
          <span className="text-xs text-muted-foreground">{logs.length} API log(s) found</span>
        </div>
      )}

      {/* Tracing records grouped by request_id */}
      {logs.map(({ node: log }) => {
        const records = log.records || [];
        if (records.length === 0) return null;

        return Object.values(
          groupBy(records, (r: any) => r.record?.request_id),
        ).map((groupedRecords: any, key) => {
          const request = groupedRecords.find((r: any) => r.key === "request");
          const response = groupedRecords.find((r: any) => r.key !== "request");
          const requestData = parseRecordData(request?.record);
          const responseData = parseRecordData(response?.record);
          const requestId = (request?.record || response?.record)?.request_id || key;

          return (
            <Card key={`${log.id}-${key}`} className="border border-neutral-800 bg-neutral-950">
              <CardHeader className="p-4">
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <Server className="h-4 w-4 text-neutral-500" />
                    <span className="font-medium">
                      {(request || response)?.meta?.carrier_name}
                    </span>
                    <Badge variant="outline" className="text-xs border-neutral-700 text-neutral-300">
                      {(request || response)?.meta?.carrier_id}
                    </Badge>
                  </div>
                  <div className="text-xs text-neutral-400 space-y-1">
                    <div>URL: {(request?.record || response?.record)?.url}</div>
                    <div>Request ID: {requestId}</div>
                    <div>API Log: #{log.id} {log.method} {log.path}</div>
                    {request?.timestamp && (
                      <div>Request: {moment(request.timestamp * 1000).format("LTS")}</div>
                    )}
                    {response?.timestamp && (
                      <div>Response: {moment(response.timestamp * 1000).format("LTS")}</div>
                    )}
                    {request && (() => {
                      const curl = generateTracingCurlCommand(request);
                      return curl ? (
                        <div className="flex items-center justify-between border border-neutral-800 rounded-md px-3 py-2 mt-2">
                          <span className="text-sm font-medium text-gray-300">cURL</span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={(e) => { e.stopPropagation(); copyToClipboard(curl); }}
                            className="h-7 px-2 border-neutral-800 text-neutral-300 hover:bg-purple-900/20"
                          >
                            <Terminal className="h-3 w-3 mr-1" />
                            <span className="text-xs">Copy</span>
                          </Button>
                        </div>
                      ) : null;
                    })()}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="p-4 space-y-3">
                {request && requestData && (
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-neutral-300">Request</span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(requestData || "")}
                        className="h-7 px-2 border-neutral-800 text-neutral-300 hover:bg-purple-900/20"
                      >
                        <Copy className="h-3 w-3" />
                      </Button>
                    </div>
                    <div className="border border-neutral-800 rounded-md overflow-hidden">
                      <CodeMirror
                        value={requestData || ""}
                        extensions={[
                          request.record?.format === "xml" ? xml() : json()
                        ]}
                        theme="dark"
                        className="text-xs"
                        readOnly
                        basicSetup={{
                          lineNumbers: false,
                          foldGutter: true,
                          dropCursor: false,
                          allowMultipleSelections: false,
                          indentOnInput: false,
                          bracketMatching: true,
                          closeBrackets: false,
                          autocompletion: false,
                          highlightSelectionMatches: false,
                        }}
                      />
                    </div>
                  </div>
                )}

                {response && responseData && (
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-neutral-300">{response.key}</span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(responseData || "")}
                        className="h-7 px-2 border-neutral-800 text-neutral-300 hover:bg-purple-900/20"
                      >
                        <Copy className="h-3 w-3" />
                      </Button>
                    </div>
                    <div className="border border-neutral-800 rounded-md overflow-hidden">
                      <CodeMirror
                        value={responseData || ""}
                        extensions={[
                          response.record?.format === "xml" ? xml() : json()
                        ]}
                        theme="dark"
                        className="text-xs"
                        readOnly
                        basicSetup={{
                          lineNumbers: false,
                          foldGutter: true,
                          dropCursor: false,
                          allowMultipleSelections: false,
                          indentOnInput: true,
                          bracketMatching: true,
                          closeBrackets: true,
                          autocompletion: false,
                          highlightSelectionMatches: false,
                        }}
                      />
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        });
      })}
    </div>
  );
};

const EventDetailViewer = ({ event }: { event: any }) => {
  const [copiedFull, setCopiedFull] = useState(false);
  const [activeTab, setActiveTab] = useState<"timeline" | "data">("data");
  const [showReplayDropdown, setShowReplayDropdown] = useState(false);
  const [replayStatus, setReplayStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const { query: webhooksQuery } = useWebhooks();
  const { replayEvent } = useWebhookMutation();
  const { retryWebhook } = useWorkerActions();
  const webhooks = webhooksQuery.data?.webhooks?.edges || [];

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyFullEvent = () => {
    const fullEvent = JSON.stringify(event, null, 2);
    navigator.clipboard.writeText(fullEvent);
    setCopiedFull(true);
    setTimeout(() => setCopiedFull(false), 2000);
  };

  const handleReplay = async (webhookId: string) => {
    setReplayStatus("loading");
    try {
      await replayEvent.mutateAsync({ webhookId, eventId: event.id });
      setReplayStatus("success");
      setTimeout(() => setReplayStatus("idle"), 2000);
    } catch {
      setReplayStatus("error");
      setTimeout(() => setReplayStatus("idle"), 2000);
    }
    setShowReplayDropdown(false);
  };

  if (!event) {
    return (
      <div className="flex items-center justify-center h-64 text-neutral-400">
        <div className="text-center">
          <Activity className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>Select an event to view details</p>
        </div>
      </div>
    );
  }

  const getEventTypeColor = (eventType: EventTypes | null) => {
    if (!eventType) return EVENT_TYPE_COLORS.default;
    return EVENT_TYPE_COLORS[eventType] || EVENT_TYPE_COLORS.default;
  };

  const getEventTypeIcon = (eventType: EventTypes | null) => {
    if (!eventType) return EVENT_TYPE_ICONS.default;
    const type = eventType.split('_')[0];
    return EVENT_TYPE_ICONS[type as keyof typeof EVENT_TYPE_ICONS] || EVENT_TYPE_ICONS.default;
  };

  // Extract entity_id from event data for timeline
  const entityId = event?.data?.id as string | undefined;

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="border-b border-border px-4 py-3 flex-shrink-0">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            {getEventTypeIcon(event.type as EventTypes | null)}
            <Badge className={getEventTypeColor(event.type as EventTypes | null)}>
              {event.type}
            </Badge>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => retryWebhook.mutate({ event_id: event.id })}
              disabled={retryWebhook.isLoading}
              className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
              title="Re-enqueue webhook notifications for this event"
            >
              {retryWebhook.isLoading ? (
                <RefreshCw className="h-3 w-3 animate-spin" />
              ) : (
                <Webhook className="h-3 w-3" />
              )}
              <span className="ml-1 text-xs">
                {retryWebhook.isLoading ? "Retrying..." : "Retry Webhooks"}
              </span>
            </Button>
            <div className="relative">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowReplayDropdown(!showReplayDropdown)}
                disabled={replayStatus === "loading"}
                className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
                title="Replay event to a webhook"
              >
                {replayStatus === "loading" ? (
                  <RefreshCw className="h-3 w-3 animate-spin" />
                ) : replayStatus === "success" ? (
                  <Check className="h-3 w-3 text-green-400" />
                ) : replayStatus === "error" ? (
                  <AlertCircle className="h-3 w-3 text-red-400" />
                ) : (
                  <Play className="h-3 w-3" />
                )}
                <span className="ml-1 text-xs">
                  {replayStatus === "loading" ? "Sending..." : replayStatus === "success" ? "Sent" : replayStatus === "error" ? "Failed" : "Replay"}
                </span>
              </Button>
              {showReplayDropdown && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setShowReplayDropdown(false)} />
                  <div className="absolute right-0 top-full mt-1 w-64 bg-popover border border-border rounded-md shadow-lg z-20">
                    <div className="p-2">
                      <div className="text-xs font-medium text-muted-foreground px-2 py-1 mb-1">Send to webhook</div>
                      {webhooksQuery.isFetching && (
                        <div className="flex items-center justify-center py-4">
                          <RefreshCw className="h-4 w-4 animate-spin text-muted-foreground" />
                        </div>
                      )}
                      {!webhooksQuery.isFetching && webhooks.length === 0 && (
                        <div className="text-xs text-muted-foreground px-2 py-4 text-center">No webhooks configured</div>
                      )}
                      {!webhooksQuery.isFetching && webhooks.map(({ node: webhook }: any) => (
                        <button
                          key={webhook.id}
                          onClick={() => handleReplay(webhook.id)}
                          className="w-full text-left px-2 py-1.5 text-xs rounded hover:bg-primary/20 text-foreground truncate"
                        >
                          <div className="font-medium truncate">{webhook.url}</div>
                          <div className="text-muted-foreground truncate">{webhook.id}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={copyFullEvent}
              className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
              title="Copy full event as JSON"
            >
              {copiedFull ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
              <span className="ml-1 text-xs">{copiedFull ? "Copied" : "Copy"}</span>
            </Button>
          </div>
        </div>
        <div className="text-xs text-muted-foreground space-y-1">
          <div>ID: {event.id}</div>
          {entityId && <div>Entity: {entityId}</div>}
          <div>{formatDateTimeLong(event.created_at)}</div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-border px-4 py-2 flex-shrink-0">
        <div className="flex gap-1">
          <button
            onClick={() => setActiveTab("data")}
            className={`px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${activeTab === "data"
              ? "bg-primary border-primary text-primary-foreground"
              : "bg-transparent border-neutral-800 text-neutral-300 hover:bg-neutral-800/40 hover:text-white"
              }`}
          >
            Event Data
          </button>
          <button
            onClick={() => setActiveTab("timeline")}
            className={`px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${activeTab === "timeline"
              ? "bg-primary border-primary text-primary-foreground"
              : "bg-transparent border-neutral-800 text-neutral-300 hover:bg-neutral-800/40 hover:text-white"
              }`}
          >
            <Clock className="h-3 w-3 mr-1 inline" />
            Timeline
          </button>
        </div>
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === "timeline" && (
          <EventTimelineTab entityId={entityId} />
        )}

        {activeTab === "data" && (
          <div className="p-4">
            {event.data && (
              <div className="mb-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-muted-foreground">Event Data</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => copyToClipboard(JSON.stringify(event.data, null, 2))}
                    className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
                  >
                    <Copy className="h-3 w-3" />
                  </Button>
                </div>
                <div className="border border-border rounded-md overflow-hidden">
                  <CodeMirror
                    value={JSON.stringify(event.data, null, 2)}
                    extensions={[json()]}
                    theme="dark"
                    className="text-xs"
                    readOnly

                    basicSetup={{
                      lineNumbers: false,
                      foldGutter: true,
                      dropCursor: false,
                      allowMultipleSelections: false,
                      indentOnInput: false,
                      bracketMatching: true,
                      closeBrackets: false,
                      autocompletion: false,
                      highlightSelectionMatches: false,
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const EventListItem = ({
  event,
  isSelected,
  onSelect
}: {
  event: any;
  isSelected: boolean;
  onSelect: (event: any) => void;
}) => {
  const getEventTypeColor = (eventType: EventTypes | null) => {
    if (!eventType) return EVENT_TYPE_COLORS.default;
    return EVENT_TYPE_COLORS[eventType] || EVENT_TYPE_COLORS.default;
  };

  const getEventTypeIcon = (eventType: EventTypes | null) => {
    if (!eventType) return EVENT_TYPE_ICONS.default;
    const type = eventType.split('_')[0];
    return EVENT_TYPE_ICONS[type as keyof typeof EVENT_TYPE_ICONS] || EVENT_TYPE_ICONS.default;
  };

  return (
    <div
      className={cn(
        "p-4 border-b border-neutral-800 cursor-pointer transition-all duration-150 hover:bg-primary/10",
        isSelected ? "bg-primary/20 border-l-4 border-l-primary/60" : "border-l-4 border-l-transparent"
      )}
      onClick={() => onSelect(event)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3 flex-1 min-w-0">
          {getEventTypeIcon(event.type as EventTypes | null)}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <Badge className={`${getEventTypeColor(event.type as EventTypes | null)} border-none text-xs`}>
                {event.type}
              </Badge>
              {event.pending_webhooks > 0 && (
                <span className="text-xs text-orange-300">
                  {event.pending_webhooks} pending
                </span>
              )}
            </div>
            <div className="text-xs text-neutral-400 truncate">
              ID: {event.id}
              {event.data?.id && ` • ${event.data.id}`}
            </div>
          </div>
          <div className="text-xs text-neutral-400 flex-shrink-0">
            {formatDateTimeLong(event.created_at)}
          </div>
        </div>
      </div>
    </div>
  );
};

// Custom Events Filter Component
const EventsFilterDropdown = ({ context }: { context: ReturnType<typeof useEvents> }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [tempFilters, setTempFilters] = useState<any>({});
  const { query, filter, setFilter } = context;

  const handleTempFilterChange = (key: string, value: any) => {
    setTempFilters((prev: any) => ({
      ...prev,
      [key]: value === "" ? undefined : value
    }));
  };

  const handleApply = () => {
    const cleanFilters = Object.entries(tempFilters).reduce((acc, [key, value]) => {
      if (value !== undefined && value !== "") {
        acc[key] = value;
      }
      return acc;
    }, {} as any);

    setFilter({ ...cleanFilters, offset: 0, first: 20 });
    setIsOpen(false);
  };

  const handleClear = () => {
    setTempFilters({});
    setFilter({ offset: 0, first: 20 });
    setIsOpen(false);
  };

  const hasActiveFilters = () => {
    const { offset, first, ...otherFilters } = filter;
    return Object.keys(otherFilters).length > 0;
  };

  // Sync temp filters with actual filters when opened
  React.useEffect(() => {
    if (isOpen) {
      const { offset, first, ...activeFilters } = filter;
      setTempFilters(activeFilters);
    }
  }, [isOpen, filter]);

  return (
    <div className="relative">
      <Button
        variant="outline"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="h-8 text-foreground border-border hover:bg-primary/10"
      >
        <Filter className="h-4 w-4 mr-2 text-foreground" />
        Filters
        {hasActiveFilters() && (
          <Badge variant="secondary" className="ml-2 h-5 px-1.5 text-xs">
            {Object.keys(filter).filter(k => k !== 'offset' && k !== 'first' && filter[k]).length}
          </Badge>
        )}
      </Button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setIsOpen(false)} />
          <div className="absolute right-0 top-full mt-1 w-80 bg-popover border border-border rounded-md shadow-lg z-20 text-foreground">
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-medium text-sm text-foreground">Filter Events</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsOpen(false)}
                  className="h-6 w-6 p-0 text-foreground hover:bg-primary/10"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>

              <div className="space-y-4">
                {/* Search */}
                <div>
                  <Label htmlFor="search" className="text-sm font-medium text-muted-foreground">Search</Label>
                  <Input
                    id="search"
                    placeholder="Search by tracking number, ID, type..."
                    value={tempFilters.keyword || ""}
                    onChange={(e) => handleTempFilterChange('keyword', e.target.value)}
                    className="mt-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
                  />
                </div>

                {/* Event Type */}
                <div>
                  <Label htmlFor="type" className="text-sm font-medium text-muted-foreground">Event Type</Label>
                  <Select
                    value={tempFilters.type?.[0] || "all"}
                    onValueChange={(value) => handleTempFilterChange('type', value === 'all' ? undefined : [value])}
                  >
                    <SelectTrigger className="w-full mt-1 text-foreground">
                      <SelectValue placeholder="All event types" />
                    </SelectTrigger>
                    <SelectContent className="devtools-theme dark bg-popover text-foreground border-border">
                      <SelectItem value="all" className="text-foreground focus:bg-primary/20 focus:text-foreground"></SelectItem>
                      {EVENT_TYPES.map((type) => (
                        <SelectItem key={type} value={type} className="text-foreground focus:bg-primary/20 focus:text-foreground">{type}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Entity ID */}
                <div>
                  <Label htmlFor="entity_id" className="text-sm font-medium text-muted-foreground">Related Object ID</Label>
                  <Input
                    id="entity_id"
                    placeholder="e.g: shp_123456"
                    value={tempFilters.entity_id || ""}
                    onChange={(e) => handleTempFilterChange('entity_id', e.target.value)}
                    className="mt-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
                  />
                </div>

              </div>

              <div className="flex items-center justify-between mt-6 pt-4 border-t border-border">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleClear}
                  disabled={!hasActiveFilters() && Object.keys(tempFilters).length === 0}
                  className="text-foreground border-border hover:bg-primary/10"
                >
                  Clear All
                </Button>
                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsOpen(false)}
                    className="text-foreground hover:bg-primary/10"
                  >
                    Cancel
                  </Button>
                  <Button
                    size="sm"
                    onClick={handleApply}
                    disabled={query.isLoading}
                    className="text-foreground border-border hover:bg-primary/10"
                  >
                    {query.isLoading ? 'Applying...' : 'Apply'}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export function EventsView() {
  const [selectedEvent, setSelectedEvent] = useState<any>(null);

  // Use the proper events hook without initial filters - let the hook manage the state
  const eventsContext = useEvents();
  const { query, filter, setFilter } = eventsContext;

  const events = query.data?.events?.edges || [];

  const updateFilter = (extra: any = {}) => {
    setFilter({ ...filter, ...extra });
  };

  const handleRefresh = () => {
    query.refetch();
  };

  const clearFilters = () => {
    setFilter({ offset: 0, first: 20 });
  };

  const hasActiveFilters = () => {
    const {
      offset,
      first,
      ...otherFilters
    } = filter;
    return Object.keys(otherFilters).length > 0;
  };

  return (
    <div className="h-full flex overflow-hidden bg-background">
      {/* Left Panel - Events List */}
      <div className="w-1/2 border-r border-border flex flex-col lg:flex hidden h-full">
        {/* Header */}
        <div className="border-b border-border px-4 py-3 flex-shrink-0">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-foreground">Events</h2>
            <div className="flex items-center gap-2">
              {/* Use the custom EventsFilterDropdown component */}
              <EventsFilterDropdown context={eventsContext} />
              <Button
                variant="outline"
                size="sm"
                onClick={handleRefresh}
                disabled={query.isFetching}
                className="text-foreground border-border hover:bg-primary/10"
              >
                <RefreshCw className={`h-4 w-4 ${query.isFetching ? 'animate-spin' : ''}`} />
              </Button>
            </div>
          </div>

          {/* Show active filters indicator */}
          {hasActiveFilters() && (
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs text-muted-foreground">Filters active:</span>
              <Badge variant="secondary" className="text-xs">
                {Object.keys(filter).filter(key => !['offset', 'first'].includes(key)).length} active
              </Badge>
              <Button
                variant="ghost"
                size="sm"
                onClick={clearFilters}
                className="h-6 px-2 text-xs"
              >
                <X className="h-3 w-3 mr-1" />
                Clear all
              </Button>
            </div>
          )}
        </div>

        {/* Events List */}
        <div className="flex-1 overflow-y-auto">
          {query.isFetching && (
            <div className="flex items-center justify-center py-8">
              <RefreshCw className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          )}

          {!query.isFetching && events.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No events found</p>
              {hasActiveFilters() && (
                <p className="text-xs mt-1 text-muted-foreground">Try adjusting your filters</p>
              )}
            </div>
          )}

          {!query.isFetching && events.length > 0 && (
            <div className="divide-y">
              {events.map(({ node: event }) => (
                <EventListItem
                  key={event.id}
                  event={event}
                  isSelected={selectedEvent?.id === event.id}
                  onSelect={setSelectedEvent}
                />
              ))}
            </div>
          )}
        </div>

        {/* Pagination */}
        {events.length > 0 && (
          <div className="border-t border-border px-4 py-2 flex items-center justify-between text-sm flex-shrink-0">
            <span className="text-muted-foreground">
              Showing {((filter.offset as number) || 0) + 1}-{((filter.offset as number) || 0) + events.length}
              {query.data?.events?.page_info.count != null && ` of ${query.data.events.page_info.count}`}
            </span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => updateFilter({ offset: Math.max(0, ((filter.offset as number) || 0) - 20) })}
                disabled={(filter.offset as number) === 0 || filter.offset === undefined}
                className="h-7 px-2 text-xs text-foreground border-border hover:bg-primary/10"
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => updateFilter({ offset: ((filter.offset as number) || 0) + 20 })}
                disabled={!query.data?.events?.page_info.has_next_page}
                className="h-7 px-2 text-xs text-foreground border-border hover:bg-primary/10"
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Right Panel - Event Details */}
      <div className="flex-1 lg:w-1/2 w-full h-full overflow-hidden">
        <EventDetailViewer event={selectedEvent} />
      </div>

      {/* Mobile View */}
      <div className="lg:hidden w-full">
        {selectedEvent ? (
          <div className="h-full flex flex-col">
            <div className="border-b border-border px-4 py-2 flex items-center gap-2">
              <Button
                variant="ghost"
                size="default"
                onClick={() => setSelectedEvent(null)}
                className="text-primary"
              >
                ← Back
              </Button>
              <span className="text-sm font-medium text-foreground">Event Details</span>
            </div>
            <div className="flex-1">
              <EventDetailViewer event={selectedEvent} />
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col">
            {/* Mobile Header */}
            <div className="border-b border-border px-4 py-3">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-lg font-semibold text-foreground">Events</h2>
                <div className="flex items-center gap-2">
                  {/* Use the custom EventsFilterDropdown component for mobile */}
                  <EventsFilterDropdown context={eventsContext} />
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleRefresh}
                    disabled={query.isFetching}
                    className="text-foreground border-border hover:bg-primary/10"
                  >
                    <RefreshCw className={`h-4 w-4 ${query.isFetching ? 'animate-spin' : ''}`} />
                  </Button>
                </div>
              </div>

              {/* Show active filters indicator for mobile */}
              {hasActiveFilters() && (
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs text-muted-foreground">Filters active:</span>
                  <Badge variant="secondary" className="text-xs">
                    {Object.keys(filter).filter(key => !['offset', 'first'].includes(key)).length} active
                  </Badge>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={clearFilters}
                    className="h-6 px-2 text-xs"
                  >
                    <X className="h-3 w-3 mr-1" />
                    Clear all
                  </Button>
                </div>
              )}
            </div>

            {/* Mobile Events List */}
            <div className="flex-1 overflow-auto">
              {query.isFetching && (
                <div className="flex items-center justify-center py-8">
                  <RefreshCw className="h-6 w-6 animate-spin text-muted-foreground" />
                </div>
              )}

              {!query.isFetching && events.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No events found</p>
                  {hasActiveFilters() && (
                    <p className="text-xs mt-1 text-muted-foreground">Try adjusting your filters</p>
                  )}
                </div>
              )}

              {!query.isFetching && events.length > 0 && (
                <div className="divide-y">
                  {events.map(({ node: event }) => (
                    <EventListItem
                      key={event.id}
                      event={event}
                      isSelected={false}
                      onSelect={setSelectedEvent}
                    />
                  ))}
                </div>
              )}
            </div>

            {/* Mobile Pagination */}
            {events.length > 0 && (
              <div className="border-t border-border px-4 py-2 flex items-center justify-between text-sm">
                <span className="text-muted-foreground">
                  Showing {((filter.offset as number) || 0) + 1}-{((filter.offset as number) || 0) + events.length}
                  {query.data?.events?.page_info.count != null && ` of ${query.data.events.page_info.count}`}
                </span>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => updateFilter({ offset: Math.max(0, ((filter.offset as number) || 0) - 20) })}
                    disabled={(filter.offset as number) === 0 || filter.offset === undefined}
                    className="h-7 px-2 text-xs text-foreground border-border hover:bg-primary/10"
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => updateFilter({ offset: ((filter.offset as number) || 0) + 20 })}
                    disabled={!query.data?.events?.page_info.has_next_page}
                    className="h-7 px-2 text-xs text-foreground border-border hover:bg-primary/10"
                  >
                    Next
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}