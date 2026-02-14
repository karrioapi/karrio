import {
  TracingRecordFilter,
  get_tracing_records,
  GET_TRACING_RECORDS,
  get_tracing_record,
  GET_TRACING_RECORD,
} from "@karrio/types";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import { useQueryClient } from "@tanstack/react-query";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = TracingRecordFilter & { setVariablesToURL?: boolean };

export function useTracingRecords({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<TracingRecordFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: TracingRecordFilter }) => karrio.graphql.request<get_tracing_records>(
    gqlstr(GET_TRACING_RECORDS), { variables }
  );

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ['tracing_records', filter],
    queryFn: () => fetch({ filter }),
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  function setFilter(options: TracingRecordFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      return isNoneOrEmpty(options[key as keyof TracingRecordFilter]) ? acc : {
        ...acc,
        [key]: (["offset", "first", "request_log_id"].includes(key)
          ? parseInt(options[key as keyof TracingRecordFilter] as any)
          : options[key as keyof TracingRecordFilter]
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.tracing_records.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + PAGE_SIZE };
      queryClient.prefetchQuery(
        ['tracing_records', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])

  return {
    query,
    filter,
    setFilter,
  };
}

export function useTracingRecord(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ['tracing_records', id],
    queryFn: () => karrio.graphql.request<get_tracing_record>(gqlstr(GET_TRACING_RECORD), { variables: { id } }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}
