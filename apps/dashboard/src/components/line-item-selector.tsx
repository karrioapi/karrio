import { CommodityType, OrderType, ShipmentType } from '@/lib/types';
import { getShipmentCommodities, isNone, isNoneOrEmpty } from '@/lib/helper';
import React, { useEffect, useState } from 'react';
import { useOrders } from '@/context/order';

interface LineItemSelectorComponent {
  title?: string;
  shipment?: ShipmentType;
  onChange?: (value: Partial<CommodityType>[]) => void;
}

const LineItemSelector: React.FC<LineItemSelectorComponent> = ({ title, shipment, onChange }) => {
  const { query } = useOrders({ first: 10, status: ["partial", "unfulfilled"] as any });
  const [search, setSearch] = useState<string>("");
  const [orders, setOrders] = useState<OrderType[]>([]);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [selection, setSelection] = useState<string[]>([]);
  const [lineItems, setLineItems] = useState<CommodityType[]>([]);
  const [extraItems, setExtraItems] = useState<CommodityType[]>([]);

  const selectItems = (_: React.MouseEvent) => {
    setIsActive(true);
    setSelection([]);
  };
  const close = (_?: React.MouseEvent) => {
    setIsActive(false);
    setSelection([]);
  };
  const getUsedQuantity = (id: string) => {
    return (shipment?.parcels || [])
      .map(({ items }) => items || []).flat()
      .filter(({ parent_id }) => parent_id === id)
      .reduce((acc, item) => acc + (item.quantity as number), 0);
  };

  const onSearch = (e: React.ChangeEvent<any>) => {
    setSearch(e.target.value as string);
  };
  const handleChange = (keys: string[]) => (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      setSelection([...(new Set([...selection, ...keys]) as any)]);
    } else {
      setSelection(selection.filter(item => !keys.includes(item)));
    }
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const commodities = (
      lineItems
        .filter(item => selection.includes(item.id as string))
        .map((item) => {
          const { id: parent_id, ...content } = item;
          return { ...content, parent_id };
        })
    );
    const extraCommodities = (
      extraItems
        .filter((_, id) => selection.includes(`ex-${id}`))
    );

    onChange && onChange([...commodities, ...extraCommodities]);
    close();
  };

  useEffect(() => {
    if (query.isFetched && !isNone(query.data?.orders)) {
      const filteredOrders = (query.data?.orders.edges || [])
        .map(({ node: order }) => ({
          ...order,
          line_items: order.line_items
            .map(({ unfulfilled_quantity: quantity, ...item }) => ({
              ...item,
              quantity: (quantity || 0) - getUsedQuantity(item.id as string)
            }))
            .filter(item => item.quantity > 0)
        }))
        .filter(order => order.line_items.length > 0);

      setOrders(filteredOrders as any);
      setLineItems(filteredOrders.map(order => order.line_items).flat());
    }
  }, [query.isFetched, query.data?.orders, isActive]);
  useEffect(() => {
    if (!!shipment) {
      const extraItems = (
        getShipmentCommodities(shipment, shipment.customs?.commodities)
          .filter(({ parent_id }) => !parent_id)
          .map(item => ({ ...item, quantity: 1 }))
      );
      setExtraItems(extraItems);
    }
  }, [shipment]);

  return (
    <>
      <button type="button" className="button is-primary is-small is-outlined" onClick={selectItems}>
        <span className="icon is-small">
          <i className="fas fa-tasks"></i>
        </span>
        <span>{title || "Add line items"}</span>
      </button>

      <div className={`modal ${isActive ? "is-active" : ""}`}>
        <div className="modal-background"></div>
        <div className="modal-card max-modal-height">

          <section className="modal-card-body modal-form p-2">
            <div className="form-floating-header p-4">
              <span className="has-text-weight-bold is-size-6">{title || "Select line items"}</span>
            </div>
            <div className="p-3 my-4"></div>

            <div className="panel-block px-1 pt-0 pb-3">
              <p className="control has-icons-left">
                <input type="text" className={"input is-small"} defaultValue={search || ''} onInput={onSearch} />
                <span className="icon is-left">
                  <i className="fas fa-search" aria-hidden="true"></i>
                </span>
              </p>
            </div>

            {[...lineItems, extraItems].length === 0 && <div className="notification is-warning is-light px-3 py-2 my-2">
              All items are packed.
            </div>}

            <nav className="is-shadowless px-1" style={{ minHeight: '30vh', maxHeight: '60vh', overflowY: 'auto' }}>
              {extraItems.length > 0 && <>
                <p className="is-size-7 my-2 has-text-info">Manually added items</p>

                <div className="columns m-0 pl-6 is-size-7">
                  <p className="column p-0 is-5 has-text-info"></p>
                  <p className="column p-0 is-3">| SKU</p>
                  <p className="column p-0 is-2">| Ship qty</p>
                  <p className="column p-0">| Unfulfilled</p>
                </div>

                <label className="panel-block has-background-grey-lighter is-size-7" key="extra-items">
                  <input type="checkbox"
                    checked={(extraItems.filter((_, id) => selection.includes(`ex-${id}`)).length === extraItems.length)}
                    onChange={handleChange(extraItems.map((_, id) => `ex-${id}`))}
                  />
                  <span>Extra items - <span className="has-text-grey is-size-7">MANUALLY DEFINED</span></span>
                </label>

                {extraItems.map((item, item_index) => (
                  <label className="panel-block pl-5 is-size-7 has-text-weight-semibold columns m-0" key={`extra-${item.id}`}>
                    <input type="checkbox"
                      name={`ex-${item_index}`}
                      checked={selection.includes(`ex-${item_index}`)}
                      onChange={handleChange([`ex-${item_index}`])}
                    />
                    <p className="column is-5 p-0 my-1">
                      {item_index + 1} {`${item.title || item.description || 'Item'}`}
                    </p>
                    <p className="column is-3 p-0 my-1">{item.sku}</p>
                    <p className="column is-2 p-0 my-1 has-text-centered">{item.metadata?.ship_qty}</p>
                    <p className="column p-0 my-1 has-text-centered">{item.quantity}</p>
                  </label>
                ))}

                <hr className='my-4' style={{ height: '1px' }} />
              </>}

              {orders.length > 0 && <>
                <p className="is-size-7 mb-2 has-text-info">Unfulfilled order line items</p>

                <div className="columns m-0 pl-6 is-size-7">
                  <p className="column p-0 is-5"></p>
                  <p className="column p-0 is-3">| SKU</p>
                  <p className="column p-0 is-2">| Ship qty</p>
                  <p className="column p-0">| Unfulfilled</p>
                </div>
              </>}

              {orders.map(order => (
                <React.Fragment key={`order-${order.id}`}>
                  <label className="panel-block has-background-grey-lighter is-size-7" key={`order-${order.id}`}>
                    <input type="checkbox"
                      name={order.id}
                      checked={(order.line_items.filter(({ id }) => selection.includes(id as string)).length === order.line_items.length)}
                      onChange={handleChange(order.line_items.map(({ id }) => id as string))}
                    />
                    <span>{order.order_id} - <span className="has-text-grey is-size-7">ORDER ID</span></span>
                  </label>

                  {order.line_items.map((item, item_index) => (
                    <label className="panel-block pl-5 is-size-7 has-text-weight-semibold columns m-0" key={`line-${item.id}`}>
                      <input type="checkbox"
                        name={item.id}
                        checked={selection.includes(item.id)}
                        onChange={handleChange([item.id])}
                      />
                      <p className="column is-5 p-0 my-1">
                        {item_index + 1} {`${item.title || item.description || 'Item'}`}
                      </p>
                      <p className="column is-3 p-0 my-1">{item.sku}</p>
                      <p className="column is-2 p-0 my-1 has-text-centered">{item.metadata?.ship_qty}</p>
                      <p className="column p-0 my-1 has-text-centered">{item.quantity}</p>
                    </label>
                  ))}
                </React.Fragment>
              ))}
            </nav>

            <div className="p-3 my-5"></div>
            <div className="form-floating-footer has-text-centered p-1">
              <button className="button is-default m-1 is-small" onClick={close} disabled={query.isFetching}>
                <span>Cancel</span>
              </button>
              <button className={`button is-primary ${query.isFetching ? 'is-loading' : ''} m-1 is-small`}
                disabled={query.isFetching || selection.length === 0} type="button" onClick={handleSubmit}>
                <span>Add selection</span>
              </button>
            </div>
          </section>

        </div>

        <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
      </div>
    </>
  )
};

export default LineItemSelector;
