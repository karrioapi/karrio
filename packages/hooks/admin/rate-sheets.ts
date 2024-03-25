import { CREATE_RATE_SHEET, CreateRateSheet, CreateRateSheetMutationInput, DELETE_RATE_SHEET, DeleteRateSheet, GET_RATE_SHEET, GET_RATE_SHEETS, GetRateSheet, GetRateSheets, RateSheetFilter, UPDATE_RATE_SHEET, UpdateRateSheet, UpdateRateSheetMutationInput, } from "@karrio/types/graphql/admin";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "../karrio";
import React from "react";


export function useRateSheets() {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<RateSheetFilter>();

  // Queries
  const query = useQuery(
    ['rate_sheets', filter],
    () => karrio.admin.request<GetRateSheets>(gqlstr(GET_RATE_SHEETS), { variables: filter }),
    { onError },
  );

  return {
    query,
    filter,
    setFilter,
  };
}

export function useRateSheet(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery({
    queryKey: ['rate_sheets', id],
    queryFn: () => karrio.admin.request<GetRateSheet>(gqlstr(GET_RATE_SHEET), { variables: { id } }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}

export function useRateSheetMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['rate_sheets']);
  };

  // Mutations
  const createRateSheet = useMutation(
    (data: CreateRateSheetMutationInput) => karrio.admin.request<CreateRateSheet>(
      gqlstr(CREATE_RATE_SHEET), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateRateSheet = useMutation(
    (data: UpdateRateSheetMutationInput) => karrio.admin.request<UpdateRateSheet>(
      gqlstr(UPDATE_RATE_SHEET), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteRateSheet = useMutation(
    (data: { id: string }) => karrio.admin.request<DeleteRateSheet>(gqlstr(DELETE_RATE_SHEET), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createRateSheet,
    updateRateSheet,
    deleteRateSheet,
  };
}
