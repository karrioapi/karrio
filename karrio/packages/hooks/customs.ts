import { TemplateFilter, CreateCustomsTemplateInput, CREATE_CUSTOMS_TEMPLATE, DELETE_TEMPLATE, get_customs_info_templates, GET_CUSTOMS_TEMPLATES, UpdateCustomsTemplateInput, UPDATE_CUSTOMS_TEMPLATE, DISCARD_COMMODITY, create_customs_template, update_customs_template, delete_template, discard_commodity } from "@karrio/types";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import { gqlstr, onError } from "@karrio/lib";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

export function useCustomsTemplates() {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<TemplateFilter>(PAGINATION);

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ['customs_infos', filter],
    queryFn: () => karrio.graphql.request<get_customs_info_templates>(gqlstr(GET_CUSTOMS_TEMPLATES), { variables: { filter } }),
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  return {
    query,
    filter,
    setFilter,
  };
}


export function useCustomsTemplateMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ['customs_infos'] });
    queryClient.invalidateQueries({ queryKey: ['default_templates'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['customs_infos'] });
  };

  // Mutations
  const createCustomsTemplate = useMutation(
    (data: CreateCustomsTemplateInput) => karrio.graphql.request<create_customs_template>(
      gqlstr(CREATE_CUSTOMS_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateCustomsTemplate = useMutation(
    (data: UpdateCustomsTemplateInput) => karrio.graphql.request<update_customs_template>(
      gqlstr(UPDATE_CUSTOMS_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteCustomsTemplate = useMutation(
    (data: { id: string }) => karrio.graphql.request<delete_template>(gqlstr(DELETE_TEMPLATE), { data }),
    { onSuccess: invalidateCache, onError }
  );
  const deleteCommodity = useMutation(
    (data: { id: string }) => karrio.graphql.request<discard_commodity>(gqlstr(DISCARD_COMMODITY), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createCustomsTemplate,
    updateCustomsTemplate,
    deleteCustomsTemplate,
    deleteCommodity,
  };
}
