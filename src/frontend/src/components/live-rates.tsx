import { NotificationType, state } from '@/library/api';
import { Reference } from '@/library/context';
import { deepEqual, formatAddressName, formatDate, formatDimension, formatFullAddress, formatParcelLabel, formatRef, formatWeight, isNone } from '@/library/helper';
import { Collection } from '@/library/types';
import { Payment, References, Shipment } from '@purplship/purplship';
import { useNavigate } from '@reach/router';
import React, { useContext, useState } from 'react';
import ButtonField from './generic/button-field';

interface LiveRatesComponent {
    shipment: Shipment;
    update: (payload: {}, refresh?: boolean) => void;
}

const LiveRates: React.FC<LiveRatesComponent> = ({ shipment, update }) => {
    const navigate = useNavigate();
    const Ref = useContext<References>(Reference);
    const [loading, setLoading] = useState<boolean>(false);
    const [selected_rate_id, setSelectedRate] = useState<string | undefined>(shipment?.selected_rate_id);
    const [lastState, setLastSate] = useState<Shipment>((shipment?.rates || []).length === 0 ? {} as Shipment : shipment);
    const [countries] = useState<Collection | undefined>(Ref?.countries);

    const computeDisabled = (shipment: Shipment) => {
        return (
            shipment.recipient.address_line1 === undefined ||
            shipment.shipper.address_line1 === undefined ||
            shipment.parcels.length === 0 ||
            deepEqual(lastState || {}, shipment) ||
            loading === true
        );
    };
    const fetchRates = async () => {
        if (computeDisabled(shipment)) return;
        setLastSate({ ...shipment });
        let data: Partial<Shipment> = { rates: undefined, selected_rate_id: undefined };
        try {
            setLoading(true);
            setLastSate(shipment);
            const response = await state.fetchRates(shipment);
            data = { ...data, ...(response || {}) };
            if (shipment.id === undefined) navigate('/buy_label/' + response.id);
            update(data, true);
        } catch (err) {
            state.setNotification({ type: NotificationType.error, message: err });
        } finally {
            setLoading(false);
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

                    <button className={`button is-small is-outlined is-info is-pulled-right ${loading ? 'is-loading' : ''}`} onClick={fetchRates} disabled={computeDisabled(shipment)}>
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
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{formatParcelLabel(shipment.parcels[0])}</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatDimension(shipment.parcels[0])}</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatWeight(shipment.parcels[0])}</p>

                </div>

                <div className="column is-12 py-1" style={{ display: `${Object.values(shipment.options).length === 0 ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Options</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                        {isNone(shipment.options.shipment_date) ? '' : <span>Shipment Date: <strong>{` ${formatDate(shipment.options.shipment_date)}`}</strong></span>}
                    </p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                        {isNone(shipment.options.currency) ? '' : <span>Preferred Currency: <strong>{` ${shipment.options.currency}`}</strong></span>}
                    </p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                        {isNone(shipment.options.signature_confirmation) ? '' : <span>Signature Confirmation <strong>Required</strong></span>}
                    </p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                        {isNone(shipment.options.insurance) ? '' : <>
                            <span>Insurance (Package Value <strong>{shipment.options.insurance} {shipment.options.currency}</strong>)</span>
                        </>}
                    </p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                        {isNone(shipment.options.cash_on_delivery) ? '' : <>
                            <span>Amount To Collect <strong>{shipment.options.cash_on_delivery}{shipment.options.currency}</strong></span>
                        </>}
                    </p>

                </div>

                <div className="column is-12 py-3" style={{ display: `${(shipment.rates || []).length === 0 ? 'none' : 'block'}` }}>

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
                style={(shipment.rates || []).length === 0 ? { display: 'none' } : {}}
                disabled={(shipment.rates || []).filter(r => r.id === selected_rate_id).length === 0}>
                <span>Buy</span>
            </ButtonField>

        </div>
    )
};

export default LiveRates;