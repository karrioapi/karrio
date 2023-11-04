import { SEARCH_DATA, search_data, search_dataVariables } from "@karrio/graphql";
import { gqlstr, isNone, onError } from "@/lib/helper";
import { useQuery } from "@tanstack/react-query";
import { debounceTime, Subject } from "rxjs";
import { useKarrio } from "@/lib/client";
import React from "react";

const observable$ = new Subject<search_dataVariables>();
const search$ = observable$.pipe(debounceTime(500));

export function useSearch() {
  const karrio = useKarrio();
  const [filter, _setFilter] = React.useState<search_dataVariables>({});

  // Queries
  const query = useQuery(['search', filter], {
    queryFn: () => (
      karrio.graphql$.request<search_data>(gqlstr(SEARCH_DATA), { variables: { ...filter } })
        .then((data) => {
          const results = [
            ...(data?.order_results?.edges || []),
            ...(data?.trackers_results?.edges || []),
            ...(data?.shipment_results?.edges || []),
          ]
            .map((item: any) => item.node)
            .sort((i1, i2) => {
              return (new Date(i2.created_at as string) as any) - (new Date(i1.created_at as string) as any)
            });
          return { results };
        })
    ),
    enabled: !isNone(filter?.keyword),
    staleTime: 0,
    cacheTime: 0,
    onError,
  });

  React.useEffect(() => { search$.subscribe(_ => _setFilter(_)); }, []);

  return {
    query,
    filter,
    setFilter: (_: search_dataVariables) => observable$.next(_),
  };
}
