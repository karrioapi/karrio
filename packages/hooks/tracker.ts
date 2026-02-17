import {
  TrackerFilter,
  get_trackers,
  GET_TRACKERS,
  get_tracker,
  GET_TRACKER,
} from "@karrio/types";
import {
  gqlstr,
  handleFailure,
  insertUrlParam,
  isNoneOrEmpty,
  onError,
} from "@karrio/lib";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = TrackerFilter & {
  setVariablesToURL?: boolean;
  preloadNextPage?: boolean;
};

export function useTrackers({
  setVariablesToURL = false,
  preloadNextPage = false,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<TrackerFilter>({
    ...PAGINATION,
    ...initialData,
  });
  const fetch = (variables: { filter: TrackerFilter }) =>
    karrio.graphql.request<get_trackers>(gqlstr(GET_TRACKERS), { variables });

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["trackers", filter],
    queryFn: () => fetch({ filter }),
    keepPreviousData: true,
    staleTime: 5000,
    refetchInterval: 120000,
    onError,
  });

  function setFilter(options: TrackerFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof TrackerFilter])
        ? acc
        : {
          ...acc,
          [key]: ["carrier_name", "status"].includes(key)
            ? ([] as string[])
              .concat(options[key as keyof TrackerFilter] as any)
              .reduce(
                (acc: string[], item: string) =>
                  ([] as string[]).concat(acc, item.split(",") as string[]),
                [] as string[],
              )
            : ["offset", "first"].includes(key)
              ? parseInt(options[key as keyof TrackerFilter] as string)
              : options[key as keyof TrackerFilter],
        };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (preloadNextPage === false) return;
    if (query.data?.trackers.page_info.has_next_page) {
      const _filter = { ...filter, offset: (filter.offset as number) + 20 };
      queryClient.prefetchQuery(["trackers", _filter], () =>
        fetch({ filter: _filter }),
      );
    }
  }, [query.data, filter.offset, queryClient]);

  return {
    query,
    get filter() {
      return filter;
    },
    setFilter,
  };
}

export function useTracker(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["trackers", id],
    queryFn: () => karrio.graphql.request<get_tracker>(gqlstr(GET_TRACKER), { data: { id } }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}

export function useTrackerMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => {
    queryClient.invalidateQueries(["trackers"]);
  };

  // Mutations
  const createTracker = useMutation(
    (data: { tracking_number: string; carrier_name: string }) =>
      handleFailure(
        karrio.trackers.add({
          trackingData: data as any,
        }),
      ),
    { onSuccess: invalidateCache, onError },
  );
  const deleteTracker = useMutation(
    (data: { idOrTrackingNumber: string }) =>
      handleFailure(karrio.trackers.remove(data)),
    { onSuccess: invalidateCache, onError },
  );
  const resendWebhooks = useMutation(
    ({
      entityIds,
      webhookId,
    }: {
      entityIds: string[];
      webhookId?: string;
    }) =>
      handleFailure(
        karrio.axios
          .post(`/v1/batches/webhooks`, {
            entity_ids: entityIds,
            object_type: "tracker",
            ...(webhookId ? { webhook_id: webhookId } : {}),
          })
          .then(({ data }) => data),
      ),
    { onSuccess: invalidateCache, onError },
  );
  const refreshTracker = useMutation(
    (data: { tracking_number: string; carrier_name: string }) =>
      handleFailure(
        karrio.trackers.add({
          trackingData: data as any,
        }),
      ),
    { onSuccess: invalidateCache, onError },
  );

  return {
    createTracker,
    deleteTracker,
    resendWebhooks,
    refreshTracker,
  };
}

