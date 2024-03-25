import { GetPermissionGroups, GET_GROUP_PERMISSIONS, PermissionGroupFilter } from "@karrio/types/graphql/admin";
import { useQuery } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "../karrio";
import React from "react";


export function usePermissionGroups() {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<PermissionGroupFilter>();

  // Queries
  const query = useQuery(
    ['permissions', filter],
    () => karrio.admin.request<GetPermissionGroups>(gqlstr(GET_GROUP_PERMISSIONS), { variables: filter }),
    { onError },
  );

  return {
    query,
    filter,
    setFilter,
  };
}
