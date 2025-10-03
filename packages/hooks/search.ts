import { SEARCH_DATA, search_data, search_dataVariables } from "@karrio/types";
import { gqlstr, isNone, onError } from "@karrio/lib";
import { useAuthenticatedQuery } from "./karrio";
import { useKarrio } from "./karrio";
import { useState, useCallback, useEffect } from "react";

export function useSearch() {
  const karrio = useKarrio();
  const [filter, setFilter] = useState<search_dataVariables>({});
  const [debouncedFilter, setDebouncedFilter] = useState<search_dataVariables>({});

  // Debounce the filter to avoid too many API calls
  const debounceFilter = useCallback(
    (() => {
      let timeoutId: NodeJS.Timeout;
      return (newFilter: search_dataVariables) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
          // Only update if keyword actually changed (distinctUntilChanged equivalent)
          setDebouncedFilter(prev => {
            if (prev.keyword !== newFilter.keyword) {
              return newFilter;
            }
            return prev;
          });
        }, 800); // Increased debounce time
      };
    })(),
    []
  );

  // Update debounced filter when filter changes
  useEffect(() => {
    debounceFilter(filter);
  }, [filter, debounceFilter]);

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ['search', debouncedFilter],
    queryFn: () => (
      karrio.graphql.request<search_data>(gqlstr(SEARCH_DATA), { variables: { ...debouncedFilter } })
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
    enabled: !isNone(debouncedFilter?.keyword) && (debouncedFilter?.keyword?.length || 0) >= 2, // Only search with 2+ characters
    staleTime: 30000, // Cache results for 30 seconds
    cacheTime: 300000, // Keep in cache for 5 minutes
    refetchOnWindowFocus: false, // Don't refetch on window focus
    retry: 1, // Only retry once on failure
    onError,
  });

  return {
    query,
    filter,
    setFilter,
  };
}
