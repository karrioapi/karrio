import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { createGraphiQLFetcher } from '@graphiql/toolkit';
import { useSyncedSession } from "@karrio/hooks/session";
import { EmbedLayout } from "@/layouts/embed-layout";
import { GraphiQL } from 'graphiql';
import Head from "next/head";
import React from "react";

import 'graphiql/graphiql.css';

export { getServerSideProps } from "@/context/main";

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
    const { metadata } = useAPIMetadata();
    const { query: { data: session } } = useSyncedSession();

    const fetcher = React.useMemo(() => {
      return createGraphiQLFetcher({
        url: metadata?.GRAPHQL,
        headers: {
          ...(!!session?.orgId ? { 'x-org-id': session.orgId } : {}),
          ...(!!session?.testMode ? { 'x-test-mode': session.testMode } : {}),
          ...(!!session?.accessToken ? { 'authorization': `Bearer ${session.accessToken}` } : {})
        },
      })
    }, [session.accessToken]);

    return (
      <div className="playground-wrapper" style={{ position: 'absolute', top: 0, left: 0, bottom: 0, right: 0 }}>

        <GraphiQL fetcher={fetcher} editorTheme="light" />

      </div>
    );
  };

  return AuthenticatedPage((
    <EmbedLayout showModeIndicator={true}>
      <Head><title>{`GraphiQL - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <Component />

    </EmbedLayout>
  ), pageProps)
}
