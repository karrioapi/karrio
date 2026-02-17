"use client";

import React, { useState } from "react";
import { Clock, Activity, Filter, RefreshCw, X, Server, Copy, Check, Terminal } from "lucide-react";
import { Card, CardContent, CardHeader } from "@karrio/ui/components/ui/card";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { formatDateTimeLong, groupBy, failsafe } from "@karrio/lib";
import { useTracingRecords } from "@karrio/hooks/tracing-record";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";
import { xml } from "@codemirror/lang-xml";
import { cn } from "@karrio/ui/lib/utils";
import moment from "moment";

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

const TracingRecordDetailViewer = ({ records }: { records: any[] | null }) => {
  const [copiedFull, setCopiedFull] = useState(false);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const copyFullRecords = () => {
    const full = JSON.stringify(records, null, 2);
    navigator.clipboard.writeText(full);
    setCopiedFull(true);
    setTimeout(() => setCopiedFull(false), 2000);
  };

  if (!records || records.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-neutral-400">
        <div className="text-center">
          <Activity className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>Select a tracing record to view details</p>
        </div>
      </div>
    );
  }

  const request = records.find((r: any) => r.key === "request");
  const response = records.find((r: any) => r.key !== "request");
  const requestData = parseRecordData(request?.record);
  const responseData = parseRecordData(response?.record);
  const requestId = (request?.record || response?.record)?.request_id;

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="border-b border-border px-4 py-3 flex-shrink-0">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Server className="h-4 w-4 text-primary" />
            <span className="font-medium text-foreground">
              {(request || response)?.meta?.carrier_name || "Unknown"}
            </span>
            <Badge variant="outline" className="text-xs border-border text-muted-foreground">
              {(request || response)?.meta?.carrier_id || "N/A"}
            </Badge>
          </div>
          <div className="flex items-center gap-2">
            {(() => {
              const curl = generateTracingCurlCommand(request);
              return curl ? (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => { navigator.clipboard.writeText(curl); setCopiedFull(true); setTimeout(() => setCopiedFull(false), 2000); }}
                  className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
                  title="Copy as cURL command"
                >
                  <Terminal className="h-3 w-3" />
                  <span className="ml-1 text-xs">cURL</span>
                </Button>
              ) : null;
            })()}
            <Button
              variant="outline"
              size="sm"
              onClick={copyFullRecords}
              className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
              title="Copy full record as JSON"
            >
              {copiedFull ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
              <span className="ml-1 text-xs">{copiedFull ? "Copied" : "Copy"}</span>
            </Button>
          </div>
        </div>
        <div className="text-xs text-muted-foreground space-y-1">
          <div>URL: {(request?.record || response?.record)?.url || "N/A"}</div>
          {requestId && <div>Request ID: {requestId}</div>}
          {(request || response)?.meta?.object_id && (
            <div>Entity: {(request || response)?.meta?.object_id}</div>
          )}
          {request?.timestamp && (
            <div>Request: {moment(request.timestamp * 1000).format("LTS")}</div>
          )}
          {response?.timestamp && (
            <div>Response: {moment(response.timestamp * 1000).format("LTS")}</div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {request && requestData && (
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-muted-foreground">Request</span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => copyToClipboard(requestData || "")}
                className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
              >
                <Copy className="h-3 w-3" />
              </Button>
            </div>
            <div className="border border-border rounded-md overflow-hidden">
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
              <span className="text-sm font-medium text-muted-foreground">{response.key}</span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => copyToClipboard(responseData || "")}
                className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
              >
                <Copy className="h-3 w-3" />
              </Button>
            </div>
            <div className="border border-border rounded-md overflow-hidden">
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
      </div>
    </div>
  );
};

const TracingRecordListItem = ({
  records,
  isSelected,
  onSelect,
}: {
  records: any[];
  isSelected: boolean;
  onSelect: (records: any[]) => void;
}) => {
  const request = records.find((r: any) => r.key === "request");
  const response = records.find((r: any) => r.key !== "request");
  const representative = request || response;

  return (
    <div
      className={cn(
        "p-4 border-b border-neutral-800 cursor-pointer transition-all duration-150 hover:bg-primary/10",
        isSelected ? "bg-primary/20 border-l-4 border-l-primary/60" : "border-l-4 border-l-transparent"
      )}
      onClick={() => onSelect(records)}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3 flex-1 min-w-0">
          <Server className="h-4 w-4 text-primary flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <Badge className="bg-indigo-900/30 text-indigo-200 border-none text-xs">
                {representative?.meta?.carrier_name || "unknown"}
              </Badge>
              {request && response && (
                <span className="text-xs text-neutral-400">
                  {records.length} records
                </span>
              )}
            </div>
            <div className="text-sm text-neutral-200 truncate font-mono">
              {representative?.record?.url || "N/A"}
            </div>
            <div className="text-xs text-neutral-400 truncate">
              {representative?.meta?.carrier_id || "N/A"}
              {representative?.meta?.object_id && ` • ${representative.meta.object_id}`}
            </div>
          </div>
          <div className="text-xs text-neutral-400 flex-shrink-0">
            {representative?.timestamp
              ? moment(representative.timestamp * 1000).format("LTS")
              : ""}
          </div>
        </div>
      </div>
    </div>
  );
};

// Custom Tracing Filter Component
const TracingRecordsFilterDropdown = ({ context }: { context: ReturnType<typeof useTracingRecords> }) => {
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
                <h3 className="font-medium text-sm text-foreground">Filter Tracing</h3>
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
                {/* Keyword Search */}
                <div>
                  <Label htmlFor="keyword" className="text-sm font-medium text-muted-foreground">Search</Label>
                  <Input
                    id="keyword"
                    type="text"
                    placeholder="Search record data..."
                    value={tempFilters.keyword || ""}
                    onChange={(e) => handleTempFilterChange('keyword', e.target.value)}
                    className="mt-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
                  />
                </div>

                {/* Key */}
                <div>
                  <Label htmlFor="key" className="text-sm font-medium text-muted-foreground">Record Type</Label>
                  <Select
                    value={tempFilters.key || "all"}
                    onValueChange={(value) => handleTempFilterChange('key', value === 'all' ? undefined : value)}
                  >
                    <SelectTrigger className="w-full mt-1 text-foreground">
                      <SelectValue placeholder="All types" />
                    </SelectTrigger>
                    <SelectContent className="devtools-theme dark bg-popover text-foreground border-border">
                      <SelectItem value="all" className="text-foreground focus:bg-primary/20 focus:text-foreground">All types</SelectItem>
                      <SelectItem value="request" className="text-foreground focus:bg-primary/20 focus:text-foreground">Request</SelectItem>
                      <SelectItem value="response" className="text-foreground focus:bg-primary/20 focus:text-foreground">Response</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Date After */}
                <div>
                  <Label htmlFor="date_after" className="text-sm font-medium text-muted-foreground">Date After</Label>
                  <Input
                    id="date_after"
                    type="datetime-local"
                    value={tempFilters.date_after || ""}
                    onChange={(e) => handleTempFilterChange('date_after', e.target.value)}
                    className="mt-1 bg-input border-border text-foreground placeholder:text-muted-foreground"
                  />
                </div>

                {/* Date Before */}
                <div>
                  <Label htmlFor="date_before" className="text-sm font-medium text-muted-foreground">Date Before</Label>
                  <Input
                    id="date_before"
                    type="datetime-local"
                    value={tempFilters.date_before || ""}
                    onChange={(e) => handleTempFilterChange('date_before', e.target.value)}
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

export function TracingRecordsView() {
  const [selectedRecords, setSelectedRecords] = useState<any[] | null>(null);

  const tracingContext = useTracingRecords();
  const { query, filter, setFilter } = tracingContext;

  const records = query.data?.tracing_records?.edges || [];

  // Group records by request_id for pairing request/response
  const groupedRecords = React.useMemo(() => {
    const allNodes = records.map(({ node }) => node);
    const groups = groupBy(allNodes, (r: any) => r.record?.request_id || r.id);
    return Object.values(groups) as any[][];
  }, [records]);

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
    const { offset, first, ...otherFilters } = filter;
    return Object.keys(otherFilters).length > 0;
  };

  const isGroupSelected = (group: any[]) => {
    if (!selectedRecords) return false;
    return group.some(r => selectedRecords.some(sr => sr.id === r.id));
  };

  return (
    <div className="h-full flex overflow-hidden bg-background">
      {/* Left Panel - Records List */}
      <div className="w-1/2 border-r border-border flex flex-col lg:flex hidden h-full">
        {/* Header */}
        <div className="border-b border-border px-4 py-3 flex-shrink-0">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-foreground">Tracing</h2>
            <div className="flex items-center gap-2">
              <TracingRecordsFilterDropdown context={tracingContext} />
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

        {/* Records List */}
        <div className="flex-1 overflow-y-auto">
          {query.isFetching && (
            <div className="flex items-center justify-center py-8">
              <RefreshCw className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          )}

          {!query.isFetching && groupedRecords.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No tracing records found</p>
              {hasActiveFilters() && (
                <p className="text-xs mt-1 text-muted-foreground">Try adjusting your filters</p>
              )}
            </div>
          )}

          {!query.isFetching && groupedRecords.length > 0 && (
            <div className="divide-y">
              {groupedRecords.map((group, idx) => (
                <TracingRecordListItem
                  key={group[0]?.id || idx}
                  records={group}
                  isSelected={isGroupSelected(group)}
                  onSelect={setSelectedRecords}
                />
              ))}
            </div>
          )}
        </div>

        {/* Pagination */}
        {records.length > 0 && (
          <div className="border-t border-border px-4 py-2 flex items-center justify-between text-sm flex-shrink-0">
            <span className="text-muted-foreground">
              Showing {((filter.offset as number) || 0) + 1}-{((filter.offset as number) || 0) + records.length}
              {query.data?.tracing_records?.page_info.count != null && ` of ${query.data.tracing_records.page_info.count}`}
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
                disabled={!query.data?.tracing_records?.page_info.has_next_page}
                className="h-7 px-2 text-xs text-foreground border-border hover:bg-primary/10"
              >
                Next
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Right Panel - Record Details */}
      <div className="flex-1 lg:w-1/2 w-full h-full overflow-hidden">
        <TracingRecordDetailViewer records={selectedRecords} />
      </div>

      {/* Mobile View */}
      <div className="lg:hidden w-full">
        {selectedRecords ? (
          <div className="h-full flex flex-col">
            <div className="border-b border-border px-4 py-2 flex items-center gap-2">
              <Button
                variant="ghost"
                size="default"
                onClick={() => setSelectedRecords(null)}
                className="text-primary"
              >
                ← Back
              </Button>
              <span className="text-sm font-medium text-foreground">Record Details</span>
            </div>
            <div className="flex-1">
              <TracingRecordDetailViewer records={selectedRecords} />
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col">
            {/* Mobile Header */}
            <div className="border-b border-border px-4 py-3">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-lg font-semibold text-foreground">Tracing</h2>
                <div className="flex items-center gap-2">
                  <TracingRecordsFilterDropdown context={tracingContext} />
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

            {/* Mobile Records List */}
            <div className="flex-1 overflow-auto">
              {query.isFetching && (
                <div className="flex items-center justify-center py-8">
                  <RefreshCw className="h-6 w-6 animate-spin text-muted-foreground" />
                </div>
              )}

              {!query.isFetching && groupedRecords.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No tracing records found</p>
                  {hasActiveFilters() && (
                    <p className="text-xs mt-1 text-muted-foreground">Try adjusting your filters</p>
                  )}
                </div>
              )}

              {!query.isFetching && groupedRecords.length > 0 && (
                <div className="divide-y">
                  {groupedRecords.map((group, idx) => (
                    <TracingRecordListItem
                      key={group[0]?.id || idx}
                      records={group}
                      isSelected={false}
                      onSelect={setSelectedRecords}
                    />
                  ))}
                </div>
              )}
            </div>

            {/* Mobile Pagination */}
            {records.length > 0 && (
              <div className="border-t border-border px-4 py-2 flex items-center justify-between text-sm">
                <span className="text-muted-foreground">
                  Showing {((filter.offset as number) || 0) + 1}-{((filter.offset as number) || 0) + records.length}
                  {query.data?.tracing_records?.page_info.count != null && ` of ${query.data.tracing_records.page_info.count}`}
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
                    disabled={!query.data?.tracing_records?.page_info.has_next_page}
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
