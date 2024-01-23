import { formatAddressLocationShort, formatCarrierSlug, formatRef, isNone } from '@karrio/lib';
import { ParcelDescription } from '../components/parcel-description';
import { useBulkShipmentForm } from '@karrio/hooks/bulk-shipments';
import { AddressType, NotificationType } from '@karrio/types';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { CarrierImage } from '../components/carrier-image';
import { ShipmentData } from '@karrio/types/rest/api';
import { useNotifier } from '../components/notifier';
import { ModalFormProps, useModal } from './modal';
import { useLoader } from '../components/loader';
import React from 'react';
import { RateDescription } from '../components/rate-description';

type BulkShipmentModalEditorProps = {
  header?: string;
  shipments: ShipmentData[];
};

export const BulkShipmentModalEditor: React.FC<ModalFormProps<BulkShipmentModalEditorProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const Component: React.FC<BulkShipmentModalEditorProps> = props => {
    const { shipments, header } = props;
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const { metadata } = useAPIMetadata();
    const [key, setKey] = React.useState<string>(`bulk-labels-${Date.now()}`);
    const { mutations, ...mutation } = useBulkShipmentForm(shipments);

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      try {
        await mutation.buyLabels();
        // setTimeout(() => close(), 1000);
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
      }
      loader.setLoading(false);
    };

    return (
      <div className="modal-card-body modal-form has-background-white">

        <header className="pb-4 pt-0 is-flex is-justify-content-space-between">
          <div className="is-vcentered">
            <button className="button is-white is-small" aria-label="close" onClick={close}>
              <span className="icon is-large">
                <i className="fas fa-lg fa-times"></i>
              </span>
            </button>
            <span className="title is-6 has-text-weight-semibold p-3">Create shipping labels</span>
          </div>
          <div>
            <button type="button" className="button is-small is-success" onClick={handleSubmit}
              disabled={loader.loading || Object.keys(mutations || {}).length === 0}>
              <span>Create labels</span>
            </button>
          </div>
        </header>

        <hr className='mt-1 mb-5' style={{ height: '1px' }} />

        {Object.keys(mutations || {}).length > 0 && <>

          <div className="table-container pb-1">
            <table className="batch-labels-table table is-fullwidth">

              <tbody className="card">

                <tr className="is-size-6 has-text-weight-bold">
                  <td className="selector has-text-centered p-2" onClick={e => e.preventDefault()}>
                    <label className="checkbox p-2">
                      <input
                        name="all"
                        type="checkbox"
                      />
                    </label>
                  </td>
                  <td className="order is-vcentered">Order #</td>
                  <td className="items is-vcentered">Items</td>
                  <td className="package is-vcentered">Package</td>
                  <td className="total is-vcentered">Total weight</td>
                  <td className="service is-vcentered">Shipping service</td>
                </tr>

                {Object.entries(mutations).map(([index, mutation]) => (
                  <tr key={`${index}-${mutation.state.shipment.id}-${new Date()}`} className="items is-size-7">
                    <td className="selector has-text-centered is-vcentered p-0">
                      <label className="checkbox py-3 px-2">
                        <input
                          type="checkbox"
                          name={`${index}`}
                        />
                      </label>
                    </td>
                    <td className="order is-vcentered panel is-size-7">
                      <label className="panel-block p-2 card">
                        <div>
                          <span className="has-text-weight-bold text-ellipsis">
                            {`#${mutation.state.shipment.meta?.order_id || mutation.state.shipment.metadata?.order_ids || ' - '}`}
                          </span>
                          <br />
                          <span className="has-text-weight-medium text-ellipsis">
                            {formatAddressLocationShort(mutation.state.shipment.recipient as AddressType)}
                          </span>
                        </div>
                      </label>
                    </td>
                    <td className="items is-vcentered panel is-size-7">
                      <label className="panel-block p-2 card">
                        <div>
                          <p className="is-size-7 has-text-weight-bold has-text-grey">
                            {((items: number): any => `${items} item${items === 1 ? '' : 's'}`)(
                              (mutation.state.shipment.parcels[0]?.items || []).reduce(
                                (acc, item) => acc + (item.quantity as number) || 1, 0
                              )
                            )}
                          </p>
                          <p className="is-size-7 has-text-grey" style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                            {(mutation.state.shipment.parcels[0]?.items || []).length > 1
                              ? "(Multiple)"
                              : (mutation.state.shipment.parcels[0]?.items || [])[0]?.title || (mutation.state.shipment.parcels[0]?.items || [])[0]?.description || (mutation.state.shipment.parcels[0]?.items || [])[0]?.sku}
                          </p>
                        </div>
                      </label>
                    </td>
                    <td className="package is-vcentered text-ellipsis">
                      <label className="panel-block p-2 card">
                        <div>
                          <ParcelDescription parcel={mutation.state.shipment.parcels[0]} />
                        </div>
                      </label>
                    </td>
                    <td className="total is-vcentered">
                      <label className="panel-block px-2 p-4 card">
                        <div>
                          <span className="has-text-weight-bold">
                            {`${mutation.state.shipment.parcels[0]?.weight || 0}`}
                            {` `}
                            {mutation.state.shipment.parcels[0]?.weight_unit || 'KG'}
                          </span>
                        </div>
                      </label>
                    </td>
                    <td className="service is-vcentered">
                      <label className="panel-block p-1 card">
                        <div className="icon-text">
                          <CarrierImage
                            carrier_name={(mutation.state.shipment.rates || [])[0]?.carrier_name || formatCarrierSlug(metadata.APP_NAME)}
                            containerClassName="mt-1 ml-1 mr-2" height={28} width={28}
                          />
                          <div className="text-ellipsis" style={{ maxWidth: '190px', lineHeight: '16px' }}>
                            {!!(mutation.state.shipment.rates || [])[0] &&
                              <RateDescription rate={(mutation.state.shipment.rates || [])[0]} />}
                          </div>
                        </div>
                      </label>
                    </td>
                  </tr>
                ))}

              </tbody>

            </table>
          </div>

        </>}

      </div>
    )
  };

  return React.cloneElement(trigger, {
    onClick: () => modal.open(<Component {...args} />, {
      className: 'is-large-modal',
      addCloseButton: false,
    })
  });
};
