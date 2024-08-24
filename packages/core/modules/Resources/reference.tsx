import { AuthenticatedPage } from "@karrio/core/layouts/authenticated-page";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { EmbedLayout } from "@karrio/core/layouts/embed-layout";
import { RedocStandalone } from "redoc";
import { url$ } from "@karrio/lib";
import Head from "next/head";
import React from "react";

export { getServerSideProps } from "@karrio/core/context/main";

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

  return AuthenticatedPage(
    <EmbedLayout showModeIndicator={true}>
      <Head>
        <title>{`API Reference - ${(pageProps as any).metadata?.APP_NAME}`}</title>
      </Head>

      <Component />
    </EmbedLayout>,
    pageProps,
  );
}
