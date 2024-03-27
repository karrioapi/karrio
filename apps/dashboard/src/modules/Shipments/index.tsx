import { formatAddressShort, formatAddressLocationShort, formatDateTime, formatRef, getURLSearchParams, isListEqual, isNone, isNoneOrEmpty, formatCarrierSlug, url$, preventPropagation } from "@karrio/lib";
import { ShipmentPreview, ShipmentPreviewContext } from "@/components/shipment-preview";
import { useSystemCarrierConnections } from "@karrio/hooks/admin/connections";
import { useDocumentTemplates } from "@karrio/hooks/document-template";
import { useCarrierConnections } from "@karrio/hooks/user-connection";
import { ShipmentsFilter } from "@karrio/ui/filters/shipments-filter";
import { ShipmentMenu } from "@karrio/ui/components/shipment-menu";
import { CarrierImage } from "@karrio/ui/components/carrier-image";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AddressType, ShipmentType } from "@karrio/types";
import { useLoader } from "@karrio/ui/components/loader";
import { AppLink } from "@karrio/ui/components/app-link";
import { Spinner } from "@karrio/ui/components/spinner";
import { useShipments } from "@karrio/hooks/shipment";
import React, { useContext, useEffect } from "react";
import { useRouter } from "next/dist/client/router";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function ShipmentsPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { setLoading } = useLoader();
    const { metadata } = useAPIMetadata();
    const [allChecked, setAllChecked] = React.useState(false);
    const [initialized, setInitialized] = React.useState(false);
    const [selection, setSelection] = React.useState<string[]>([]);
    const { previewShipment } = useContext(ShipmentPreviewContext);
    const { query: { data: { user_connections } = {} } } = useCarrierConnections();
    const { query: { data: { system_connections } = {} } } = useSystemCarrierConnections();
    const context = useShipments({
      status: ['purchased', 'delivered', 'in_transit', 'cancelled', 'needs_attention', 'out_for_delivery', 'delivery_failed'] as any,
      setVariablesToURL: true,
      preloadNextPage: true,
    })
    const { query: { data: { shipments } = {}, ...query }, filter, setFilter } = context;
    const { query: { data: { document_templates } = {} } } = useDocumentTemplates({
      related_object: "shipment" as any, active: true,
    });

    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra
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
    const computeDocFormat = (selection: string[]) => {
      const _shipment = (shipments?.edges || []).find(({ node: shipment }) => (shipment.id == selection[0]));
      return (_shipment?.node || {}).label_type;
    };
    const compatibleTypeSelection = (selection: string[]) => {
      const format = computeDocFormat(selection);
      return (shipments?.edges || []).filter(({ node: shipment }) => (
        selection.includes(shipment.id) && shipment.label_type == format
      )).length === selection.length;
    };
    const draftSelection = (selection: string[]) => {
      return (shipments?.edges || []).filter(({ node: shipment }) => (
        selection.includes(shipment.id) && shipment.status == "draft"
      )).length === selection.length;
    };
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

    useEffect(() => { updateFilter(); }, [router.query]);
    useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);
    useEffect(() => { updatedSelection(selection, shipments); }, [selection, shipments]);
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
        previewShipment(router.query.modal as string);
        setInitialized(true);
      }
    }, [router.query.modal, query.isFetched]);

    return (
      <>

        <header className="columns px-0 pb-0 pt-4">
          <div className="column">
            <span className="title is-4">Shipments</span>
          </div>
          <div className="column has-text-right">
            <AppLink href="/create_label?shipment_id=new" className="button is-primary is-small mx-1">
              <span>Create Label</span>
            </AppLink>
            <AppLink href="/manifests/create_manifests" className="button is-primary is-small mx-1">
              <span>Manage manifests</span>
            </AppLink>
            <ShipmentsFilter context={context} />
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
                      <AppLink className={`button is-small is-default px-3 ${draftSelection(selection) ? '' : 'is-static'}`}
                        href={`/shipments/create_labels?shipment_ids=${selection.join(',')}`}>
                        <span className="has-text-weight-semibold">Create labels</span>
                      </AppLink>
                      <a
                        href={url$`${metadata.HOST}/documents/shipments/label.${(computeDocFormat(selection) || "pdf")?.toLocaleLowerCase()}?shipments=${selection.join(',')}`}
                        className={`button is-small is-default px-3 ${compatibleTypeSelection(selection) ? '' : 'is-static'}`} target="_blank" rel="noreferrer">
                        <span className="has-text-weight-semibold">Print Labels</span>
                      </a>
                      <a
                        href={url$`${metadata.HOST}/documents/shipments/invoice.pdf?shipments=${selection.join(',')}`}
                        className={`button is-small is-default px-3`} target="_blank" rel="noreferrer">
                        <span className="has-text-weight-semibold">Print Invoices</span>
                      </a>
                      {(document_templates?.edges || []).map(({ node: template }) =>
                        <a
                          key={template.id}
                          href={url$`${metadata.HOST}/documents/templates/${template.id}.${template.slug}?shipments=${selection.join(',')}`}
                          className="button is-small is-default px-3"
                          target="_blank"
                          rel="noreferrer">
                          <span className="has-text-weight-semibold">Print {template.name}</span>
                        </a>
                      )}
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
                      onClick={() => previewShipment(shipment.id)}
                      title={(
                        isNone(getRate(shipment))
                          ? "UNFULFILLED"
                          : formatRef(((shipment.meta as any)?.service_name || getRate(shipment).service) as string)
                      )}
                    >
                      <div className="icon-text">
                        <CarrierImage
                          carrier_name={shipment.meta?.carrier || getRate(shipment).meta?.rate_provider || getRate(shipment).carrier_name || formatCarrierSlug(metadata.APP_NAME)}
                          containerClassName="mt-1 ml-1 mr-2" height={28} width={28}
                          text_color={(shipment.selected_rate_carrier || getCarrier(getRate(shipment)))?.config?.text_color}
                          background={(shipment.selected_rate_carrier || getCarrier(getRate(shipment)))?.config?.brand_color}
                        />
                        <div className="text-ellipsis" style={{ maxWidth: '190px', lineHeight: '16px' }}>
                          <span className="has-text-info has-text-weight-bold">
                            {!isNone(shipment.tracking_number) && <span>{shipment.tracking_number}</span>}
                            {isNone(shipment.tracking_number) && <span> - </span>}
                          </span><br />
                          <span className="text-ellipsis">
                            {!isNone(getRate(shipment).carrier_name) && formatRef(((getRate(shipment).meta as any)?.service_name || getRate(shipment).service) as string)}
                            {isNone(getRate(shipment).carrier_name) && "UNFULFILLED"}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td className="status is-vcentered" onClick={() => previewShipment(shipment.id)}>
                      <StatusBadge status={shipment.status as string} style={{ width: '100%' }} />
                    </td>
                    <td className="recipient is-vcentered is-size-7 has-text-weight-bold has-text-grey is-relative" onClick={() => previewShipment(shipment.id)}>
                      <div className="p-2" style={{ position: 'absolute', maxWidth: '100%', top: 0, left: 0 }}>
                        <p className="text-ellipsis" title={formatAddressShort(shipment.recipient as AddressType)}>
                          {formatAddressShort(shipment.recipient as AddressType)}
                        </p>
                        <p className="has-text-weight-medium">{formatAddressLocationShort(shipment.recipient as AddressType)}</p>
                      </div>
                    </td>
                    <td className="reference is-vcentered is-size-7 has-text-weight-bold has-text-grey text-ellipsis" onClick={() => previewShipment(shipment.id)}>
                      <span>{shipment.reference || ''}</span>
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
