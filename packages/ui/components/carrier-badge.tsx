import { CarrierSettingsCarrierNameEnum } from '@karrio/types';
import { p } from '@karrio/lib';
import Image from "next/image";
import React from 'react';


interface CarrierBadgeComponent extends React.AllHTMLAttributes<HTMLDivElement> {
  carrier_name?: CarrierSettingsCarrierNameEnum | string;
  width?: number;
  height?: number;
}

export const CarrierBadge: React.FC<CarrierBadgeComponent> = ({ carrier_name, className, width, height, ...props }) => {
  return (
    <div className='mt-1'>
      <Image
        src={p`/carriers/${carrier_name}_logo.svg`}
        height={height || 14}
        width={width || 70}
        alt="carrier logo"
      />
    </div>
  );
};
