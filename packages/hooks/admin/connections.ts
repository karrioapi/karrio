import { CREATE_CARRIER_CONNECTION, GetSystemConnection_system_connection, CreateConnectionMutationInput, UpdateConnectionMutationInput, GET_SYSTEM_CONNECTIONS, UPDATE_CARRIER_CONNECTION, DELETE_CARRIER_CONNECTION, GetSystemConnections } from "@karrio/types/graphql/admin";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "../karrio";


export type SystemCarrierConnectionType = GetSystemConnection_system_connection;

export function useSystemCarrierConnections() {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(
    ['system_carrier_connections'],
    () => karrio.admin.request<GetSystemConnections>(gqlstr(GET_SYSTEM_CONNECTIONS)),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  return {
    query,
  };
}


export function useSystemCarrierConnectionMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => { queryClient.invalidateQueries(['system_carrier_connections']) };

  // Mutations
  const createSystemCarrierConnection = useMutation(
    (data: CreateConnectionMutationInput) => karrio.admin.request(gqlstr(CREATE_CARRIER_CONNECTION), { data }),
    { onSuccess: invalidateCache, onError }
  );
  const updateSystemCarrierConnection = useMutation(
    (data: UpdateConnectionMutationInput) => karrio.admin.request(gqlstr(UPDATE_CARRIER_CONNECTION), { data }),
    { onSuccess: invalidateCache, onError }
  );
  const deleteSystemCarrierConnection = useMutation(
    (data: { id: string }) => karrio.admin.request(gqlstr(DELETE_CARRIER_CONNECTION), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createSystemCarrierConnection,
    updateSystemCarrierConnection,
    deleteSystemCarrierConnection,
  };
}
