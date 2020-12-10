import { NotificationType, state } from '@/library/api';
import { Reference } from '@/library/context';
import { formatAddressName, formatDimension, formatFullAddress, formatRef, formatWeight } from '@/library/helper';
import { Collection } from '@/library/types';
import { Payment, References, Shipment } from '@purplship/purplship';
import { useNavigate } from '@reach/router';
import React, { useContext, useState } from 'react';
import ButtonField from './generic/button-field';

interface LiveRatesComponent {
    shipment: Shipment;
    update: (payload: {}) => void;
}

const LiveRates: React.FC<LiveRatesComponent> = ({ shipment, update }) => {
    const navigate = useNavigate();
    const Ref = useContext<References>(Reference);
    const [loading, setLoading] = useState<boolean>(false);
    const [selected_rate_id, setSelectedRate] = useState<string | undefined>(shipment?.selected_rate_id);
    const [lastState, setLastSate] = useState<Shipment | undefined>(undefined);
    const [countries] = useState<Collection | undefined>(Ref?.countries);

    const computeEnable = (shipment: Shipment) => {
        return (
            shipment.recipient.address_line1 === undefined ||
            shipment.shipper.address_line1 === undefined ||
            shipment.parcels.length === 0 ||
            lastState == shipment
        );
    };
    const fetchRates = async () => {
        let data: Partial<Shipment> = { rates: undefined };
        try {
            setLoading(true);
            setLastSate(shipment);
            const response = await state.fetchRates(shipment);
            data = { ...data, ...(response || {}) };
        } catch (err) {
            state.setNotification({ type: NotificationType.error, message: err });
        } finally {
            setLoading(false);
            setSelectedRate(data.selected_rate_id);
            update(data);
        }
    };
    const buyShipment = async () => {
        try {
            setLoading(true);
            let currency = (shipment.options || {}).currency || Payment.CurrencyEnum.CAD;
            const response = await state.buyLabel({
                ...shipment,
                selected_rate_id: selected_rate_id as string,
                payment: { paid_by: Payment.PaidByEnum.Sender, currency } as Payment
            });
            update(response.shipment as Shipment);
            state.setNotification({ type: NotificationType.success, message: 'Label successfully purchased!' });
            navigate('/');
        } catch (err) {
            state.setNotification({ type: NotificationType.error, message: err });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="columns is-multiline">

                <div className="column is-12 pb-2">
                    <span className="title is-5">Shipment Details</span>

                    <button className={`button is-small is-outlined is-info is-pulled-right ${loading ? 'is-loading' : ''}`} onClick={fetchRates} disabled={computeEnable(shipment)}>
                        <span>Fetch Rates</span>
                    </button>
                </div>

                <div className="column is-12 py-1" style={shipment.shipper.address_line1 === undefined ? { display: 'none' } : {}}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Shipper Address</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{formatAddressName(shipment.shipper)}</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatFullAddress(shipment.shipper, countries)}</p>
                    {shipment.shipper.email !== undefined && 
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-info">{shipment.shipper.email}</p>}
                    {shipment.shipper.phone_number !== undefined && 
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{shipment.shipper.phone_number}</p>}

                </div>

                <div className="column is-12 py-1" style={{ display: `${shipment.recipient.address_line1 === undefined ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Recipient Address</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{formatAddressName(shipment.recipient)}</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatFullAddress(shipment.recipient, countries)}</p>
                    {shipment.recipient.email !== undefined && 
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-info">{shipment.recipient.email}</p>}
                    {shipment.recipient.phone_number !== undefined && 
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{shipment.recipient.phone_number}</p>}

                </div>

                <div className="column is-12 py-1" style={{ display: `${shipment.parcels.length == 0 ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Parcel</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatDimension(shipment.parcels[0])}</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatWeight(shipment.parcels[0])}</p>

                </div>

                <div className="column is-12 py-3" style={{ display: `${shipment.rates === undefined ? 'none' : 'block'}` }}>

                    <h6 className="is-title is-size-6 mt-1 mb-4 has-text-weight-semibold">Live Rates</h6>

                    <ul className="menu-list">
                        {shipment.rates?.map(rate => (
                            <li key={rate.id}>
                                <a className={`columns mb-0 ${rate.id === selected_rate_id ? 'has-text-grey-dark' : 'has-text-grey'}`} onClick={() => setSelectedRate(rate.id)}>

                                    <span className={`icon is-medium ${rate.id === selected_rate_id ? 'has-text-success' : ''}`}>
                                        {(rate.id === selected_rate_id) ? <i className="fas fa-check-square"></i> : <i className="fas fa-square"></i>}
                                    </span>

                                    <div className="is-size-7 has-text-weight-semibold">
                                        <h6 className="has-text-weight-bold">{formatRef(rate.service as string)}</h6>
                                        <span>{rate.total_charge} {rate.currency}</span>
                                        {(rate.transit_days !== null) && <span> - {rate.transit_days} Transit days</span>}
                                    </div>
                                </a>
                            </li>
                        ))}
                    </ul>

                </div>

            </div>

            <ButtonField
                onClick={buyShipment}
                fieldClass="has-text-centered mt-3"
                className={`is-success ${loading ? 'is-loading' : ''}`}
                style={shipment.rates === undefined ? { display: 'none' } : {}}
                disabled={selected_rate_id === undefined}>
                <span>Buy</span>
            </ButtonField>

        </div>
    )
};

export default LiveRates;