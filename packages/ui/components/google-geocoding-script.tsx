import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import Script from 'next/script';
import React from 'react';


export const GoogleGeocodingScript: React.FC = () => {
  const { references: { ADDRESS_AUTO_COMPLETE } } = useAPIMetadata();
  const initMap = () => { };

  React.useEffect(() => (window as any).initMap = initMap, []);

  return (
    <>
      {(ADDRESS_AUTO_COMPLETE?.provider === 'google') &&
        <Script strategy='lazyOnload' src={`https://maps.googleapis.com/maps/api/js?key=${ADDRESS_AUTO_COMPLETE.key}&libraries=places&callback=initMap`}></Script>
      }
    </>
  )
};
