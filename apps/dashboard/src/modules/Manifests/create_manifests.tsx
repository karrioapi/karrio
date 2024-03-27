import { formatAddressLocationShort, formatAddressShort, formatCarrierSlug, formatDateTime, formatRef, isNone, preventPropagation, url$ } from '@karrio/lib';
import { useSystemCarrierConnections } from '@karrio/hooks/admin/connections';
import { CreateManifestModal } from '@karrio/ui/modals/create-manifest-modal';
import { useCarrierConnections } from '@karrio/hooks/user-connection';
import { CarrierImage } from '@karrio/ui/components/carrier-image';
import { ShipmentMenu } from '@karrio/ui/components/shipment-menu';
import { AuthenticatedPage } from '@/layouts/authenticated-page';
import { StatusBadge } from '@karrio/ui/components/status-badge';
import { ConfirmModal } from '@karrio/ui/modals/confirm-modal';
import { DashboardLayout } from '@/layouts/dashboard-layout';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { AddressType, ShipmentType } from '@karrio/types';
import { useLoader } from '@karrio/ui/components/loader';
import { AppLink } from '@karrio/ui/components/app-link';
import { ModalProvider } from '@karrio/ui/modals/modal';
import { useShipments } from '@karrio/hooks/shipment';
import { ManifestData } from '@karrio/types/rest/api';
import { bundleContexts } from '@karrio/hooks/utils';
import { Spinner } from '@karrio/ui/components';
import { useRouter } from 'next/router';
import Head from 'next/head';
import React from 'react';

export { getServerSideProps } from "@/context/main";

const ContextProviders = bundleContexts([
  ModalProvider,
  ConfirmModal,
]);

export default function Page(pageProps: any) {
  const Component: React.FC = () => {

    // General context data         -----------------------------------------------------------
    //#region

    const router = useRouter();
    const loader = useLoader();
    const { metadata } = useAPIMetadata();
    const [allChecked, setAllChecked] = React.useState(false);
    const [selection, setSelection] = React.useState<string[]>([]);
    const { query: { data: { user_connections } = {} } } = useCarrierConnections();
    const { query: { data: { system_connections } = {} } } = useSystemCarrierConnections();
    const context = useShipments({
      status: ['purchased'] as any,
      meta_key: 'manifest_required',
      meta_value: true,
      has_manifest: false,
      preloadNextPage: true,
    });
    const { query: { data: { shipments } = {}, ...query }, filter, setFilter } = context;

    //#endregion

    // Helper functions            -----------------------------------------------------------
    //#region

    const getRate = (shipment: any) => (
      shipment.selected_rate
      || (shipment?.rates || []).find(_ => _.service === shipment?.options?.preferred_service)
      || (shipment?.rates || [])[0]
      || shipment
    );
    const getCarrier = (rate?: ShipmentType['rates'][0]) => (
      user_connections?.find(_ => _.id === rate?.meta?.carrier_connection_id || _.carrier_id === rate?.carrier_id)
      || system_connections?.find(_ => _.id === rate?.meta?.carrier_connection_id || _.carrier_id === rate?.carrier_id)
    );
    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...extra,
      };

      setFilter(query);
    };
    const updatedSelection = (selectedShipments: string[], current: typeof shipments) => {
      const shipment_ids = (current?.edges || []).map(({ node: shipment }) => shipment.id);
      const selection = selectedShipments.filter(id => shipment_ids.includes(id));
      const selected = selection.length > 0 && selection.length === (shipment_ids || []).length;
      setAllChecked(selected);
      if (selectedShipments.filter(id => !shipment_ids.includes(id)).length > 0) {
        setSelection(selection);
      }
    };
    const handleSelection = (e: React.ChangeEvent) => {
      const { checked, name } = e.target as HTMLInputElement;
      if (name === "all") {
        setSelection(!checked ? [] : (shipments?.edges || []).map(({ node: { id } }) => id));
      } else {
        setSelection(checked ? [...selection, name] : selection.filter(id => id !== name));
      }
    };
    const compatibleCarrierSelection = (selection: string[]) => {
      const carrier_id = shipments?.edges?.find(({ node: shipment }) => selection.includes(shipment.id))?.node?.carrier_id;
      return (shipments?.edges || []).filter(({ node: shipment }) => (
        selection.includes(shipment.id) && shipment.carrier_id == carrier_id
      )).length === selection.length;
    };
    const computeManifestData = (selection: string[], current: typeof shipments): ManifestData => {
      const shipment = (current?.edges || []).find(({ node: shipment }) => selection.includes(shipment.id))?.node;
      const { id, ...address } = shipment?.shipper || {} as any

      return {
        address,
        shipment_ids: selection,
        reference: shipment?.reference as string,
        carrier_name: shipment?.carrier_name as string,
      };
    }


    //#endregion

    React.useEffect(() => { updateFilter(); }, [router.query]);
    React.useEffect(() => { loader.setLoading(query.isLoading); }, [query.isLoading]);
    React.useEffect(() => { updatedSelection(selection, shipments); }, [selection, shipments]);

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <div className="title is-4">
            <span className="title is-4">Manifests</span>
            <span className="tag is-warning is-size-7 has-text-weight-bold mx-2">BETA</span>
          </div>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/manifests"><span>Ready</span></AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <a>Pending Shipments</a>
            </li>
          </ul>
        </div>

        {query.isLoading && <Spinner />}

        {(query.isLoading === false && (shipments?.edges || []).length > 0) && <>
          <div className="table-container">
            <table className="shipments-table table is-fullwidth">

              <tbody>

                <tr>
                  <td className="selector has-text-centered p-0 control is-vcentered" onClick={preventPropagation}>
                    <label className="checkbox p-2">
                      <input
                        name="all"
                        type="checkbox"
                        onChange={handleSelection}
                        checked={allChecked}
                      />
                    </label>
                  </td>

                  {selection.length > 0 && <td className="p-1 is-vcentered" colSpan={6}>
                    <div className="buttons has-addons">

                      <CreateManifestModal
                        manifest={computeManifestData(selection, shipments)}
                        trigger={
                          <button type="button" className="button is-default" disabled={!compatibleCarrierSelection(selection)}>
                            <span className="has-text-weight-semibold">Create Manifests</span>
                          </button>
                        }
                      />

                    </div>
                  </td>}

                  {selection.length === 0 && <>
                    <td className="service is-size-7 is-vcentered">SHIPPING SERVICE</td>
                    <td className="status is-vcentered"></td>
                    <td className="recipient is-size-7 is-vcentered">RECIPIENT</td>
                    <td className="reference is-size-7 is-vcentered">REFERENCE</td>
                    <td className="date is-size-7 is-vcentered">DATE</td>
                    <td className="action"></td>
                  </>}
                </tr>

                {(shipments?.edges || []).map(({ node: shipment }) => (
                  <tr key={shipment.id} className="items is-clickable">
                    <td className="selector has-text-centered is-vcentered p-0">
                      <label className="checkbox py-3 px-2">
                        <input
                          type="checkbox"
                          name={shipment.id}
                          onChange={handleSelection}
                          checked={selection.includes(shipment.id)}
                        />
                      </label>
                    </td>
                    <td className="service is-vcentered py-1 px-0 is-size-7 has-text-weight-bold has-text-grey"
                      title={formatRef(((shipment.meta as any)?.service_name || getRate(shipment).service) as string)}
                    >
                      <div className="icon-text">
                        <CarrierImage
                          carrier_name={shipment.meta?.carrier || getRate(shipment).meta?.rate_provider || getRate(shipment).carrier_name || formatCarrierSlug(metadata.APP_NAME)}
                          containerClassName="mt-1 ml-1 mr-2" height={28} width={28}
                          text_color={(shipment.selected_rate_carrier || getCarrier(getRate(shipment)))?.config?.text_color}
                          background={(shipment.selected_rate_carrier || getCarrier(getRate(shipment)))?.config?.brand_color}
                        />
                        <div className="text-ellipsis" style={{ maxWidth: '190px', lineHeight: '16px' }}>
                          <span className="has-text-info has-text-weight-bold">{shipment.tracking_number}</span>
                          <br />
                          <span className="text-ellipsis">
                            {formatRef(((getRate(shipment).meta as any)?.service_name || getRate(shipment).service) as string)}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td className="status is-vcentered" >
                      <StatusBadge status={shipment.status as string} style={{ width: '100%' }} />
                    </td>
                    <td className="recipient is-vcentered is-size-7 has-text-weight-bold has-text-grey is-relative" >
                      <div className="p-2" style={{ position: 'absolute', maxWidth: '100%', top: 0, left: 0 }}>
                        <p className="text-ellipsis" title={formatAddressShort(shipment.recipient as AddressType)}>
                          {formatAddressShort(shipment.recipient as AddressType)}
                        </p>
                        <p className="has-text-weight-medium">{formatAddressLocationShort(shipment.recipient as AddressType)}</p>
                      </div>
                    </td>
                    <td className="reference is-vcentered is-size-7 has-text-weight-bold has-text-grey text-ellipsis" >
                      <span>{shipment.reference || ''}</span>
                    </td>
                    <td className="date is-vcentered px-1" >
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

        {(query.isLoading === false && (shipments?.edges || []).length == 0) && <>
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No pending shipment found.</p>
            </div>

          </div>
        </>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Manifests - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <ContextProviders>
        <Component />
      </ContextProviders>

    </DashboardLayout>
  ), pageProps)
}
