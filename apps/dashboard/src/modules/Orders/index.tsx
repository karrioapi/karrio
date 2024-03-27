import { formatAddressLocationShort, formatAddressShort, formatCarrierSlug, formatDateTime, formatRef, getURLSearchParams, isListEqual, isNone, isNoneOrEmpty, url$ } from "@karrio/lib";
import { GoogleGeocodingScript } from "@karrio/ui/components/google-geocoding-script";
import { OrderPreview, OrderPreviewContext } from "@/components/order-preview";
import { useSystemCarrierConnections } from "@karrio/hooks/admin/connections";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { CarrierImage } from "@karrio/ui/components/carrier-image";
import React, { ChangeEvent, useContext, useEffect } from "react";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { OrdersFilter } from "@karrio/ui/filters/orders-filter";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { OrderMenu } from "@karrio/ui/components/order-menu";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AddressType, ShipmentType } from "@karrio/types";
import { useLoader } from "@karrio/ui/components/loader";
import { AppLink } from "@karrio/ui/components/app-link";
import { ModalProvider } from "@karrio/ui/modals/modal";
import { Spinner } from "@karrio/ui/components/spinner";
import { bundleContexts } from "@karrio/hooks/utils";
import { useRouter } from "next/dist/client/router";
import { useOrders } from "@karrio/hooks/order";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";

const ContextProviders = bundleContexts([
  OrderPreview,
  ConfirmModal,
  ModalProvider,
]);


export default function OrdersPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { setLoading } = useLoader();
    const { references } = useAPIMetadata();
    const { previewOrder } = useContext(OrderPreviewContext);
    const [allChecked, setAllChecked] = React.useState(false);
    const [initialized, setInitialized] = React.useState(false);
    const [selection, setSelection] = React.useState<string[]>([]);
    const context = useOrders({ setVariablesToURL: true, preloadNextPage: true });
    const { query: { data: { user_connections } = {} } } = useCarrierConnections();
    const { query: { data: { system_connections } = {} } } = useSystemCarrierConnections();
    const { query: { data: { orders } = {}, ...query }, filter, setFilter } = context;
    const { query: { data: { document_templates } = {} } } = useDocumentTemplates({
      related_object: "order" as any
    });

    const preventPropagation = (e: React.MouseEvent) => e.stopPropagation();
    const getRate = (shipment: any, default_rate?: any) => (
      default_rate
      || shipment?.selected_rate
      || (shipment?.rates || []).find(_ => _.service === shipment?.options?.preferred_service)
      || (shipment?.rates || [])[0]
      || shipment
    );
    const getCarrier = (rate?: ShipmentType['rates'][0]) => (
      user_connections?.find(_ => _.id === rate?.meta?.carrier_connection_id || _.carrier_id === rate?.carrier_id)
      || system_connections?.find(_ => _.id === rate?.meta?.carrier_connection_id || _.carrier_id === rate?.carrier_id)
    );
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
    const computeDocFormat = (selection: string[]): string | null => {
      const _order = (orders?.edges || []).find(({ node: order }) => (order.id == selection[0]));
      return (_order?.node?.shipments || [])[0]?.label_type;
    };
    const compatibleTypeSelection = (selection: string[]) => {
      const format = computeDocFormat(selection);
      return (orders?.edges || []).filter(({ node: order }) => (
        selection.includes(order.id) &&
        !!order.shipments.find(({ label_type }) => label_type === format)
      )).length === selection.length;
    };
    const computeOrderService = (order: any) => {
      const shipment = (
        order.shipments.find(({ status, tracking_number }) => !!tracking_number && !["cancelled", "draft"].includes(status)) ||
        order.shipments.find(({ status }) => ["draft"].includes(status))
      );
      const rate = getRate(shipment);

      if (!shipment) {
        const _shipment = (
          order.shipments.find(({ status }) => !["cancelled", "draft"].includes(status)) ||
          order.shipments.find(({ status }) => !["draft"].includes(status))
        );
        const _rate = getRate(_shipment);

        return <>
          <CarrierImage
            carrier_name={_shipment?.meta?.carrier || _rate?.meta?.rate_provider || _rate?.carrier_name || formatCarrierSlug(references.APP_NAME)}
            containerClassName="mt-1 ml-1 mr-2" height={28} width={28}
            text_color={getCarrier(_rate)?.config?.text_color}
            background={getCarrier(_rate)?.config?.background}
          />
          <div className="text-ellipsis" style={{ maxWidth: '190px', lineHeight: '15px' }}>
            <span className="has-text-info has-text-weight-bold"><span>{` - `}</span></span><br />
            <span className="text-ellipsis">
              {!isNone(_rate?.carrier_name) && formatRef((_rate.meta?.service_name || _rate.service) as string)}
              {isNone(_rate?.carrier_name) && "UNFULFILLED"}
            </span>
          </div>
        </>
      }

      return (
        <>
          <CarrierImage
            carrier_name={shipment.meta?.carrier || rate.meta?.carrier_name || rate.carrier_name || formatCarrierSlug(references.APP_NAME)}
            containerClassName="mt-1 ml-1 mr-2" height={28} width={28}
            text_color={getCarrier(rate)?.config?.text_color}
            background={getCarrier(rate)?.config?.background}
          />
          <div className="text-ellipsis" style={{ maxWidth: '190px', lineHeight: '15px' }}>
            <span className="has-text-info has-text-weight-bold">
              {!isNone(shipment.carrier_name) && <span>{shipment.tracking_number}</span>}
              {isNone(shipment.carrier_name) && <span>{` - `}</span>}
            </span><br />
            <span className="text-ellipsis">
              {!isNone(rate.carrier_name) && formatRef((rate.meta?.service_name || rate.service) as string)}
              {isNone(rate.carrier_name) && "UNFULFILLED"}
            </span>
          </div>
        </>
      )
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

        <header className="columns px-0 pb-0 pt-4">
          <div className="column">
            <span className="title is-4">Orders</span>
          </div>
          <div className="column has-text-right-desktop">
            <AppLink href="/draft_orders/new" className="button is-primary is-small mx-1">
              <span>Create order</span>
            </AppLink>
            <AppLink href="/manifests" className="button is-primary is-small mx-1">
              <span>Manage manifests</span>
            </AppLink>
            <OrdersFilter context={context} />
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold ${isNone(filter?.status) && isNone(filter?.source) ? 'is-active' : ''}`}>
              <a onClick={() => (!isNone(filter?.status) && isNone(filter?.source)) && updateFilter({ status: null, source: null, offset: 0 })}>all</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${isListEqual(filter?.status || [], ['unfulfilled', 'partial']) ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('unfulfilled' as any) && updateFilter({ status: ['unfulfilled', 'partial'], source: null, offset: 0 })}>unfulfilled</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${isListEqual(filter?.status || [], ['fulfilled', 'delivered']) ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('fulfilled' as any) && updateFilter({ status: ['fulfilled', 'delivered'], source: null, offset: 0 })}>fulfilled</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('cancelled' as any) && filter?.status?.length === 1 ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('cancelled' as any) && updateFilter({ status: ['cancelled'], source: null, offset: 0 })}>cancelled</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${(filter?.source as any === "draft") ? 'is-active' : ''}`}>
              <a onClick={() => !(filter?.source as any === "draft") && updateFilter({ status: null, source: "draft", offset: 0 })}>drafts</a>
            </li>
          </ul>
        </div>

        {!query.isFetched && <Spinner />}

        {(query.isFetched && (orders?.edges || []).length > 0) && <>
          <div className="table-container">
            <table className="orders-table table is-fullwidth">
              <tbody>

                <tr>
                  <td className="selector has-text-centered p-0 control" onClick={preventPropagation}>
                    <label className="checkbox p-2">
                      <input
                        name="all"
                        type="checkbox"
                        onChange={handleSelection}
                        checked={allChecked}
                      />
                    </label>
                  </td>

                  {selection.length > 0 && <td className="p-1 is-vcentered" colSpan={8}>
                    <div className="buttons has-addons ">
                      <AppLink className={`button is-small is-default px-3 ${unfulfilledSelection(selection) ? '' : 'is-static'}`}
                        href={`/orders/create_labels?order_ids=${selection.join(',')}`}>
                        <span className="has-text-weight-semibold">Create labels</span>
                      </AppLink>
                      <a
                        href={url$`${references.HOST}/documents/orders/label.${(computeDocFormat(selection) || "pdf")?.toLocaleLowerCase()}?orders=${selection.join(',')}`}
                        className={`button is-small is-default px-3 ${compatibleTypeSelection(selection) ? '' : 'is-static'}`} target="_blank" rel="noreferrer">
                        <span className="has-text-weight-semibold">Print Labels</span>
                      </a>
                      <a
                        href={url$`${references.HOST}/documents/orders/invoice.pdf?orders=${selection.join(',')}`}
                        className={`button is-small is-default px-3`} target="_blank" rel="noreferrer">
                        <span className="has-text-weight-semibold">Print Invoices</span>
                      </a>
                      {(document_templates?.edges || []).map(({ node: template }) =>
                        <a
                          key={template.id}
                          href={url$`${references.HOST}/documents/templates/${template.id}.${template.slug}?orders=${selection.join(',')}`}
                          className="button is-small is-default px-3"
                          target="_blank"
                          rel="noreferrer">
                          <span className="has-text-weight-semibold">Print {template.name}</span>
                        </a>
                      )}
                    </div>
                  </td>}

                  {selection.length === 0 && <>
                    <td className="order is-size-7 is-vcentered">ORDER #</td>
                    <td className="status"></td>
                    <td className="line-items is-size-7 is-vcentered">ITEMS</td>
                    <td className="customer is-size-7 is-vcentered">SHIP TO</td>
                    <td className="total is-size-7 is-vcentered">TOTAL</td>
                    <td className="date is-size-7 is-vcentered">DATE</td>
                    <td className="service is-size-7 is-vcentered">SHIPPING SERVICE</td>
                    <td className="action"></td>
                  </>}
                </tr>

                {(orders?.edges || []).map(({ node: order }) => (
                  <tr key={order.id} className="items">
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
                    <td className="order is-vcentered is-clickable is-relative" onClick={() => previewOrder(order.id)}>
                      <div className="p-2" style={{ position: 'absolute', maxWidth: '100%', top: 0, left: 0 }}>
                        <p className="is-size-7 has-text-weight-bold has-text-grey-dark text-ellipsis">
                          {order.order_id}
                        </p>
                        <p className="is-size-7 has-text-grey is-lowercase text-ellipsis">
                          {order.source}
                        </p>
                      </div>
                    </td>
                    <td className="status is-vcentered is-clickable" onClick={() => previewOrder(order.id)}>
                      <StatusBadge status={order.status as string} style={{ width: '100%' }} />
                    </td>
                    <td className="line-items is-vcentered is-clickable is-relative" onClick={() => previewOrder(order.id)}>
                      <div className="p-2" style={{ position: 'absolute', maxWidth: '100%', top: 0, left: 0 }}>
                        <p className="is-size-7 has-text-weight-bold has-text-grey text-ellipsis">
                          {((items: number): any => `${items} item${items === 1 ? '' : 's'}`)(
                            order.line_items.reduce((acc, item) => acc + (item.quantity as number) || 1, 0)
                          )}
                        </p>
                        <p className="is-size-7 has-text-grey text-ellipsis">
                          {order.line_items.length > 1 ? "(Multiple)" : order.line_items[0].title || order.line_items[0].description || order.line_items[0].sku}
                        </p>
                      </div>
                    </td>
                    <td className="customer is-vcentered is-clickable is-size-7 has-text-weight-bold has-text-grey is-relative" onClick={() => previewOrder(order.id)}>
                      <div className="p-2" style={{ position: 'absolute', maxWidth: '100%', top: 0, left: 0 }}>
                        <p className="text-ellipsis" title={formatAddressShort(order.shipping_to as AddressType)}>
                          {formatAddressShort(order.shipping_to as AddressType)}
                        </p>
                        <p className="has-text-weight-medium">{formatAddressLocationShort(order.shipping_to as AddressType)}</p>
                      </div>
                    </td>
                    <td className="total px-1 is-clickable" onClick={() => previewOrder(order.id)}>
                      <p className="is-size-7 has-text-weight-semibold has-text-grey">
                        {order.line_items.reduce((acc, item) => acc + ((item.quantity as number) * (item.value_amount as number)), 0)}
                        {` `}
                        {order.options.currency || order.line_items[0].value_currency}
                      </p>
                    </td>
                    <td className="date px-1 is-clickable" onClick={() => previewOrder(order.id)}>
                      <p className="is-size-7 has-text-weight-semibold has-text-grey">
                        {formatDateTime(order.created_at)}
                      </p>
                    </td>
                    <td className="service is-vcentered p-1 is-size-7 has-text-weight-bold has-text-grey">
                      <div className="icon-text">{computeOrderService(order)}</div>
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
      <GoogleGeocodingScript />
      <Head><title>{`Orders - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <ContextProviders>
        <Component />
      </ContextProviders>

    </DashboardLayout>
  ), pageProps)
};
