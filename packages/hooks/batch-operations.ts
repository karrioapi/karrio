import { BatchOperationFilter, get_batch_operations, GET_BATCH_OPERATIONS, get_batch_operation, GET_BATCH_OPERATION } from "@karrio/types";
import { BatchOrderData, BatchShipmentData, BatchTrackerData, BatchesApiImportFileRequest } from "@karrio/types/rest/api";
import { gqlstr, handleFailure, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = BatchOperationFilter & { setVariablesToURL?: boolean };

export function useBatchOperations({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<BatchOperationFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: BatchOperationFilter }) => karrio.graphql.request<get_batch_operations>(
    gqlstr(GET_BATCH_OPERATIONS), { variables }
  );

  // Queries
  const query = useQuery(
    ['batch-operations', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  function setFilter(options: BatchOperationFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal", "tab"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof BatchOperationFilter]) ? acc : {
        ...acc,
        [key]: (["status", "resource_type"].includes(key)
          ? ([].concat(options[key as keyof BatchOperationFilter] as any).reduce(
            (acc, item: string) => (
              typeof item == 'string'
                ? [].concat(acc, item.split(',') as any)
                : [].concat(acc, item)
            ), []
          ))
          : (["offset", "first"].includes(key)
            ? parseInt(options[key as keyof BatchOperationFilter] as any)
            : options[key as keyof BatchOperationFilter]
          )
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.batch_operations.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['batch-operations', _filter],
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

export function useBatchOperation(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery({
    queryKey: ['batch-operations', id],
    queryFn: () => karrio.graphql.request<get_batch_operation>(gqlstr(GET_BATCH_OPERATION), { variables: { id } }),
    enabled: (!!id && id !== 'new'),
    onError,
  });

  return {
    query,
  };
}

export function useBatchOperationMutation(id?: string) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['batch-operations']);
    queryClient.invalidateQueries(['batch-operations', id]);
  };

  // Mutations
  // REST requests
  const importFile = useMutation(
    (data: BatchesApiImportFileRequest) => handleFailure(
      karrio.batches.importFile(data).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );
  const createOrders = useMutation(
    (data: BatchOrderData) => handleFailure(
      karrio.batches.createOrders({ batchOrderData: data }).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );
  const createTrackers = useMutation(
    (data: BatchTrackerData) => handleFailure(
      karrio.batches.createTrackers({ batchTrackerData: data }).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );
  const createShipments = useMutation(
    (data: BatchShipmentData) => handleFailure(
      karrio.batches.createShipments({ batchShipmentData: data }).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    importFile,
    createOrders,
    createTrackers,
    createShipments,
  };
}
