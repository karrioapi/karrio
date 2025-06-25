import { GET_SYSTEM_USAGE, GetSystemUsage, UsageFilter } from "@karrio/types";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import { gqlstr, onError } from "@karrio/lib";
import React from "react";

export function useSystemUsage() {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<UsageFilter>();

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["system_usage", filter],
    queryFn: () => karrio.graphql.request<GetSystemUsage>(gqlstr(GET_SYSTEM_USAGE), { variables: filter }),
    onError,
  });

  return {
    query,
    filter,
    setFilter,
  };
}
