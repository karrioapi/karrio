import { state } from '@/library/api';
import { LabelData, NotificationType, View } from '@/library/types';
import { Link, useNavigate } from '@reach/router';
import React, { useEffect, useState } from 'react';
import CustomsInfoForm from '@/components/form-parts/customs-info-form';
import AddressForm from '@/components/form-parts/address-form';
import ShipmentOptions from '@/components/form-parts/shipment-options';
import ParcelForm from '@/components/form-parts/parcel-form';
import LiveRates from '@/components/live-rates';
import Tabs from '@/components/generic/tabs';
import { Shipment } from '@purplship/purplship';

interface LabelCreatorComponent extends View {
    id?: string;
    data: LabelData;
}

const LabelCreator: React.FC<LabelCreatorComponent> = ({ data, id }) => {
    const navigate = useNavigate();
    const tabs = ["shipper", "recipient", "parcel", "customs info", "options"];
    const [ckey, setKey] = useState<string>(`${id}-${Date.now()}`);
    const filterDisabled = (shipment: Shipment) => {
        return tabs.reduce((disabled: string[], value: string) => {
            const is_local = shipment?.shipper.country_code === shipment?.recipient.country_code;

            // Disable tab if >>>
            if (
                // is 'recipient' AND 'shipment.shipper' hasn't been defined yet
                (value === "recipient" && shipment.shipper.address_line1 === undefined)

                || // OR

                // is 'parcel' AND 'shipment.recipient' hasn't been defined yet
                (value === "parcel" && shipment.recipient.address_line1 === undefined)

                || // OR

                // is 'customs info' AND local shipment
                (value === "customs info" && is_local)

                || // OR

                // is 'customs info' AND 'shipment.parcels' is empty
                (value === "customs info" && shipment.parcels.length == 0)

                || // OR

                // is 'options' AND 'shipment.parcels' is empty
                (value === "options" && shipment.parcels.length == 0)
            ) {
                return disabled.concat(value);
            }

            return disabled;
        }, []);
    };
    const update = (payload: Partial<Shipment>, refresh?: boolean) => {
        const new_state = { ...data, shipment: { ...data.shipment, ...payload } };
        Object.entries(payload).forEach(([key, val]) => {
            if (val === undefined) delete new_state.shipment[key as keyof Shipment];
        });
        state.setLabelData(new_state);
        if (refresh) setKey(`${id}-${Date.now()}`);
    };

    useEffect(() => {
        if (id !== undefined && id !== 'new') {
            state.retrieveShipment(id).then(shipment => {
                if (shipment.status === Shipment.StatusEnum.Created) {
                    state.setLabelData({ shipment });
                    setKey(`${id}-${Date.now()}`);
                } else {
                    state.setNotification({ type: NotificationType.info, message: 'Label already purchased!' });
                    navigate('/');
                }
            });
        } else {
            state.fetchDefaultTemplates();
        }
    }, []);

    return (
        <>
            <nav className="breadcrumb has-succeeds-separator" aria-label="breadcrumbs">
                <ul>
                    <li><Link to="/">Shipments</Link></li>
                    <li className="is-active"><a href="#" aria-current="page">Create Label</a></li>
                </ul>
            </nav>

            <div className="columns px-2">
                <div className="column is-7 px-0">

                    <div className="card px-3 py-3">
                        <Tabs tabs={tabs} disabled={filterDisabled(data.shipment)} eventKey="label-select-tab">

                            <AddressForm key={ckey} value={data.shipment.shipper} shipment={data.shipment} update={update} name="shipper" />

                            <AddressForm key={ckey} value={data.shipment.recipient} shipment={data.shipment} update={update} name="recipient" />

                            <ParcelForm key={ckey} value={data.shipment.parcels[0]} shipment={data.shipment} update={update} />

                            <CustomsInfoForm key={ckey} value={data.shipment.customs} shipment={data.shipment} update={update} />

                            <ShipmentOptions key={ckey} shipment={data.shipment} update={update} />

                        </Tabs>
                    </div>

                </div>
                <div className="column is-5">

                    <div className="card px-3 py-3">
                        <LiveRates key={ckey} shipment={data.shipment} update={update} />
                    </div>

                </div>
            </div>

        </>
    )
};

export default LabelCreator;