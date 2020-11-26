import { LabelData, state } from '@/library/api';
import { View } from '@/library/types';
import { Link } from '@reach/router';
import React, { useEffect, useState } from 'react';
import ShipmentCustomsInfo from '@/components/form-parts/shipment-customs-info';
import ShipmentAddress from '@/components/form-parts/shipment-address';
import ShipmentOptions from '@/components/form-parts/shipment-options';
import ShipmentParcel from '@/components/form-parts/shipment-parcel';
import LiveRates from '@/components/live-rates';
import Tabs from '@/components/generic/tabs';
import { Shipment } from '@purplship/purplship';

interface LabelCreatorComponent extends View {
    id?: string;
    data: LabelData;
}

const LabelCreator: React.FC<LabelCreatorComponent> = ({ data, id }) => {
    const tabs = ["shipper", "recipient", "parcel", "customs info", "options"];
    const [key, setKey] = useState<string>(`${id}-${Date.now()}`);
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
    const update = (payload: Partial<Shipment>) => {
        const new_state = { ...data, shipment: { ...data.shipment, ...payload } };
        Object.entries(payload).forEach(([key, val]) => {
            if (val === undefined) delete new_state.shipment[key as keyof Shipment];
        });
        state.setLabelData(new_state);
    };

    useEffect(() => {
        if (id !== undefined && id !== 'new') {
            state.retrieveShipment(id).then(shipment => {
                state.setLabelData({ shipment });
                setKey(`${id}-${Date.now()}`);
            });
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

            <div className="columns px-2" key={key}>
                <div className="column is-7 px-0">

                    <div className="card px-3 py-3">
                        <Tabs tabs={tabs} disabled={filterDisabled(data.shipment)} eventKey="label-select-tab">

                            <ShipmentAddress shipment={data.shipment} addressName="shipper" update={update} />

                            <ShipmentAddress shipment={data.shipment} addressName="recipient" update={update} />

                            <ShipmentParcel shipment={data.shipment} update={update} />

                            <ShipmentCustomsInfo shipment={data.shipment} update={update} />

                            <ShipmentOptions shipment={data.shipment} update={update} />

                        </Tabs>
                    </div>

                </div>
                <div className="column is-5">

                    <div className="card px-3 py-3">
                        <LiveRates shipment={data.shipment} update={(data) => { update(data); setKey(`${id}-${Date.now()}`); }} />
                    </div>

                </div>
            </div>

        </>
    )
};

export default LabelCreator;