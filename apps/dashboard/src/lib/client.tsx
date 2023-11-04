import { useAPIMetadata } from "@/context/api-metadata";
import { RequestError, SessionType } from "@/lib/types";
import { useSyncedSession } from "@/context/session";
import axios, { AxiosRequestConfig } from "axios";
import { KarrioClient } from "karrio/rest/index";
import { url$ } from "@/lib/helper";
import getConfig from 'next/config';
import logger from "@/lib/logger";
import React from "react";

const { publicRuntimeConfig, serverRuntimeConfig } = getConfig();
type Interceptor = (config: AxiosRequestConfig<any>) => AxiosRequestConfig<any>;
type requestArgs = {
  variables?: Record<string, any>;
  data?: Record<string, any>;
  operationName?: string;
  url?: string;
} & Record<string, any>;
type APIClientsType = {
  rest$: ReturnType<typeof setupRestClient>;
  graphql$: ReturnType<typeof setupGraphQLClient>;
};

export const BASE_PATH = (publicRuntimeConfig?.BASE_PATH || '/').replace('//', '/');
export const TEST_BASE_PATH = (publicRuntimeConfig?.BASE_PATH + '/test').replace('//', '/');
export const KARRIO_API = (
  typeof window === 'undefined'
    ? serverRuntimeConfig?.KARRIO_URL
    : publicRuntimeConfig?.KARRIO_PUBLIC_URL
);

logger.debug("API clients initialized for Server: " + KARRIO_API);

export const APIClientsContext = React.createContext<APIClientsType>({} as any);

export const ClientsProvider: React.FC<{ authenticated?: boolean }> = ({ children, authenticated }) => {
  const { host } = useAPIMetadata();
  const { query: { data: session } } = useSyncedSession();

  if (authenticated && !host) return <></>;

  return (
    <APIClientsContext.Provider value={{
      rest$: setupRestClient(host, session),
      graphql$: setupGraphQLClient(host, session),
    }}>
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

function setupGraphQLClient(host: string, session?: SessionType) {
  const axiosInstance = axios.create({ baseURL: host });
  axiosInstance.interceptors.request.use(requestInterceptor(session));

  async function request<T>(query: string, args?: requestArgs): Promise<T> {
    const { url, data, variables: reqVariables, operationName, ...config } = args || {};
    try {
      const APIUrl = url || url$`${host}/graphql`;
      const variables = data ? { data } : reqVariables;
      const { data: response } = await axiosInstance.post<{ data?: T, errors?: any }>(
        APIUrl, { query, operationName, variables }, config,
      );

      if (response.errors) {
        throw new RequestError({ errors: response.errors });
      }

      return response.data || (response as T);
    } catch (error: any) {
      throw new RequestError(error.response?.data || error.data || error);
    }
  }

  return { request };
}

export function p(strings: TemplateStringsArray, ...keys: any[]) {
  return url$`${BASE_PATH}/${url$(strings, ...keys)}`.replace("//", "/");
}
