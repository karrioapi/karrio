import { CarrierSettingsCarrierNameEnum } from '@karrio/rest';
import { p } from '@/lib/client';
import Image from "next/image";
import React from 'react';


interface CarrierBadgeComponent extends React.AllHTMLAttributes<HTMLDivElement> {
  carrier_name?: CarrierSettingsCarrierNameEnum | string;
}

const CarrierBadge: React.FC<CarrierBadgeComponent> = ({ carrier_name, className, ...props }) => {
  return (
    <div className='mt-1'>
      <Image src={p`/carriers/${carrier_name}_logo.svg`} height="25" width="100" alt="carrier logo" />
    </div>
  );
};

export default CarrierBadge;
