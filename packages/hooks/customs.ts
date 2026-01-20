import { DISCARD_COMMODITY, discard_commodity } from "@karrio/types";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useKarrio } from "./karrio";
import { gqlstr, onError } from "@karrio/lib";

/**
 * @deprecated Customs templates have been deprecated. Use this hook only for deleteCommodity mutation.
 */
export function useCustomsTemplateMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries({ queryKey: ['shipments'] });
  };

  const deleteCommodity = useMutation(
    (data: { id: string }) => karrio.graphql.request<discard_commodity>(gqlstr(DISCARD_COMMODITY), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    deleteCommodity,
  };
}
