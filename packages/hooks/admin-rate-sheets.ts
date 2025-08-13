import React from "react";
import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import {
  GET_RATE_SHEETS,
  GET_RATE_SHEET,
  CREATE_RATE_SHEET,
  UPDATE_RATE_SHEET,
  UPDATE_RATE_SHEET_ZONE_CELL,
  BATCH_UPDATE_RATE_SHEET_CELLS,
  DELETE_RATE_SHEET_SERVICE,
  UPDATE_SERVICE_ZONE,
  DELETE_RATE_SHEET
} from "@karrio/types/graphql/admin/queries";
import {
  GetRateSheets,
  GetRateSheetsVariables,
  GetRateSheet,
  GetRateSheetVariables,
  CreateRateSheet,
  CreateRateSheetVariables,
  UpdateRateSheet,
  UpdateRateSheetVariables,
  UpdateServiceZone,
  UpdateServiceZoneVariables,
  DeleteRateSheet,
  DeleteRateSheetVariables,
  RateSheetFilter,
} from "@karrio/types/graphql/admin";
import { useQueryClient } from "@tanstack/react-query";

// Types
export type RateSheetType = GetRateSheets['rate_sheets']['edges'][0]['node'];

// -----------------------------------------------------------
// Rate Sheets List Hook
// -----------------------------------------------------------
export function useRateSheets(filter: RateSheetFilter = {}) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_rate_sheets', filter],
    queryFn: () => karrio.admin.request<GetRateSheets>(gqlstr(GET_RATE_SHEETS), { variables: { filter } }),
    staleTime: 5000,
  });

  return {
    query,
    rate_sheets: query.data?.rate_sheets,
  };
}

// -----------------------------------------------------------
// Single Rate Sheet Hook
// -----------------------------------------------------------
export function useRateSheet(params: { id: string }) {
  const karrio = useKarrio();
  const [rateSheetId, setRateSheetId] = React.useState(params.id);

  const query = useAuthenticatedQuery({
    queryKey: ['admin_rate_sheet', rateSheetId],
    queryFn: () => karrio.admin.request<GetRateSheet>(gqlstr(GET_RATE_SHEET), { variables: { id: rateSheetId } }),
    staleTime: 5000,
    enabled: !!rateSheetId && rateSheetId !== 'new',
  });

  return {
    query,
    rate_sheet: query.data?.rate_sheet,
    setRateSheetId,
  };
}

// -----------------------------------------------------------
// Rate Sheet Mutations Hook
// -----------------------------------------------------------
export function useRateSheetMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateCache = () => {
    queryClient.invalidateQueries(['admin_rate_sheets']);
    queryClient.invalidateQueries(['admin_rate_sheet']);
  };

  const createRateSheet = useAuthenticatedMutation({
    mutationFn: (data: CreateRateSheetVariables["data"]) => karrio.admin.request<CreateRateSheet>(
      gqlstr(CREATE_RATE_SHEET),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const updateRateSheet = useAuthenticatedMutation({
    mutationFn: (data: UpdateRateSheetVariables["data"]) => karrio.admin.request<UpdateRateSheet>(
      gqlstr(UPDATE_RATE_SHEET),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const updateRateSheetZoneCell = useAuthenticatedMutation({
    mutationFn: (data: any) => karrio.admin.request(
      gqlstr(UPDATE_RATE_SHEET_ZONE_CELL),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const batchUpdateRateSheetCells = useAuthenticatedMutation({
    mutationFn: (data: any) => karrio.admin.request(
      gqlstr(BATCH_UPDATE_RATE_SHEET_CELLS),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteRateSheetService = useAuthenticatedMutation({
    mutationFn: (data: any) => karrio.admin.request(
      gqlstr(DELETE_RATE_SHEET_SERVICE),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const updateServiceZone = useAuthenticatedMutation({
    mutationFn: (data: UpdateServiceZoneVariables["data"]) => karrio.admin.request<UpdateServiceZone>(
      gqlstr(UPDATE_SERVICE_ZONE),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteRateSheet = useAuthenticatedMutation({
    mutationFn: (data: DeleteRateSheetVariables["data"]) => karrio.admin.request<DeleteRateSheet>(
      gqlstr(DELETE_RATE_SHEET),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createRateSheet,
    updateRateSheet,
    updateRateSheetZoneCell,
    batchUpdateRateSheetCells,
    deleteRateSheetService,
    updateServiceZone,
    deleteRateSheet,
  };
}
