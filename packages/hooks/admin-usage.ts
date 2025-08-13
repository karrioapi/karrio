import { gqlstr, insertUrlParam, isNoneOrEmpty } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery } from "./karrio";
import { GET_ADMIN_SYSTEM_USAGE } from "@karrio/types/graphql/admin/queries";
import {
  UsageFilter,
  GetAdminSystemUsage,
  GetAdminSystemUsage_usage,
} from "@karrio/types/graphql/admin";
import moment from "moment";
import React from "react";

// Types
export type AdminUsageType = GetAdminSystemUsage_usage;
type FilterType = UsageFilter & { setVariablesToURL?: boolean };

// Usage filters for different time periods
const ADMIN_USAGE_FILTERS: Record<string, UsageFilter> = {
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

// Days lists for chart generation
const ADMIN_DAYS_LIST: Record<string, string[]> = {
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

// -----------------------------------------------------------
// Admin System Usage Hook
// -----------------------------------------------------------
export function useAdminSystemUsage({
  setVariablesToURL = false,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const [filter, _setFilter] = React.useState<UsageFilter>({
    ...ADMIN_USAGE_FILTERS["15 days"],
    ...initialData,
  });

  const query = useAuthenticatedQuery({
    queryKey: ["admin_system_usage", filter],
    queryFn: () =>
      karrio.admin.request<GetAdminSystemUsage>(gqlstr(GET_ADMIN_SYSTEM_USAGE), {
        variables: { filter },
      }),
    staleTime: 1500000, // 25 minutes
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
    }, {} as UsageFilter);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  return {
    query,
    filter,
    setFilter,
    usage: query.data?.usage,
    DAYS_LIST: ADMIN_DAYS_LIST,
    USAGE_FILTERS: ADMIN_USAGE_FILTERS,
    currentFilter: () =>
      Object.keys(ADMIN_USAGE_FILTERS).find(
        (_: any) =>
          ADMIN_USAGE_FILTERS[_].date_before === filter.date_before &&
          ADMIN_USAGE_FILTERS[_].date_after === filter.date_after,
      ),
  };
}
