import { CarrierSettingsCarrierNameEnum } from '@karrio/types';
import Image from "next/legacy/image";
import { p } from '@karrio/lib';
import React from 'react';


interface CarrierImageComponent extends React.AllHTMLAttributes<HTMLImageElement> {
  carrier_name?: CarrierSettingsCarrierNameEnum | string;
  containerClassName?: string;
}

export const CarrierImage: React.FC<CarrierImageComponent> = ({ carrier_name, containerClassName, className, width, height, ...props }) => {
  return (
    <div className={containerClassName || 'm-1'} {...props}>
      <Image
        src={p`/carriers/${carrier_name as string}_icon.svg`}
        width={width as number || 60} height={height as number || 60}
        alt={carrier_name}
        className={className || ''}
      />
    </div>
  );
};
