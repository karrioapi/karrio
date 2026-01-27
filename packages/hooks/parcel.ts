import { TemplateFilter, CreateParcelInput, CREATE_PARCEL, DELETE_PARCEL, get_parcels, GET_PARCELS, UpdateParcelInput, UPDATE_PARCEL, create_parcel, update_parcel, delete_parcel } from "@karrio/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = TemplateFilter & { setVariablesToURL?: boolean };

export function useParcels({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<TemplateFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: TemplateFilter }) => karrio.graphql.request<get_parcels>(
    gqlstr(GET_PARCELS), { variables }
  );

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ['parcels'],
    queryFn: () => fetch({ filter }),
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

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
    if (query.data?.parcels.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['parcels', _filter],
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


export function useParcelMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ['parcels'] });
    queryClient.invalidateQueries({ queryKey: ['default_templates'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['parcels'] });
  };

  // Mutations
  const createParcel = useMutation(
    (data: CreateParcelInput) => karrio.graphql.request<create_parcel>(
      gqlstr(CREATE_PARCEL), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateParcel = useMutation(
    (data: UpdateParcelInput) => karrio.graphql.request<update_parcel>(
      gqlstr(UPDATE_PARCEL), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteParcel = useMutation(
    (data: { id: string }) => karrio.graphql.request<delete_parcel>(
      gqlstr(DELETE_PARCEL), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createParcel,
    updateParcel,
    deleteParcel,
  };
}
