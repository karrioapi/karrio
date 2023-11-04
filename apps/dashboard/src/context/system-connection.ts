import { get_system_connections, GET_SYSTEM_CONNECTIONS, SystemCarrierMutationInput, MUTATE_SYSTEM_CONNECTION, get_system_connections_system_connections } from "@karrio/graphql";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@/lib/helper";
import { useKarrio } from "@/lib/client";

export type SystemConnectionType = get_system_connections_system_connections;

export function useSystemConnections() {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(
    ['system_connections'],
    () => karrio.graphql$.request<get_system_connections>(gqlstr(GET_SYSTEM_CONNECTIONS)),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  return {
    query,
  };
}


export function useSystemConnectionMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => { queryClient.invalidateQueries(['system_connections']) };

  // Mutations
  const updateSystemConnection = useMutation(
    (data: SystemCarrierMutationInput) => karrio.graphql$.request(gqlstr(MUTATE_SYSTEM_CONNECTION), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    updateSystemConnection,
  };
}
