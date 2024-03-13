import { SessionType, KarrioClient, Metadata, UserType, GetWorkspaceConfig_workspace_config } from "@karrio/types";
import { get_organizations_organizations } from "@karrio/types/graphql/ee";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useSyncedSession } from "@karrio/hooks/session";
import { getCookie, logger, url$ } from "@karrio/lib";
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

type ClientProviderProps = {
  children?: React.ReactNode,
};
type APIClientsContextProps = KarrioClient & {
  pageData?: {
    orgId?: string,
    user?: UserType,
    pathname?: string,
    metadata?: Metadata,
    organizations?: get_organizations_organizations[],
    workspace_config?: GetWorkspaceConfig_workspace_config,
  }
};

export const APIClientsContext = React.createContext<APIClientsContextProps>({} as any);

export const ClientProvider: React.FC<ClientProviderProps> = ({ children, ...pageData }) => {
  const { host } = useAPIMetadata();
  const { query: { data: session } } = useSyncedSession();

  if (!host) return <></>;

  return (
    <APIClientsContext.Provider value={{ ...setupRestClient(host, session), pageData }}>
      {children}
    </APIClientsContext.Provider>
  );
};

export function useKarrio() {
  return React.useContext(APIClientsContext)
}

function requestInterceptor(session?: SessionType) {
  return (config: any = { headers: {} }) => {
    const testHeader: any = !!session?.testMode ? { 'x-test-mode': session.testMode } : {};
    const authHeader: any = !!session?.accessToken ? { 'authorization': `Bearer ${session.accessToken}` } : {};
    const orgHeader: any = !!session?.orgId ? { 'x-org-id': getCookie("orgId") } : {};

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
