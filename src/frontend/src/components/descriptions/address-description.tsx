import React, { useContext } from 'react';
import { Address, References } from '@/api';
import { formatAddressName, formatFullAddress } from '@/library/helper';
import { Reference } from '@/library/context';

interface AddressDescriptionComponent {
    address: Address;
}

const AddressDescription: React.FC<AddressDescriptionComponent> = ({ address }) => {
    const Ref = useContext<References>(Reference);
    return (
        <>

            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{formatAddressName(address)}</p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatFullAddress(address, Ref?.countries as any)}</p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-info">{address.email}</p>
            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-info">{address.phone_number}</p>

        </>
    );
};

export default AddressDescription;
