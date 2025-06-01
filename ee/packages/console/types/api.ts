import {
  GetTenant_tenant,
  GetTenants_tenants_edges_node,
} from "./graphql/platform/types";
import { ConfigurationParameters } from "@karrio/types/rest/configuration";
import { Configuration } from "@karrio/types/rest/configuration";
import axios, { AxiosRequestHeaders } from "axios";
import { GraphQLApi } from "@karrio/types";

export * from "@karrio/console/types/graphql/platform";

export type TenantType = GetTenant_tenant | GetTenants_tenants_edges_node;

export interface KarrioPlatformClientInterface {
  platform: GraphQLApi;
}

export function KarrioPlatformClient({
  headers,
  ...clientConfig
}: ConfigurationParameters & { headers?: AxiosRequestHeaders }) {
  const config = new Configuration(clientConfig);
  const axiosInstance = axios.create({ baseURL: config.basePath, headers });

  return new GraphQLApi(`${config.basePath}/platform/graphql`, axiosInstance);
}
