import { get_system_connections, GET_SYSTEM_CONNECTIONS, SystemCarrierMutationInput, MUTATE_SYSTEM_CONNECTION, get_system_connections_system_connections } from "@karrio/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery } from "./karrio";
import { useSyncedSession } from "./session";

export type SystemConnectionType = get_system_connections_system_connections;

export function useSystemConnections() {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ["system-connections"],
    queryFn: () => karrio.graphql.request<get_system_connections>(gqlstr(GET_SYSTEM_CONNECTIONS)),
    staleTime: 5000,
  });

  return {
    query,
    system_carrier_connections: query.data?.system_connections,
  };
}


export function useSystemConnectionMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => { queryClient.invalidateQueries(['system_connections']) };

  // Mutations
  const updateSystemConnection = useMutation(
    (data: SystemCarrierMutationInput) => karrio.graphql.request(gqlstr(MUTATE_SYSTEM_CONNECTION), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    updateSystemConnection,
  };
}
