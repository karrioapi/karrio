import { CREATE_SURCHARGE, CreateSurcharge, CreateSurchargeMutationInput, DELETE_SURCHARGE, DeleteSurcharge, GET_SURCHARGE, GET_SURCHARGES, GetSurcharge, GetSurcharges, SurchargeFilter, UPDATE_SURCHARGE, UpdateSurcharge, UpdateSurchargeMutationInput, } from "@karrio/types/graphql/admin";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "../karrio";
import React from "react";


export function useSurcharges() {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<SurchargeFilter>();

  // Queries
  const query = useQuery(
    ['surcharges', filter],
    () => karrio.admin.request<GetSurcharges>(gqlstr(GET_SURCHARGES), { variables: filter }),
    { onError },
  );

  return {
    query,
    filter,
    setFilter,
  };
}

export function useSurcharge(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery({
    queryKey: ['surcharges', id],
    queryFn: () => karrio.admin.request<GetSurcharge>(gqlstr(GET_SURCHARGE), { variables: { id } }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}

export function useSurchargeMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['surcharges']);
  };

  // Mutations
  const createSurcharge = useMutation(
    (data: CreateSurchargeMutationInput) => karrio.admin.request<CreateSurcharge>(
      gqlstr(CREATE_SURCHARGE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateSurcharge = useMutation(
    (data: UpdateSurchargeMutationInput) => karrio.admin.request<UpdateSurcharge>(
      gqlstr(UPDATE_SURCHARGE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteSurcharge = useMutation(
    (data: { id: string }) => karrio.admin.request<DeleteSurcharge>(gqlstr(DELETE_SURCHARGE), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createSurcharge,
    updateSurcharge,
    deleteSurcharge,
  };
}
