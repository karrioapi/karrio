"use client";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { RedocStandalone } from "redoc";
import { url$ } from "@karrio/lib";
import React from "react";

export const generateMetadata = dynamicMetadata("API Reference");

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
    const { references } = useAPIMetadata();

    return (
      <>
        <RedocStandalone
          specUrl={url$`${references?.HOST}/shipping-openapi`}
          options={{
            nativeScrollbars: true,
          }}
        />
      </>
    );
  };

  return (
    <>
      <Component />
    </>
  );
}
