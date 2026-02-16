"use client";

import React, { useState } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Clock, Activity, AlertCircle, CheckCircle, Filter, RefreshCw, X } from "lucide-react";
import { formatDateTimeLong, groupBy, jsonify, notEmptyJSON, failsafe } from "@karrio/lib";
import { Card, CardContent, CardHeader } from "@karrio/ui/components/ui/card";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";
import { Copy, Check, Server, Terminal } from "lucide-react";
import { useLogs } from "@karrio/hooks/log";
import { xml } from "@codemirror/lang-xml";
import { cn } from "@karrio/ui/lib/utils";
import moment from "moment";


// Generate cURL command from an API log entry
const generateLogCurlCommand = (log: any): string | null => {
  if (!log) return null;

  const method = log.method || "GET";
  const host = log.host || "";
  const path = log.path || "";
  if (!host && !path) return null;

  let url = host ? `${host}${path}` : path;

  // Append query params if present
  const queryParams = failsafe(() => {
    if (!log.query_params) return null;
    const params = typeof log.query_params === "string"
      ? JSON.parse(log.query_params)
      : log.query_params;
    if (!params || typeof params !== "object") return null;
    const entries = Object.entries(params).filter(([_, v]) => v != null && v !== "");
    if (entries.length === 0) return null;
    return entries
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
      .join("&");
  });
  if (queryParams) {
    url += (url.includes("?") ? "&" : "?") + queryParams;
  }

  const parts: string[] = [`curl -X ${method}`];
  parts.push(`  '${url}'`);
  parts.push(`  -H 'Content-Type: application/json'`);

  // Add request body for methods that typically have one
  if (["POST", "PUT", "PATCH"].includes(method.toUpperCase()) && log.data) {
    const body = failsafe(() => {
      const d = typeof log.data === "string" ? JSON.parse(log.data) : log.data;
      return JSON.stringify(d);
    });
    if (body && body !== "{}" && body !== "null") {
      parts.push(`  -d '${body.replace(/'/g, "'\\''")}'`);
    }
  }

  return parts.join(" \\\n");
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

// Timeline Tab Component
const TimelineTab = ({ log, parseRecordData, copyToClipboard }: {
  log: any;
  parseRecordData: (record: any) => string | null;
  copyToClipboard: (text: string) => void;
}) => {

  return (
    <div className="p-4">
      {(log?.records || []).length === 0 && (
        <div className="text-center py-8 text-neutral-400">
          <Clock className="h-8 w-8 mx-auto mb-2 opacity-50" />
          <p>No tracing records available</p>
        </div>
      )}
      {(log?.records || []).length > 0 && (
        <div className="space-y-4">
          {Object.values(
            groupBy(log!.records, (r: any) => r.record?.request_id),
          ).map((records: any, key) => {
            const request = records.find((r: any) => r.key === "request");
            const response = records.find((r: any) => r.key !== "request");
            const requestData = parseRecordData(request?.record);
            const responseData = parseRecordData(response?.record);
            const requestId = (request?.record || response?.record)?.request_id || key;

            return (
              <Card key={key} className="border border-neutral-800 bg-neutral-950">
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
                      {request?.timestamp && (
                        <div>
                          Request: {moment(request.timestamp * 1000).format("LTS")}
                        </div>
                      )}
                      {response?.timestamp && (
                        <div>
                          Response: {moment(response.timestamp * 1000).format("LTS")}
                        </div>
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
          })}
        </div>
      )}
    </div>
  );
};

const LogDetailViewer = ({ log }: { log: any }) => {
  const [data, setData] = useState<string>();
  const [response, setResponse] = useState<string>();
  const [queryParams, setQueryParams] = useState<string>();
  const [activeTab, setActiveTab] = useState<"request" | "response" | "timeline">("response");
  const [copiedFull, setCopiedFull] = useState(false);
  const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({
    request: false,
    response: false,
    queryParams: false
  });

  React.useEffect(() => {
    if (log !== undefined) {
      setQueryParams(failsafe(() => jsonify(log?.query_params), "{}"));
      setResponse(failsafe(() => jsonify(log?.response), "{}"));
      setData(failsafe(() => jsonify(log?.data), "{}"));
    }
  }, [log]);

  const getStatusColor = (statusCode: number | null) => {
    if (!statusCode) return "bg-slate-900/30 text-slate-200";
    if (statusCode >= 200 && statusCode < 300) return "bg-green-900/40 text-green-300";
    if (statusCode >= 400) return "bg-red-900/40 text-red-300";
    return "bg-yellow-900/40 text-yellow-300";
  };

  const getMethodColor = (method: string | null) => {
    switch (method?.toUpperCase()) {
      case 'GET': return "bg-blue-900/40 text-blue-300";
      case 'POST': return "bg-green-900/40 text-green-300";
      case 'PUT': return "bg-yellow-900/40 text-yellow-300";
      case 'DELETE': return "bg-red-900/40 text-red-300";
      case 'PATCH': return "bg-purple-900/40 text-purple-300";
      default: return "bg-slate-900/40 text-slate-300";
    }
  };

  const getStatusIcon = (statusCode: number | null) => {
    if (!statusCode) return null;
    if (statusCode >= 200 && statusCode < 300) return "✓";
    if (statusCode >= 400) return "✗";
    return "!";
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyFullLog = () => {
    const fullLog = failsafe(() => jsonify(log), "{}");
    navigator.clipboard.writeText(fullLog);
    setCopiedFull(true);
    setTimeout(() => setCopiedFull(false), 2000);
  };

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const parseRecordData = (record: any) => {
    if (!record) return null;

    const rawData = record.data || record.response || record.error;
    if (!rawData) return null;

    // Handle XML format
    if (record?.format === "xml") {
      if (typeof rawData === 'string') {
        return rawData.replace(/></g, '>\n<');
      }
      return rawData;
    }

    // Handle JSON format
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

  if (!log) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        <div className="text-center">
          <Activity className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>Select a log entry to view details</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-border px-4 py-3 flex-shrink-0">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Badge className={`${getMethodColor(log.method)} border-none hover:bg-black`}>
              {log.method}
            </Badge>
            <Badge className={`${getStatusColor(log.status_code)} border-none hover:bg-black`}>
              {getStatusIcon(log.status_code)} {log.status_code}
            </Badge>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={copyFullLog}
              className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
              title="Copy full log as JSON"
            >
              {copiedFull ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
              <span className="ml-1 text-xs">{copiedFull ? "Copied" : "Copy"}</span>
            </Button>
          </div>
        </div>
        <div className="text-xs text-muted-foreground space-y-1">
          <div className="text-sm font-medium truncate text-foreground">{log.method} {log.path}</div>
          <div>ID: {log.id}</div>
          {log.response_ms && <div>Response: {log.response_ms}ms</div>}
          {log.remote_addr && <div>Remote: {log.remote_addr}</div>}
          <div>{formatDateTimeLong(log.requested_at)}</div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b px-4 py-2 flex-shrink-0">
        <div className="flex gap-1">
          {notEmptyJSON(response) && (
            <button
              onClick={() => setActiveTab("response")}
              className={`px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${activeTab === "response"
                ? "bg-primary border-primary text-primary-foreground"
                : "bg-transparent border-neutral-800 text-neutral-300 hover:bg-neutral-800/40 hover:text-white"
                }`}
            >
              Response
            </button>
          )}
          <button
            onClick={() => setActiveTab("request")}
            className={`px-3 py-1.5 text-xs font-medium rounded-md border transition-colors ${activeTab === "request"
              ? "bg-primary border-primary text-primary-foreground"
              : "bg-transparent border-neutral-800 text-neutral-300 hover:bg-neutral-800/40 hover:text-white"
              }`}
          >
            Request
          </button>
          {(log?.records || []).length > 0 && (
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
          )}
        </div>
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === "response" && notEmptyJSON(response) && (
          <div className="p-4">
            <div className="mb-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-300">Response Body</span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => copyToClipboard(response || "")}
                  className="h-7 px-2 text-white"
                >
                  <Copy className="h-3 w-3" />
                </Button>
              </div>
              <div className="border rounded-md overflow-hidden">
                <CodeMirror
                  value={response || ""}
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
          </div>
        )}

        {activeTab === "request" && (
          <div className="p-4 space-y-4">
            {/* Copy as cURL */}
            {(() => {
              const curl = generateLogCurlCommand(log);
              return curl ? (
                <div className="flex items-center justify-between border border-neutral-800 rounded-md px-3 py-2">
                  <span className="text-sm font-medium text-gray-300">cURL</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => copyToClipboard(curl)}
                    className="h-7 px-2 border-neutral-800 text-neutral-300 hover:bg-purple-900/20"
                  >
                    <Terminal className="h-3 w-3 mr-1" />
                    <span className="text-xs">Copy</span>
                  </Button>
                </div>
              ) : null;
            })()}

            {notEmptyJSON(queryParams) && queryParams !== data && (
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-300">Query Parameters</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => copyToClipboard(queryParams || "")}
                    className="h-7 px-2 text-white"
                  >
                    <Copy className="h-3 w-3" />
                  </Button>
                </div>
                <div className="border rounded-md overflow-hidden">
                  <CodeMirror
                    value={queryParams || ""}
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

            {notEmptyJSON(data) && (
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-300">Request {log?.method} Body</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => copyToClipboard(data || "")}
                    className="h-7 px-2 text-white"
                  >
                    <Copy className="h-3 w-3" />
                  </Button>
                </div>
                <div className="border rounded-md overflow-hidden">
                  <CodeMirror
                    value={data || ""}
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

        {activeTab === "timeline" && (
          <TimelineTab log={log} parseRecordData={parseRecordData} copyToClipboard={copyToClipboard} />
        )}
      </div>
    </div>
  );
};

const LogListItem = ({
  log,
  isSelected,
  onSelect
}: {
  log: any;
  isSelected: boolean;
  onSelect: (log: any) => void;
}) => {
  const getStatusColor = (statusCode: number | null) => {
    if (!statusCode) return "bg-gray-900/40 text-gray-300";
    if (statusCode >= 200 && statusCode < 300) return "bg-green-900/40 text-green-300";
    if (statusCode >= 400) return "bg-red-900/40 text-red-300";
    return "bg-yellow-900/40 text-yellow-300";
  };

  const getMethodColor = (method: string | null) => {
    switch (method?.toUpperCase()) {
      case "GET": return "bg-blue-900/40 text-blue-300";
      case "POST": return "bg-green-900/40 text-green-300";
      case "PUT": return "bg-yellow-900/40 text-yellow-300";
      case "DELETE": return "bg-red-900/40 text-red-300";
      case "PATCH": return "bg-purple-900/40 text-purple-300";
      default: return "bg-gray-900/40 text-gray-300";
    }
  };

  const getStatusIcon = (statusCode: number | null) => {
    if (!statusCode) return <AlertCircle className="h-4 w-4 text-primary" />;
    if (statusCode >= 200 && statusCode < 300) return <CheckCircle className="h-4 w-4 text-primary" />;
    if (statusCode >= 400) return <AlertCircle className="h-4 w-4 text-primary" />;
    return <Activity className="h-4 w-4 text-primary" />;
  };

  // Extract object_id from tracing records meta if available
  const objectId = failsafe(() => {
    const records = log.records || [];
    for (const r of records) {
      if (r?.meta?.object_id) return r.meta.object_id;
    }
    return null;
  });

  return (
    <div
      className={cn(
        "p-4 border-b border-neutral-800 cursor-pointer transition-all duration-150 hover:bg-primary/10",
        isSelected ? "bg-primary/20 border-l-4 border-l-primary/60" : "border-l-4 border-l-transparent"
      )}
      onClick={() => onSelect(log)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3 flex-1 min-w-0">
          {getStatusIcon(log.status_code)}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <Badge className={`${getMethodColor(log.method)} border-none text-xs hover:bg-black`}>
                {log.method}
              </Badge>
              <Badge className={`${getStatusColor(log.status_code)} border-none text-xs hover:bg-black`}>
                {log.status_code}
              </Badge>
              {log.response_ms && (
                <span className="text-xs text-neutral-400">
                  {log.response_ms}ms
                </span>
              )}
            </div>
            <div className="text-sm text-neutral-200 truncate font-mono">
              {log.path}
            </div>
            <div className="text-xs text-neutral-400 truncate">
              ID: {log.id}
              {objectId && ` • ${objectId}`}
            </div>
          </div>
          <div className="text-xs text-neutral-400 flex-shrink-0">
            {formatDateTimeLong(log.requested_at)}
          </div>
        </div>
      </div>
    </div>
  );
};

// Custom Logs Filter Component
const LogsFilterDropdown = ({ context }: { context: ReturnType<typeof useLogs> }) => {
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
        className="h-8 text-white border-neutral-800 hover:bg-neutral-800/40"
      >
        <Filter className="h-4 w-4 mr-2 text-white" />
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
                <h3 className="font-medium text-sm text-foreground">Filter Logs</h3>
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
                    placeholder="Search logs..."
                    value={tempFilters.query || ""}
                    onChange={(e) => handleTempFilterChange('query', e.target.value)}
                    className="mt-1 bg-input text-foreground border-border placeholder:text-muted-foreground"
                  />
                </div>

                {/* Status Code */}
                <div>
                  <Label htmlFor="status" className="text-sm font-medium text-muted-foreground">Status Code</Label>
                  <Select
                    value={tempFilters.status_code?.toString() || "all"}
                    onValueChange={(value) => handleTempFilterChange('status_code', value === 'all' ? undefined : parseInt(value))}
                  >
                    <SelectTrigger className="w-full mt-1 text-foreground">
                      <SelectValue placeholder="All status codes" />
                    </SelectTrigger>
                    <SelectContent className="devtools-theme dark bg-popover text-foreground border-border">
                      <SelectItem value="all" className="text-foreground focus:bg-primary/20 focus:text-foreground">All status codes</SelectItem>
                      <SelectItem value="200" className="text-foreground focus:bg-primary/20 focus:text-foreground">200 - OK</SelectItem>
                      <SelectItem value="201" className="text-foreground focus:bg-primary/20 focus:text-foreground">201 - Created</SelectItem>
                      <SelectItem value="400" className="text-foreground focus:bg-primary/20 focus:text-foreground">400 - Bad Request</SelectItem>
                      <SelectItem value="401" className="text-foreground focus:bg-primary/20 focus:text-foreground">401 - Unauthorized</SelectItem>
                      <SelectItem value="404" className="text-foreground focus:bg-primary/20 focus:text-foreground">404 - Not Found</SelectItem>
                      <SelectItem value="500" className="text-foreground focus:bg-primary/20 focus:text-foreground">500 - Server Error</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Entity ID */}
                <div>
                  <Label htmlFor="entity_id" className="text-sm font-medium text-muted-foreground">Entity ID</Label>
                  <Input
                    id="entity_id"
                    placeholder="e.g: shp_123456, trk_123456"
                    value={tempFilters.entity_id || ""}
                    onChange={(e) => handleTempFilterChange('entity_id', e.target.value)}
                    className="mt-1 bg-input text-foreground border-border placeholder:text-muted-foreground"
                  />
                </div>

                {/* Method */}
                <div>
                  <Label htmlFor="method" className="text-sm font-medium text-muted-foreground">HTTP Method</Label>
                  <Select
                    value={tempFilters.method || "all"}
                    onValueChange={(value) => handleTempFilterChange('method', value === 'all' ? undefined : value)}
                  >
                    <SelectTrigger className="w-full mt-1 text-foreground">
                      <SelectValue placeholder="All methods" />
                    </SelectTrigger>
                    <SelectContent className="devtools-theme dark bg-popover text-foreground border-border">
                      <SelectItem value="all" className="text-foreground focus:bg-primary/20 focus:text-foreground">All methods</SelectItem>
                      <SelectItem value="GET" className="text-foreground focus:bg-primary/20 focus:text-foreground">GET</SelectItem>
                      <SelectItem value="POST" className="text-foreground focus:bg-primary/20 focus:text-foreground">POST</SelectItem>
                      <SelectItem value="PUT" className="text-foreground focus:bg-primary/20 focus:text-foreground">PUT</SelectItem>
                      <SelectItem value="DELETE" className="text-foreground focus:bg-primary/20 focus:text-foreground">DELETE</SelectItem>
                      <SelectItem value="PATCH" className="text-foreground focus:bg-primary/20 focus:text-foreground">PATCH</SelectItem>
                    </SelectContent>
                  </Select>
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

export function LogsView() {
  const [selectedLog, setSelectedLog] = useState<any>(null);

  // Use the proper logs hook without initial filters - let the hook manage the state
  const logsContext = useLogs();
  const { query, filter, setFilter } = logsContext;

  const logs = query.data?.logs?.edges || [];

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
      {/* Left Panel - Logs List */}
      <div className="w-1/2 border-r border-border flex flex-col lg:flex hidden h-full">
        {/* Header */}
        <div className="border-b border-border px-4 py-3 flex-shrink-0">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-foreground">API Logs</h2>
            <div className="flex items-center gap-2">
              {/* Use the custom LogsFilterDropdown component */}
              <LogsFilterDropdown context={logsContext} />
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

        {/* Logs List */}
        <div className="flex-1 overflow-y-auto">
          {query.isFetching && (
            <div className="flex items-center justify-center py-8">
              <RefreshCw className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          )}

          {!query.isFetching && logs.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No logs found</p>
              {hasActiveFilters() && (
                <p className="text-xs mt-1 text-muted-foreground">Try adjusting your filters</p>
              )}
            </div>
          )}

          {!query.isFetching && logs.length > 0 && (
            <div className="divide-y">
              {logs.map(({ node: log }) => (
                <LogListItem
                  key={log.id}
                  log={log}
                  isSelected={selectedLog?.id === log.id}
                  onSelect={setSelectedLog}
                />
              ))}
            </div>
          )}
        </div>

        {/* Pagination */}
        {logs.length > 0 && (
          <div className="border-t border-border px-4 py-2 flex items-center justify-between text-sm flex-shrink-0">
            <span className="text-muted-foreground">
              Showing {((filter.offset as number) || 0) + 1}-{((filter.offset as number) || 0) + logs.length}
              {query.data?.logs?.page_info.count != null && ` of ${query.data.logs.page_info.count}`}
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
                disabled={!query.data?.logs?.page_info.has_next_page}
                className="h-7 px-2 text-xs text-foreground border-border hover:bg-primary/10"
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Right Panel - Log Details */}
      <div className="flex-1 lg:w-1/2 w-full h-full overflow-hidden">
        <LogDetailViewer log={selectedLog} />
      </div>

      {/* Mobile View */}
      <div className="lg:hidden w-full">
        {selectedLog ? (
          <div className="h-full flex flex-col">
            <div className="border-b border-border px-4 py-2 flex items-center gap-2 text-primary">
              <Button
                variant="ghost"
                size="default"
                onClick={() => setSelectedLog(null)}
              >
                ← Back
              </Button>
              <span className="text-sm font-medium text-foreground">Log Details</span>
            </div>
            <div className="flex-1">
              <LogDetailViewer log={selectedLog} />
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col">
            {/* Mobile Header */}
            <div className="border-b border-border px-4 py-3">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-lg font-semibold text-foreground">API Logs</h2>
                <div className="flex items-center gap-2">
                  {/* Use the custom LogsFilterDropdown component for mobile */}
                  <LogsFilterDropdown context={logsContext} />
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

            {/* Mobile Logs List */}
            <div className="flex-1 overflow-auto">
              {query.isFetching && (
                <div className="flex items-center justify-center py-8">
                  <RefreshCw className="h-6 w-6 animate-spin text-muted-foreground" />
                </div>
              )}

              {!query.isFetching && logs.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No logs found</p>
                  {hasActiveFilters() && (
                    <p className="text-xs mt-1 text-muted-foreground">Try adjusting your filters</p>
                  )}
                </div>
              )}

              {!query.isFetching && logs.length > 0 && (
                <div className="divide-y">
                  {logs.map(({ node: log }) => (
                    <LogListItem
                      key={log.id}
                      log={log}
                      isSelected={false}
                      onSelect={setSelectedLog}
                    />
                  ))}
                </div>
              )}
            </div>

            {/* Mobile Pagination */}
            {logs.length > 0 && (
              <div className="border-t border-border px-4 py-2 flex items-center justify-between text-sm">
                <span className="text-muted-foreground">
                  Showing {((filter.offset as number) || 0) + 1}-{((filter.offset as number) || 0) + logs.length}
                  {query.data?.logs?.page_info.count != null && ` of ${query.data.logs.page_info.count}`}
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
                    disabled={!query.data?.logs?.page_info.has_next_page}
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
