import { GET_SYSTEM_USAGE, GetSystemUsage, UsageFilter } from "@karrio/types/graphql/admin";
import { useQuery } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "../karrio";
import React from "react";


export function useSystemUsage() {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<UsageFilter>();

  // Queries
  const query = useQuery(
    ['system_usage', filter],
    () => karrio.admin.request<GetSystemUsage>(gqlstr(GET_SYSTEM_USAGE), { variables: filter }),
    { onError },
  );

  return {
    query,
    filter,
    setFilter,
  };
}
