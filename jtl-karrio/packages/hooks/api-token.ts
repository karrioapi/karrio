import { MUTATE_API_TOKEN, GET_API_TOKEN, GetToken, mutate_token, TokenMutationInput } from "@karrio/types";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import { useQueryClient } from "@tanstack/react-query";
import { gqlstr } from "@karrio/lib";

export function useAPIToken(org_id?: string) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['api_token', org_id],
    queryFn: () => karrio.graphql.request<GetToken>(gqlstr(GET_API_TOKEN), {
      variables: { org_id }
    }),
    staleTime: 1500000,
    refetchOnWindowFocus: false,
  });

  return {
    query,
  };
}

export function useAPITokenMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['api_token']);
    queryClient.invalidateQueries(['organizations']);
  };

  const updateToken = useAuthenticatedMutation({
    mutationFn: (data: TokenMutationInput) => karrio.graphql.request<mutate_token>(
      gqlstr(MUTATE_API_TOKEN),
      { data }
    ),
    onSuccess: invalidateCache,
  });

  return {
    updateToken,
  };
}
