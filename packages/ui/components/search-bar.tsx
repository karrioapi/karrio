"use client";

import { Command, CommandEmpty, CommandGroup, CommandItem, CommandList } from "@karrio/ui/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@karrio/ui/components/ui/popover";
import { StatusBadge } from '@karrio/ui/core/components/status-badge';
import { formatAddressShort, isNoneOrEmpty } from '@karrio/lib';
import { AppLink } from '@karrio/ui/core/components/app-link';
import { useSearch } from '@karrio/hooks/search';
import { Search, Loader2, Package, MapPin, X } from "lucide-react";
import React, { useEffect, useState, useRef } from "react";
import moment from 'moment';

export function SearchBar() {
  const { query, setFilter } = useSearch();
  const [searchValue, setSearchValue] = useState<string>("");
  const [open, setOpen] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setFilter({ keyword: searchValue });
    if (searchValue && searchValue.length >= 2) {
      setOpen(true);
    } else {
      setOpen(false);
    }
  }, [searchValue, setFilter]);

  const clear = () => {
    setSearchValue("");
    setOpen(false);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setOpen(false);
      inputRef.current?.blur();
    }
  };

  const handleResultClick = () => {
    setOpen(false);
    setSearchValue("");
    inputRef.current?.blur();
  };

  const handleFocus = () => {
    setIsFocused(true);
    if (searchValue && searchValue.length >= 2) {
      setOpen(true);
    }
  };

  const handleBlur = () => {
    setIsFocused(false);
    // Delay closing to allow clicking on results
    setTimeout(() => {
      if (!containerRef.current?.contains(document.activeElement)) {
        setOpen(false);
      }
    }, 150);
  };

  const isLoading = query.isFetching && searchValue.length >= 2;
  const hasResults = !isNoneOrEmpty(searchValue) && searchValue.length >= 2 && (query.data?.results || []).length > 0;

  return (
    <div className="relative w-full max-w-md min-w-[300px]" ref={containerRef}>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <div className="relative">
            <div className={`
                            relative flex items-center rounded-lg transition-all duration-200
                            ${isFocused ? 'bg-white ring-2 ring-blue-500 shadow-sm' : 'bg-gray-100 hover:bg-gray-200'}
                        `}>
              <Search className="absolute left-3 h-4 w-4 text-gray-500 pointer-events-none" />
              <input
                ref={inputRef}
                type="text"
                placeholder="Search..."
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onFocus={handleFocus}
                onBlur={handleBlur}
                onKeyDown={handleKeyDown}
                className="
                                    w-full h-10 pl-10 pr-10 bg-transparent border-0 outline-none
                                    text-sm placeholder:text-gray-500 text-gray-900
                                "
              />
              <div className="absolute right-3 flex items-center">
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin text-gray-400" />
                ) : searchValue ? (
                  <button
                    onClick={clear}
                    className="h-4 w-4 text-gray-400 hover:text-gray-600 transition-colors"
                    type="button"
                  >
                    <X className="h-4 w-4" />
                  </button>
                ) : null}
              </div>
            </div>
          </div>
        </PopoverTrigger>

        <PopoverContent
          className="w-[400px] p-0 mt-1"
          align="start"
          side="bottom"
          sideOffset={4}
          onOpenAutoFocus={(e) => e.preventDefault()}
        >
          <Command shouldFilter={false}>
            <CommandList className="max-h-80">
              {isLoading ? (
                <CommandEmpty>
                  <div className="flex items-center justify-center py-6">
                    <Loader2 className="h-4 w-4 animate-spin mr-2 text-gray-400" />
                    <span className="text-sm text-gray-600">Searching...</span>
                  </div>
                </CommandEmpty>
              ) : hasResults ? (
                <CommandGroup>
                  {(query.data?.results || []).slice(0, 8).map((result, key) => (
                    <React.Fragment key={key}>
                      {(result as any).recipient && (
                        <CommandItem className="p-0" onSelect={handleResultClick}>
                          <AppLink
                            href={`/shipments/${result.id}`}
                            className="flex items-center w-full px-4 py-3 text-sm hover:bg-gray-50 transition-colors"
                          >
                            <div className="flex items-center justify-center w-8 h-8 bg-blue-50 rounded-lg mr-3">
                              <Package className="h-4 w-4 text-blue-600" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="font-medium text-gray-900 truncate">
                                {formatAddressShort((result as any).recipient)}
                              </div>
                              <div className="text-xs text-gray-500">Shipment</div>
                            </div>
                            <div className="flex items-center gap-2 ml-3">
                              <StatusBadge status={result.status as string} className="text-xs" />
                              <span className="text-xs text-gray-500 whitespace-nowrap">
                                {moment(result.created_at).format("MMM D")}
                              </span>
                            </div>
                          </AppLink>
                        </CommandItem>
                      )}
                      {(result as any).shipping_to && (
                        <CommandItem className="p-0" onSelect={handleResultClick}>
                          <AppLink
                            href={`/orders/${result.id}`}
                            className="flex items-center w-full px-4 py-3 text-sm hover:bg-gray-50 transition-colors"
                          >
                            <div className="flex items-center justify-center w-8 h-8 bg-green-50 rounded-lg mr-3">
                              <Package className="h-4 w-4 text-green-600" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="font-medium text-gray-900 truncate">
                                {formatAddressShort((result as any).shipping_to)}
                              </div>
                              <div className="text-xs text-gray-500">Order</div>
                            </div>
                            <div className="flex items-center gap-2 ml-3">
                              <StatusBadge status={result.status as string} className="text-xs" />
                              <span className="text-xs text-gray-500 whitespace-nowrap">
                                {moment(result.created_at).format("MMM D")}
                              </span>
                            </div>
                          </AppLink>
                        </CommandItem>
                      )}
                      {(!(result as any).shipping_to && !(result as any).recipient) && (
                        <CommandItem className="p-0" onSelect={handleResultClick}>
                          <a
                            href={`/tracking/${result.id}`}
                            className="flex items-center w-full px-4 py-3 text-sm hover:bg-gray-50 transition-colors"
                          >
                            <div className="flex items-center justify-center w-8 h-8 bg-orange-50 rounded-lg mr-3">
                              <MapPin className="h-4 w-4 text-orange-600" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="font-medium text-gray-900 truncate">
                                {(result as any).tracking_number}
                              </div>
                              <div className="text-xs text-gray-500">Tracker</div>
                            </div>
                            <div className="flex items-center gap-2 ml-3">
                              <StatusBadge status={result.status as string} className="text-xs" />
                              <span className="text-xs text-gray-500 whitespace-nowrap">
                                {moment(result.created_at).format("MMM D")}
                              </span>
                            </div>
                          </a>
                        </CommandItem>
                      )}
                    </React.Fragment>
                  ))}
                </CommandGroup>
              ) : (
                <CommandEmpty>
                  <div className="py-8 text-center">
                    <div className="text-sm text-gray-500">
                      {isNoneOrEmpty(searchValue) ? "Start typing to search..." :
                        searchValue.length < 2 ? "Type at least 2 characters..." :
                          "No results found."}
                    </div>
                    {searchValue.length >= 2 && !isLoading && (
                      <div className="text-xs text-gray-400 mt-1">
                        Try searching for shipments, orders, or tracking numbers
                      </div>
                    )}
                  </div>
                </CommandEmpty>
              )}
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}
