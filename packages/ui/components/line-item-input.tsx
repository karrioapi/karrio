import React, { useEffect, useState } from 'react';
import { Button } from "@karrio/ui/components/ui/button";
import { Label } from "@karrio/ui/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@karrio/ui/components/ui/popover";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@karrio/ui/components/ui/command";
import { Check, ChevronsUpDown } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";
import { formatOrderLineItem, isNone } from '@karrio/lib';
import { useOrders } from '@karrio/hooks/order';
import { CommodityType } from '@karrio/types';

interface LineItemInputComponent {
  label?: string;
  required?: boolean;
  placeholder?: string;
  value?: string | null;
  onValueChange?: (value: string | null) => void;
  onUnlink?: () => void;
  query: ReturnType<typeof useOrders>['query'];
  className?: string;
  disabled?: boolean;
  showUnlinkButton?: boolean;
}

export const LineItemInput = React.forwardRef<HTMLButtonElement, LineItemInputComponent>(
  ({
    label,
    required,
    placeholder = "Link an order line item",
    value,
    onValueChange,
    onUnlink,
    query,
    className,
    disabled,
    showUnlinkButton = true,
    ...props
  }, ref) => {
    const [items, setItems] = useState<Array<{ value: string; label: string }>>([]);
    const [popoverOpen, setPopoverOpen] = useState<boolean>(false);

    const handleSelect = (newValue: string) => {
      const selectedValue = newValue === "" ? null : newValue;
      onValueChange?.(selectedValue);
      setPopoverOpen(false);
    };

    const handleUnlink = () => {
      onUnlink?.();
    };

    useEffect(() => {
      if (query.isFetched && !isNone(query.data?.orders)) {
        const dropdownItems = (query.data?.orders.edges || [])
          .map(({ node: order }) => order.line_items
            .filter((item) => item.id !== null)
            .map((item, index) => ({
              value: item.id as string,
              label: formatOrderLineItem(order as any, item as any, index)
            }))
          ).flat();

        setItems(dropdownItems);
      }
    }, [query.isFetched]);

    // Find selected item display value
    const selectedItem = items.find(item => item.value === value);
    const displayValue = selectedItem?.label || placeholder;

    return (
      <div className="space-y-2" {...props}>
        {label && (
          <Label className="text-xs text-slate-700 font-bold">
            {label}
            {required && (
              <span className="ml-1 text-red-500 text-xs">
                <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
              </span>
            )}
          </Label>
        )}

        <div className="flex gap-2">
          <div className="flex-1 min-w-0">
            <Popover open={popoverOpen} onOpenChange={setPopoverOpen}>
              <PopoverTrigger asChild>
                <Button
                  ref={ref}
                  variant="outline"
                  role="combobox"
                  className={cn(
                    "h-8 w-full justify-between",
                    !value && "text-muted-foreground",
                    className
                  )}
                  disabled={disabled}
                >
                  <span className="truncate">{displayValue}</span>
                  <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="p-2" align="start" style={{ width: 'var(--radix-popover-trigger-width)', minWidth: '400px' }}>
                <Command>
                  <CommandInput placeholder="Search order line items..." className="h-8" />
                  <CommandList>
                    <CommandEmpty>No order line items found.</CommandEmpty>
                    <CommandGroup>
                      <CommandItem
                        value=""
                        onSelect={() => handleSelect("")}
                      >
                        <Check
                          className={cn(
                            "mr-2 h-4 w-4",
                            !value ? "opacity-100" : "opacity-0"
                          )}
                        />
                        ---
                      </CommandItem>
                      {items.map((item) => (
                        <CommandItem
                          key={item.value}
                          value={item.label}
                          onSelect={() => handleSelect(item.value)}
                        >
                          <Check
                            className={cn(
                              "mr-2 h-4 w-4",
                              value === item.value ? "opacity-100" : "opacity-0"
                            )}
                          />
                          {item.label}
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  </CommandList>
                </Command>
              </PopoverContent>
            </Popover>
          </div>

          {showUnlinkButton && (
            <Button
              type="button"
              variant="outline"
              disabled={isNone(value) || value?.startsWith('unlinked_')}
              title="unlink order line item"
              onClick={handleUnlink}
              className="h-8 w-10 px-0 py-0 flex-shrink-0"
            >
              <i className="fas fa-unlink text-sm"></i>
            </Button>
          )}
        </div>
      </div>
    );
  }
);

LineItemInput.displayName = "LineItemInput";
