import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { SessionType, KarrioClient } from "@karrio/types";
import { useSyncedSession } from "@karrio/hooks/session";
import { logger, url$ } from "@karrio/lib";
import { AxiosRequestConfig } from "axios";
import getConfig from 'next/config';
import React from "react";

const { publicRuntimeConfig, serverRuntimeConfig } = getConfig();

export const BASE_PATH = (publicRuntimeConfig?.BASE_PATH || '/').replace('//', '/');
export const TEST_BASE_PATH = (publicRuntimeConfig?.BASE_PATH + '/test').replace('//', '/');
export const KARRIO_API = (
  typeof window === 'undefined'
    ? serverRuntimeConfig?.KARRIO_URL
    : publicRuntimeConfig?.KARRIO_PUBLIC_URL
);

logger.debug("API clients initialized for Server: " + KARRIO_API);

export const APIClientsContext = React.createContext<KarrioClient>({} as any);

export const ClientProvider: React.FC<{ authenticated?: boolean, children?: React.ReactNode }> = ({ children, authenticated }) => {
  const { host } = useAPIMetadata();
  const { query: { data: session } } = useSyncedSession();

  if (authenticated && !host) return <></>;

  return (
    <APIClientsContext.Provider value={setupRestClient(host, session)}>
      {children}
    </APIClientsContext.Provider>
  );
};

export function useKarrio() {
  return React.useContext(APIClientsContext)
}

function requestInterceptor(session?: SessionType) {
  return (config: AxiosRequestConfig<any> = { headers: {} }) => {
    const orgHeader: any = !!session?.orgId ? { 'x-org-id': session.orgId } : {};
    const testHeader: any = !!session?.testMode ? { 'x-test-mode': session.testMode } : {};
    const authHeader: any = !!session?.accessToken ? { 'authorization': `Bearer ${session.accessToken}` } : {};

    config.headers = {
      ...config.headers,
      ...authHeader,
      ...orgHeader,
      ...testHeader
    };

    return config;
  };
}

function setupRestClient(host: string, session?: SessionType): KarrioClient {
  const client = new KarrioClient({ basePath: url$`${host || ''}` });

  client.axios.interceptors.request.use(requestInterceptor(session));

  return client;
}
