import { SystemCarrierMutationInput, MUTATE_SYSTEM_CONNECTION } from "@karrio/types";
import { GET_SYSTEM_CONNECTIONS } from "@karrio/types/graphql/queries";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import { gqlstr, onError } from "@karrio/lib";

// Using admin query shape which returns edges -> node
export type SystemConnectionType = any;

export function useSystemConnections(usageFilter?: any) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ["system_connections", usageFilter],
    queryFn: () => karrio.graphql.request<any>(gqlstr(GET_SYSTEM_CONNECTIONS), { filter: usageFilter }),
    staleTime: 5000,
  });

  return {
    query,
    // System connections now returns a paginated connection
    system_connections: query.data?.system_connections?.edges?.map((e: any) => e.node) || [],
    pageInfo: query.data?.system_connections?.page_info,
  };
}


export function useSystemConnectionMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ['system_connections'] });
    queryClient.invalidateQueries({ queryKey: ['admin_system_connections'] });
    queryClient.invalidateQueries({ queryKey: ['user_connections'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['system_connections'] });
  };

  // Mutations
  const updateSystemConnection = useAuthenticatedMutation({
    mutationFn: (data: SystemCarrierMutationInput) => karrio.graphql.request(gqlstr(MUTATE_SYSTEM_CONNECTION), { data }),
    onSuccess: invalidateCache,
    onError,
  });

  return {
    updateSystemConnection,
  };
}
