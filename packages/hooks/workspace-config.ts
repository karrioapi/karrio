import { UPDATE_WORKSPACE_CONFIG, GET_WORKSPACE_CONFIG, GetWorkspaceConfig, WorkspaceConfigMutationInput, UpdateWorkspaceConfig, GetWorkspaceConfig_workspace_config } from "@karrio/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";

type Pops = {
  defaultValue?: GetWorkspaceConfig_workspace_config;
};

export function useWorkspaceConfig({ defaultValue }: Pops = {}) {
  const karrio = useKarrio();
  const workspace_config = defaultValue || karrio.pageData?.workspace_config;

  // Queries
  const query = useQuery({
    queryKey: ['workspace-config'],
    queryFn: () => karrio.graphql.request<GetWorkspaceConfig>(gqlstr(GET_WORKSPACE_CONFIG)),
    initialData: !!workspace_config ? { workspace_config } : undefined,
    refetchOnWindowFocus: false,
    staleTime: 300000,
    onError
  });

  return {
    query,
    get customsOptions() {
      return (
        Object.entries(query.data?.workspace_config || {})
          .filter(([key, value]) => key.includes('customs') && !!value)
          .reduce((acc, [key, value]) => ({ ...acc, [key.replace("customs_", "")]: value }), {})
      );
    }
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
