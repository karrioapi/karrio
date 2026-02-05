"use client";

import React, { useReducer, useEffect, useState } from 'react';
import { Filter } from "lucide-react";
import { ORDER_STATUSES } from '@karrio/types';
import { useOrders } from '@karrio/hooks/order';
import { isNone } from '@karrio/lib';
import { Button } from "@karrio/ui/components/ui/button";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@karrio/ui/components/ui/popover";
import { Separator } from "@karrio/ui/components/ui/separator";
import { cn } from "@karrio/ui/lib/utils";

interface OrdersFilterComponent {
  context: ReturnType<typeof useOrders>;
}

export const OrdersFilter = ({ context }: OrdersFilterComponent): JSX.Element => {
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

      case 'hasSource':
        if (checked) return { ...state, source: [] };
        return Object.keys(state).reduce((acc, key) => key === 'source' ? acc : { ...acc, [key]: state[key] }, {});
      case 'source':
        return { ...state, [name]: [...(value as string).split(',').map(s => s.trim())] };

      case 'hasOrderId':
        if (checked) return { ...state, order_id: [] };
        return Object.keys(state).reduce((acc, key) => key === 'order_id' ? acc : { ...acc, [key]: state[key] }, {});
      case 'order_id':
        return { ...state, [name]: [...(value as string).split(',').map(s => s.trim())] };

      case 'hasDate':
        if (checked) return { ...state, created_before: "", created_after: "" };
        return Object.keys(state).reduce((acc, key) => ["created_before", "created_after"].includes(key) ? acc : { ...acc, [key]: state[key] }, {});

      case 'hasAddress':
        if (checked) return { ...state, [value as string]: "" };
        return Object.keys(state).reduce((acc, key) => key === value ? acc : { ...acc, [key]: state[key] }, {});

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
            {/* Address Filter */}
            <div className="px-4 py-2">
              <div className="flex items-center space-x-2 mb-1">
                <Checkbox
                  id="hasAddress"
                  checked={!isNone(filters?.address)}
                  onCheckedChange={(checked) => 
                    handleChange('hasAddress', 'address', checked as boolean)
                  }
                />
                <Label htmlFor="hasAddress" className="text-sm font-medium">
                  Address
                </Label>
              </div>
              
              {!isNone(filters?.address) && (
                <div className="ml-5 p-2 bg-gray-50 rounded">
                  <Input
                    value={filters?.address || ''}
                    onChange={(e) => handleChange('address', e.target.value)}
                    placeholder="e.g: 100 Main St, New York, NY"
                    className="text-sm h-8"
                  />
                </div>
              )}
            </div>

            <Separator />

            {/* Order ID Filter */}
            <div className="px-4 py-2">
              <div className="flex items-center space-x-2 mb-1">
                <Checkbox
                  id="hasOrderId"
                  checked={!isNone(filters?.order_id)}
                  onCheckedChange={(checked) => 
                    handleChange('hasOrderId', 'order_id', checked as boolean)
                  }
                />
                <Label htmlFor="hasOrderId" className="text-sm font-medium">
                  Order ID
                </Label>
              </div>
              
              {!isNone(filters?.order_id) && (
                <div className="ml-5 p-2 bg-gray-50 rounded">
                  <Input
                    value={filters?.order_id?.join(', ') || ''}
                    onChange={(e) => handleChange('order_id', e.target.value)}
                    placeholder="11616493, 11616494, ..."
                    className="text-sm h-8"
                  />
                </div>
              )}
            </div>

            <Separator />

            {/* Source Filter */}
            <div className="px-4 py-2">
              <div className="flex items-center space-x-2 mb-1">
                <Checkbox
                  id="hasSource"
                  checked={!isNone(filters?.source)}
                  onCheckedChange={(checked) => 
                    handleChange('hasSource', 'source', checked as boolean)
                  }
                />
                <Label htmlFor="hasSource" className="text-sm font-medium">
                  Source
                </Label>
              </div>
              
              {!isNone(filters?.source) && (
                <div className="ml-5 p-2 bg-gray-50 rounded">
                  <Input
                    value={filters?.source?.join(', ') || ''}
                    onChange={(e) => handleChange('source', e.target.value)}
                    placeholder="shopify, erp, ..."
                    className="text-sm h-8"
                  />
                </div>
              )}
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
                  {ORDER_STATUSES.map((status: string, index) => (
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