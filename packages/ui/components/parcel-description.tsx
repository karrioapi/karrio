import { formatParcelLabel, formatDimension, formatWeight, isNoneOrEmpty } from '@karrio/lib';
import { ParcelType } from '@karrio/types';
import React from 'react';

interface ParcelDescriptionComponent {
  parcel?: ParcelType;
  suffix?: React.ReactNode | string;
  prefix?: React.ReactNode | string;
}

export const ParcelDescription: React.FC<ParcelDescriptionComponent> = ({ parcel, prefix, suffix }) => {
  const weightDescription = formatWeight(parcel);
  const dimensionDescription = formatDimension(parcel);

  return (
    <>
      <p className="is-size-7 has-text-weight-semibold text-ellipsis">{prefix} {formatParcelLabel(parcel)} {suffix}</p>
      <p className="is-size-7 has-text-weight-semibold has-text-grey text-ellipsis">
        {dimensionDescription}
        {isNoneOrEmpty(dimensionDescription) || isNoneOrEmpty(weightDescription) ? '' : ', '}
        {weightDescription}
      </p>
    </>
  );
};
