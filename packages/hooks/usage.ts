import { GET_SYSTEM_USAGE, GetSystemUsage, UsageFilter } from "@karrio/types/graphql/admin";
import { GET_ORGANIZATION, get_organization } from "@karrio/types/graphql/ee";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useQuery } from "@tanstack/react-query";
import { useAPIMetadata } from "./api-metadata";
import { useSyncedSession } from "./session";
import { useKarrio } from "./karrio";
import moment from "moment";
import React from "react";

type FilterType = UsageFilter & { setVariablesToURL?: boolean };
const USAGE_FILTERS: Record<string, UsageFilter> = {
  "7 days": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(7, 'days').toISOString(),
  },
  "15 days": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(15, 'days').toISOString(),
  },
  "30 days": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(30, 'days').toISOString(),
  },
};
const DAYS_LIST = {
  "7 days": Array.from(Array(7)).map((_, i) => i).reverse().map(
    (i) => moment().subtract(i, 'days').format('MMM D')
  ),
  "15 days": Array.from(Array(15)).map((_, i) => i).reverse().map(
    (i) => moment().subtract(i, 'days').format('MMM D')
  ),
  "30 days": Array.from(Array(30)).map((_, i) => i).reverse().map(
    (i) => moment().subtract(i, 'days').format('MMM D')
  )
};


export function useAPIUsage({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const { metadata } = useAPIMetadata();
  const { query: { data: session } } = useSyncedSession();
  const [filter, _setFilter] = React.useState<UsageFilter>({ ...USAGE_FILTERS["15 days"], ...initialData });
  const systemUsage = (
    () => karrio.admin.request<GetSystemUsage>(gqlstr(GET_SYSTEM_USAGE), { variables: { filter } })
      .then(({ system_usage }) => ({ usage: system_usage }))
  );
  const orgUsage = (
    () => karrio.graphql.request<get_organization>(gqlstr(GET_ORGANIZATION), { variables: { id: session.orgId, usage: filter } })
      .then(({ organization }) => ({ usage: organization?.usage }))
  );

  // Queries
  const query = useQuery({
    queryKey: ['usage', filter],
    queryFn: (metadata.MULTI_ORGANIZATIONS == true ? orgUsage : systemUsage),
    staleTime: 1500000,
    onError
  });

  function setFilter(options: UsageFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal", "tab"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof UsageFilter]) ? acc : {
        ...acc,
        [key]: options[key as keyof UsageFilter],
      };
    }, {});

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  return {
    query,
    filter,
    setFilter,
    DAYS_LIST,
    USAGE_FILTERS,
    currentFilter: () => Object.keys(USAGE_FILTERS).find((_: any) => (
      USAGE_FILTERS[_].date_before == filter.date_before &&
      USAGE_FILTERS[_].date_after == filter.date_after
    )),
  };
}
