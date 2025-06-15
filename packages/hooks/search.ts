import { SEARCH_DATA, search_data, search_dataVariables } from "@karrio/types";
import { gqlstr, isNone, onError } from "@karrio/lib";
import { useQuery } from "@tanstack/react-query";
import { debounceTime, Subject, distinctUntilChanged } from "rxjs";
import { useKarrio } from "./karrio";
import React from "react";

const observable$ = new Subject<search_dataVariables>();
const search$ = observable$.pipe(
  debounceTime(800), // Increased debounce time
  distinctUntilChanged((prev, curr) => prev.keyword === curr.keyword) // Only trigger if keyword actually changed
);

export function useSearch() {
  const karrio = useKarrio();
  const [filter, _setFilter] = React.useState<search_dataVariables>({});

  // Queries
  const query = useQuery(['search', filter], {
    queryFn: () => (
      karrio.graphql.request<search_data>(gqlstr(SEARCH_DATA), { variables: { ...filter } })
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
    enabled: !isNone(filter?.keyword) && (filter?.keyword?.length || 0) >= 2, // Only search with 2+ characters
    staleTime: 30000, // Cache results for 30 seconds
    cacheTime: 300000, // Keep in cache for 5 minutes
    refetchOnWindowFocus: false, // Don't refetch on window focus
    retry: 1, // Only retry once on failure
    onError,
  });

  React.useEffect(() => { search$.subscribe(_ => _setFilter(_)); }, []);

  return {
    query,
    filter,
    setFilter: (_: search_dataVariables) => observable$.next(_),
  };
}
