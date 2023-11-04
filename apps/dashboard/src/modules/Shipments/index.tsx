import { formatAddressShort, formatAddressLocationShort, formatDateTime, formatRef, getURLSearchParams, isListEqual, isNone, isNoneOrEmpty } from "@/lib/helper";
import ShipmentPreview, { ShipmentPreviewContext } from "@/components/descriptions/shipment-preview";
import ShipmentsFilter from "@/components/filters/shipments-filter";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import ShipmentMenu from "@/components/shipment-menu";
import CarrierBadge from "@/components/carrier-badge";
import ConfirmModal from "@/components/confirm-modal";
import React, { useContext, useEffect } from "react";
import StatusBadge from "@/components/status-badge";
import { useRouter } from "next/dist/client/router";
import { useShipments } from "@/context/shipment";
import { useLoader } from "@/components/loader";
import AppBadge from "@/components/app-badge";
import AppLink from "@/components/app-link";
import Spinner from "@/components/spinner";
import { AddressType } from "@/lib/types";
import Head from "next/head";

export { getServerSideProps } from "@/lib/data-fetching";


export default function ShipmentsPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { setLoading } = useLoader();
    const [initialized, setInitialized] = React.useState(false);
    const { previewShipment } = useContext(ShipmentPreviewContext);
    const context = useShipments({
      status: ['purchased', 'delivered', 'in_transit', 'cancelled', 'needs_attention', 'out_for_delivery', 'delivery_failed'] as any,
      setVariablesToURL: true,
    });
    const { query: { data: { shipments } = {}, ...query }, filter, setFilter } = context;

    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra
      };

      setFilter(query);
    }

    useEffect(() => { updateFilter(); }, [router.query]);
    useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
        previewShipment(router.query.modal as string);
        setInitialized(true);
      }
    }, [router.query.modal, query.isFetched]);

    return (
      <>
        <header className="px-0 pb-3 pt-6 is-flex is-justify-content-space-between">
          <span className="title is-4">Shipments</span>
          <div>
            <ShipmentsFilter context={context} />
            <AppLink href="/create_label?shipment_id=new" className="button is-primary is-small is-pulled-right ml-1">
              <span>Create Label</span>
            </AppLink>
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold ${isListEqual(filter?.status || [], ['purchased', 'delivered', 'in_transit', 'cancelled', 'needs_attention', 'out_for_delivery', 'delivery_failed']) ? 'is-active' : ''}`}>
              <a onClick={() => updateFilter({ status: ['purchased', 'delivered', 'in_transit', 'cancelled', 'needs_attention', 'out_for_delivery', 'delivery_failed'], offset: 0 })}>all</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${isListEqual(filter?.status || [], ['purchased', 'in_transit', 'out_for_delivery']) ? 'is-active' : ''}`}>
              <a onClick={() => updateFilter({ status: ['purchased', 'in_transit', 'out_for_delivery'], offset: 0 })}>purchased</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('delivered' as any) && filter?.status?.length === 1 ? 'is-active' : ''}`}>
              <a onClick={() => updateFilter({ status: ['delivered'], offset: 0 })}>delivered</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('needs_attention' as any) && filter?.status?.length === 2 ? 'is-active' : ''}`}>
              <a onClick={() => updateFilter({ status: ['needs_attention', 'delivery_failed'], offset: 0 })}>exception</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('cancelled' as any) && filter?.status?.length === 1 ? 'is-active' : ''}`}>
              <a onClick={() => updateFilter({ status: ['cancelled'], offset: 0 })}>cancelled</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold ${filter?.status?.includes('draft' as any) && filter?.status?.length === 1 ? 'is-active' : ''}`}>
              <a onClick={() => !filter?.status?.includes('draft' as any) && updateFilter({ status: ['draft'], offset: 0 })}>draft</a>
            </li>
          </ul>
        </div>

        {!query.isFetched && <Spinner />}

        {(query.isFetched && (shipments?.edges || []).length > 0) && <>
          <div className="table-container">
            <table className="shipments-table table is-fullwidth">

              <tbody>

                <tr>
                  <td className="carrier is-size-7 has-text-centered">CARRIER</td>
                  <td className="service is-size-7">SERVICE</td>
                  <td className="status"></td>
                  <td className="recipient is-size-7">RECIPIENT</td>
                  <td className="date is-size-7">DATE</td>
                  <td className="action"></td>
                </tr>

                {(shipments?.edges || []).map(({ node: shipment }) => (
                  <tr key={shipment.id} className="items is-clickable">
                    <td className="carrier is-vcentered has-text-centered p-2" onClick={() => previewShipment(shipment.id)}>
                      {!!shipment.carrier_name && <CarrierBadge
                        className="has-background-primary has-text-weight-bold has-text-white-bis"
                        style={{ fontSize: '0.6rem' }}
                        carrier_name={shipment.meta.carrier || shipment.carrier_name}
                      />}
                      {!shipment.carrier_name && <AppBadge />}
                    </td>
                    <td className="service is-vcentered p-1 pl-2 is-size-7 has-text-weight-bold has-text-grey text-ellipsis"
                      onClick={() => previewShipment(shipment.id)}
                      title={
                        isNone(shipment.carrier_name) ? "NOT COMPLETED"
                          : formatRef(((shipment.meta as any)?.service_name || shipment.service) as string)
                      }>
                      <span className="text-ellipsis">
                        {!isNone(shipment.carrier_name) && formatRef(((shipment.meta as any)?.service_name || shipment.service) as string)}
                        {isNone(shipment.carrier_name) && "NOT COMPLETED"}
                      </span>
                      <br />
                      <span className="has-text-weight-medium has-text-info">{shipment.tracking_number}</span>
                    </td>
                    <td className="status is-vcentered" onClick={() => previewShipment(shipment.id)}>
                      <StatusBadge status={shipment.status as string} style={{ width: '100%' }} />
                    </td>
                    <td className="recipient is-vcentered is-size-7 has-text-weight-bold has-text-grey text-ellipsis"
                      onClick={() => previewShipment(shipment.id)}>
                      <span className="text-ellipsis" title={formatAddressShort(shipment.recipient as AddressType)}>
                        {formatAddressShort(shipment.recipient as AddressType)}
                      </span>
                      <br />
                      <span className="has-text-weight-medium">{formatAddressLocationShort(shipment.recipient as AddressType)}</span>
                    </td>
                    <td className="date is-vcentered px-1" onClick={() => previewShipment(shipment.id)}>
                      <p className="is-size-7 has-text-weight-semibold has-text-grey">
                        {formatDateTime(shipment.created_at)}
                      </p>
                    </td>
                    <td className="action is-vcentered px-0">
                      <ShipmentMenu shipment={shipment as any} className="is-fullwidth" />
                    </td>
                  </tr>
                ))}

              </tbody>

            </table>
          </div>

          <div className="px-2 py-2 is-vcentered">
            <span className="is-size-7 has-text-weight-semibold">
              {(shipments?.edges || []).length} results
            </span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number - 20) })}
                disabled={filter.offset == 0}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number + 20) })}
                disabled={!shipments?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </div>
        </>}

        {(query.isFetched && (shipments?.edges || []).length == 0) &&
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No shipment found.</p>
            </div>

          </div>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Shipments - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <ShipmentPreview>
        <ConfirmModal>

          <Component />

        </ConfirmModal>
      </ShipmentPreview>
    </DashboardLayout>
  ), pageProps)
};
