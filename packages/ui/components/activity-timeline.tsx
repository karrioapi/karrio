"use client";

import React, { useState } from "react";
import { LogType, EventType } from "@karrio/types";
import { formatDateTime } from "@karrio/lib";
import { StatusCode } from "@karrio/ui/core/components/status-code-badge";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { cn } from "@karrio/ui/lib/utils";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";
import { xml } from "@codemirror/lang-xml";
import { Copy } from "lucide-react";
import { Button } from "@karrio/ui/components/ui/button";

type ActivityItem =
  | ({ activityType: 'api-call'; parentLog: LogType; requestContent: any; responseContent: any; })
  | ({ activityType: 'trace-call'; parentLog: LogType; traceRequestRecord: any; traceResponseRecord: any; requestContent: any; responseContent: any; })
  | ({ activityType: 'event'; content: any; } & EventType);

interface ActivityTimelineProps {
  logs?: {
    isFetching: boolean;
    isFetched: boolean;
    data?: {
      logs: {
        edges: Array<{ node: LogType }>;
      };
    };
  };
  events?: {
    isFetching: boolean;
    isFetched: boolean;
    data?: {
      events: {
        edges: Array<{ node: EventType }>;
      };
    };
  };
  className?: string;
}

const TimelineDot = ({ activityType, statusCode, isSelected }: {
  activityType: ActivityItem['activityType'];
  statusCode?: number;
  isSelected: boolean;
}) => {
  const getDotColor = () => {
    if (isSelected) {
      return "bg-gray-700 border-gray-700";
    }

    switch (activityType) {
      case 'api-call':
        return "bg-gray-500 border-gray-500";
      case 'trace-call':
        return "bg-gray-500 border-gray-500";
      case 'event':
        return "bg-gray-600 border-gray-600";
      default:
        return "bg-gray-300 border-gray-300";
    }
  };

  return (
    <div className="absolute left-3 top-4 transform -translate-x-1/2">
      <div
        className={cn(
          "w-2 h-2 rounded-full border-2 border-white shadow-sm transition-all duration-200",
          getDotColor(),
          isSelected && "scale-125"
        )}
      />
    </div>
  );
};

const TimelineLine = () => (
  <div className="absolute left-3 top-6 bottom-0 w-px bg-gray-200 transform -translate-x-1/2" />
);

const RawContentViewer = ({
  content,
  contentType,
  responseContent,
  showTabs = false,
  activityItem
}: {
  content: any;
  contentType: string;
  responseContent?: any;
  showTabs?: boolean;
  activityItem?: ActivityItem;
}) => {
  const [activeTab, setActiveTab] = React.useState<'request' | 'response'>('request');
  if (!content) {
    return (
      <div className="flex items-center justify-center max-h-[80vh] text-gray-500">
        <div className="text-center">
          <p className="text-sm">No content available</p>
        </div>
      </div>
    );
  }

  // Enhanced content parsing with trace data handling
  const parseContent = (rawContent: any): { content: any; type: string; formatted: string; isTraceData?: boolean } => {
    // Handle trace data objects that might contain JSON strings
    if (typeof rawContent === 'object' && rawContent !== null) {
      // Check if it's a trace record with nested JSON strings
      if (rawContent.data || rawContent.response || rawContent.request) {
        const traceContent = rawContent.data || rawContent.response || rawContent.request;

        // If the nested content is a string, try to parse it
        if (typeof traceContent === 'string') {
          const parsedTrace: { content: any; type: string; formatted: string; isTraceData?: boolean } = parseContent(traceContent);
          // Return the parsed content but preserve original structure info
          return {
            content: parsedTrace.content,
            type: parsedTrace.type,
            formatted: parsedTrace.formatted,
            isTraceData: true
          };
        }

        // If nested content is already an object, format it
        if (typeof traceContent === 'object') {
          return {
            content: traceContent,
            type: 'json',
            formatted: JSON.stringify(traceContent, null, 2)
          };
        }
      }

      // Regular object handling
      return {
        content: rawContent,
        type: 'json',
        formatted: JSON.stringify(rawContent, null, 2)
      };
    }

    if (typeof rawContent === 'string') {
      const trimmed = rawContent.trim();

      // XML detection
      if (trimmed.startsWith('<') && trimmed.endsWith('>')) {
        try {
          const formatted = trimmed
            .replace(/></g, '>\n<')
            .replace(/^\s*</gm, '<')
            .split('\n')
            .map((line, index) => {
              const depth = (line.match(/^\s*</g) || []).length;
              const indent = '  '.repeat(Math.max(0, depth - 1));
              return indent + line.trim();
            })
            .join('\n');

          return { content: rawContent, type: 'xml', formatted };
        } catch {
          return { content: rawContent, type: 'xml', formatted: trimmed };
        }
      }

      // Enhanced JSON detection
      try {
        const parsed = JSON.parse(trimmed);
        return {
          content: parsed,
          type: 'json',
          formatted: JSON.stringify(parsed, null, 2)
        };
      } catch {
        // Try to detect malformed JSON-like strings
        if ((trimmed.startsWith('{') && trimmed.endsWith('}')) ||
          (trimmed.startsWith('[') && trimmed.endsWith(']'))) {
          // Attempt to fix common JSON issues
          try {
            // Fix single quotes to double quotes
            let fixedJson = trimmed.replace(/'/g, '"');
            // Fix unquoted keys
            fixedJson = fixedJson.replace(/([{,]\s*)([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:/g, '$1"$2":');
            const parsed = JSON.parse(fixedJson);
            return {
              content: parsed,
              type: 'json',
              formatted: JSON.stringify(parsed, null, 2)
            };
          } catch {
            return { content: rawContent, type: 'json', formatted: trimmed };
          }
        }

        // URL-encoded
        if (trimmed.includes('%') && trimmed.includes('=')) {
          try {
            const decoded = decodeURIComponent(trimmed);
            // Check if decoded content is JSON
            try {
              const parsed = JSON.parse(decoded);
              return {
                content: parsed,
                type: 'json',
                formatted: JSON.stringify(parsed, null, 2)
              };
            } catch {
              return { content: decoded, type: 'url-encoded', formatted: decoded };
            }
          } catch {
            return { content: rawContent, type: 'text', formatted: trimmed };
          }
        }

        // Form data
        if (trimmed.includes('=') && trimmed.includes('&')) {
          const formatted = trimmed.split('&').map(param => param.trim()).join('\n');
          return { content: rawContent, type: 'form-data', formatted };
        }

        return { content: rawContent, type: 'text', formatted: trimmed };
      }
    }

    return { content: rawContent, type: 'text', formatted: String(rawContent) };
  };

  // Helper function to get CodeMirror extension based on content type
  const getCodeMirrorExtension = (contentType: string) => {
    switch (contentType) {
      case 'xml':
        return xml();
      case 'json':
      default:
        return json();
    }
  };

  const parsedContent = parseContent(content);

  const getBadgeStyle = (type: string) => {
    switch (type) {
      case 'json':
        return "bg-blue-100 text-blue-800";
      case 'xml':
        return "bg-gray-100 text-gray-800";
      case 'url-encoded':
        return "bg-orange-100 text-orange-800";
      case 'form-data':
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const badgeStyle = getBadgeStyle(parsedContent.type);

  // Handle tabs for request/response viewing
  const currentContent = showTabs && responseContent ?
    (activeTab === 'request' ? content : responseContent) : content;

  const currentParsedContent = parseContent(currentContent);
  const currentBadgeStyle = getBadgeStyle(currentParsedContent.type);

  // Get detailed header information
  const getDetailedHeader = () => {
    if (!activityItem) {
      return {
        title: contentType,
        statusCode: null,
        method: null,
        metadata: []
      };
    }

    switch (activityItem.activityType) {
      case 'api-call':
        return {
          title: contentType,
          statusCode: activityItem.parentLog.status_code,
          method: activityItem.parentLog.method,
          metadata: [
            ...(activityItem.parentLog.response_ms ? [`${activityItem.parentLog.response_ms}ms`] : []),
            ...(activityItem.parentLog.remote_addr ? [activityItem.parentLog.remote_addr] : [])
          ]
        };
      case 'trace-call':
        const traceRecord = activityItem.traceRequestRecord?.record || activityItem.traceResponseRecord?.record;
        return {
          title: contentType,
          statusCode: null,
          method: traceRecord?.method || 'POST', // Most carrier APIs use POST
          metadata: [
            ...(activityItem.traceRequestRecord?.meta?.carrier_name ? [activityItem.traceRequestRecord.meta.carrier_name] : []),
            ...(traceRecord?.request_id ? [`ID: ${traceRecord.request_id.slice(0, 8)}...`] : [])
          ]
        };
      default:
        return {
          title: contentType,
          statusCode: null,
          method: null,
          metadata: []
        };
    }
  };

  const headerInfo = getDetailedHeader();

  return (
    <div className="h-full flex flex-col bg-white max-h-[80vh] overflow-y-auto">
      <div className="px-4 py-3 border-b border-gray-200 bg-gray-50">
        {/* Main request line */}
        <div className="flex items-center gap-3 mb-2">
          <span className="text-xs text-gray-500">From your application</span>
        </div>
        <div className="flex items-center gap-3 min-w-0 flex-1 overflow-hidden mb-3">
          {headerInfo.method && (
            <span className="text-sm font-semibold text-gray-900">{headerInfo.method}</span>
          )}
          <span className="text-sm font-medium text-gray-900 truncate">{headerInfo.title}</span>
          {headerInfo.statusCode && (
            <span className={cn(
              "px-2 py-1 rounded text-xs font-medium whitespace-nowrap",
              headerInfo.statusCode >= 200 && headerInfo.statusCode < 300
                ? "bg-green-100 text-green-700"
                : headerInfo.statusCode >= 400
                  ? "bg-red-100 text-red-700"
                  : "bg-gray-100 text-gray-700"
            )}>
              {headerInfo.statusCode} {headerInfo.statusCode >= 200 && headerInfo.statusCode < 300 ? 'OK' : 'ERROR'}
            </span>
          )}
        </div>

        {/* Metadata and actions */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 min-w-0 flex-1">
            <span className={cn("px-2 py-1 rounded text-xs font-medium whitespace-nowrap", currentBadgeStyle)}>
              {currentParsedContent.type.toUpperCase()}
            </span>
            {headerInfo.metadata.length > 0 && (
              <span className="text-xs text-gray-500 truncate">
                {headerInfo.metadata.join(' • ')}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            {currentParsedContent.type === 'json' && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  try {
                    const minified = JSON.stringify(currentParsedContent.content);
                    navigator.clipboard.writeText(minified);
                  } catch {
                    navigator.clipboard.writeText(currentParsedContent.formatted);
                  }
                }}
                className="h-7 px-2"
              >
                <Copy className="h-3 w-3 mr-1" />
                Copy Minified
              </Button>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigator.clipboard.writeText(currentParsedContent.formatted)}
              className="h-7 px-2"
            >
              <Copy className="h-3 w-3 mr-1" />
              Copy
            </Button>
          </div>
        </div>
      </div>

      {/* Tabs for request/response */}
      {showTabs && responseContent && (
        <div className="border-b border-gray-200 bg-gray-50">
          <div className="flex">
            <button
              onClick={() => setActiveTab('request')}
              className={cn(
                "px-4 py-2 text-sm font-medium border-b-2 transition-colors",
                activeTab === 'request'
                  ? "border-blue-500 text-blue-600 bg-white"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              )}
            >
              Request {activityItem?.activityType === 'api-call' ? 'parameters' : 'data'}
            </button>
            <button
              onClick={() => setActiveTab('response')}
              className={cn(
                "px-4 py-2 text-sm font-medium border-b-2 transition-colors",
                activeTab === 'response'
                  ? "border-blue-500 text-blue-600 bg-white"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              )}
            >
              Response {activityItem?.activityType === 'api-call' ? 'body' : 'data'}
            </button>
          </div>
        </div>
      )}

      <div className="flex-1 overflow-auto">
        <div className="border rounded-md overflow-hidden">
          <CodeMirror
            value={currentParsedContent.formatted}
            extensions={[getCodeMirrorExtension(currentParsedContent.type)]}
            theme="light"
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
  );
};

const ActivityTitle = ({ item }: { item: ActivityItem }) => {
  const getTitle = () => {
    switch (item.activityType) {
      case 'api-call':
        return `${item.parentLog.method} ${item.parentLog.path}`;
      case 'trace-call': {
        const carrierName =
          item.traceRequestRecord?.meta?.carrier_name ||
          item.traceResponseRecord?.meta?.carrier_name;
        return carrierName || 'Trace';
      }
      case 'event':
        return item.type?.toString().replace(/_/g, ' ') || 'Unknown Event';
      default:
        return 'Unknown Activity';
    }
  };

  const getBadgeText = () => {
    switch (item.activityType) {
      case 'api-call':
        return 'API Call';
      case 'trace-call':
        return 'Trace';
      case 'event':
        return 'Event';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="flex items-center gap-2 overflow-hidden">
      <span className="text-sm font-semibold text-gray-900 truncate">
        {item.activityType === 'trace-call' ? (
          <>
            {getTitle()}
            {(item.traceRequestRecord?.meta?.carrier_id || item.traceResponseRecord?.meta?.carrier_id) && (
              <span className="text-xs text-gray-600 font-normal ml-1">
                {' - '}{item.traceRequestRecord?.meta?.carrier_id || item.traceResponseRecord?.meta?.carrier_id}
              </span>
            )}
          </>
        ) : (
          getTitle()
        )}
      </span>
      {item.activityType === 'api-call' && (
        <StatusCode code={item.parentLog.status_code as number} />
      )}
      <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded whitespace-nowrap">
        {getBadgeText()}
      </span>
    </div>
  );
};

const ActivityMeta = ({ item }: { item: ActivityItem }) => {
  const getMeta = () => {
    switch (item.activityType) {
      case 'api-call':
        const meta: string[] = [];
        if (item.parentLog.response_ms) meta.push(`${item.parentLog.response_ms as number}ms`);
        if (item.parentLog.remote_addr) meta.push(item.parentLog.remote_addr);
        return meta;
      case 'trace-call':
        const traceMeta: string[] = [];
        
        // Calculate duration from request and response timestamps
        const requestTimestamp = item.traceRequestRecord?.timestamp;
        const responseTimestamp = item.traceResponseRecord?.timestamp;
        if (requestTimestamp && responseTimestamp) {
          const durationMs = Math.round((responseTimestamp - requestTimestamp) * 1000);
          traceMeta.push(`${durationMs}ms`);
        }
        
        if (item.traceRequestRecord.timestamp) {
          traceMeta.push(new Date(item.traceRequestRecord.timestamp * 1000).toLocaleTimeString());
        }
        const traceUrl =
          item.traceRequestRecord?.record?.url ||
          item.traceResponseRecord?.record?.url;
        if (traceUrl) {
          traceMeta.push(traceUrl.length > 40 ? `${traceUrl.slice(0, 40)}...` : traceUrl);
        }
        if (item.traceRequestRecord.test_mode) traceMeta.push('Test');
        return traceMeta;
      case 'event':
        const eventMeta: string[] = [];
        if (item.pending_webhooks !== null && item.pending_webhooks !== undefined) {
          eventMeta.push(`${item.pending_webhooks} pending webhooks`);
        }
        if (item.test_mode) eventMeta.push('Test');
        return eventMeta;
      default:
        return [];
    }
  };

  const metaItems = getMeta();

  if (metaItems.length === 0) return null;

  return (
    <div className="text-xs text-gray-500 mt-1 truncate">
      {metaItems.join(' • ')}
    </div>
  );
};

const ActivityListItem = ({
  item,
  index,
  isLast,
  isSelected,
  onSelect
}: {
  item: ActivityItem;
  index: number;
  isLast: boolean;
  isSelected: boolean;
  onSelect: (item: ActivityItem) => void;
}) => {
  const getItemTimestamp = (item: ActivityItem) => {
    switch (item.activityType) {
      case 'api-call':
        return item.parentLog.requested_at;
      case 'trace-call':
        return item.traceRequestRecord.timestamp
          ? new Date(item.traceRequestRecord.timestamp * 1000).toISOString()
          : item.parentLog.requested_at;
      case 'event':
        return item.created_at;
      default:
        return null;
    }
  };

  return (
    <div className="relative px-4 py-3">
      {/* Timeline elements */}
      <TimelineDot
        activityType={item.activityType}
        statusCode={
          item.activityType === 'api-call'
            ? (item.parentLog.status_code ?? undefined)
            : undefined
        }
        isSelected={isSelected}
      />
      {!isLast && <TimelineLine />}

      {/* Card Container */}
      <div
        className={cn(
          "ml-8 border border-gray-200 rounded-lg bg-white cursor-pointer transition-all duration-150 overflow-hidden",
          isSelected
            ? "border-gray-400 bg-gray-50"
            : "hover:border-gray-300 hover:bg-gray-50"
        )}
        onClick={() => onSelect(item)}
      >
        {/* Content */}
        <div className="p-4 overflow-hidden">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0 overflow-hidden">
              <ActivityTitle item={item} />
              <ActivityMeta item={item} />
            </div>
            <div className="text-xs text-gray-400 whitespace-nowrap flex-shrink-0">
              {getItemTimestamp(item) && formatDateTime(getItemTimestamp(item)!)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export const ActivityTimeline: React.FC<ActivityTimelineProps> = ({
  logs,
  events,
  className,
}) => {
  const [selectedItem, setSelectedItem] = useState<ActivityItem | null>(null);

  const isLoading = (logs?.isFetching && !logs?.isFetched) || (events?.isFetching && !events?.isFetched);
  const isLoaded = logs?.isFetched || events?.isFetched;

  // Transform and combine activities
  const activities = React.useMemo(() => {
    const activityItems: ActivityItem[] = [];

    // Process logs
    (logs?.data?.logs.edges || []).forEach(({ node: log }) => {
      // Add API call (request + response grouped together)
      if (log.data || log.response) {
        activityItems.push({
          activityType: 'api-call',
          parentLog: log,
          requestContent: log.data,
          responseContent: log.response,
        });
      }

      // Add tracing records (group request/response pairs by request_id)
      if (log.records && log.records.length > 0) {
        // Group records by request_id
        const recordGroups: { [key: string]: any[] } = {};
        log.records.forEach((record) => {
          const requestId = record.record?.request_id || 'unknown';
          if (!recordGroups[requestId]) {
            recordGroups[requestId] = [];
          }
          recordGroups[requestId].push(record);
        });

        // Process each group
        Object.values(recordGroups).forEach((records) => {
          const requestRecord = records.find((r) => r.key === 'request');
          const responseRecord = records.find((r) => r.key !== 'request');

          if (requestRecord || responseRecord) {
            const requestData = requestRecord?.record?.data || requestRecord?.record?.request || requestRecord?.record;
            const responseData = responseRecord?.record?.data || responseRecord?.record?.response || responseRecord?.record?.error;

            activityItems.push({
              activityType: 'trace-call',
              parentLog: log,
              traceRequestRecord: requestRecord || responseRecord,
              traceResponseRecord: responseRecord || requestRecord,
              requestContent: requestData,
              responseContent: responseData,
            });
          }
        });
      }
    });

    // Process events
    (events?.data?.events.edges || []).forEach(({ node: event }) => {
      activityItems.push({
        activityType: 'event',
        content: event.data,
        ...event,
      });
    });

    // Sort by timestamp (most recent first)
    return activityItems.sort((a, b) => {
      let timestampA: string;
      let timestampB: string;

      switch (a.activityType) {
        case 'api-call':
          timestampA = a.parentLog.requested_at;
          break;
        case 'trace-call':
          timestampA = a.traceRequestRecord.timestamp
            ? new Date(a.traceRequestRecord.timestamp * 1000).toISOString()
            : a.parentLog.requested_at;
          break;
        case 'event':
          timestampA = a.created_at;
          break;
        default:
          timestampA = new Date().toISOString();
      }

      switch (b.activityType) {
        case 'api-call':
          timestampB = b.parentLog.requested_at;
          break;
        case 'trace-call':
          timestampB = b.traceRequestRecord.timestamp
            ? new Date(b.traceRequestRecord.timestamp * 1000).toISOString()
            : b.parentLog.requested_at;
          break;
        case 'event':
          timestampB = b.created_at;
          break;
        default:
          timestampB = new Date().toISOString();
      }

      return new Date(timestampB).getTime() - new Date(timestampA).getTime();
    });
  }, [logs?.data, events?.data]);

  const handleSelectItem = (item: ActivityItem) => {
    setSelectedItem(item);
  };

  const handleCloseDetail = () => {
    setSelectedItem(null);
  };

  const getContentType = (item: ActivityItem): string => {
    switch (item.activityType) {
      case 'api-call':
        return `${item.parentLog.method} ${item.parentLog.path}`;
      case 'trace-call':
        // Try to get URL from trace record, fallback to key
        const traceUrl = item.traceRequestRecord?.record?.url || item.traceRequestRecord?.key || 'Unknown';
        return traceUrl;
      case 'event':
        return `Event - ${item.type?.toString().replace(/_/g, ' ') || 'Unknown Event'}`;
      default:
        return 'Unknown Content';
    }
  };

  const getItemId = (item: ActivityItem, index: number) => {
    switch (item.activityType) {
      case 'api-call':
        return `api-call-${item.parentLog.id}`;
      case 'trace-call':
        return `trace-call-${item.parentLog.id}-${item.traceRequestRecord.id || index}`;
      case 'event':
        return `event-${item.id}`;
      default:
        return `unknown-${index}`;
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center py-8">
        <Spinner className="h-6 w-6" />
      </div>
    );
  }

  if (isLoaded && activities.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No activity to display
      </div>
    );
  }

  return (
    <div className={cn("bg-white", className)}>
      {/* Mobile Layout */}
      <div className="lg:hidden">
        <div className="overflow-auto bg-white max-h-[80vh]">
          {activities.map((item, index) => (
            <ActivityListItem
              key={getItemId(item, index)}
              item={item}
              index={index}
              isLast={index === activities.length - 1}
              isSelected={selectedItem === item}
              onSelect={handleSelectItem}
            />
          ))}
        </div>

        {/* Mobile Detail Modal */}
        {selectedItem && (
          <div className="fixed inset-0 z-50 bg-white">
            <div className="h-full flex flex-col">
              <div className="flex items-center justify-between p-4 border-b border-gray-200">
                <h3 className="font-medium text-gray-900">{getContentType(selectedItem)}</h3>
                <button
                  onClick={handleCloseDetail}
                  className="p-1 hover:bg-gray-100 rounded text-gray-400 hover:text-gray-600"
                >
                  <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="flex-1">
                <RawContentViewer
                  content={selectedItem.activityType === 'event' ? selectedItem.content : selectedItem.requestContent}
                  contentType={getContentType(selectedItem)}
                  responseContent={selectedItem.activityType !== 'event' ? selectedItem.responseContent : undefined}
                  showTabs={selectedItem.activityType !== 'event'}
                  activityItem={selectedItem}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Desktop Layout - Side by Side */}
      <div className="hidden lg:flex bg-white">
        {/* Left Panel - Timeline */}
        <div className="w-1/2 border-r border-gray-200">
          <div className="overflow-auto bg-white max-h-[80vh]">
            {activities.map((item, index) => (
              <ActivityListItem
                key={getItemId(item, index)}
                item={item}
                index={index}
                isLast={index === activities.length - 1}
                isSelected={selectedItem === item}
                onSelect={handleSelectItem}
              />
            ))}
          </div>
        </div>

        {/* Right Panel - Raw Content */}
        <div className="w-1/2">
          {selectedItem ? (
            <div className="max-h-[80vh]">
              <RawContentViewer
                content={selectedItem.activityType === 'event' ? selectedItem.content : selectedItem.requestContent}
                contentType={getContentType(selectedItem)}
                responseContent={selectedItem.activityType !== 'event' ? selectedItem.responseContent : undefined}
                showTabs={selectedItem.activityType !== 'event'}
                activityItem={selectedItem}
              />
            </div>
          ) : (
            <div
              className="flex items-center justify-center text-gray-400 bg-white max-h-[80vh]"
            >
              <div className="text-center">
                <svg className="h-12 w-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <p className="text-sm text-gray-500">Select an activity to view raw content</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
