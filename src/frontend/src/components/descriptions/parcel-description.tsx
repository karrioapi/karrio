import React from 'react';
import { Parcel } from '@/api';
import { formatParcelLabel, formatDimension, formatWeight } from '@/library/helper';

interface ParcelDescriptionComponent {
    parcel?: Parcel;
}

const ParcelDescription: React.FC<ParcelDescriptionComponent> = ({ parcel }) => {
    return (
        <>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{formatParcelLabel(parcel)}</p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatDimension(parcel)}</p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatWeight(parcel)}</p>
        </>
    );
};

export default ParcelDescription;
