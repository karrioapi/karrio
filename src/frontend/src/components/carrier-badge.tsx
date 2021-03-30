import { Reference } from '@/library/context';
import { Collection } from '@/library/types';
import { CarrierSettingsCarrierNameEnum } from '@/api';
import React from 'react';

const THEME: Collection = {
    'aramex': 'is-aramex',
    'australiapost': 'is-australiapost',
    'boxknight': 'is-boxknight',
    'canadapost': 'is-canadapost',
    'canpar': 'is-canpar',
    'dicom': 'is-dicom',
    'dhl_express': 'is-dhl',
    'dhl_universal': 'is-dhl',
    'eshipper': 'is-eshipper',
    'fedex_express': 'is-fedex',
    'freightcom': 'is-freightcom',
    'purolator_courier': 'is-purolator',
    'royalmail': 'is-royalmail',
    'sendle': 'is-sendle',
    'sf_express': 'is-sf_express',
    'ups_package': 'is-ups',
    'usps': 'is-usps',
    'yanwen': 'is-yanwen',
    'yunexpress': 'is-yunexpress',
};

interface CarrierBadgeComponent extends React.AllHTMLAttributes<HTMLSpanElement> {
    carrier?: CarrierSettingsCarrierNameEnum | string;
}

const CarrierBadge: React.FC<CarrierBadgeComponent> = ({ carrier, className, ...props }) => {
    const name = carrier || '';
    return (
        <Reference.Consumer>
            {ref => (Object.values(ref || {}).length > 0) && (
                <span className={`${className} ${THEME[name] || 'is-light'}`} {...props}>{(ref.carriers as Collection)[name] || "Unknown"}</span>
            )}
        </Reference.Consumer>
    );
};

export default CarrierBadge;
