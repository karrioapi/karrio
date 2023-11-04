import { getShipmentCommodities, getUnfulfilledOrderLineItems, isNone } from '@/lib/helper';
import CommodityDescription from '@/components/descriptions/commodity-description';
import { CommodityType, OrderType, ShipmentType } from '@/lib/types';
import React from 'react';

type PackedItems = ReturnType<typeof getShipmentCommodities>;
type OrderItems = ReturnType<typeof getUnfulfilledOrderLineItems>;

interface CommoditySummaryComponent extends React.HTMLAttributes<any> {
  shipment?: ShipmentType;
  orders?: OrderType[];
}

const CommoditySummary: React.FC<CommoditySummaryComponent> = ({ shipment, orders, className }) => {
  const [unpackedItems, setUnpackedItems] = React.useState<OrderItems>([]);
  const [packedItems, setPackedItems] = React.useState<PackedItems>([]);
  const [orderItems, setOrderItems] = React.useState<OrderItems>([]);

  const computeItemQuantity = (item: CommodityType, line_items: OrderItems) => {
    const parent = line_items.find(({ id }) => id === item.parent_id);
    return parent?.quantity || item.quantity;
  };
  const computeTotalItems = (items: PackedItems, line_items: OrderItems) => {
    return [...items, ...line_items].reduce(
      (_, item) => _ + (computeItemQuantity(item as any, orderItems) || 1), 0
    );
  };
  const computeTotalPackedItems = (items: PackedItems) => {
    return items.reduce((_, item) => _ + (item.quantity || 1), 0);
  };

  React.useEffect(() => {
    if (!!shipment) {
      const parcelItems = getShipmentCommodities(shipment, shipment.customs?.commodities);
      const packedItems = (parcelItems.length === 0
        ? shipment.customs?.commodities || []
        : parcelItems
      );
      setPackedItems(packedItems);
    }
  }, [shipment]);
  React.useEffect(() => {
    if (!!orders) {
      const unfulfilledItems = getUnfulfilledOrderLineItems(orders);
      const unpackedItems = unfulfilledItems.filter(({ parent_id }) => (
        isNone(packedItems.find(item => item.parent_id === parent_id))
      ));
      setOrderItems(unfulfilledItems);
      setUnpackedItems(unpackedItems);
    }
  }, [orders, packedItems]);

  return (
    <div className={className || "card px-0"}>

      <header className="px-3 py-2 is-flex is-justify-content-space-between">
        <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">SUMMARY</span>
      </header>

      {(packedItems.length > 0 || unpackedItems.length > 0) && <div className="p-0 pb-1">
        <p className="is-title is-size-7 px-3 has-text-weight-semibold">
          ITEMS
          {' ('}
          <span>{computeTotalItems(packedItems, unpackedItems)} total</span>
          {' | '}
          <span className="has-text-info">{computeTotalPackedItems(packedItems)} packed</span>
          {')'}
        </p>

        <div className="menu-list px-3 py-1" style={{ maxHeight: '14em', overflow: 'auto' }}>

          {packedItems.map((item, index) => <React.Fragment key={index + "parcel-info"}>
            <hr className="my-1" style={{ height: '1px' }} />
            <CommodityDescription
              commodity={{ ...item, quantity: computeItemQuantity(item, orderItems) }}
              comments={`${item.quantity} packed`}
            />
          </React.Fragment>)}

          {unpackedItems.map((item, index) => <React.Fragment key={packedItems.length + index + "parcel-info"}>
            <hr className="my-1" style={{ height: '1px' }} />
            <CommodityDescription
              commodity={item as CommodityType}
              comments={`0 packed`}
            />
          </React.Fragment>)}

        </div>
      </div>}

      <footer className="px-3 py-1">
        <p className="is-subtitle is-size-7 is-vcentered my-1">
          TOTAL: {shipment?.options?.declared_value && <span>{shipment?.options?.declared_value} {shipment?.options?.currency}</span>}
        </p>
      </footer>

    </div>
  );
};

export default CommoditySummary;
