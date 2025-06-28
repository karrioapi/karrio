"use client";

import React, { useState } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Search, Filter, RefreshCw, Calendar, Package, Truck, Webhook, AlertCircle, X } from "lucide-react";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { formatDateTimeLong } from "@karrio/lib";
import { useEvents } from "@karrio/hooks/event";
import { EventsFilter } from "@karrio/ui/core/filters/events-filter";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";
import { EventTypes } from "@karrio/types";
import { cn } from "@karrio/ui/lib/utils";

const EVENT_TYPE_COLORS = {
  [EventTypes.order_created]: "bg-indigo-100 text-indigo-800",
  [EventTypes.order_updated]: "bg-cyan-100 text-cyan-800",
  [EventTypes.order_fulfilled]: "bg-emerald-100 text-emerald-800",
  [EventTypes.order_cancelled]: "bg-red-100 text-red-800",
  [EventTypes.shipment_purchased]: "bg-blue-100 text-blue-800",
  [EventTypes.shipment_cancelled]: "bg-red-100 text-red-800",
  [EventTypes.shipment_fulfilled]: "bg-purple-100 text-purple-800",
  [EventTypes.tracker_created]: "bg-orange-100 text-orange-800",
  [EventTypes.tracker_updated]: "bg-yellow-100 text-yellow-800",
  default: "bg-slate-100 text-slate-800",
};

const EVENT_TYPE_ICONS = {
  shipment: <Package className="h-4 w-4" />,
  tracker: <Truck className="h-4 w-4" />,
  order: <Calendar className="h-4 w-4" />,
  webhook: <Webhook className="h-4 w-4" />,
  default: <AlertCircle className="h-4 w-4" />,
};

const EventDetailViewer = ({ event }: { event: any }) => {
  if (!event) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400 bg-white">
        <div className="text-center">
          <svg className="h-12 w-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          <p className="text-sm text-gray-500">Select an event to view details</p>
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

  return (
    <div className="h-full flex flex-col bg-white">
      <div className="px-4 py-3 border-b border-gray-200 bg-gray-50 flex-shrink-0">
        <div className="flex items-center gap-3 mb-2">
          <span className="text-xs text-gray-500">Event Details</span>
        </div>
        <div className="flex items-center gap-3 min-w-0 flex-1 overflow-hidden mb-3">
          {getEventTypeIcon(event.type as EventTypes | null)}
          <span className="text-sm font-medium text-gray-900 truncate">{event.type}</span>
          <Badge className={`${getEventTypeColor(event.type as EventTypes | null)} border-none text-xs`}>
            {event.type}
          </Badge>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 min-w-0 flex-1">
            <code className="text-xs bg-gray-100 px-2 py-1 rounded font-mono">
              ID: {event.id}
            </code>
            <span className="text-xs text-gray-500">
              {formatDateTimeLong(event.created_at)}
            </span>
          </div>
          <div className="flex items-center gap-2 flex-shrink-0">
            <button
              onClick={() => navigator.clipboard.writeText(JSON.stringify(event.data, null, 2))}
              className="text-xs text-blue-600 hover:text-blue-800 px-2 py-1 rounded hover:bg-blue-50 whitespace-nowrap"
            >
              Copy Data
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <Label className="font-medium">Event ID</Label>
              <p className="text-slate-600 font-mono">{event.id}</p>
            </div>
            <div>
              <Label className="font-medium">Timestamp</Label>
              <p className="text-slate-600">{formatDateTimeLong(event.created_at)}</p>
            </div>
            <div>
              <Label className="font-medium">Test Mode</Label>
              <p className="text-slate-600">{event.test_mode ? "Yes" : "No"}</p>
            </div>
            <div>
              <Label className="font-medium">Pending Webhooks</Label>
              <p className="text-slate-600">{event.pending_webhooks || 0}</p>
            </div>
          </div>

          {event.data && (
            <div>
              <Label className="font-medium">Event Data</Label>
              <div className="mt-1 border rounded-md overflow-hidden">
                <CodeMirror
                  value={JSON.stringify(event.data, null, 2)}
                  extensions={[json()]}
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
          )}
        </div>
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
        "p-4 border-b border-gray-200 cursor-pointer transition-all duration-150 hover:bg-gray-50",
        isSelected ? "bg-gray-50 border-l-4 border-l-gray-400" : "border-l-4 border-l-transparent"
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
              {event.id && (
                <code className="text-xs bg-slate-100 px-2 py-1 rounded truncate">
                  {event.id}
                </code>
              )}
            </div>
            <div className="text-sm text-slate-600 truncate">
              Event ID: {event.id}
            </div>
          </div>
          <div className="text-xs text-slate-500 flex-shrink-0">
            {formatDateTimeLong(event.created_at)}
          </div>
        </div>
      </div>
    </div>
  );
};

export function EventsView() {
  const [selectedEvent, setSelectedEvent] = useState<any>(null);

  // Use the proper events hook without initial filters - let the hook manage the state
  const eventsContext = useEvents();
  const { query, filter, setFilter } = eventsContext;

  const events = query.data?.events?.edges?.map(edge => edge.node) || [];

  const updateFilter = (extra: any = {}) => {
    const newFilter = {
      ...filter,
      ...extra,
      offset: extra.offset || 0,
    };
    setFilter(newFilter);
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
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="px-4 py-3 border-b border-slate-200">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Events</h2>
          </div>
          <div className="flex items-center gap-2">
            {/* Use the proper EventsFilter component */}
            <EventsFilter context={eventsContext} />
            <Button size="sm" onClick={handleRefresh} disabled={query.isLoading}>
              <RefreshCw className={`h-4 w-4 mr-2 ${query.isLoading ? 'animate-spin' : ''}`} />
              Refresh
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

      {/* Mobile Layout */}
      <div className="lg:hidden flex-1 overflow-auto">
        {query.isLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-6 w-6 border-2 border-slate-300 border-t-slate-600"></div>
          </div>
        ) : events.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-slate-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM15 17H9a4 4 0 01-4-4V8a4 4 0 014-4h6a4 4 0 014 4v5l-4 4z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-slate-900 mb-2">No events found</h3>
            <p className="text-slate-500">No events match your current filters.</p>
            {hasActiveFilters() && (
              <p className="text-xs mt-1">Try adjusting your filters</p>
            )}
          </div>
        ) : (
          <div>
            {events.map((event) => (
              <EventListItem
                key={event.id}
                event={event}
                isSelected={selectedEvent?.id === event.id}
                onSelect={setSelectedEvent}
              />
            ))}

            {/* Pagination */}
            {query.data?.events?.page_info && (
              <div className="flex items-center justify-between px-4 py-3 border-t bg-slate-50">
                <div className="text-sm text-slate-500">
                  Showing {events.length} events
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    disabled={!query.data.events.page_info.has_previous_page}
                    onClick={() => updateFilter({ offset: Math.max(0, (filter.offset || 0) - 20) })}
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    disabled={!query.data.events.page_info.has_next_page}
                    onClick={() => updateFilter({ offset: (filter.offset || 0) + 20 })}
                  >
                    Next
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Mobile Detail Modal */}
        {selectedEvent && (
          <div className="fixed inset-0 z-50 bg-white">
            <div className="h-full flex flex-col">
              <div className="flex items-center justify-between p-4 border-b border-gray-200">
                <h3 className="font-medium text-gray-900">{selectedEvent.type}</h3>
                <button
                  onClick={() => setSelectedEvent(null)}
                  className="p-1 hover:bg-gray-100 rounded text-gray-400 hover:text-gray-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <div className="flex-1">
                <EventDetailViewer event={selectedEvent} />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Desktop Layout - Side by Side */}
      <div className="hidden lg:flex flex-1 bg-white overflow-hidden">
        {/* Left Panel - Events List */}
        <div className="w-1/2 border-r border-gray-200 flex flex-col h-full">
          <div className="flex-1 overflow-y-auto bg-white">
            {query.isLoading ? (
              <div className="flex items-center justify-center h-32">
                <div className="animate-spin rounded-full h-6 w-6 border-2 border-slate-300 border-t-slate-600"></div>
              </div>
            ) : events.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-slate-400 mb-4">
                  <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM15 17H9a4 4 0 01-4-4V8a4 4 0 014-4h6a4 4 0 014 4v5l-4 4z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-slate-900 mb-2">No events found</h3>
                <p className="text-slate-500">No events match your current filters.</p>
                {hasActiveFilters() && (
                  <p className="text-xs mt-1">Try adjusting your filters</p>
                )}
              </div>
            ) : (
              events.map((event) => (
                <EventListItem
                  key={event.id}
                  event={event}
                  isSelected={selectedEvent?.id === event.id}
                  onSelect={setSelectedEvent}
                />
              ))
            )}
          </div>

          {/* Pagination */}
          {query.data?.events?.page_info && (
            <div className="flex items-center justify-between px-4 py-3 border-t bg-slate-50 flex-shrink-0">
              <div className="text-sm text-slate-500">
                Showing {events.length} events
              </div>
              <div className="flex space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={!query.data.events.page_info.has_previous_page}
                  onClick={() => updateFilter({ offset: Math.max(0, (filter.offset || 0) - 20) })}
                >
                  Previous
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={!query.data.events.page_info.has_next_page}
                  onClick={() => updateFilter({ offset: (filter.offset || 0) + 20 })}
                >
                  Next
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Right Panel - Event Details */}
        <div className="w-1/2 h-full overflow-hidden">
          <EventDetailViewer event={selectedEvent} />
        </div>
      </div>
    </div>
  );
}
