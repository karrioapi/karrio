import {
  GET_ORGANIZATION,
  get_organization,
  get_organization_organization_usage
} from "@karrio/types/graphql/ee";
import {
  GET_SYSTEM_USAGE,
  GetSystemUsage,
  GetSystemUsage_system_usage,
  UsageFilter,
} from "@karrio/types";
import { gqlstr, insertUrlParam, isNoneOrEmpty } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery } from "./karrio";
import { useAPIMetadata } from "./api-metadata";
import { useSyncedSession } from "./session";
import moment from "moment";
import React from "react";

type UsageType = GetSystemUsage_system_usage &
  get_organization_organization_usage;
type FilterType = UsageFilter & { setVariablesToURL?: boolean };
const USAGE_FILTERS: Record<string, UsageFilter> = {
  "7 days": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(7, "days").toISOString(),
  },
  "15 days": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(15, "days").toISOString(),
  },
  "Last 30 days": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(30, "days").toISOString(),
  },
  "Last 3 months": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(90, "days").toISOString(),
  },
  "Last 6 months": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(180, "days").toISOString(),
  },
  "Last year": {
    date_before: moment().toISOString(),
    date_after: moment().subtract(360, "days").toISOString(),
  },
};
const DAYS_LIST: Record<string, string[]> = {
  "7 days": Array.from(Array(7))
    .map((_, i) => i)
    .reverse()
    .map((i) => moment().subtract(i, "days").format("MMM D")),
  "15 days": Array.from(Array(15))
    .map((_, i) => i)
    .reverse()
    .map((i) => moment().subtract(i, "days").format("MMM D")),
  "Last 30 days": Array.from(Array(30))
    .map((_, i) => i)
    .reverse()
    .map((i) => moment().subtract(i, "days").format("MMM D")),
  "Last 3 months": Array.from(Array(90))
    .map((_, i) => i)
    .reverse()
    .map((i) => moment().subtract(i, "days").format("MMM D")),
  "Last 6 months": Array.from(Array(180))
    .map((_, i) => i)
    .reverse()
    .map((i) => moment().subtract(i, "days").format("MMM D")),
  "Last year": Array.from(Array(360))
    .map((_, i) => i)
    .reverse()
    .map((i) => moment().subtract(i, "days").format("MMM D")),
};

export function useAPIUsage({
  setVariablesToURL = false,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const { metadata } = useAPIMetadata();
  const { query: sessionQuery } = useSyncedSession();
  const session = sessionQuery.data;
  const [filter, _setFilter] = React.useState<UsageFilter>({
    ...USAGE_FILTERS["15 days"],
    ...initialData,
  });

  const systemUsage = () =>
    karrio.graphql
      .request<GetSystemUsage>(gqlstr(GET_SYSTEM_USAGE), {
        variables: { filter },
      })
      .then(({ system_usage }) => ({ usage: system_usage as UsageType }));

  const orgUsage = () =>
    karrio.graphql
      .request<get_organization>(gqlstr(GET_ORGANIZATION), {
        variables: { id: session?.orgId, usage: filter },
      })
      .then(({ organization }) => ({ usage: organization?.usage as UsageType }))
      .catch((e) => {
        // Gracefully fallback so dashboard still loads if org context is missing
        if ((e as any)?.response?.errors?.[0]?.code === "authentication_required" ||
          /No active organization/i.test((e as any)?.response?.errors?.[0]?.message || "")) {
          return systemUsage();
        }
        throw e;
      });

  const query = useAuthenticatedQuery({
    queryKey: ["usage", filter],
    queryFn: metadata.MULTI_ORGANIZATIONS == true ? orgUsage : systemUsage,
    staleTime: 1500000,
    enabled: metadata.MULTI_ORGANIZATIONS ? !!session?.orgId : true,
    retry: (failureCount, error) => {
      // Don't retry if it's an authentication error
      if ((error as any)?.response?.errors?.[0]?.code === "authentication_required") {
        return false;
      }
      return failureCount < 3;
    },
  });

  function setFilter(options: UsageFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal", "tab"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof UsageFilter])
        ? acc
        : {
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
    currentFilter: () =>
      Object.keys(USAGE_FILTERS).find(
        (_: any) =>
          USAGE_FILTERS[_].date_before == filter.date_before &&
          USAGE_FILTERS[_].date_after == filter.date_after,
      ),
  };
}
