import { TemplateFilter, CreateParcelTemplateInput, CREATE_PARCEL_TEMPLATE, DELETE_TEMPLATE, get_parcel_templates, GET_PARCEL_TEMPLATES, UpdateParcelTemplateInput, UPDATE_PARCEL_TEMPLATE, create_parcel_template, update_parcel_template, delete_template } from "@karrio/graphql";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@/lib/helper";
import { useKarrio } from "@/lib/client";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

export function useParcelTemplates() {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<TemplateFilter>(PAGINATION);

  // Queries
  const query = useQuery(
    ['parcels'],
    () => karrio.graphql$.request<get_parcel_templates>(gqlstr(GET_PARCEL_TEMPLATES), { data: filter }),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  return {
    query,
    filter,
    setFilter,
  };
}


export function useParcelTemplateMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['parcels']);
    queryClient.invalidateQueries(['default_templates']);
  };

  // Mutations
  const createParcelTemplate = useMutation(
    (data: CreateParcelTemplateInput) => karrio.graphql$.request<create_parcel_template>(
      gqlstr(CREATE_PARCEL_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateParcelTemplate = useMutation(
    (data: UpdateParcelTemplateInput) => karrio.graphql$.request<update_parcel_template>(
      gqlstr(UPDATE_PARCEL_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteParcelTemplate = useMutation(
    (data: { id: string }) => karrio.graphql$.request<delete_template>(
      gqlstr(DELETE_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createParcelTemplate,
    updateParcelTemplate,
    deleteParcelTemplate,
  };
}
