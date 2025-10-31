"use client";

import React, { useState } from "react";
import { RefreshCw, Calendar, Package, Truck, Webhook, AlertCircle, X, Filter, Copy, Activity } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { formatDateTimeLong } from "@karrio/lib";
import { useEvents } from "@karrio/hooks/event";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";
import { EventTypes, EVENT_TYPES } from "@karrio/types";
import { cn } from "@karrio/ui/lib/utils";

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
  shipment: <Package className="h-4 w-4" />,
  tracker: <Truck className="h-4 w-4" />,
  order: <Calendar className="h-4 w-4" />,
  webhook: <Webhook className="h-4 w-4" />,
  default: <AlertCircle className="h-4 w-4" />,
};

const EventDetailViewer = ({ event }: { event: any }) => {
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
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

  return (
    <div className="h-full flex flex-col bg-[#0f0c24]">
      {/* Header */}
      <div className="border-b border-neutral-800 px-4 py-3 flex-shrink-0">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            {getEventTypeIcon(event.type as EventTypes | null)}
            <Badge className={getEventTypeColor(event.type as EventTypes | null)}>
              {event.type}
            </Badge>
          </div>
          <div className="text-xs text-neutral-400">
            {formatDateTimeLong(event.created_at)}
          </div>
        </div>
        <div className="text-sm font-medium truncate text-neutral-200">
          Event: {event.type}
        </div>
        <div className="text-xs text-neutral-400 mt-1">
          ID: {event.id} • Test: {event.test_mode ? "Yes" : "No"}
        </div>
      </div>

      {/* Event Content */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-4">
          {event.data && (
            <div className="mb-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-neutral-300">Event Data</span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => copyToClipboard(JSON.stringify(event.data, null, 2))}
                  className="h-7 px-2 border-neutral-800 text-neutral-300 hover:bg-purple-900/20"
                >
                  <Copy className="h-3 w-3" />
                </Button>
              </div>
              <div className="border border-neutral-800 rounded-md overflow-hidden">
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
        "p-4 border-b border-neutral-800 cursor-pointer transition-all duration-150 hover:bg-purple-900/10",
        isSelected ? "bg-purple-900/20 border-l-4 border-l-purple-800/60" : "border-l-4 border-l-transparent"
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
            <div className="text-sm text-neutral-200 truncate font-mono">
              {event.type}
            </div>
            <div className="text-xs text-neutral-400 truncate">
              ID: {event.id} • Test: {event.test_mode ? "Yes" : "No"}
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
          <div className="absolute right-0 top-full mt-1 w-80 bg-white border border-gray-200 rounded-md shadow-lg z-20">
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-medium text-sm">Filter Events</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsOpen(false)}
                  className="h-6 w-6 p-0"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>

              <div className="space-y-4">
                {/* Search */}
                <div>
                  <Label htmlFor="search" className="text-sm font-medium">Search</Label>
                  <Input
                    id="search"
                    placeholder="Search events..."
                    value={tempFilters.query || ""}
                    onChange={(e) => handleTempFilterChange('query', e.target.value)}
                    className="mt-1"
                  />
                </div>

                {/* Event Type */}
                <div>
                  <Label htmlFor="type" className="text-sm font-medium">Event Type</Label>
                  <Select
                    value={tempFilters.type?.[0] || "all"}
                    onValueChange={(value) => handleTempFilterChange('type', value === 'all' ? undefined : [value])}
                  >
                    <SelectTrigger className="w-full mt-1">
                      <SelectValue placeholder="All event types" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All event types</SelectItem>
                      {EVENT_TYPES.map((type) => (
                        <SelectItem key={type} value={type}>{type}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Entity ID */}
                <div>
                  <Label htmlFor="entity_id" className="text-sm font-medium">Related Object ID</Label>
                  <Input
                    id="entity_id"
                    placeholder="e.g: shp_123456"
                    value={tempFilters.entity_id || ""}
                    onChange={(e) => handleTempFilterChange('entity_id', e.target.value)}
                    className="mt-1"
                  />
                </div>

              </div>

              <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleClear}
                  disabled={!hasActiveFilters() && Object.keys(tempFilters).length === 0}
                >
                  Clear All
                </Button>
                <div className="flex gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setIsOpen(false)}
                  >
                    Cancel
                  </Button>
                  <Button
                    size="sm"
                    onClick={handleApply}
                    disabled={query.isLoading}
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
    <div className="h-full flex overflow-hidden bg-[#0f0c24]">
      {/* Left Panel - Events List */}
      <div className="w-1/2 border-r border-neutral-800 flex flex-col lg:flex hidden h-full">
        {/* Header */}
        <div className="border-b border-neutral-800 px-4 py-3 flex-shrink-0">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold">Events</h2>
            <div className="flex items-center gap-2">
              {/* Use the custom EventsFilterDropdown component */}
              <EventsFilterDropdown context={eventsContext} />
              <Button
                variant="outline"
                size="sm"
                onClick={handleRefresh}
                disabled={query.isFetching}
                className="text-white border-neutral-800 hover:bg-neutral-800/40"
              >
                <RefreshCw className={`h-4 w-4 text-white ${query.isFetching ? 'animate-spin' : ''}`} />
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
              <RefreshCw className="h-6 w-6 animate-spin text-neutral-500" />
            </div>
          )}

          {!query.isFetching && events.length === 0 && (
            <div className="text-center py-8 text-neutral-400">
              <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No events found</p>
              {hasActiveFilters() && (
                <p className="text-xs mt-1 text-neutral-500">Try adjusting your filters</p>
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
          <div className="border-t border-neutral-800 px-4 py-2 flex items-center justify-between text-sm flex-shrink-0">
            <span className="text-neutral-400">
              Showing {((filter.offset as number) || 0) + 1}-{((filter.offset as number) || 0) + events.length}
              {query.data?.events?.page_info.has_next_page && " of many"}
            </span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => updateFilter({ offset: Math.max(0, ((filter.offset as number) || 0) - 20) })}
                disabled={(filter.offset as number) === 0 || filter.offset === undefined}
                className="h-7 px-2 text-xs text-white border-neutral-800 hover:bg-neutral-800/40"
              >
                Previous
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => updateFilter({ offset: ((filter.offset as number) || 0) + 20 })}
                disabled={!query.data?.events?.page_info.has_next_page}
                className="h-7 px-2 text-xs text-white border-neutral-800 hover:bg-neutral-800/40"
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
            <div className="border-b px-4 py-2 flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSelectedEvent(null)}
              >
                ← Back
              </Button>
              <span className="text-sm font-medium">Event Details</span>
            </div>
            <div className="flex-1">
              <EventDetailViewer event={selectedEvent} />
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col">
            {/* Mobile Header */}
            <div className="border-b border-neutral-800 px-4 py-3">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-lg font-semibold">Events</h2>
                <div className="flex items-center gap-2">
                  {/* Use the custom EventsFilterDropdown component for mobile */}
                  <EventsFilterDropdown context={eventsContext} />
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleRefresh}
                    disabled={query.isFetching}
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
                  <RefreshCw className="h-6 w-6 animate-spin text-neutral-500" />
                </div>
              )}

              {!query.isFetching && events.length === 0 && (
                <div className="text-center py-8 text-neutral-400">
                  <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No events found</p>
                  {hasActiveFilters() && (
                    <p className="text-xs mt-1 text-neutral-500">Try adjusting your filters</p>
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
              <div className="border-t border-neutral-800 px-4 py-2 flex items-center justify-between text-sm">
                <span className="text-neutral-400">
                  Showing {((filter.offset as number) || 0) + 1}-{((filter.offset as number) || 0) + events.length}
                  {query.data?.events?.page_info.has_next_page && " of many"}
                </span>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => updateFilter({ offset: Math.max(0, ((filter.offset as number) || 0) - 20) })}
                    disabled={(filter.offset as number) === 0 || filter.offset === undefined}
                    className="h-7 px-2 text-xs text-white border-neutral-800 hover:bg-neutral-800/40"
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => updateFilter({ offset: ((filter.offset as number) || 0) + 20 })}
                    disabled={!query.data?.events?.page_info.has_next_page}
                    className="h-7 px-2 text-xs text-white border-neutral-800 hover:bg-neutral-800/40"
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