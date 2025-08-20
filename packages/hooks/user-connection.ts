import { CreateCarrierConnectionMutationInput, CREATE_CARRIER_CONNECTION, DELETE_CARRIER_CONNECTION, GET_USER_CONNECTIONS, get_user_connections_user_connections, UpdateCarrierConnectionMutationInput, UPDATE_CARRIER_CONNECTION, get_user_connections } from "@karrio/types";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import { useQueryClient } from "@tanstack/react-query";
import { gqlstr } from "@karrio/lib";

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
    user_connections: query.data?.user_connections?.edges?.map((e: any) => e.node) || [],
    pageInfo: query.data?.user_connections?.page_info,
  };
}

export function useCarrierConnectionMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ['user_connections'] });
    queryClient.invalidateQueries({ queryKey: ['system_connections'] });
    queryClient.invalidateQueries({ queryKey: ['admin_system_connections'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['user_connections'] });
    queryClient.refetchQueries({ queryKey: ['system_connections'] });
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

export function useCarrierConnectionForm() {
  const mutation = useCarrierConnectionMutation();

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
      // Update existing connection - exclude carrier_name as it's immutable
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
      // Create new connection - include carrier_name as it's required
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
