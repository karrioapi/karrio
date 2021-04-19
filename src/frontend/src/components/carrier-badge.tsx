import { Collection } from '@/library/types';
import { CarrierSettingsCarrierNameEnum } from '@/api';
import React, { useContext } from 'react';
import { APIReference } from './data/references-query';

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
    const { carriers } = useContext(APIReference);
    const name = carrier || '';
    
    return (
        <>
            {carriers && (
                <span className={`${className} ${THEME[name] || 'is-light'}`} {...props}>{(carriers as Collection)[name] || "Unknown"}</span>
            )}
        </>
    );
};

export default CarrierBadge;
