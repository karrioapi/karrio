import { ADDRESS_AUTO_COMPLETE_SERVICE, ADDRESS_AUTO_COMPLETE_SERVICE_KEY } from "@karrio/lib/constants";
import Script from "next/script";
import React from "react";

export const GoogleGeocodingScript = (): JSX.Element => {
  const initMap = () => { };

  React.useEffect(() => ((window as any).initMap = initMap), []);
  return (
    <>
      {/*
        Using strategy="lazyOnload" per Next.js best practices for third-party scripts:
        https://nextjs.org/docs/pages/api-reference/components/script
        This ensures the Google Maps API is loaded asynchronously during browser idle time.
      */}
      {ADDRESS_AUTO_COMPLETE_SERVICE === "google" && ADDRESS_AUTO_COMPLETE_SERVICE_KEY && (
        <Script
          strategy="lazyOnload"
          src={`https://maps.googleapis.com/maps/api/js?key=${ADDRESS_AUTO_COMPLETE_SERVICE_KEY}&libraries=places&callback=initMap`}
          onError={(e) => {
            console.error("Failed to load Google Maps JavaScript API", e);
          }}
        ></Script>
      )}
    </>
  );
};
