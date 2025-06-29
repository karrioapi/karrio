import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import {
  GET_SURCHARGES,
  GET_SURCHARGE,
  CREATE_SURCHARGE,
  UPDATE_SURCHARGE,
  DELETE_SURCHARGE
} from "@karrio/types/graphql/admin/queries";
import {
  GetSurcharges,
  GetSurchargesVariables,
  GetSurcharge,
  GetSurchargeVariables,
  CreateSurcharge,
  CreateSurchargeVariables,
  UpdateSurcharge,
  UpdateSurchargeVariables,
  DeleteSurcharge,
  DeleteSurchargeVariables,
  SurchargeFilter,
} from "@karrio/types/graphql/admin";
import { useQueryClient } from "@tanstack/react-query";

// Types
export type SurchargeType = GetSurcharges['surcharges']['edges'][0]['node'];

// -----------------------------------------------------------
// Surcharges List Hook
// -----------------------------------------------------------
export function useSurcharges(filter: SurchargeFilter = {}) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_surcharges', filter],
    queryFn: () => karrio.admin.request<GetSurcharges>(gqlstr(GET_SURCHARGES), { variables: { filter } }),
    staleTime: 5000,
  });

  return {
    query,
    surcharges: query.data?.surcharges,
  };
}

// -----------------------------------------------------------
// Single Surcharge Hook
// -----------------------------------------------------------
export function useSurcharge(id: string) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_surcharge', id],
    queryFn: () => karrio.admin.request<GetSurcharge>(gqlstr(GET_SURCHARGE), { variables: { id } }),
    staleTime: 5000,
    enabled: !!id,
  });

  return {
    query,
    surcharge: query.data?.surcharge,
  };
}

// -----------------------------------------------------------
// Surcharge Mutations Hook
// -----------------------------------------------------------
export function useSurchargeMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateCache = () => {
    queryClient.invalidateQueries(['admin_surcharges']);
    queryClient.invalidateQueries(['admin_surcharge']);
  };

  const createSurcharge = useAuthenticatedMutation({
    mutationFn: (data: CreateSurchargeVariables["data"]) => karrio.admin.request<CreateSurcharge>(
      gqlstr(CREATE_SURCHARGE),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const updateSurcharge = useAuthenticatedMutation({
    mutationFn: (data: UpdateSurchargeVariables["data"]) => karrio.admin.request<UpdateSurcharge>(
      gqlstr(UPDATE_SURCHARGE),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteSurcharge = useAuthenticatedMutation({
    mutationFn: (data: DeleteSurchargeVariables["data"]) => karrio.admin.request<DeleteSurcharge>(
      gqlstr(DELETE_SURCHARGE),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createSurcharge,
    updateSurcharge,
    deleteSurcharge,
  };
}
