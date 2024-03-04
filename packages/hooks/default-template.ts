import { get_default_templates, GET_DEFAULT_TEMPLATES } from "@karrio/types";
import { useQuery } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";


export function useDefaultTemplates() {
  const karrio = useKarrio();

  // Queries
  const query = useQuery({
    queryKey: ['default_templates'],
    queryFn: () => karrio.graphql.request<get_default_templates>(gqlstr(GET_DEFAULT_TEMPLATES)),
    keepPreviousData: true,
    staleTime: 10000,
    onError,
  });

  return {
    query,
  };
}
