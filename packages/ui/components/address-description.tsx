import { formatAddressName, formatFullAddress } from '@karrio/lib';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { AddressType, Collection } from '@karrio/types';
import React from 'react';

interface AddressDescriptionComponent {
  address: AddressType;
}

export const AddressDescription: React.FC<AddressDescriptionComponent> = ({ address }) => {
  const { references } = useAPIMetadata();
  return (
    <>

      <p className="is-size-7 my-1 has-text-weight-semibold">{formatAddressName(address)}</p>
      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatFullAddress(address, references.countries as Collection)}</p>
      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">{address.email}</p>
      <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">{address.phone_number}</p>

    </>
  );
};
