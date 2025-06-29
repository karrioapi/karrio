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
    queryClient.invalidateQueries(['admin_configs']);
  };

  const updateConfigs = useAuthenticatedMutation({
    mutationFn: (data: UpdateConfigsVariables["data"]) => karrio.admin.request<UpdateConfigs>(
      gqlstr(UPDATE_CONFIGS),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    updateConfigs,
  };
}
