import { state } from '@/library/api';
import { deepEqual, formatRef, isNone } from '@/library/helper';
import { NotificationType } from '@/library/types';
import { Customs, Payment, Shipment } from '@purplship/purplship';
import { useNavigate } from '@reach/router';
import React, { useState } from 'react';
import AddressDescription from './descriptions/address-description';
import CustomsInfoDescription from './descriptions/customs-info-description';
import OptionsDescription from './descriptions/options-description';
import ParcelDescription from './descriptions/parcel-description';
import ButtonField from './generic/button-field';

interface LiveRatesComponent {
    shipment: Shipment;
    update: (payload: {}, refresh?: boolean) => void;
}

const LiveRates: React.FC<LiveRatesComponent> = ({ shipment, update }) => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState<boolean>(false);
    const [selected_rate_id, setSelectedRate] = useState<string | undefined>(shipment?.selected_rate_id);
    const [label_type, setLabelType] = useState<Shipment.LabelTypeEnum>(shipment?.label_type || Shipment.LabelTypeEnum.PDF);
    const [lastState, setLastSate] = useState<Shipment>((shipment?.rates || []).length === 0 ? {} as Shipment : shipment);

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
        let data: Partial<Shipment> = { rates: undefined, selected_rate_id: undefined };
        try {
            setLoading(true);
            const response = await state.fetchRates(shipment);
            data = { ...data, ...(response || {}) };
            if (shipment.id === undefined) navigate('/buy_label/' + response.id);
            update(data, true);
            setLastSate({ ...shipment });
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
                label_type: label_type,
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
                    <AddressDescription address={shipment.shipper} />

                </div>

                <div className="column is-12 py-1" style={{ display: `${shipment.recipient.address_line1 === undefined ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Recipient Address</p>
                    <AddressDescription address={shipment.recipient} />

                </div>

                <div className="column is-12 py-1" style={{ display: `${shipment.parcels.length == 0 ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Parcel</p>
                    <ParcelDescription parcel={shipment.parcels[0]} />

                </div>

                <div className="column is-12 py-1" style={{ display: `${Object.values(shipment.options).length === 0 ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Options</p>
                    <OptionsDescription options={shipment.options} />

                </div>

                <div className="column is-12 py-1" style={{ display: `${isNone(shipment.customs) ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Customs Declaration</p>
                    <CustomsInfoDescription customs={(shipment.customs || {}) as Customs} />

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

                <div className="column is-12 py-3" style={{ display: `${(shipment.rates || []).length === 0 ? 'none' : 'block'}` }}>

                    <h6 className="is-title is-size-6 mt-1 mb-4 has-text-weight-semibold">Select your label type</h6>
                    <div className="control">
                        <label className="radio">
                            <input className="mr-1" type="radio" name="label_type" defaultChecked={label_type === Shipment.LabelTypeEnum.PDF} onChange={() => setLabelType(Shipment.LabelTypeEnum.PDF)}/>
                            <span className="is-size-6 has-text-weight-bold">{Shipment.LabelTypeEnum.PDF}</span>
                        </label>
                        <label className="radio">
                            <input className="mr-1" type="radio" name="label_type" defaultChecked={label_type === Shipment.LabelTypeEnum.ZPL} onChange={() => setLabelType(Shipment.LabelTypeEnum.ZPL)} />
                            <span className="is-size-6 has-text-weight-bold">{Shipment.LabelTypeEnum.ZPL}</span>
                        </label>
                    </div>

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