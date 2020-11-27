import { Reference } from '@/library/context';
import { Collection } from '@/library/types';
import React from 'react';

const THEME: Collection = {
    'boxknight': 'is-boxknight',
    'canadapost': 'is-canadapost',
    'canpar': 'is-canpar',
    'dicom': 'is-dicom',
    'dhl_express': 'is-dhl',
    'eshipper': 'is-eshipper',
    'fedex_express': 'is-fedex',
    'freightcom': 'is-freightcom',
    'purolator_courier': 'is-purolator',
    'ups_package': 'is-ups',
    'usps': 'is-usps',
};

interface CarrierBadgeComponent extends React.AllHTMLAttributes<HTMLSpanElement> {
    name: string;
}

const CarrierBadge: React.FC<CarrierBadgeComponent> = ({ name, className, ...props }) => {
    return (
        <Reference.Consumer>
            {ref => (Object.values(ref || {}).length > 0) && (
                <span className={`${className} ${THEME[name] || 'is-light'}`} {...props}>{ref.carriers[name] || "Unknown"}</span>
            )}
        </Reference.Consumer>
    );
};

export default CarrierBadge;
