import {
  GET_MARKUPS,
  CREATE_MARKUP,
  UPDATE_MARKUP,
  DELETE_MARKUP,
} from "@karrio/types/graphql/admin-ee/queries";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useKarrioEmbed } from "../providers/karrio-embed-provider";
import { gqlstr, onError } from "@karrio/lib";

export function useEmbedMarkups(enabled = true) {
  const { graphqlRequest } = useKarrioEmbed();

  const query = useQuery({
    queryKey: ["admin_markups"],
    queryFn: () =>
      graphqlRequest<{ markups: { edges: { node: any }[] } }>(
        gqlstr(GET_MARKUPS),
        { filter: {} },
      ),
    enabled,
    onError,
  });

  const markups = query.data?.markups?.edges?.map((e: any) => e.node) || [];

  return { query, markups };
}

export function useEmbedMarkupMutation() {
  const queryClient = useQueryClient();
  const { graphqlRequest } = useKarrioEmbed();

  const invalidateCache = () => {
    queryClient.invalidateQueries(["admin_markups"]);
  };

  const createMarkup = useMutation(
    (input: any) =>
      graphqlRequest(gqlstr(CREATE_MARKUP), { input }),
    { onSuccess: invalidateCache, onError },
  );

  const updateMarkup = useMutation(
    (input: any) =>
      graphqlRequest(gqlstr(UPDATE_MARKUP), { input }),
    { onSuccess: invalidateCache, onError },
  );

  const deleteMarkup = useMutation(
    (input: any) =>
      graphqlRequest(gqlstr(DELETE_MARKUP), { input }),
    { onSuccess: invalidateCache, onError },
  );

  return { createMarkup, updateMarkup, deleteMarkup };
}
