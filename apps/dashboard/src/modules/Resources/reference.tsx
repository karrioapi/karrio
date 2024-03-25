import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useSyncedSession } from "@karrio/hooks/session";
import { EmbedLayout } from "@/layouts/embed-layout";
import { RedocStandalone } from 'redoc';
import { url$ } from "@karrio/lib";
import Head from "next/head";
import React from "react";

export { getServerSideProps } from "@/context/main";

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
    const { metadata } = useAPIMetadata();

    return (
      <>

        <RedocStandalone
          specUrl={url$`${metadata?.HOST}/shipping-openapi`}
          options={{
            nativeScrollbars: true,
          }}
        />

      </>
    );
  };

  return AuthenticatedPage((
    <EmbedLayout showModeIndicator={true}>
      <Head><title>{`API Reference - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <Component />

    </EmbedLayout>
  ), pageProps)
}
