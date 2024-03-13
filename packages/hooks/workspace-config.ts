import { UPDATE_WORKSPACE_CONFIG, GET_WORKSPACE_CONFIG, GetWorkspaceConfig, WorkspaceConfigMutationInput, UpdateWorkspaceConfig, GetWorkspaceConfig_workspace_config } from "@karrio/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";


export function useWorkspaceConfig({ defaultValue }: { defaultValue?: GetWorkspaceConfig_workspace_config }) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery({
    queryKey: ['workspace-config'],
    queryFn: () => karrio.graphql.request<GetWorkspaceConfig>(gqlstr(GET_WORKSPACE_CONFIG)),
    initialData: !!defaultValue ? { workspace_config: defaultValue } : undefined,
    refetchOnWindowFocus: false,
    staleTime: 300000,
    onError
  });

  return {
    query,
  };
}

export function useWorkspaceConfigMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => { queryClient.invalidateQueries(['workspace-config']) };

  // Mutations
  const updateWorkspaceConfig = useMutation(
    (data: WorkspaceConfigMutationInput) => karrio.graphql.request<UpdateWorkspaceConfig>(gqlstr(UPDATE_WORKSPACE_CONFIG), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    updateWorkspaceConfig,
  };
}
