import { formatParcelLabel, formatDimension, formatWeight, isNoneOrEmpty } from '@/lib/helper';
import { ParcelType } from '@/lib/types';
import React from 'react';

interface ParcelDescriptionComponent {
  parcel?: ParcelType;
  suffix?: React.ReactNode | string;
  prefix?: React.ReactNode | string;
}

const ParcelDescription: React.FC<ParcelDescriptionComponent> = ({ parcel, prefix, suffix }) => {
  const weightDescription = formatWeight(parcel);
  const dimensionDescription = formatDimension(parcel);

  return (
    <>
      <p className="is-size-7 my-1 has-text-weight-semibold">{prefix} {formatParcelLabel(parcel)} {suffix}</p>
      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">
        {dimensionDescription}
        {isNoneOrEmpty(dimensionDescription) || isNoneOrEmpty(weightDescription) ? '' : ', '}
        {weightDescription}
      </p>
    </>
  );
};

export default ParcelDescription;
