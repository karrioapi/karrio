import { get_default_templates, GET_DEFAULT_TEMPLATES } from "@karrio/types";
import { useQuery } from "@tanstack/react-query";
import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery } from "./karrio";

export function useDefaultTemplates() {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ["default_templates"],
    queryFn: () => karrio.graphql.request<get_default_templates>(gqlstr(GET_DEFAULT_TEMPLATES)),
    staleTime: 5000,
  });

  return {
    query,
  };
}
