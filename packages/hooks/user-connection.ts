import { CreateCarrierConnectionMutationInput, CREATE_CARRIER_CONNECTION, DELETE_CARRIER_CONNECTION, get_user_connections, GET_USER_CONNECTIONS, get_user_connections_user_connections, UpdateCarrierConnectionMutationInput, UPDATE_CARRIER_CONNECTION } from "@karrio/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";

export type CarrierConnectionType = get_user_connections_user_connections;

export function useCarrierConnections() {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['user_connections'],
    queryFn: () => karrio.graphql.request<get_user_connections>(gqlstr(GET_USER_CONNECTIONS)),
    staleTime: 5000,
  });

  return {
    query,
    user_carrier_connections: query.data?.user_connections,
  };
}

export function useCarrierConnectionMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['user_connections']);
    queryClient.invalidateQueries(['system_connections']);
  };

  const createCarrierConnection = useAuthenticatedMutation({
    mutationFn: (data: CreateCarrierConnectionMutationInput) => karrio.graphql.request(
      gqlstr(CREATE_CARRIER_CONNECTION),
      { data }
    ),
    onSuccess: invalidateCache,
  });

  const updateCarrierConnection = useAuthenticatedMutation({
    mutationFn: (data: UpdateCarrierConnectionMutationInput) => karrio.graphql.request(
      gqlstr(UPDATE_CARRIER_CONNECTION),
      { data }
    ),
    onSuccess: invalidateCache,
  });

  const deleteCarrierConnection = useAuthenticatedMutation({
    mutationFn: (data: { id: string }) => karrio.graphql.request(
      gqlstr(DELETE_CARRIER_CONNECTION),
      { data }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createCarrierConnection,
    updateCarrierConnection,
    deleteCarrierConnection,
  };
}
