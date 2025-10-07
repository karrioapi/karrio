import { RateSheetFilter, GetRateSheets, GET_RATE_SHEETS, GetRateSheet, GET_RATE_SHEET, CreateRateSheet, UpdateRateSheet, UpdateRateSheetMutationInput, CreateRateSheetMutationInput, DELETE_RATE_SHEET, UPDATE_RATE_SHEET, CREATE_RATE_SHEET, UPDATE_RATE_SHEET_ZONE_CELL, BATCH_UPDATE_RATE_SHEET_CELLS, DELETE_RATE_SHEET_SERVICE, DeleteMutationInput, GetRateSheets_rate_sheets_edges_node } from "@karrio/types/graphql";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
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
  const query = useAuthenticatedQuery({
    queryKey: ['rate-sheets', filter],
    queryFn: () => fetch({ filter }),
    keepPreviousData: true,
    staleTime: 5000,
    refetchInterval: 120000,
    onError,
  });

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
    rate_sheets: query.data?.rate_sheets,
  };
}


type Args = { id?: string, setVariablesToURL?: boolean };

export function useRateSheet({ id, setVariablesToURL = false }: Args = {}) {
  const karrio = useKarrio();
  const [rateSheetId, _setRateSheetId] = React.useState<string>(id || 'new');

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ['rate-sheets', rateSheetId],
    queryFn: () => karrio.graphql.request<GetRateSheet>(gqlstr(GET_RATE_SHEET), { variables: { id: rateSheetId } }),
    enabled: (rateSheetId !== 'new'),
    onError,
  });

  function setRateSheetId(id: string) {
    if (setVariablesToURL) insertUrlParam({ id });
    _setRateSheetId(id);
  }

  return {
    query,
    rateSheetId,
    setRateSheetId,
  };
}


export function useRateSheetMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => {
    // Invalidate rate sheets cache
    queryClient.invalidateQueries(['rate-sheets']);
    // Also invalidate carrier connections cache since they include rate sheet info
    queryClient.invalidateQueries(['user-connections']);
  };

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

  const deleteRateSheetService = useMutation(
    (data: { rate_sheet_id: string; service_id: string }) => karrio.graphql.request<any>(
      gqlstr(DELETE_RATE_SHEET_SERVICE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createRateSheet,
    updateRateSheet,
    deleteRateSheet,
    deleteRateSheetService,
  };
}


export function useRateSheetCellMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => { 
    queryClient.invalidateQueries(['rate-sheets']);
  };

  const updateRateSheetZoneCell = useMutation(
    (data: any) => karrio.graphql.request<any>(
      gqlstr(UPDATE_RATE_SHEET_ZONE_CELL), { data }
    ),
    { 
      onSuccess: invalidateCache,
      // Optimistic update
      onMutate: async (data) => {
        await queryClient.cancelQueries(['rate-sheets', data.id]);
        const previousData = queryClient.getQueryData(['rate-sheets', data.id]);
        
        queryClient.setQueryData(['rate-sheets', data.id], (old: any) => {
          if (!old) return old;
          // Update the specific cell optimistically
          const updatedServices = old.rate_sheet.services.map((service: any) => {
            if (service.id === data.service_id) {
              const updatedZones = service.zones.map((zone: any) => {
                // Use zone.id for zone identification
                if (zone.id === data.zone_id) {
                  return { ...zone, [data.field]: data.value };
                }
                return zone;
              });
              return { ...service, zones: updatedZones };
            }
            return service;
          });
          return {
            ...old,
            rate_sheet: {
              ...old.rate_sheet,
              services: updatedServices
            }
          };
        });
        
        return { previousData };
      },
      onError: (err, data, context: any) => {
        // Rollback on error with original error handling
        if (context?.previousData) {
          queryClient.setQueryData(['rate-sheets', data.id], context.previousData);
        }
        onError(err);
      }
    }
  );

  const batchUpdateRateSheetCells = useMutation(
    (data: any) => karrio.graphql.request<any>(
      gqlstr(BATCH_UPDATE_RATE_SHEET_CELLS), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    updateRateSheetZoneCell,
    batchUpdateRateSheetCells,
  };
}
