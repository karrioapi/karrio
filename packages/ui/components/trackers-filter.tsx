"use client";

import React, { useReducer, useEffect, useState } from 'react';
import { Filter } from "lucide-react";
import { CARRIER_NAMES, TRACKER_STATUSES } from '@karrio/types';
import { useTrackers } from '@karrio/hooks/tracker';
import { isNone } from '@karrio/lib';
import { Button } from "@karrio/ui/components/ui/button";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@karrio/ui/components/ui/popover";
import { Separator } from "@karrio/ui/components/ui/separator";
import { cn } from "@karrio/ui/lib/utils";

interface TrackersFilterComponent {
  context: ReturnType<typeof useTrackers>;
}

export const TrackersFilter = ({ context }: TrackersFilterComponent): JSX.Element => {
  const [isReady, setIsReady] = useState(true);
  const [open, setOpen] = useState(false);
  const { query, filter: variables, setFilter } = context;
  
  const [filters, dispatch] = useReducer((state: any, { name, checked, value }: { name: string, checked?: boolean, value?: string | boolean | object }) => {
    switch (name) {
      case 'clear':
        return {};
      case 'full':
        return { ...(value as typeof variables) };

      case 'hasStatus':
        if (checked) return { ...state, status: [] };
        return Object.keys(state).reduce((acc, key) => key === 'status' ? acc : { ...acc, [key]: state[key] }, {});
      case 'status':
        return checked
          ? { ...state, status: [...(new Set([...state.status, value]) as any)] }
          : { ...state, status: state.status.filter((item: string) => item !== value) };

      case 'hasCarrierName':
        if (checked) return { ...state, carrier_name: [] };
        return Object.keys(state).reduce((acc, key) => key === 'carrier_name' ? acc : { ...acc, [key]: state[key] }, {});
      case 'carrier_name':
        return checked
          ? { ...state, carrier_name: [...(new Set([...state.carrier_name, value]) as any)] }
          : { ...state, carrier_name: state.carrier_name.filter((item: string) => item !== value) };

      case 'hasDate':
        if (checked) return { ...state, created_before: "", created_after: "" };
        return Object.keys(state).reduce((acc, key) => ["created_before", "created_after"].includes(key) ? acc : { ...acc, [key]: state[key] }, {});

      default:
        return { ...state, [name]: value };
    }
  }, variables, () => variables);

  const handleChange = (name: string, value: string | boolean, checked?: boolean) => {
    dispatch({ name, value, checked });
  };

  const handleClear = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    event.preventDefault();
    setIsReady(false);
    dispatch({ name: 'clear' });
    setTimeout(() => {
      setIsReady(true);
    }, 200);
  };

  const handleApply = async (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    event.preventDefault();
    setFilter({ ...filters, offset: 0 });
    setOpen(false);
  };

  const variablesKey = JSON.stringify(variables);
  useEffect(() => {
    dispatch({ name: 'full', value: variables })
  }, [variablesKey]);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" className="mx-1">
          <Filter className="mr-2 h-4 w-4" />
          <span className="font-bold">Filter</span>
        </Button>
      </PopoverTrigger>
      
      <PopoverContent 
        className="w-80 max-h-[80vh] overflow-y-auto p-0" 
        align="end"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b bg-gray-50">
          <Button variant="outline" size="sm" onClick={handleClear}>
            Clear
          </Button>
          <span className="text-sm font-semibold">Filters</span>
          <Button
            size="sm"
            disabled={query.isFetching}
            onClick={handleApply}
            className={cn(query.isFetching && "opacity-50")}
          >
            {query.isFetching ? "Loading..." : "Done"}
          </Button>
        </div>

        {!isReady ? (
          <div className="p-4 text-center">
            <div className="animate-pulse">Loading...</div>
          </div>
        ) : (
          <div className="p-0">
            {/* Keyword Search */}
            <div className="px-4 py-2">
              <Label htmlFor="keyword" className="text-sm font-medium">
                Search
              </Label>
              <Input
                id="keyword"
                placeholder="Tracking number, ID..."
                value={filters?.keyword || ''}
                onChange={(e) => handleChange('keyword', e.target.value)}
                className="mt-1 text-sm h-8"
              />
            </div>

            <Separator />

            {/* Date Filter */}
            <div className="px-4 py-2">
              <div className="flex items-center space-x-2 mb-1">
                <Checkbox
                  id="hasDate"
                  checked={!isNone(filters?.created_before) || !isNone(filters?.created_after)}
                  onCheckedChange={(checked) => handleChange('hasDate', '', checked as boolean)}
                />
                <Label htmlFor="hasDate" className="text-sm font-medium">
                  Date
                </Label>
              </div>
              
              {(!isNone(filters?.created_before) || !isNone(filters?.created_after)) && (
                <div className="ml-5 p-2 bg-gray-50 rounded space-y-2">
                  <div>
                    <Label htmlFor="created_after" className="text-xs text-gray-600 mb-1 block">
                      After
                    </Label>
                    <Input
                      id="created_after"
                      type="datetime-local"
                      value={filters?.created_after || ''}
                      onChange={(e) => handleChange('created_after', e.target.value)}
                      className="text-sm h-8"
                    />
                  </div>
                  <div>
                    <Label htmlFor="created_before" className="text-xs text-gray-600 mb-1 block">
                      Before
                    </Label>
                    <Input
                      id="created_before"
                      type="datetime-local"
                      value={filters?.created_before || ''}
                      onChange={(e) => handleChange('created_before', e.target.value)}
                      className="text-sm h-8"
                    />
                  </div>
                </div>
              )}
            </div>

            <Separator />

            {/* Carrier Filter */}
            <div className="px-4 py-2">
              <div className="flex items-center space-x-2 mb-1">
                <Checkbox
                  id="hasCarrierName"
                  checked={!isNone(filters?.carrier_name)}
                  onCheckedChange={(checked) => handleChange('hasCarrierName', '', checked as boolean)}
                />
                <Label htmlFor="hasCarrierName" className="text-sm font-medium">
                  Carrier
                </Label>
              </div>
              
              {!isNone(filters?.carrier_name) && (
                <div className="ml-5 bg-gray-50 rounded">
                  {CARRIER_NAMES.map((carrier_name: string, index) => (
                    <div key={index} className="flex items-center space-x-2 py-0.5 px-2">
                      <Checkbox
                        id={`carrier_${index}`}
                        checked={filters?.carrier_name?.includes(carrier_name) || false}
                        onCheckedChange={(checked) => 
                          handleChange('carrier_name', carrier_name, checked as boolean)
                        }
                      />
                      <Label htmlFor={`carrier_${index}`} className="text-sm">
                        {carrier_name}
                      </Label>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <Separator />

            {/* Status Filter */}
            <div className="px-4 py-2">
              <div className="flex items-center space-x-2 mb-1">
                <Checkbox
                  id="hasStatus"
                  checked={!isNone(filters?.status)}
                  onCheckedChange={(checked) => handleChange('hasStatus', '', checked as boolean)}
                />
                <Label htmlFor="hasStatus" className="text-sm font-medium">
                  Status
                </Label>
              </div>
              
              {!isNone(filters?.status) && (
                <div className="ml-5 bg-gray-50 rounded">
                  {TRACKER_STATUSES.map((status: string, index) => (
                    <div key={index} className="flex items-center space-x-2 py-0.5 px-2">
                      <Checkbox
                        id={`status_${index}`}
                        checked={filters?.status?.includes(status) || false}
                        onCheckedChange={(checked) => 
                          handleChange('status', status, checked as boolean)
                        }
                      />
                      <Label htmlFor={`status_${index}`} className="text-sm">
                        {status}
                      </Label>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </PopoverContent>
    </Popover>
  );
};