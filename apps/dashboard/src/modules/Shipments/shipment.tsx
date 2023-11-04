import CustomsInfoDescription from "@/components/descriptions/customs-info-description";
import MetadataEditor, { MetadataEditorContext } from "@/components/metadata-editor";
import { useUploadRecordMutation, useUploadRecords } from "@/context/upload-record";
import CommodityDescription from "@/components/descriptions/commodity-description";
import { formatDateTime, formatDayDate, formatRef, isNone } from "@/lib/helper";
import AddressDescription from "@/components/descriptions/address-description";
import ParcelDescription from "@/components/descriptions/parcel-description";
import { CustomsType, NotificationType, ParcelType } from "@/lib/types";
import AuthenticatedPage from "@/layouts/authenticated-page";
import SelectField from "@/components/generic/select-field";
import InputField from "@/components/generic/input-field";
import DashboardLayout from "@/layouts/dashboard-layout";
import StatusCode from "@/components/status-code-badge";
import { MetadataObjectTypeEnum } from "karrio/graphql";
import CopiableLink from "@/components/copiable-link";
import CarrierBadge from "@/components/carrier-badge";
import ShipmentMenu from "@/components/shipment-menu";
import ConfirmModal from "@/components/confirm-modal";
import { useRouter } from "next/dist/client/router";
import StatusBadge from "@/components/status-badge";
import { useNotifier } from "@/components/notifier";
import { DocumentUploadData, DocumentUploadRecord } from "@karrio/rest";
import { useShipment } from "@/context/shipment";
import { useLoader } from "@/components/loader";
import { useEvents } from "@/context/event";
import AppLink from "@/components/app-link";
import Spinner from "@/components/spinner";
import { useLogs } from "@/context/log";
import Head from "next/head";
import React from "react";
import { useAPIMetadata } from "@/context/api-metadata";
import OptionsDescription from "@/components/descriptions/options-description";

export { getServerSideProps } from "@/lib/data-fetching";

type FileDataType = DocumentUploadData['document_files'][0];

export const ShipmentComponent: React.FC<{ shipmentId?: string }> = ({ shipmentId }) => {
  const router = useRouter();
  const notifier = useNotifier();
  const { setLoading } = useLoader();
  const $fileInput = React.useRef<HTMLInputElement>();
  const $fileSelectInput = React.useRef<HTMLSelectElement>();
  const { references: { carrier_capabilities = {} } } = useAPIMetadata();
  const entity_id = shipmentId || router.query.id as string;
  const { query: logs } = useLogs({ entity_id });
  const { query: events } = useEvents({ entity_id });
  const { query: { data: { shipment } = {}, ...query } } = useShipment(entity_id);
  const { uploadDocument } = useUploadRecordMutation();
  const { query: { data: { results: uploads } = {}, ...documents } } = useUploadRecords({ shipmentId: entity_id });
  const [fileData, setFileData] = React.useState<FileDataType>({} as FileDataType)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    try {
      if (!!e.target.files && !!e.target.files[0]) {
        let file = e.target.files[0];
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
          let sections = (reader.result as string).split(',');
          let doc_file = sections[sections.length - 1];
          let doc_name = file.name;
          setFileData({ ...fileData, doc_name, doc_file });
        };
      } else {
        setFileData({ doc_file: fileData.doc_file } as FileDataType);
      }
    } catch (_) {
      setFileData({ doc_file: fileData.doc_file } as FileDataType);
    }
  };
  const uploadCustomsDocument = async () => {
    try {
      await uploadDocument.mutateAsync({
        shipment_id: entity_id,
        document_files: [fileData],
      });
      notifier.notify({
        type: NotificationType.success,
        message: `document updloaded successfully`,
      });
      if (!!$fileInput.current) $fileInput.current.value = '';
      if (!!$fileSelectInput.current) $fileSelectInput.current.value = 'other';
    } catch (message: any) {
      notifier.notify({ type: NotificationType.error, message });
    }
  };

  React.useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);

  return (
    <>

      {!query.isFetched && query.isFetching && <Spinner />}

      {shipment && <>

        {/* Header Section */}
        <div className="columns my-1">
          <div className="column is-6">
            <span className="subtitle is-size-7 has-text-weight-semibold">SHIPMENT</span>
            <br />
            <span className="title is-4 mr-2">{shipment.tracking_number || "NOT COMPLETED"}</span>
            <StatusBadge status={shipment.status} />
          </div>

          <div className="column is-6 pb-0">
            <div className="is-flex is-justify-content-right">
              <CopiableLink text={shipment.id as string} title="Copy ID" />
            </div>
            <div className="is-flex is-justify-content-right">

              {!isNone(shipmentId) && <AppLink
                href={`/shipments/${shipmentId}`} target="blank"
                className="button is-white has-text-info is-small mx-1">
                <span className="icon">
                  <i className="fas fa-external-link-alt"></i>
                </span>
              </AppLink>}

              <div style={{ display: 'inline-flex' }}>
                <ShipmentMenu
                  shipment={shipment as any}
                  isViewing
                />
              </div>

            </div>
          </div>
        </div>

        <hr className="mt-1 mb-2" style={{ height: '1px' }} />

        {/* Reference and highlights section */}
        <div className="columns mb-4">
          <div className="p-4 mr-4">
            <span className="subtitle is-size-7 my-4">Date</span><br />
            <span className="subtitle is-size-7 mt-1 has-text-weight-semibold">{formatDateTime(shipment.created_at)}</span>
          </div>

          {!isNone(shipment.service) && <>
            <div className="my-2" style={{ width: '1px', backgroundColor: '#ddd' }}></div>
            <div className="p-4 mr-4">
              <span className="subtitle is-size-7 my-4">Courier</span><br />
              <CarrierBadge
                className="has-background-primary has-text-centered has-text-weight-bold has-text-white-bis is-size-7"
                carrier_name={shipment.meta.carrier as string}
              />
            </div>

            <div className="my-2" style={{ width: '1px', backgroundColor: '#ddd' }}></div>
            <div className="p-4 mr-4">
              <span className="subtitle is-size-7 my-4">Service Level</span><br />
              <span className="subtitle is-size-7 mt-1 has-text-weight-semibold">
                {formatRef(((shipment.meta as any)?.service_name || shipment.service) as string)}
              </span>
            </div>
          </>}

          {!isNone(shipment.reference) && <>
            <div className="my-2" style={{ width: '1px', backgroundColor: '#ddd' }}></div>
            <div className="p-4 mr-4">
              <span className="subtitle is-size-7 my-4">Reference</span><br />
              <span className="subtitle is-size-7 has-text-weight-semibold">{shipment.reference}</span>
            </div>
          </>}
        </div>

        {!isNone(shipment.selected_rate) && <>

          <h2 className="title is-5 my-4">Service Details</h2>
          <hr className="mt-1 mb-2" style={{ height: '1px' }} />

          <div className="mt-3 mb-6">
            <div className="columns my-0 py-1">
              <div className="column is-6 is-size-6">
                <div className="columns my-0">
                  <div className="column is-4 is-size-6 py-1">Service</div>
                  <div className="column is-size-6 has-text-weight-semibold py-1">
                    {formatRef(((shipment.meta as any)?.service_name || shipment.service) as string)}
                  </div>
                </div>
                <div className="columns my-0">
                  <div className="column is-4 is-size-6 py-1">Courier</div>
                  <div className="column is-size-6 has-text-weight-semibold py-1">
                    {formatRef(shipment.meta.carrier as string)}
                  </div>
                </div>
                <div className="columns my-0">
                  <div className="column is-4 is-size-6 py-1">Rate</div>
                  <div className="column is-size-6 py-1">
                    <span className="has-text-weight-semibold mr-1">{shipment.selected_rate?.total_charge}</span>
                    <span>{shipment.selected_rate?.currency}</span>
                  </div>
                </div>
                <div className="columns my-0">
                  <div className="column is-4 is-size-7 py-1">Rate Provider</div>
                  <div className="column is-size-7 has-text-info has-text-weight-semibold py-1">
                    {formatRef(shipment.meta.ext as string)}
                  </div>
                </div>
                <div className="columns my-0">
                  <div className="column is-4 is-size-7 py-1">Tracking Number</div>
                  <div className="column has-text-info py-1">
                    <span className="is-size-7 has-text-weight-semibold">{shipment.tracking_number as string}</span>
                  </div>
                </div>
              </div>

              {(shipment.selected_rate?.extra_charges || []).length > 0 && <>
                <div className="column is-6 is-size-6 py-1">
                  <p className="is-title is-size-6 my-2 has-text-weight-semibold">CHARGES</p>
                  <hr className="mt-1 mb-2" style={{ height: '1px' }} />

                  {(shipment.selected_rate?.extra_charges || []).map((charge, index) => <div key={index} className="columns m-0">
                    <div className="column is-5 is-size-7 px-0 py-1">
                      <span className="is-uppercase">{charge?.name?.toLocaleLowerCase()}</span>
                    </div>
                    <div className="is-size-7 py-1 has-text-grey has-text-right" style={{ minWidth: '100px' }}>
                      <span className="mr-1">{charge?.amount}</span>
                      {!isNone(charge?.currency) && <span>{charge?.currency}</span>}
                    </div>
                  </div>)}
                </div>
              </>}

            </div>
          </div>

        </>}

        {!isNone(shipment.tracker) && <>

          <h2 className="title is-5 my-4">
            <span>Tracking Details</span>
            <a className="p-0 mx-2 my-0 is-size-6 has-text-weight-semibold"
              href={`/tracking/${shipment.tracker_id}`} target="_blank" rel="noreferrer">
              <span><i className="fas fa-external-link-alt"></i></span>
            </a>
          </h2>
          <hr className="mt-1 mb-2" style={{ height: '1px' }} />
          <div className="mt-3 mb-6">
            <div className="columns my-0 py-1">

              <div className="column is-6 is-size-7">
                {!isNone(shipment.tracker?.estimated_delivery) && <div className="columns my-0">
                  <div className="column is-4 is-size-6 py-0">{shipment.tracker?.delivered ? 'Delivered' : 'Estimated Delivery'}</div>
                  <div className="column has-text-weight-semibold py-1">
                    {formatDayDate(shipment.tracker!.estimated_delivery as string)}
                  </div>
                </div>}
                <div className="columns my-0">
                  <div className="column is-4 is-size-6 py-0">Last event</div>
                  <div className="column has-text-weight-semibold py-1">
                    <p className="is-capitalized">
                      {formatDayDate((shipment.tracker?.events || [])[0]?.date as string)}
                      {' '}
                      <code>{(shipment.tracker?.events || [])[0]?.time}</code>
                    </p>
                  </div>
                </div>
                {!isNone((shipment.tracker?.events || [])[0]?.location) && <div className="columns my-0">
                  <div className="column is-4"></div>
                  <div className="column has-text-weight-semibold py-1">
                    {(shipment.tracker?.events || [])[0]?.location}
                  </div>
                </div>}
                {!isNone((shipment.tracker?.events || [])[0]?.description) && <div className="columns my-0">
                  <div className="column is-4"></div>
                  <div className="column has-text-weight-semibold py-1">
                    {(shipment.tracker?.events || [])[0]?.description}
                  </div>
                </div>}
              </div>

            </div>
          </div>

        </>}


        {/* Shipment details section */}
        <h2 className="title is-5 my-4">Shipment Details</h2>
        <hr className="mt-1 mb-2" style={{ height: '1px' }} />

        <div className="mt-3 mb-6">

          <div className="columns my-0">
            {/* Recipient Address section */}
            <div className="column is-6 is-size-6 py-1">
              <p className="is-title is-size-6 my-2 has-text-weight-semibold">ADDRESS</p>

              <AddressDescription address={shipment.recipient} />
            </div>

            {/* Options section */}
            {(Object.values(shipment.options as object).length > 0) && <div className="column is-6 is-size-6 py-1">
              <p className="is-title is-size-6 my-2 has-text-weight-semibold">OPTIONS</p>

              <OptionsDescription options={shipment.options} />

            </div>}
          </div>

          {/* Parcels section */}
          <div className="mt-6 mb-0">
            <p className="is-title is-size-6 my-2 has-text-weight-semibold">
              PARCEL{shipment.parcels.length > 1 && "S"}
            </p>

            {shipment.parcels.map((parcel: ParcelType, index) => <React.Fragment key={index + "parcel-info"}>

              <hr className="my-4" style={{ height: '1px' }} />

              <div className="columns mb-0 is-multiline">

                {/* Parcel details */}
                <div className="column is-6 is-size-6 py-1">
                  <ParcelDescription parcel={parcel} />
                </div>

                {/* Parcel items */}
                {((parcel.items || []).length > 0) &&
                  <div className="column is-6 is-size-6 py-1">
                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">
                      ITEMS {" "}
                      <span className="is-size-7">({(parcel.items || []).reduce((acc, { quantity }) => acc + (quantity || 0), 0)})</span>
                    </p>

                    <div className="menu-list py-2 pr-1" style={{ maxHeight: '40em', overflow: 'auto' }}>
                      {(parcel.items || []).map((item, index) => <React.Fragment key={index + "item-info"}>
                        <hr className="mt-1 mb-2" style={{ height: '1px' }} />
                        <CommodityDescription commodity={item} />
                      </React.Fragment>)}
                    </div>
                  </div>}

              </div>

            </React.Fragment>)}
          </div>

          {/* Customs section */}
          <div className="columns mt-6 mb-0 is-multiline">

            {/* Customs details */}
            {!isNone(shipment.customs) && <div className="column is-6 is-size-6 py-1">
              <p className="is-title is-size-6 my-2 has-text-weight-semibold">CUSTOMS DECLARATION</p>

              <CustomsInfoDescription customs={shipment.customs as CustomsType} />
            </div>}

            {/* Customs commodities */}
            {(!isNone(shipment.customs) && (shipment.customs?.commodities || []).length > 0) && <div className="column is-6 is-size-6 py-1">
              <p className="is-title is-size-6 my-2 has-text-weight-semibold">
                COMMODITIES {" "}
                <span className="is-size-7">({(shipment.customs?.commodities || []).reduce((acc, { quantity }) => acc + (quantity || 0), 0)})</span>
              </p>

              {(shipment.customs?.commodities || []).map((commodity, index) => <React.Fragment key={index + "parcel-info"}>
                <hr className="mt-1 mb-2" style={{ height: '1px' }} />
                <CommodityDescription commodity={commodity} />
              </React.Fragment>)}
            </div>}

          </div>

        </div>


        {/* Document section */}
        {((carrier_capabilities[shipment.carrier_name as string] || []) as any).includes("paperless") && ("paperless_trade" in shipment.options) && <>

          <h2 className="title is-5 my-4">Paperless Trade Documents</h2>

          {(!documents.isFetched && documents.isFetching) && <Spinner />}

          {(documents.isFetched && !documents.isFetching) && [...(uploads || []), ...(shipment.options.doc_files || [])].length == 0 && <>
            <hr className="mt-1 mb-3" style={{ height: '1px' }} />
            <div className="pb-3">No documents uploaded</div>
          </>}

          {documents.isFetched && [...(uploads || []), ...(shipment.options.doc_files || [])].length > 0 &&
            <div className="table-container">
              <table className="related-item-table table is-hoverable is-fullwidth">
                <tbody>
                  {(uploads || []).map(upload => <React.Fragment key={shipment.id}>
                    {(upload.documents || []).map(doc => (
                      <tr key={doc.doc_id} className="items">
                        <td className="description is-vcentered p-0">
                          <span>{doc.file_name}</span>
                        </td>
                        <td className="status is-vcentered p-0">
                          <span className="tag is-success my-2">uploaded</span>
                        </td>
                      </tr>
                    ))}
                  </React.Fragment>)}
                  {(shipment.options.doc_files || []).map((doc: any, idx: number) => (
                    <tr key={`${new Date()}-${idx}`} className="items">
                      <td className="description is-vcentered p-0">
                        <span>{doc.doc_name}</span>
                      </td>
                      <td className="status is-vcentered p-0">
                        <span className="tag is-success my-2">uploaded</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>}

          <div className="is-flex is-justify-content-space-between">
            <div className="is-flex">
              <SelectField
                onChange={e => setFileData({ ...fileData, doc_type: e.target.value })}
                defaultValue="other"
                className="is-small is-fullwidth">
                <option value="other">other</option>
                <option value="commercial_invoice">Commercial invoice</option>
                <option value="pro_forma_invoice">Pro forma invoice</option>
                <option value="packing_list">Packing list</option>
                <option value="certificate_of_origin">Certificate of origin</option>
              </SelectField>
              <InputField className="is-small mx-2" type="file" onChange={handleFileChange} />
            </div>

            <button
              type="button"
              className="button is-default is-small is-align-self-center"
              disabled={(uploads || [])?.length > 4 || !fileData.doc_file || documents.isFetching || uploadDocument.isLoading}
              onClick={() => uploadCustomsDocument()}>
              <span className="icon is-small">
                <i className="fas fa-upload"></i>
              </span>
              <span>Upload</span>
            </button>
          </div>

          <div className="my-3 pt-1"></div>
        </>}


        {/* Metadata section */}
        <MetadataEditor
          id={shipment.id}
          object_type={MetadataObjectTypeEnum.shipment}
          metadata={shipment.metadata}
        >
          <MetadataEditorContext.Consumer>{({ isEditing, editMetadata }) => (<>

            <div className="is-flex is-justify-content-space-between">
              <h2 className="title is-5 my-4">Metadata</h2>

              <button
                type="button"
                className="button is-default is-small is-align-self-center"
                disabled={isEditing}
                onClick={() => editMetadata()}>
                <span className="icon is-small">
                  <i className="fas fa-pen"></i>
                </span>
                <span>Edit metadata</span>
              </button>
            </div>

            <hr className="mt-1 mb-2" style={{ height: '1px' }} />

          </>)}</MetadataEditorContext.Consumer>
        </MetadataEditor>

        <div className="my-6 pt-1"></div>

        {/* Logs section */}
        <h2 className="title is-5 my-4">Logs</h2>

        {!logs.isFetched && logs.isFetching && <Spinner className="my-1 p-1 has-text-centered" size={6} />}

        {logs.isFetched && (logs.data?.logs.edges || []).length == 0 && <div>No logs</div>}

        {logs.isFetched && (logs.data?.logs.edges || []).length > 0 &&
          <div className="table-container py-2" style={{ maxHeight: '20em', overflow: 'auto' }}>
            <table className="related-item-table table is-hoverable is-fullwidth">
              <tbody>
                {(logs.data?.logs.edges || []).map(({ node: log }) => (
                  <tr key={log.id} className="items is-clickable">
                    <td className="status is-vcentered p-0">
                      <AppLink href={`/developers/logs/${log.id}`} className="pr-2">
                        <StatusCode code={log.status_code as number} />
                      </AppLink>
                    </td>
                    <td className="description is-vcentered p-0">
                      <AppLink href={`/developers/logs/${log.id}`} className="is-size-7 has-text-weight-semibold has-text-grey is-flex py-3">
                        {`${log.method} ${log.path}`}
                      </AppLink>
                    </td>
                    <td className="date is-vcentered p-0">
                      <AppLink href={`/developers/logs/${log.id}`} className="is-size-7 has-text-weight-semibold has-text-grey is-flex is-justify-content-right py-3">
                        <span>{formatDateTime(log.requested_at)}</span>
                      </AppLink>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>}

        <div className="my-6 pt-1"></div>

        {/* Events section */}
        <h2 className="title is-5 my-4">Events</h2>

        {!events.isFetched && events.isFetching && <Spinner className="my-1 p-1 has-text-centered" size={6} />}

        {events.isFetched && (events.data?.events.edges || []).length == 0 && <div>No events</div>}

        {events.isFetched && (events.data?.events.edges || []).length > 0 &&
          <div className="table-container py-2" style={{ maxHeight: '20em', overflow: 'auto' }}>
            <table className="related-item-table table is-hoverable is-fullwidth">
              <tbody>
                {(events.data?.events.edges || []).map(({ node: event }) => (
                  <tr key={event.id} className="items is-clickable">
                    <td className="description is-vcentered p-0">
                      <AppLink href={`/developers/events/${event.id}`} className="is-size-7 has-text-weight-semibold has-text-grey is-flex py-3">
                        {`${event.type}`}
                      </AppLink>
                    </td>
                    <td className="date is-vcentered p-0">
                      <AppLink href={`/developers/events/${event.id}`} className="is-size-7 has-text-weight-semibold has-text-grey is-flex is-justify-content-right py-3">
                        <span>{formatDateTime(event.created_at)}</span>
                      </AppLink>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>}

      </>}

      {query.isFetched && isNone(shipment) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>Uh Oh!</p>
          <p>{"We couldn't find any shipment with that reference"}</p>
        </div>

      </div>}
    </>
  );
};

export default function ShipmentPage(pageProps: any) {
  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Shipment - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <ConfirmModal>

        <ShipmentComponent />

      </ConfirmModal>
    </DashboardLayout>
  ), pageProps);
}
