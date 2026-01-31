import {
  PickupFilter,
  get_pickups,
  get_pickup,
  GET_PICKUPS,
  GET_PICKUP,
} from "@karrio/types";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { gqlstr, handleFailure, insertUrlParam, onError } from "@karrio/lib";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

type FilterType = PickupFilter & {
  setVariablesToURL?: boolean;
  cacheKey?: string;
  isDisabled?: boolean;
  preloadNextPage?: boolean;
};

export function usePickups({
  setVariablesToURL = false,
  isDisabled = false,
  preloadNextPage = false,
  cacheKey,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<PickupFilter>({
    ...PAGINATION,
    ...initialData,
  });

  const fetch = (variables: { filter: PickupFilter }) =>
    karrio.graphql.request<get_pickups>(gqlstr(GET_PICKUPS), { variables });

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: [cacheKey || "pickups", filter],
    queryFn: () => fetch({ filter }),
    enabled: !isDisabled,
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  function setFilter(options: PickupFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      if (["carrier_name"].includes(key))
        return {
          ...acc,
          [key]: []
            .concat(options[key as keyof PickupFilter])
            .reduce(
              (acc, item: string) =>
                typeof item == "string"
                  ? [].concat(acc, item.split(",") as any)
                  : [].concat(acc, item),
              [],
            ),
        };
      if (["offset", "first"].includes(key))
        return {
          ...acc,
          [key]: parseInt(options[key as keyof PickupFilter]),
        };

      return {
        ...acc,
        [key]: options[key as keyof PickupFilter],
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (preloadNextPage === false) return;
    if (query.data?.pickups.page_info.has_next_page) {
      const _filter = { ...filter, offset: (filter.offset as number) + 20 };
      queryClient.prefetchQuery(["pickups", _filter], () =>
        fetch({ filter: _filter }),
      );
    }
  }, [query.data, filter.offset, queryClient]);

  return {
    query,
    filter,
    setFilter,
  };
}

export function usePickup(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["pickups", id],
    queryFn: () =>
      karrio.graphql.request<get_pickup>(gqlstr(GET_PICKUP), {
        variables: { id },
      }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}

export function usePickupMutation(id?: string) {
  const queryClient = useQueryClient();
  const karrio = useKarrio();

  const invalidateCache = () => {
    queryClient.invalidateQueries(["pickups"]);
    if (id) queryClient.invalidateQueries(["pickups", id]);
  };

  // REST mutations for pickup operations
  const cancelPickup = useMutation(
    (pickupId: string) =>
      handleFailure(
        karrio.pickups.cancel({ id: pickupId }).then(({ data }) => data),
      ),
    { onSuccess: invalidateCache, onError },
  );

  const schedulePickup = useMutation(
    (data: any) =>
      handleFailure(
        karrio.axios
          .post("/v1/pickups", data, {
            headers: { "Content-Type": "application/json" },
          })
          .then(({ data }) => data),
      ),
    { onSuccess: invalidateCache, onError },
  );

  const updatePickup = useMutation(
    ({ pickupId, data }: { pickupId: string; data: any }) =>
      handleFailure(
        karrio.pickups
          .update({ id: pickupId, pickupUpdateData: data })
          .then(({ data }) => data),
      ),
    { onSuccess: invalidateCache, onError },
  );

  return {
    cancelPickup,
    schedulePickup,
    updatePickup,
    invalidateCache,
  };
}
