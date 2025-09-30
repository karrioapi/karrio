"use client";

import { Dialog, DialogContent, DialogTitle } from "@karrio/ui/components/ui/dialog";
import { VisuallyHidden } from "@radix-ui/react-visually-hidden";
import { Command, CommandEmpty, CommandGroup, CommandItem, CommandList } from "@karrio/ui/components/ui/command";
import { StatusBadge } from '@karrio/ui/core/components/status-badge';
import { formatAddressShort, isNoneOrEmpty } from '@karrio/lib';
import { AppLink } from '@karrio/ui/core/components/app-link';
import { useSearch } from '@karrio/hooks/search';
import { Search, Loader2, Package, MapPin, X } from "lucide-react";
import React, { useEffect, useState, useRef } from "react";
import moment from 'moment';

interface SearchModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function SearchModal({ open, onOpenChange }: SearchModalProps) {
  const { query, setFilter } = useSearch();
  const [searchValue, setSearchValue] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setFilter({ keyword: searchValue });
  }, [searchValue, setFilter]);

  useEffect(() => {
    if (open && inputRef.current) {
      inputRef.current.focus();
    }
  }, [open]);

  const clear = () => {
    setSearchValue("");
    inputRef.current?.focus();
  };

  const handleResultClick = () => {
    onOpenChange(false);
    setSearchValue("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onOpenChange(false);
    }
  };

  const isLoading = query.isFetching && searchValue.length >= 2;
  const hasResults = !isNoneOrEmpty(searchValue) && searchValue.length >= 2 && (query.data?.results || []).length > 0;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl p-4 pb-8 gap-0">
        <VisuallyHidden>
          <DialogTitle>Search</DialogTitle>
        </VisuallyHidden>
        <div className="flex items-center border-b px-4 py-4">
          <Search className="mr-3 h-5 w-5 text-gray-400" />
          <input
            ref={inputRef}
            type="text"
            placeholder="Search shipments, orders, tracking numbers..."
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 bg-transparent text-sm outline-none placeholder:text-gray-500"
          />
          {isLoading && (
            <Loader2 className="ml-2 h-4 w-4 animate-spin text-gray-400" />
          )}
          {searchValue && !isLoading && (
            <button
              onClick={clear}
              className="ml-2 p-1 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>

        <Command className="max-h-[400px]" shouldFilter={false}>
          <CommandList>
            {isLoading ? (
              <CommandEmpty>
                <div className="flex items-center justify-center py-8">
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
      </DialogContent>
    </Dialog>
  );
}
