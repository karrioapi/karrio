import { MUTATE_API_TOKEN, GET_API_TOKEN, GetToken, mutate_token, TokenMutationInput } from "@karrio/graphql";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@/lib/helper";
import { useKarrio } from "@/lib/client";


export function useAPIToken() {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(
    ['api_token'],
    () => karrio.graphql$.request<GetToken>(gqlstr(GET_API_TOKEN)),
    { onError, staleTime: 1500000 }
  );

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

  // Mutations
  const updateToken = useMutation(
    (data: TokenMutationInput) => karrio.graphql$.request<mutate_token>(gqlstr(MUTATE_API_TOKEN), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    updateToken,
  };
}
