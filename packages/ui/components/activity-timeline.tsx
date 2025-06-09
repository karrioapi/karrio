"use client";

import React, { useState } from "react";
import { LogType, EventType } from "@karrio/types";
import { formatDateTime } from "@karrio/lib";
import { StatusCode } from "@karrio/ui/core/components/status-code-badge";
import { Spinner } from "@karrio/ui/core/components/spinner";
import { cn } from "@karrio/ui/lib/utils";

type ActivityItem =
  | ({ activityType: 'api-request'; parentLog: LogType; content: any; })
  | ({ activityType: 'api-response'; parentLog: LogType; content: any; })
  | ({ activityType: 'trace-request'; parentLog: LogType; traceRecord: any; content: any; })
  | ({ activityType: 'trace-response'; parentLog: LogType; traceRecord: any; content: any; })
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
      case 'api-request':
        return "bg-gray-500 border-gray-500";
      case 'api-response':
        return statusCode && statusCode >= 400
          ? "bg-gray-600 border-gray-600"
          : "bg-gray-400 border-gray-400";
      case 'trace-request':
        return "bg-gray-500 border-gray-500";
      case 'trace-response':
        return "bg-gray-400 border-gray-400";
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

const RawContentViewer = ({ content, contentType }: { content: any; contentType: string }) => {
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

  const parsedContent = parseContent(content);

  const getBadgeStyle = (type: string) => {
    switch (type) {
      case 'json':
        return "bg-blue-600 text-white";
      case 'xml':
        return "bg-gray-600 text-white";
      case 'url-encoded':
        return "bg-orange-600 text-white";
      case 'form-data':
        return "bg-green-600 text-white";
      default:
        return "bg-gray-500 text-white";
    }
  };

  const badgeStyle = getBadgeStyle(parsedContent.type);

  return (
    <div className="h-full flex flex-col bg-white max-h-[80vh] overflow-y-auto">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-gray-50 overflow-hidden">
        <div className="flex items-center gap-3 min-w-0 flex-1 overflow-hidden">
          <span className="text-sm font-medium text-gray-900 truncate">{contentType}</span>
          <span className={cn("px-2 py-1 rounded text-xs font-medium whitespace-nowrap", badgeStyle)}>
            {parsedContent.type.toUpperCase()}
          </span>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          {parsedContent.type === 'json' && (
            <button
              onClick={() => {
                try {
                  const minified = JSON.stringify(parsedContent.content);
                  navigator.clipboard.writeText(minified);
                } catch {
                  navigator.clipboard.writeText(parsedContent.formatted);
                }
              }}
              className="text-xs text-blue-600 hover:text-blue-800 px-2 py-1 rounded hover:bg-blue-50 whitespace-nowrap"
            >
              Copy Minified
            </button>
          )}
          <button
            onClick={() => navigator.clipboard.writeText(parsedContent.formatted)}
            className="text-xs text-blue-600 hover:text-blue-800 px-2 py-1 rounded hover:bg-blue-50 whitespace-nowrap"
          >
            Copy
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        <pre className="p-4 text-xs font-mono leading-relaxed text-gray-800 whitespace-pre-wrap break-words overflow-x-auto">
          {parsedContent.formatted}
        </pre>
      </div>
    </div>
  );
};

const ActivityTitle = ({ item }: { item: ActivityItem }) => {
  const getTitle = () => {
    switch (item.activityType) {
      case 'api-request':
        return `${item.parentLog.method} ${item.parentLog.path}`;
      case 'api-response':
        return `${item.parentLog.method} ${item.parentLog.path}`;
      case 'trace-request':
        return item.traceRecord.key || 'Trace Request';
      case 'trace-response':
        return item.traceRecord.key || 'Trace Response';
      case 'event':
        return item.type?.toString().replace(/_/g, ' ') || 'Unknown Event';
      default:
        return 'Unknown Activity';
    }
  };

  const getBadgeText = () => {
    switch (item.activityType) {
      case 'api-request':
        return 'Request';
      case 'api-response':
        return 'Response';
      case 'trace-request':
        return 'Trace Request';
      case 'trace-response':
        return 'Trace Response';
      case 'event':
        return 'Event';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="flex items-center gap-2 overflow-hidden">
      <span className="text-sm font-semibold text-gray-900 truncate">
        {getTitle()}
      </span>
      {item.activityType === 'api-response' && (
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
      case 'api-request':
      case 'api-response':
        const meta: string[] = [];
        if (item.parentLog.response_ms) meta.push(`${item.parentLog.response_ms as number}ms`);
        if (item.parentLog.remote_addr) meta.push(item.parentLog.remote_addr);
        return meta;
      case 'trace-request':
      case 'trace-response':
        const traceMeta: string[] = [];
        if (item.traceRecord.timestamp) {
          traceMeta.push(new Date(item.traceRecord.timestamp * 1000).toLocaleTimeString());
        }
        if (item.traceRecord.test_mode) traceMeta.push('Test');
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
      case 'api-request':
      case 'api-response':
        return item.parentLog.requested_at;
      case 'trace-request':
      case 'trace-response':
        return item.traceRecord.timestamp
          ? new Date(item.traceRecord.timestamp * 1000).toISOString()
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
          item.activityType === 'api-response'
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
      // Add API request
      if (log.data) {
        activityItems.push({
          activityType: 'api-request',
          parentLog: log,
          content: log.data,
        });
      }

      // Add tracing records
      if (log.records && log.records.length > 0) {
        log.records.forEach((record, recordIndex) => {
          const recordData = record.record;

          if (recordData) {
            if (recordData.request || recordData.response) {
              if (recordData.request) {
                activityItems.push({
                  activityType: 'trace-request',
                  parentLog: log,
                  traceRecord: record,
                  content: recordData.request,
                });
              }
              if (recordData.response) {
                activityItems.push({
                  activityType: 'trace-response',
                  parentLog: log,
                  traceRecord: record,
                  content: recordData.response,
                });
              }
            } else {
              activityItems.push({
                activityType: 'trace-request',
                parentLog: log,
                traceRecord: record,
                content: recordData,
              });
            }
          }
        });
      }

      // Add API response
      if (log.response) {
        activityItems.push({
          activityType: 'api-response',
          parentLog: log,
          content: log.response,
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
        case 'api-request':
        case 'api-response':
          timestampA = a.parentLog.requested_at;
          break;
        case 'trace-request':
        case 'trace-response':
          timestampA = a.traceRecord.timestamp
            ? new Date(a.traceRecord.timestamp * 1000).toISOString()
            : a.parentLog.requested_at;
          break;
        case 'event':
          timestampA = a.created_at;
          break;
        default:
          timestampA = new Date().toISOString();
      }

      switch (b.activityType) {
        case 'api-request':
        case 'api-response':
          timestampB = b.parentLog.requested_at;
          break;
        case 'trace-request':
        case 'trace-response':
          timestampB = b.traceRecord.timestamp
            ? new Date(b.traceRecord.timestamp * 1000).toISOString()
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
      case 'api-request':
        return `API Request - ${item.parentLog.status_code} ${item.parentLog.method} ${item.parentLog.path}`;
      case 'api-response':
        return `API Response - ${item.parentLog.status_code} ${item.parentLog.method} ${item.parentLog.path}`;
      case 'trace-request':
        return `Trace Request - ${item.traceRecord.key || 'Unknown'}`;
      case 'trace-response':
        return `Trace Response - ${item.traceRecord.key || 'Unknown'}`;
      case 'event':
        return `Event - ${item.type?.toString().replace(/_/g, ' ') || 'Unknown Event'}`;
      default:
        return 'Unknown Content';
    }
  };

  const getItemId = (item: ActivityItem, index: number) => {
    switch (item.activityType) {
      case 'api-request':
        return `api-request-${item.parentLog.id}`;
      case 'api-response':
        return `api-response-${item.parentLog.id}`;
      case 'trace-request':
        return `trace-request-${item.parentLog.id}-${item.traceRecord.id || index}`;
      case 'trace-response':
        return `trace-response-${item.parentLog.id}-${item.traceRecord.id || index}`;
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
                  content={selectedItem.content}
                  contentType={getContentType(selectedItem)}
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
                content={selectedItem.content}
                contentType={getContentType(selectedItem)}
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
