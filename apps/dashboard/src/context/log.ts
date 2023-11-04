import { useKarrio } from "@/lib/client";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@/lib/helper";
import { LogFilter, get_logs, GET_LOGS, get_log, GET_LOG } from "@karrio/graphql";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = LogFilter & { setVariablesToURL?: boolean };

export function useLogs({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<LogFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: LogFilter }) => karrio.graphql$.request<get_logs>(
    gqlstr(GET_LOGS), { variables }
  );

  // Queries
  const query = useQuery(
    ['logs', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  function setFilter(options: LogFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof LogFilter]) ? acc : {
        ...acc,
        [key]: (["method", "status_code"].includes(key)
          ? ([].concat(options[key as keyof LogFilter] as any).reduce(
            (acc, item: string) => (
              typeof item == 'string'
                ? [].concat(acc, item.split(',') as any)
                : [].concat(acc, item)
            ), []
          ))
          : (["offset", "first"].includes(key)
            ? parseInt(options[key as keyof LogFilter] as any)
            : options[key as keyof LogFilter]
          )
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.logs.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['logs', _filter],
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

export function useLog(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery({
    queryKey: ['logs', id],
    queryFn: () => karrio.graphql$.request<get_log>(gqlstr(GET_LOG), { variables: { id: parseInt(id) } }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}
