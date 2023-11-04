import { formatAddressLocationShort, formatAddressShort, formatDateTime, getURLSearchParams, isListEqual, isNone, isNoneOrEmpty, url$ } from "@/lib/helper";
import OrderPreview, { OrderPreviewContext } from "@/components/descriptions/order-preview";
import { useDocumentTemplates } from "@/context/document-template";
import React, { ChangeEvent, useContext, useEffect } from "react";
import OrdersFilter from "@/components/filters/orders-filter";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@/context/api-metadata";
import ConfirmModal from "@/components/confirm-modal";
import StatusBadge from "@/components/status-badge";
import { useRouter } from "next/dist/client/router";
import { useLoader } from "@/components/loader";
import OrderMenu from "@/components/order-menu";
import { useOrders } from "@/context/order";
import AppLink from "@/components/app-link";
import Spinner from "@/components/spinner";
import { AddressType } from "@/lib/types";
import Head from "next/head";

export { getServerSideProps } from "@/lib/data-fetching";


export default function OrdersPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { references } = useAPIMetadata();
    const { setLoading } = useLoader();
    const context = useOrders({ setVariablesToURL: true });
    const { previewOrder } = useContext(OrderPreviewContext);
    const [allChecked, setAllChecked] = React.useState(false);
    const [initialized, setInitialized] = React.useState(false);
    const [selection, setSelection] = React.useState<string[]>([]);
    const { query: { data: { orders } = {}, ...query }, filter, setFilter } = context;
    const { query: { data: { document_templates } = {} } } = useDocumentTemplates({
      related_object: "order" as any
    });

    const preventPropagation = (e: React.MouseEvent) => e.stopPropagation();
    const updatedSelection = (selectedOrders: string[], current: typeof orders) => {
      const order_ids = (current?.edges || []).map(({ node: order }) => order.id);
      const selection = selectedOrders.filter(id => order_ids.includes(id));
      const selected = selection.length > 0 && selection.length === (order_ids || []).length;
      setAllChecked(selected);
      if (selectedOrders.filter(id => !order_ids.includes(id)).length > 0) {
        setSelection(selection);
      }
    };
    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra
      };

      setFilter(query);
    };
    const handleSelection = (e: ChangeEvent) => {
      const { checked, name } = e.target as HTMLInputElement;
      if (name === "all") {
        setSelection(!checked ? [] : (orders?.edges || []).map(({ node: { id } }) => id));
      } else {
        setSelection(checked ? [...selection, name] : selection.filter(id => id !== name));
      }
    };
    const unfulfilledSelection = (selection: string[]) => {
      return (orders?.edges || []).filter(({ node: order }) => (
        selection.includes(order.id) &&
        !["cancelled", "fulfilled"].includes(order.status)
      )).length === selection.length;
    };

    useEffect(() => { updateFilter(); }, [router.query]);
    useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);
    useEffect(() => { updatedSelection(selection, orders); }, [selection, orders]);
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
        previewOrder(router.query.modal as string);
        setInitialized(true);
      }
    }, [router.query.modal, query.isFetched]);

    return (
      <>

        <header className="px-0 pb-3 pt-6 is-flex is-justify-content-space-between">
          <span className="title is-4">Orders</span>
          <div>
            <OrdersFilter context={context} />
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold ${isNone(filter?.status) ? 'is-active' : ''}`}>
              <a onClick={() => !isNone(filter?.status) && updateFilter({ status: null, offset: 0 })}>all</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${isListEqual(filter?.status || [], ['unfulfilled', 'partial']) ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('unfulfilled' as any) && updateFilter({ status: ['unfulfilled', 'partial'], offset: 0 })}>unfulfilled</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${isListEqual(filter?.status || [], ['fulfilled', 'delivered']) ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('fulfilled' as any) && updateFilter({ status: ['fulfilled', 'delivered'], offset: 0 })}>fulfilled</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('cancelled' as any) && filter?.status?.length === 1 ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('cancelled' as any) && updateFilter({ status: ['cancelled'], offset: 0 })}>cancelled</a>
            </li>
          </ul>
        </div>

        {!query.isFetched && <Spinner />}

        {(query.isFetched && (orders?.edges || []).length > 0) && <>
          <div className="table-container pb-3">
            <table className="orders-table table is-fullwidth">
              <tbody>

                <tr>
                  <td className="selector has-text-centered p-0" onClick={preventPropagation}>
                    <label className="checkbox p-2">
                      <input
                        name="all"
                        type="checkbox"
                        onChange={handleSelection}
                        checked={allChecked}
                      />
                    </label>
                  </td>

                  {selection.length > 0 && <td className="p-1" colSpan={5}>
                    <AppLink
                      href={`/orders/create_shipment?shipment_id=new&order_id=${selection.join(',')}`}
                      className={`button is-small is-default px-3 ${unfulfilledSelection(selection) ? '' : 'is-static'}`}>
                      <span className="has-text-weight-semibold">Create shipment</span>
                    </AppLink>
                    {(document_templates?.edges || []).map(({ node: template }) =>
                      <a
                        key={template.id}
                        href={url$`${references.HOST}/documents/${template.id}.${template.slug}?orders=${selection.join(',')}`}
                        className="button is-small is-default px-3 mx-2"
                        target="_blank"
                        rel="noreferrer">
                        <span className="has-text-weight-semibold">Print {template.name}</span>
                      </a>
                    )}
                  </td>}

                  {selection.length === 0 && <>
                    <td className="order is-size-7">ORDER #</td>
                    <td className="status"></td>
                    <td className="items is-size-7">ITEMS</td>
                    <td className="customer is-size-7">SHIP TO</td>
                    <td className="date is-size-7">DATE</td>
                    <td className="action"></td>
                  </>}
                </tr>

                {(orders?.edges || []).map(({ node: order }) => (
                  <tr key={order.id} className="items is-clickable">
                    <td className="selector has-text-centered is-vcentered p-0">
                      <label className="checkbox py-3 px-2">
                        <input
                          type="checkbox"
                          name={order.id}
                          onChange={handleSelection}
                          checked={selection.includes(order.id)}
                        />
                      </label>
                    </td>
                    <td className="order is-vcentered" onClick={() => previewOrder(order.id)}>
                      <p className="is-size-7 has-text-weight-bold has-text-grey-dark">
                        {order.order_id}
                      </p>
                      <p className="is-size-7 has-text-grey is-lowercase">
                        {order.source}
                      </p>
                    </td>
                    <td className="status is-vcentered" onClick={() => previewOrder(order.id)}>
                      <StatusBadge status={order.status as string} style={{ width: '100%' }} />
                    </td>
                    <td className="items is-vcentered" onClick={() => previewOrder(order.id)}>
                      <p className="is-size-7 has-text-weight-bold has-text-grey">
                        {((items: number): any => `${items} item${items === 1 ? '' : 's'}`)(
                          order.line_items.reduce((acc, item) => acc + (item.quantity as number) || 1, 0)
                        )}
                      </p>
                      <p className="is-size-7 has-text-grey" style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {order.line_items.length > 1 ? "(Multiple)" : order.line_items[0].title || order.line_items[0].description || order.line_items[0].sku}
                      </p>
                    </td>
                    <td className="customer is-vcentered is-size-7 has-text-weight-bold has-text-grey text-ellipsis"
                      onClick={() => previewOrder(order.id)}>
                      <span className="text-ellipsis" title={formatAddressShort(order.shipping_to as AddressType)}>
                        {formatAddressShort(order.shipping_to as AddressType)}
                      </span>
                      <br />
                      <span className="has-text-weight-medium">{formatAddressLocationShort(order.shipping_to as AddressType)}</span>
                    </td>
                    <td className="date is-vcentered px-1" onClick={() => previewOrder(order.id)}>
                      <p className="is-size-7 has-text-weight-semibold has-text-grey">
                        {formatDateTime(order.created_at)}
                      </p>
                    </td>
                    <td className="action is-vcentered px-0">
                      <OrderMenu order={order as any} className="is-fullwidth" />
                    </td>
                  </tr>
                ))}

              </tbody>
            </table>
          </div>

          <div className="px-2 py-2 is-vcentered">
            <span className="is-size-7 has-text-weight-semibold">
              {(orders?.edges || []).length} results
            </span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number - 20) })}
                disabled={filter.offset == 0}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number + 20) })}
                disabled={!orders?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </div>
        </>}

        {(query.isFetched && (orders?.edges || []).length == 0) &&
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No order found.</p>
            </div>

          </div>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Orders - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <OrderPreview>
        <ConfirmModal>

          <Component />

        </ConfirmModal>
      </OrderPreview>
    </DashboardLayout>
  ), pageProps)
};
