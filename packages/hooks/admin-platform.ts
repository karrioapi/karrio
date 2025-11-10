import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import { GET_CONFIGS, UPDATE_CONFIGS } from "@karrio/types/graphql/admin/queries";
import {
  GetConfigs,
  UpdateConfigs,
  UpdateConfigsVariables,
} from "@karrio/types/graphql/admin";
import { useQueryClient } from "@tanstack/react-query";

// Types
export type ConfigsType = GetConfigs['configs'];

// -----------------------------------------------------------
// Platform Configuration Hook
// -----------------------------------------------------------
export function useConfigs() {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_configs'],
    queryFn: () => karrio.admin.request<GetConfigs>(gqlstr(GET_CONFIGS)),
    staleTime: 10000,
  });

  return {
    query,
    configs: query.data?.configs,
  };
}

// -----------------------------------------------------------
// Platform Configuration Mutations Hook
// -----------------------------------------------------------
export function useConfigMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    // invalidateQueries will automatically trigger refetch for active queries
    queryClient.invalidateQueries({ queryKey: ['admin_configs'] });
    queryClient.invalidateQueries({ queryKey: ['admin_system_usage'] });
    // Also invalidate metadata-derived references so UI reflects feature toggles immediately
    queryClient.invalidateQueries({ queryKey: ['references'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['admin_configs'] });
    queryClient.refetchQueries({ queryKey: ['references'] });
  };

  const updateConfigs = useAuthenticatedMutation({
    mutationFn: (input: UpdateConfigsVariables["input"]) => karrio.admin.request<UpdateConfigs>(
      gqlstr(UPDATE_CONFIGS),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    updateConfigs,
  };
}
