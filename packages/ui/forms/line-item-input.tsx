import { DropdownInput, DropdownInputComponent } from '../components/dropdown-input';
import { formatOrderLineItem, isNone } from '@karrio/lib';
import React, { useEffect, useState } from 'react';
import { useOrders } from '@karrio/hooks/order';
import { CommodityType } from '@karrio/types';

interface LineItemInputComponent extends Omit<DropdownInputComponent, 'items' | 'onChange' | 'onValueChange'> {
  onChange?: (value?: CommodityType) => void;
  onReady?: (value?: CommodityType) => void;
  query: ReturnType<typeof useOrders>['query'];
}

export const LineItemInput: React.FC<LineItemInputComponent> = ({ onChange, onReady, query, ...props }) => {
  const [lineItems, setLineItems] = useState<CommodityType[]>();
  const [items, setItems] = useState<[string, string][]>([]);

  const handleChange = (key?: string | null) => {
    const item = (lineItems || []).find(item => item.id === key);
    onChange && onChange(item);
  };

  useEffect(() => {
    if (query.isFetched && !isNone(query.data?.orders)) {
      const allItems = (query.data?.orders.edges || []).map(({ node: order }) => order.line_items).flat();
      const dropdownItems = (query.data?.orders.edges || [])
        .map(({ node: order }) => order.line_items.map(
          (item, index) => [item.id, formatOrderLineItem(order as any, item as any, index)] as [string, string]
        )).flat();

      setLineItems(allItems);
      setItems(dropdownItems);

      if (!!props.value && !!onReady) {
        const selected = allItems.find(({ id }) => id === props.value);
        onReady(selected);
      }
    }
  }, [query.isFetched, props.value]);

  return (
    <DropdownInput
      items={items}
      onValueChange={handleChange}
      {...props}
    />
  )
};
