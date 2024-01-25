import { RateSheetFilter, GetRateSheets, GET_RATE_SHEETS, GetRateSheet, GET_RATE_SHEET, CreateRateSheet, UpdateRateSheet, UpdateRateSheetMutationInput, CreateRateSheetMutationInput, DELETE_RATE_SHEET, UPDATE_RATE_SHEET, CREATE_RATE_SHEET, DeleteMutationInput, GetRateSheets_rate_sheets_edges_node } from "@karrio/types/graphql";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = RateSheetFilter & { setVariablesToURL?: boolean };

export type RateSheetType = GetRateSheets_rate_sheets_edges_node;

export function useRateSheets({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<RateSheetFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: RateSheetFilter }) => karrio.graphql.request<GetRateSheets>(
    gqlstr(GET_RATE_SHEETS), { variables }
  );

  // Queries
  const query = useQuery(
    ['rate-sheets', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, refetchInterval: 120000, onError },
  );

  function setFilter(options: RateSheetFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal", "tab"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof RateSheetFilter]) ? acc : {
        ...acc,
        [key]: (["offset", "first"].includes(key)
          ? parseInt((options as any)[key])
          : options[key as keyof RateSheetFilter]
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.rate_sheets.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['rate-sheets', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])

  return {
    query,
    get filter() { return filter; },
    setFilter,
  };
}


type Args = { id?: string, setVariablesToURL?: boolean };

export function useRateSheet({ id, setVariablesToURL = false }: Args = {}) {
  const karrio = useKarrio();
  const [workflowActionId, _setRateSheetId] = React.useState<string>(id || 'new');

  // Queries
  const query = useQuery(['rate-sheets', id], {
    queryFn: () => karrio.graphql.request<GetRateSheet>(gqlstr(GET_RATE_SHEET), { variables: { id: workflowActionId } }),
    enabled: (workflowActionId !== 'new'),
    onError,
  });

  function setRateSheetId(workflowActionId: string) {
    if (setVariablesToURL) insertUrlParam({ id: workflowActionId });
    _setRateSheetId(workflowActionId);
  }

  return {
    query,
    workflowActionId,
    setRateSheetId,
  };
}


export function useRateSheetMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => { queryClient.invalidateQueries(['rate-sheets']) };

  // Mutations
  const createRateSheet = useMutation(
    (data: CreateRateSheetMutationInput) => karrio.graphql.request<CreateRateSheet>(
      gqlstr(CREATE_RATE_SHEET), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateRateSheet = useMutation(
    (data: UpdateRateSheetMutationInput) => karrio.graphql.request<UpdateRateSheet>(
      gqlstr(UPDATE_RATE_SHEET), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteRateSheet = useMutation(
    (data: { id: string }) => karrio.graphql.request<DeleteMutationInput>(
      gqlstr(DELETE_RATE_SHEET), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createRateSheet,
    updateRateSheet,
    deleteRateSheet,
  };
}
