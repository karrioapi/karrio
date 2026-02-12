import {
  GetRateSheet,
  GET_RATE_SHEET as BASE_GET_RATE_SHEET,
  CREATE_RATE_SHEET as BASE_CREATE_RATE_SHEET,
  UPDATE_RATE_SHEET as BASE_UPDATE_RATE_SHEET,
  DELETE_RATE_SHEET as BASE_DELETE_RATE_SHEET,
  DELETE_RATE_SHEET_SERVICE as BASE_DELETE_RATE_SHEET_SERVICE,
  ADD_SHARED_ZONE as BASE_ADD_SHARED_ZONE,
  UPDATE_SHARED_ZONE as BASE_UPDATE_SHARED_ZONE,
  DELETE_SHARED_ZONE as BASE_DELETE_SHARED_ZONE,
  ADD_SHARED_SURCHARGE as BASE_ADD_SHARED_SURCHARGE,
  UPDATE_SHARED_SURCHARGE as BASE_UPDATE_SHARED_SURCHARGE,
  DELETE_SHARED_SURCHARGE as BASE_DELETE_SHARED_SURCHARGE,
  BATCH_UPDATE_SURCHARGES as BASE_BATCH_UPDATE_SURCHARGES,
  UPDATE_SERVICE_RATE as BASE_UPDATE_SERVICE_RATE,
  BATCH_UPDATE_SERVICE_RATES as BASE_BATCH_UPDATE_SERVICE_RATES,
  UPDATE_SERVICE_ZONE_IDS as BASE_UPDATE_SERVICE_ZONE_IDS,
  UPDATE_SERVICE_SURCHARGE_IDS as BASE_UPDATE_SERVICE_SURCHARGE_IDS,
  ADD_WEIGHT_RANGE as BASE_ADD_WEIGHT_RANGE,
  REMOVE_WEIGHT_RANGE as BASE_REMOVE_WEIGHT_RANGE,
  DELETE_SERVICE_RATE as BASE_DELETE_SERVICE_RATE,
} from "@karrio/types/graphql";
import {
  GET_RATE_SHEET as ADMIN_GET_RATE_SHEET,
  CREATE_RATE_SHEET as ADMIN_CREATE_RATE_SHEET,
  UPDATE_RATE_SHEET as ADMIN_UPDATE_RATE_SHEET,
  DELETE_RATE_SHEET as ADMIN_DELETE_RATE_SHEET,
  DELETE_RATE_SHEET_SERVICE as ADMIN_DELETE_RATE_SHEET_SERVICE,
  ADD_SHARED_ZONE as ADMIN_ADD_SHARED_ZONE,
  UPDATE_SHARED_ZONE as ADMIN_UPDATE_SHARED_ZONE,
  DELETE_SHARED_ZONE as ADMIN_DELETE_SHARED_ZONE,
  ADD_SHARED_SURCHARGE as ADMIN_ADD_SHARED_SURCHARGE,
  UPDATE_SHARED_SURCHARGE as ADMIN_UPDATE_SHARED_SURCHARGE,
  DELETE_SHARED_SURCHARGE as ADMIN_DELETE_SHARED_SURCHARGE,
  BATCH_UPDATE_SURCHARGES as ADMIN_BATCH_UPDATE_SURCHARGES,
  UPDATE_SERVICE_RATE as ADMIN_UPDATE_SERVICE_RATE,
  BATCH_UPDATE_SERVICE_RATES as ADMIN_BATCH_UPDATE_SERVICE_RATES,
  UPDATE_SERVICE_ZONE_IDS as ADMIN_UPDATE_SERVICE_ZONE_IDS,
  UPDATE_SERVICE_SURCHARGE_IDS as ADMIN_UPDATE_SERVICE_SURCHARGE_IDS,
  ADD_WEIGHT_RANGE as ADMIN_ADD_WEIGHT_RANGE,
  REMOVE_WEIGHT_RANGE as ADMIN_REMOVE_WEIGHT_RANGE,
  DELETE_SERVICE_RATE as ADMIN_DELETE_SERVICE_RATE,
} from "@karrio/types/graphql/admin/queries";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useKarrioEmbed } from "../providers/karrio-embed-provider";
import { gqlstr, onError } from "@karrio/lib";
import React from "react";

// Pick the correct GQL document set and variable wrapping based on admin flag.
function useGQL() {
  const { admin } = useKarrioEmbed();

  // Admin mutations use `$input` variable name; base uses `$data`.
  // The wrapping key sent in the variables object must match.
  const wrapVars = (data: any) =>
    admin ? { variables: { input: data } } : { data };

  const queries = admin
    ? {
        GET_RATE_SHEET: ADMIN_GET_RATE_SHEET,
        CREATE_RATE_SHEET: ADMIN_CREATE_RATE_SHEET,
        UPDATE_RATE_SHEET: ADMIN_UPDATE_RATE_SHEET,
        DELETE_RATE_SHEET: ADMIN_DELETE_RATE_SHEET,
        DELETE_RATE_SHEET_SERVICE: ADMIN_DELETE_RATE_SHEET_SERVICE,
        ADD_SHARED_ZONE: ADMIN_ADD_SHARED_ZONE,
        UPDATE_SHARED_ZONE: ADMIN_UPDATE_SHARED_ZONE,
        DELETE_SHARED_ZONE: ADMIN_DELETE_SHARED_ZONE,
        ADD_SHARED_SURCHARGE: ADMIN_ADD_SHARED_SURCHARGE,
        UPDATE_SHARED_SURCHARGE: ADMIN_UPDATE_SHARED_SURCHARGE,
        DELETE_SHARED_SURCHARGE: ADMIN_DELETE_SHARED_SURCHARGE,
        BATCH_UPDATE_SURCHARGES: ADMIN_BATCH_UPDATE_SURCHARGES,
        UPDATE_SERVICE_RATE: ADMIN_UPDATE_SERVICE_RATE,
        BATCH_UPDATE_SERVICE_RATES: ADMIN_BATCH_UPDATE_SERVICE_RATES,
        UPDATE_SERVICE_ZONE_IDS: ADMIN_UPDATE_SERVICE_ZONE_IDS,
        UPDATE_SERVICE_SURCHARGE_IDS: ADMIN_UPDATE_SERVICE_SURCHARGE_IDS,
        ADD_WEIGHT_RANGE: ADMIN_ADD_WEIGHT_RANGE,
        REMOVE_WEIGHT_RANGE: ADMIN_REMOVE_WEIGHT_RANGE,
        DELETE_SERVICE_RATE: ADMIN_DELETE_SERVICE_RATE,
      }
    : {
        GET_RATE_SHEET: BASE_GET_RATE_SHEET,
        CREATE_RATE_SHEET: BASE_CREATE_RATE_SHEET,
        UPDATE_RATE_SHEET: BASE_UPDATE_RATE_SHEET,
        DELETE_RATE_SHEET: BASE_DELETE_RATE_SHEET,
        DELETE_RATE_SHEET_SERVICE: BASE_DELETE_RATE_SHEET_SERVICE,
        ADD_SHARED_ZONE: BASE_ADD_SHARED_ZONE,
        UPDATE_SHARED_ZONE: BASE_UPDATE_SHARED_ZONE,
        DELETE_SHARED_ZONE: BASE_DELETE_SHARED_ZONE,
        ADD_SHARED_SURCHARGE: BASE_ADD_SHARED_SURCHARGE,
        UPDATE_SHARED_SURCHARGE: BASE_UPDATE_SHARED_SURCHARGE,
        DELETE_SHARED_SURCHARGE: BASE_DELETE_SHARED_SURCHARGE,
        BATCH_UPDATE_SURCHARGES: BASE_BATCH_UPDATE_SURCHARGES,
        UPDATE_SERVICE_RATE: BASE_UPDATE_SERVICE_RATE,
        BATCH_UPDATE_SERVICE_RATES: BASE_BATCH_UPDATE_SERVICE_RATES,
        UPDATE_SERVICE_ZONE_IDS: BASE_UPDATE_SERVICE_ZONE_IDS,
        UPDATE_SERVICE_SURCHARGE_IDS: BASE_UPDATE_SERVICE_SURCHARGE_IDS,
        ADD_WEIGHT_RANGE: BASE_ADD_WEIGHT_RANGE,
        REMOVE_WEIGHT_RANGE: BASE_REMOVE_WEIGHT_RANGE,
        DELETE_SERVICE_RATE: BASE_DELETE_SERVICE_RATE,
      };

  return { queries, wrapVars, admin };
}

type Args = { id?: string };

export function useRateSheet({ id }: Args = {}) {
  const { graphqlRequest, admin } = useKarrioEmbed();
  const { queries } = useGQL();
  const [rateSheetId, _setRateSheetId] = React.useState<string>(id || "new");

  const cachePrefix = admin ? "admin_rate_sheet" : "rate-sheets";

  const query = useQuery({
    queryKey: [cachePrefix, rateSheetId],
    queryFn: () =>
      graphqlRequest<GetRateSheet>(gqlstr(queries.GET_RATE_SHEET), {
        variables: { id: rateSheetId },
      }),
    enabled: rateSheetId !== "new",
    onError,
  });

  function setRateSheetId(id: string) {
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
  const { graphqlRequest, admin } = useKarrioEmbed();
  const { queries, wrapVars } = useGQL();

  const cachePrefix = admin ? "admin_rate_sheet" : "rate-sheets";

  const invalidateCache = () => {
    queryClient.invalidateQueries([cachePrefix]);
    queryClient.invalidateQueries(
      admin ? ["admin_account_carrier_connections"] : ["user-connections"],
    );
  };

  const createRateSheet = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.CREATE_RATE_SHEET), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const updateRateSheet = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.UPDATE_RATE_SHEET), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const deleteRateSheet = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.DELETE_RATE_SHEET), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const deleteRateSheetService = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.DELETE_RATE_SHEET_SERVICE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const addSharedZone = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.ADD_SHARED_ZONE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const updateSharedZone = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.UPDATE_SHARED_ZONE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const deleteSharedZone = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.DELETE_SHARED_ZONE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const addSharedSurcharge = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.ADD_SHARED_SURCHARGE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const updateSharedSurcharge = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.UPDATE_SHARED_SURCHARGE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const deleteSharedSurcharge = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.DELETE_SHARED_SURCHARGE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const batchUpdateSurcharges = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.BATCH_UPDATE_SURCHARGES), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const updateServiceRate = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.UPDATE_SERVICE_RATE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const batchUpdateServiceRates = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.BATCH_UPDATE_SERVICE_RATES), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const addWeightRange = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.ADD_WEIGHT_RANGE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const removeWeightRange = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.REMOVE_WEIGHT_RANGE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const deleteServiceRate = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.DELETE_SERVICE_RATE), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const updateServiceZoneIds = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.UPDATE_SERVICE_ZONE_IDS), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  const updateServiceSurchargeIds = useMutation(
    (data: any) => graphqlRequest(gqlstr(queries.UPDATE_SERVICE_SURCHARGE_IDS), wrapVars(data)),
    { onSuccess: invalidateCache, onError },
  );

  return {
    createRateSheet,
    updateRateSheet,
    deleteRateSheet,
    deleteRateSheetService,
    addSharedZone,
    updateSharedZone,
    deleteSharedZone,
    addSharedSurcharge,
    updateSharedSurcharge,
    deleteSharedSurcharge,
    batchUpdateSurcharges,
    updateServiceRate,
    batchUpdateServiceRates,
    addWeightRange,
    removeWeightRange,
    deleteServiceRate,
    updateServiceZoneIds,
    updateServiceSurchargeIds,
  };
}
