import { TemplateFilter, CreateParcelTemplateInput, CREATE_PARCEL_TEMPLATE, DELETE_TEMPLATE, get_parcel_templates, GET_PARCEL_TEMPLATES, UpdateParcelTemplateInput, UPDATE_PARCEL_TEMPLATE, create_parcel_template, update_parcel_template, delete_template } from "@karrio/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = TemplateFilter & { setVariablesToURL?: boolean };

export function useParcelTemplates({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<TemplateFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: TemplateFilter }) => karrio.graphql.request<get_parcel_templates>(
    gqlstr(GET_PARCEL_TEMPLATES), { variables }
  );

  // Queries
  const query = useQuery(
    ['parcels'],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  function setFilter(options: TemplateFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof TemplateFilter]) ? acc : {
        ...acc,
        [key]: ([""].includes(key)
          ? ([].concat(options[key as keyof TemplateFilter] as any).reduce(
            (acc, item: string) => (
              typeof item == 'string'
                ? [].concat(acc, item.split(',') as any)
                : [].concat(acc, item)
            ), []
          ))
          : (["offset", "first"].includes(key)
            ? parseInt(options[key as keyof TemplateFilter] as any)
            : options[key as keyof TemplateFilter]
          )
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.parcel_templates.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['addresses', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])


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
    (data: CreateParcelTemplateInput) => karrio.graphql.request<create_parcel_template>(
      gqlstr(CREATE_PARCEL_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateParcelTemplate = useMutation(
    (data: UpdateParcelTemplateInput) => karrio.graphql.request<update_parcel_template>(
      gqlstr(UPDATE_PARCEL_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteParcelTemplate = useMutation(
    (data: { id: string }) => karrio.graphql.request<delete_template>(
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
