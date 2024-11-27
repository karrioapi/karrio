"use client";

import {
  SessionType,
  KarrioClient,
  Metadata,
  UserType,
  GetWorkspaceConfig_workspace_config,
} from "@karrio/types";
import { get_organizations_organizations } from "@karrio/types/graphql/ee";
import { getCookie, KARRIO_API, logger, url$ } from "@karrio/lib";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useSyncedSession } from "@karrio/hooks/session";
import React from "react";

logger.debug("API clients initialized for Server: " + KARRIO_API);

type ClientProviderProps = {
  children?: React.ReactNode;
};
type APIClientsContextProps = KarrioClient & {
  isAuthenticated?: boolean;
  pageData?: {
    orgId?: string;
    user?: UserType;
    pathname?: string;
    metadata?: Metadata;
    organizations?: get_organizations_organizations[];
    workspace_config?: GetWorkspaceConfig_workspace_config;
  };
};

export const APIClientsContext = React.createContext<APIClientsContextProps>(
  {} as any,
);

export const ClientProvider = ({
  children,
  ...pageData
}: ClientProviderProps): JSX.Element => {
  const { getHost, references } = useAPIMetadata();
  const {
    query: { data: session },
  } = useSyncedSession();
  const updateClient = (ref: any, session: any) => ({
    ...setupRestClient(getHost(), session),
    isAuthenticated: !!session?.accessToken,
    pageData,
  });

  if (!getHost || !getHost() || !session) return <></>;

  return (
    <APIClientsContext.Provider value={updateClient(references, session)}>
      {children}
    </APIClientsContext.Provider>
  );
};

export function useKarrio() {
  return React.useContext(APIClientsContext);
}

function requestInterceptor(session?: SessionType) {
  return (config: any = { headers: {} }) => {
    const testHeader: any = !!session?.testMode
      ? { "x-test-mode": session.testMode }
      : {};
    const authHeader: any = !!session?.accessToken
      ? { authorization: `Bearer ${session.accessToken}` }
      : {};
    const orgHeader: any = !!session?.orgId
      ? { "x-org-id": getCookie("orgId") }
      : {};

    config.headers = {
      ...config.headers,
      ...authHeader,
      ...orgHeader,
      ...testHeader,
    };

    return config;
  };
}

function setupRestClient(host: string, session?: SessionType): KarrioClient {
  const client = new KarrioClient({ basePath: url$`${host || ""}` });

  client.axios.interceptors.request.use(requestInterceptor(session));

  return client;
}
