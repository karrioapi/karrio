import { CreateCarrierConnectionMutationInput, CREATE_CARRIER_CONNECTION, DELETE_CARRIER_CONNECTION, get_user_connections, GET_USER_CONNECTIONS, get_user_connections_user_connections, UpdateCarrierConnectionMutationInput, UPDATE_CARRIER_CONNECTION } from "@karrio/graphql";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@/lib/helper";
import { useKarrio } from "@/lib/client";


export type CarrierConnectionType = get_user_connections_user_connections;

export function useCarrierConnections() {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(
    ['user_connections'],
    () => karrio.graphql$.request<get_user_connections>(gqlstr(GET_USER_CONNECTIONS)),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  return {
    query,
  };
}


export function useCarrierConnectionMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => { queryClient.invalidateQueries(['user_connections']) };

  // Mutations
  const createCarrierConnection = useMutation(
    (data: CreateCarrierConnectionMutationInput) => karrio.graphql$.request(gqlstr(CREATE_CARRIER_CONNECTION), { data }),
    { onSuccess: invalidateCache, onError }
  );
  const updateCarrierConnection = useMutation(
    (data: UpdateCarrierConnectionMutationInput) => karrio.graphql$.request(gqlstr(UPDATE_CARRIER_CONNECTION), { data }),
    { onSuccess: invalidateCache, onError }
  );
  const deleteCarrierConnection = useMutation(
    (data: { id: string }) => karrio.graphql$.request(gqlstr(DELETE_CARRIER_CONNECTION), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createCarrierConnection,
    updateCarrierConnection,
    deleteCarrierConnection,
  };
}
