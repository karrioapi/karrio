import React, { useEffect, useState } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Label } from "@karrio/ui/components/ui/label";
import { cn } from "@karrio/ui/lib/utils";
import { formatOrderLineItem, isNone } from '@karrio/lib';
import { useOrders } from '@karrio/hooks/order';
import { CommodityType } from '@karrio/types';

interface LineItemInputComponent {
  label?: string;
  required?: boolean;
  placeholder?: string;
  value?: string;
  onChange?: (value?: CommodityType) => void;
  onReady?: (value?: CommodityType) => void;
  query: ReturnType<typeof useOrders>['query'];
  className?: string;
  fieldClass?: string;
  controlClass?: string;
  wrapperClass?: string;
  disabled?: boolean;
}

export const LineItemInput = React.forwardRef<HTMLButtonElement, LineItemInputComponent>(
  ({
    label,
    required,
    placeholder = "Link an order line item",
    value,
    onChange,
    onReady,
    query,
    className,
    fieldClass,
    controlClass,
    wrapperClass,
    disabled,
    ...props
  }, ref) => {
    const [lineItems, setLineItems] = useState<CommodityType[]>([]);
    const [items, setItems] = useState<Array<{ value: string; label: string }>>([]);
    const [selectedValue, setSelectedValue] = useState<string>(value || "");

    const handleChange = (newValue: string) => {
      setSelectedValue(newValue);
      const item = lineItems.find(item => item.id === newValue);
      onChange && onChange(item);
    };

    useEffect(() => {
      if (query.isFetched && !isNone(query.data?.orders)) {
        const allItems = (query.data?.orders.edges || []).map(({ node: order }) => order.line_items).flat();
        const dropdownItems = (query.data?.orders.edges || [])
          .map(({ node: order }) => order.line_items.map(
            (item, index) => ({
              value: item.id,
              label: formatOrderLineItem(order as any, item as any, index)
            })
          )).flat();

        setLineItems(allItems);
        setItems(dropdownItems);

        if (!!value && !!onReady) {
          const selected = allItems.find(({ id }) => id === value);
          onReady(selected);
        }
      }
    }, [query.isFetched, value, onReady]);

    return (
      <div className={cn("px-1 py-2", wrapperClass)} {...props}>
        {label !== undefined && (
          <Label 
            className="capitalize text-xs font-normal mb-1 block"
            style={{ fontSize: ".8em" }}
          >
            {label}
            {required && (
              <span className="ml-1 text-red-500 text-xs">
                <i className="fas fa-asterisk" style={{ fontSize: ".7em" }}></i>
              </span>
            )}
          </Label>
        )}

        <div className={cn("relative", fieldClass)}>
          <Select
            value={selectedValue}
            onValueChange={handleChange}
            disabled={disabled}
          >
            <SelectTrigger 
              ref={ref}
              className={cn("h-9", className)} // Match small input height
            >
              <SelectValue placeholder={placeholder} />
            </SelectTrigger>
            <SelectContent>
              {items.map((item) => (
                <SelectItem 
                  key={item.value} 
                  value={item.value}
                  className="text-sm"
                >
                  {item.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
    );
  }
);

LineItemInput.displayName = "LineItemInput";
