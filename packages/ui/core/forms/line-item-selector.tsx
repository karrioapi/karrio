import { CommodityType, OrderType, ShipmentType } from "@karrio/types";
import { getShipmentCommodities, isNone } from "@karrio/lib";
import React, { useEffect, useState } from "react";
import { useOrders } from "@karrio/hooks/order";

interface LineItemSelectorComponent {
  title?: string;
  shipment?: ShipmentType;
  onChange?: (value: Partial<CommodityType>[]) => void;
  order_ids?: string[];
}

export const LineItemSelector = ({
  title,
  shipment,
  order_ids,
  onChange,
}: LineItemSelectorComponent): JSX.Element => {
  const { query } = useOrders({
    first: 10,
    status: ["partial", "unfulfilled"] as any,
    id: order_ids,
  });
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
      .map(({ items }) => items || [])
      .flat()
      .filter(({ parent_id }) => parent_id === id)
      .reduce((acc, item) => acc + (item.quantity as number), 0);
  };

  const onSearch = (e: React.ChangeEvent<any>) => {
    setSearch(e.target.value as string);
  };
  const handleChange =
    (keys: string[]) => (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.checked) {
        setSelection([...(new Set([...selection, ...keys]) as any)]);
      } else {
        setSelection(selection.filter((item) => !keys.includes(item)));
      }
    };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const commodities = lineItems
      .filter((item) => selection.includes(item.id as string))
      .map((item) => {
        const { id: parent_id, ...content } = item;
        return { ...content, parent_id };
      });
    const extraCommodities = extraItems.filter((_, id) =>
      selection.includes(`ex-${id}`),
    );

    onChange && onChange([...commodities, ...extraCommodities]);
    close();
  };

  useEffect(() => {
    if (!query.isFetched || isNone(query.data?.orders)) return;

    const filteredOrders = (query.data?.orders.edges || [])
      .map(({ node: order }) => ({
        ...order,
        line_items: order.line_items
          .map(({ unfulfilled_quantity: quantity, ...item }) => ({
            ...item,
            quantity: (quantity || 0) - getUsedQuantity(item.id as string),
          }))
          .filter((item) => item.quantity > 0),
      }))
      .filter((order) => order.line_items.length > 0);

    setOrders(filteredOrders as any);
    setLineItems(filteredOrders.map((order) => order.line_items).flat());
  }, [query.isFetched, query.data?.orders]);

  useEffect(() => {
    if (!shipment) return;

    const items = getShipmentCommodities(
      shipment,
      shipment.customs?.commodities,
    )
      .filter(({ parent_id }) => !parent_id)
      .map((item) => ({ ...item, quantity: 1 }));
    setExtraItems(items);
  }, [shipment]);

  return (
    <>
      <button
        type="button"
        className="button is-primary is-small is-outlined"
        onClick={selectItems}
      >
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
              <span className="has-text-weight-bold is-size-6">
                {title || "Select line items"}
              </span>
            </div>
            <div className="p-3 my-4"></div>

            <div className="panel-block px-1 pt-0 pb-3">
              <p className="control has-icons-left">
                <input
                  type="text"
                  className={"input is-small"}
                  defaultValue={search || ""}
                  onInput={onSearch}
                />
                <span className="icon is-left">
                  <i className="fas fa-search" aria-hidden="true"></i>
                </span>
              </p>
            </div>

            {[...lineItems, extraItems].length === 0 && (
              <div className="notification is-warning is-light px-3 py-2 my-2">
                All items are packed.
              </div>
            )}

            <nav
              className="is-shadowless px-1"
              style={{
                minHeight: "30vh",
                maxHeight: "60vh",
                overflowY: "auto",
              }}
            >
              {extraItems.length > 0 && (
                <>
                  <p className="is-size-7 my-2 has-text-info">
                    Manually added items
                  </p>

                  <div className="columns m-0 pl-6 is-size-7">
                    <p className="column p-0 is-5 has-text-info"></p>
                    <p className="column p-0 is-3">| SKU</p>
                    <p className="column p-0 is-2">| Ship qty</p>
                    <p className="column p-0">| Unfulfilled</p>
                  </div>

                  <label
                    className="panel-block has-background-grey-lighter is-size-7"
                    key="extra-items"
                  >
                    <input
                      type="checkbox"
                      checked={
                        extraItems.filter((_, id) =>
                          selection.includes(`ex-${id}`),
                        ).length === extraItems.length
                      }
                      onChange={handleChange(
                        extraItems.map((_, id) => `ex-${id}`),
                      )}
                    />
                    <span>
                      Extra items -{" "}
                      <span className="has-text-grey is-size-7">
                        MANUALLY DEFINED
                      </span>
                    </span>
                  </label>

                  {extraItems.map((item, item_index) => (
                    <label
                      className="panel-block pl-5 is-size-7 has-text-weight-semibold columns m-0"
                      key={`extra-${item.id}`}
                    >
                      <input
                        type="checkbox"
                        name={`ex-${item_index}`}
                        checked={selection.includes(`ex-${item_index}`)}
                        onChange={handleChange([`ex-${item_index}`])}
                      />
                      <span className="column p-0 is-5">{item.description}</span>
                      <span className="column p-0 is-3">{item.sku}</span>
                      <span className="column p-0 is-2">{item.quantity}</span>
                      <span className="column p-0">{item.quantity}</span>
                    </label>
                  ))}
                </>
              )}

              {orders.map((order) => (
                <React.Fragment key={order.id}>
                  <label className="panel-block has-background-grey-lighter is-size-7">
                    <input
                      type="checkbox"
                      checked={order.line_items.every((item) =>
                        selection.includes(item.id as string),
                      )}
                      onChange={handleChange(
                        order.line_items.map((item) => item.id as string),
                      )}
                    />
                    <span>
                      {order.order_id} -{" "}
                      <span className="has-text-grey is-size-7">
                        {order.source}
                      </span>
                    </span>
                  </label>

                  {order.line_items.filter((item) => item.id !== null).map((item) => (
                    <label
                      className="panel-block pl-5 is-size-7 has-text-weight-semibold columns m-0"
                      key={item.id}
                    >
                      <input
                        type="checkbox"
                        name={item.id || undefined}
                        checked={selection.includes(item.id as string)}
                        onChange={handleChange([item.id as string])}
                      />
                      <span className="column p-0 is-5">{item.description}</span>
                      <span className="column p-0 is-3">{item.sku}</span>
                      <span className="column p-0 is-2">{item.quantity}</span>
                      <span className="column p-0">{item.quantity}</span>
                    </label>
                  ))}
                </React.Fragment>
              ))}
            </nav>

            <div className="form-floating-footer has-text-centered p-1">
              <button
                className="button is-default mr-2"
                onClick={close}
                type="button"
              >
                Cancel
              </button>
              <button
                className="button is-primary"
                onClick={handleSubmit}
                type="submit"
                disabled={selection.length === 0}
              >
                Add items
              </button>
            </div>
          </section>
        </div>
      </div>
    </>
  );
};
