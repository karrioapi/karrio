"use client";

import * as React from "react";
import { Search, Loader2, Package, Truck, Inbox, X, Navigation } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandList,
} from "@karrio/ui/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverAnchor,
} from "@karrio/ui/components/ui/popover";
import { StatusBadge } from '@karrio/ui/core/components/status-badge';
import { AppLink } from '@karrio/ui/core/components/app-link';
import { useSearch } from '@karrio/hooks/search';
import { formatAddressShort, isNoneOrEmpty } from '@karrio/lib';
import moment from 'moment';

interface SearchResult {
  id: string;
  type: 'shipment' | 'order' | 'tracker';
  title: string;
  subtitle?: string;
  status?: string;
  date?: string;
  href: string;
}

interface SearchBarProps {
  placeholder?: string;
  className?: string;
  maxWidth?: string;
}

export const SearchBar = React.forwardRef<
  HTMLInputElement,
  SearchBarProps
>(({
  placeholder = "Search shipments, orders, tracking...",
  className,
  maxWidth = "max-w-md"
}, ref) => {
  const [open, setOpen] = React.useState(false);
  const [inputValue, setInputValue] = React.useState("");
  const inputRef = React.useRef<HTMLInputElement>(null);

  // Use search hook
  const { query: searchQuery, setFilter } = useSearch();

  // Simple debouncing - just like AddressCombobox
  const [debouncedValue, setDebouncedValue] = React.useState("");

  React.useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(inputValue);
    }, 300);

    return () => clearTimeout(timer);
  }, [inputValue]);

  // Update search filter when debouncedValue changes
  React.useEffect(() => {
    if (debouncedValue.trim()) {
      setFilter({ keyword: debouncedValue.trim() });
    } else {
      setFilter({});
    }
  }, [debouncedValue, setFilter]);

  const isLoading = React.useMemo(() => {
    return debouncedValue.trim() !== "" && searchQuery.isFetching;
  }, [debouncedValue, searchQuery.isFetching]);

  // Transform search results
  const searchResults = React.useMemo((): SearchResult[] => {
    if (!searchQuery.data || !debouncedValue.trim()) return [];

    const data = searchQuery.data as any;
    const results: SearchResult[] = [];

    if (data.results) {
      data.results.slice(0, 10).forEach((item: any) => {
        // Shipments have recipient field
        if (item.recipient) {
          results.push({
            id: item.id,
            type: 'shipment',
            title: `Shipment ${item.tracking_number || item.id}`,
            subtitle: formatAddressShort(item.recipient),
            status: item.status,
            date: item.created_at,
            href: `/shipments/${item.id}`,
          });
        } 
        // Orders have shipping_to field
        else if (item.shipping_to) {
          results.push({
            id: item.id,
            type: 'order',
            title: `Order ${item.order_id || item.id}`,
            subtitle: formatAddressShort(item.shipping_to),
            status: item.status,
            date: item.created_at,
            href: `/orders/${item.id}`,
          });
        } 
        // Trackers have neither recipient nor shipping_to
        else {
          results.push({
            id: item.id,
            type: 'tracker',
            title: `Tracking ${item.tracking_number || item.id}`,
            subtitle: item.delivered_to ? formatAddressShort(item.delivered_to) : undefined,
            status: item.status,
            date: item.created_at,
            href: `/tracking/${item.id}`, // Note: /tracking not /trackers
          });
        }
      });
    }

    return results;
  }, [searchQuery.data, debouncedValue]);

  const handleInputValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInputValue(newValue);

    // Show dropdown if we have results
    if (newValue.trim() && searchResults.length > 0) {
      setOpen(true);
    }
  };

  const handleInputFocus = () => {
    if (inputValue.trim() && searchResults.length > 0) {
      setOpen(true);
    }
  };

  const handleInputBlur = (e: React.FocusEvent) => {
    // Only close if focus is not moving to the popover content
    const relatedTarget = e.relatedTarget as HTMLElement;
    if (!relatedTarget || !relatedTarget.closest('[data-radix-popper-content-wrapper]')) {
      setOpen(false);
    }
  };

  const handleClear = () => {
    setInputValue("");
    setOpen(false);
    // Return focus to input after clearing
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      setOpen(false);
      inputRef.current?.blur();
    }
  };

  const getResultIcon = (type: SearchResult['type']) => {
    switch (type) {
      case 'shipment':
        return <Truck className="h-4 w-4" />; // fas fa-truck
      case 'order':
        return <Inbox className="h-4 w-4" />; // fas fa-inbox
      case 'tracker':
        return <Navigation className="h-4 w-4" />; // fas fa-location-arrow
      default:
        return <Package className="h-4 w-4" />;
    }
  };

  // Combine refs
  React.useImperativeHandle(ref, () => inputRef.current!, []);

  return (
    <div className={cn("w-full", maxWidth)}>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverAnchor asChild>
          <div className={cn(
            "flex h-8 w-full items-center rounded-md bg-gray-100 hover:bg-gray-200 focus-within:bg-white focus-within:ring-2 focus-within:ring-blue-500 transition-all duration-200",
            className
          )}>
            <Search className="ml-3 h-4 w-4 text-gray-500 pointer-events-none flex-shrink-0" />
            <input
              ref={inputRef}
              value={inputValue}
              onChange={handleInputValueChange}
              onFocus={handleInputFocus}
              onBlur={handleInputBlur}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              className="flex-1 bg-transparent border-0 px-3 py-2 text-sm placeholder:text-gray-500 focus:outline-none focus:ring-0 disabled:cursor-not-allowed disabled:opacity-50"
              autoComplete="off"
              data-lpignore="true"
              data-form-type="search"
            />
            <div className="mr-3 flex items-center">
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
              ) : inputValue ? (
                <button
                  type="button"
                  onClick={handleClear}
                  className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                  tabIndex={-1}
                >
                  <X className="h-4 w-4 text-gray-400 hover:text-gray-600" />
                </button>
              ) : null}
            </div>
          </div>
        </PopoverAnchor>

        <PopoverContent
          className="w-full p-0"
          align="start"
          side="bottom"
          sideOffset={4}
          onOpenAutoFocus={(e) => e.preventDefault()}
          style={{ width: 'var(--radix-popover-trigger-width)' }}
        >
          <Command shouldFilter={false}>
            <CommandList>
              {searchResults.length === 0 && debouncedValue.trim() && !isLoading && (
                <CommandEmpty>No results found.</CommandEmpty>
              )}

              {searchResults.length > 0 && (
                <CommandGroup>
                  {searchResults.map((result) => (
                    <CommandItem
                      key={`${result.type}-${result.id}`}
                      value={result.title}
                      onSelect={() => setOpen(false)}
                      onMouseDown={(e) => e.preventDefault()}
                    >
                      <AppLink href={result.href} className="flex items-center gap-3 p-3 hover:bg-gray-50 w-full">
                        <div className="flex-shrink-0 text-gray-400">
                          {getResultIcon(result.type)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {result.title}
                            </p>
                            {result.status && (
                              <StatusBadge status={result.status} />
                            )}
                          </div>
                          {result.subtitle && (
                            <p className="text-xs text-gray-500 truncate mt-1">
                              {result.subtitle}
                            </p>
                          )}
                          {result.date && (
                            <p className="text-xs text-gray-400 mt-1">
                              {moment(result.date).fromNow()}
                            </p>
                          )}
                        </div>
                      </AppLink>
                    </CommandItem>
                  ))}
                </CommandGroup>
              )}
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
});

SearchBar.displayName = "SearchBar";
