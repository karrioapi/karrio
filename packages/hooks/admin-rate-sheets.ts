import React from "react";
import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import {
  GET_RATE_SHEETS,
  GET_RATE_SHEET,
  CREATE_RATE_SHEET,
  UPDATE_RATE_SHEET,
  DELETE_RATE_SHEET_SERVICE,
  DELETE_RATE_SHEET,
  ADD_SHARED_ZONE,
  UPDATE_SHARED_ZONE,
  DELETE_SHARED_ZONE,
  ADD_SHARED_SURCHARGE,
  UPDATE_SHARED_SURCHARGE,
  DELETE_SHARED_SURCHARGE,
  BATCH_UPDATE_SURCHARGES,
  UPDATE_SERVICE_RATE,
  BATCH_UPDATE_SERVICE_RATES,
  UPDATE_SERVICE_ZONE_IDS,
  UPDATE_SERVICE_SURCHARGE_IDS,
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
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ['admin_rate_sheets'] });
    queryClient.invalidateQueries({ queryKey: ['admin_rate_sheet'] });
    // Also invalidate carrier connections since they include rate sheet info
    queryClient.invalidateQueries({ queryKey: ['admin_account_carrier_connections'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['admin_rate_sheets'] });
  };

  const createRateSheet = useAuthenticatedMutation({
    mutationFn: (input: CreateRateSheetVariables["input"]) => karrio.admin.request<CreateRateSheet>(
      gqlstr(CREATE_RATE_SHEET),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const updateRateSheet = useAuthenticatedMutation({
    mutationFn: (input: UpdateRateSheetVariables["input"]) => karrio.admin.request<UpdateRateSheet>(
      gqlstr(UPDATE_RATE_SHEET),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteRateSheetService = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(DELETE_RATE_SHEET_SERVICE),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteRateSheet = useAuthenticatedMutation({
    mutationFn: (input: DeleteRateSheetVariables["input"]) => karrio.admin.request<DeleteRateSheet>(
      gqlstr(DELETE_RATE_SHEET),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  // Shared Zone Mutations
  const addSharedZone = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(ADD_SHARED_ZONE),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const updateSharedZone = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(UPDATE_SHARED_ZONE),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteSharedZone = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(DELETE_SHARED_ZONE),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  // Shared Surcharge Mutations
  const addSharedSurcharge = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(ADD_SHARED_SURCHARGE),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const updateSharedSurcharge = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(UPDATE_SHARED_SURCHARGE),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteSharedSurcharge = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(DELETE_SHARED_SURCHARGE),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const batchUpdateSurcharges = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(BATCH_UPDATE_SURCHARGES),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  // Service Rate Mutations
  const updateServiceRate = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(UPDATE_SERVICE_RATE),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const batchUpdateServiceRates = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(BATCH_UPDATE_SERVICE_RATES),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  // Service Zone/Surcharge Assignment Mutations
  const updateServiceZoneIds = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(UPDATE_SERVICE_ZONE_IDS),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const updateServiceSurchargeIds = useAuthenticatedMutation({
    mutationFn: (input: any) => karrio.admin.request(
      gqlstr(UPDATE_SERVICE_SURCHARGE_IDS),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createRateSheet,
    updateRateSheet,
    deleteRateSheetService,
    deleteRateSheet,
    // Shared Zone mutations
    addSharedZone,
    updateSharedZone,
    deleteSharedZone,
    // Shared Surcharge mutations
    addSharedSurcharge,
    updateSharedSurcharge,
    deleteSharedSurcharge,
    batchUpdateSurcharges,
    // Service Rate mutations
    updateServiceRate,
    batchUpdateServiceRates,
    // Service assignment mutations
    updateServiceZoneIds,
    updateServiceSurchargeIds,
  };
}
