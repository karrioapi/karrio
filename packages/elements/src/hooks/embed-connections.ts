import {
  GET_USER_CONNECTIONS as BASE_GET_USER_CONNECTIONS,
  CREATE_CARRIER_CONNECTION as BASE_CREATE_CARRIER_CONNECTION,
  UPDATE_CARRIER_CONNECTION as BASE_UPDATE_CARRIER_CONNECTION,
  DELETE_CARRIER_CONNECTION as BASE_DELETE_CARRIER_CONNECTION,
} from "@karrio/types/graphql";
import {
  GET_SYSTEM_CONNECTIONS as ADMIN_GET_SYSTEM_CONNECTIONS,
  CREATE_SYSTEM_CONNECTION as ADMIN_CREATE_SYSTEM_CONNECTION,
  UPDATE_SYSTEM_CONNECTION as ADMIN_UPDATE_SYSTEM_CONNECTION,
  DELETE_SYSTEM_CONNECTION as ADMIN_DELETE_SYSTEM_CONNECTION,
} from "@karrio/types/graphql/admin/queries";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useKarrioEmbed } from "../providers/karrio-embed-provider";
import { gqlstr, onError } from "@karrio/lib";

function useGQL() {
  const { admin } = useKarrioEmbed();

  const wrapVars = (data: any) =>
    admin ? { variables: { input: data } } : { data };

  const queries = admin
    ? {
        GET_CONNECTIONS: ADMIN_GET_SYSTEM_CONNECTIONS,
        CREATE_CONNECTION: ADMIN_CREATE_SYSTEM_CONNECTION,
        UPDATE_CONNECTION: ADMIN_UPDATE_SYSTEM_CONNECTION,
        DELETE_CONNECTION: ADMIN_DELETE_SYSTEM_CONNECTION,
      }
    : {
        GET_CONNECTIONS: BASE_GET_USER_CONNECTIONS,
        CREATE_CONNECTION: BASE_CREATE_CARRIER_CONNECTION,
        UPDATE_CONNECTION: BASE_UPDATE_CARRIER_CONNECTION,
        DELETE_CONNECTION: BASE_DELETE_CARRIER_CONNECTION,
      };

  return { queries, wrapVars, admin };
}

export function useEmbedConnections() {
  const { graphqlRequest, admin } = useKarrioEmbed();
  const { queries } = useGQL();

  const cachePrefix = admin ? "admin_system_connections" : "user_connections";

  const query = useQuery({
    queryKey: [cachePrefix],
    queryFn: () =>
      graphqlRequest<any>(gqlstr(queries.GET_CONNECTIONS)),
    onError,
  });

  // Normalize the response shape - admin uses system_carrier_connections, user uses user_connections
  const connectionKey = admin ? "system_carrier_connections" : "user_connections";
  const connections = query.data?.[connectionKey]?.edges?.map((e: any) => e.node) || [];

  return {
    query,
    connections,
  };
}

export function useEmbedConnectionMutation() {
  const queryClient = useQueryClient();
  const { graphqlRequest, admin } = useKarrioEmbed();
  const { queries, wrapVars } = useGQL();

  const cachePrefix = admin ? "admin_system_connections" : "user_connections";

  const invalidateCache = () => {
    queryClient.invalidateQueries([cachePrefix]);
  };

  const createCarrierConnection = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.CREATE_CONNECTION), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const updateCarrierConnection = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.UPDATE_CONNECTION), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const deleteCarrierConnection = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.DELETE_CONNECTION), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  return {
    createCarrierConnection,
    updateCarrierConnection,
    deleteCarrierConnection,
  };
}

export function useEmbedConnectionForm() {
  const mutation = useEmbedConnectionMutation();

  const handleSubmit = async (values: any, selectedConnection?: any): Promise<void> => {
    const {
      carrier_name,
      carrier_id,
      active,
      capabilities,
      credentials,
      config,
      metadata,
    } = values;

    if (selectedConnection) {
      const updatePayload = {
        id: selectedConnection.id,
        carrier_id,
        active,
        capabilities,
        credentials,
        config,
        metadata,
      };
      await mutation.updateCarrierConnection.mutateAsync(updatePayload);
    } else {
      const createPayload = {
        carrier_name,
        carrier_id,
        active,
        capabilities,
        credentials,
        config,
        metadata,
      };
      await mutation.createCarrierConnection.mutateAsync(createPayload);
    }
  };

  return {
    handleSubmit,
    mutation,
  };
}
