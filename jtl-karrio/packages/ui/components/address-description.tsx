import { formatAddressName, formatFullAddress } from "@karrio/lib";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AddressType, Collection } from "@karrio/types";
import React from "react";

interface AddressDescriptionComponent {
  address: AddressType;
}

export const AddressDescription = ({
  address,
}: AddressDescriptionComponent): JSX.Element => {
  const { references } = useAPIMetadata();
  return (
    <>
      <p className="text-xs my-1 font-semibold">
        {formatAddressName(address)}
      </p>
      <p className="text-xs my-1 font-semibold text-muted-foreground">
        {formatFullAddress(address, references.countries as Collection)}
      </p>
      <p className="text-xs my-1 font-semibold text-muted-foreground">
        {address.email}
      </p>
      <p className="text-xs my-1 font-semibold text-muted-foreground">
        {address.phone_number}
      </p>
    </>
  );
};