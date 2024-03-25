import { AddressFilter, CreateAddressTemplateInput, create_address_template, CREATE_ADDRESS_TEMPLATE, delete_template, DELETE_TEMPLATE, get_address_templates, GET_ADDRESS_TEMPLATES, UpdateAddressTemplateInput, update_address_template, UPDATE_ADDRESS_TEMPLATE } from "@karrio/types";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 25;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = AddressFilter & { setVariablesToURL?: boolean, isDisabled?: boolean; preloadNextPage?: boolean; };

export function useAddressTemplates({ setVariablesToURL = false, isDisabled = false, preloadNextPage = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<AddressFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: AddressFilter }) => karrio.graphql.request<get_address_templates>(
    gqlstr(GET_ADDRESS_TEMPLATES), { variables }
  );

  // Queries
  const query = useQuery({
    queryKey: ['addresses', filter],
    queryFn: () => fetch({ filter }),
    enabled: !isDisabled,
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  function setFilter(options: AddressFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof AddressFilter]) ? acc : {
        ...acc,
        [key]: ([""].includes(key)
          ? ([].concat(options[key as keyof AddressFilter] as any).reduce(
            (acc, item: string) => (
              typeof item == 'string'
                ? [].concat(acc, item.split(',') as any)
                : [].concat(acc, item)
            ), []
          ))
          : (["offset", "first"].includes(key)
            ? parseInt(options[key as keyof AddressFilter] as any)
            : options[key as keyof AddressFilter]
          )
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (preloadNextPage === false) return;
    if (query.data?.address_templates.page_info.has_next_page) {
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

export function useAddressTemplateMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['addresses']);
    queryClient.invalidateQueries(['default_templates']);
  };

  // Mutations
  const createAddressTemplate = useMutation(
    (data: CreateAddressTemplateInput) => karrio.graphql.request<create_address_template>(
      gqlstr(CREATE_ADDRESS_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateAddressTemplate = useMutation(
    (data: UpdateAddressTemplateInput) => karrio.graphql.request<update_address_template>(
      gqlstr(UPDATE_ADDRESS_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteAddressTemplate = useMutation(
    (data: { id: string }) => karrio.graphql.request<delete_template>(gqlstr(DELETE_TEMPLATE), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createAddressTemplate,
    updateAddressTemplate,
    deleteAddressTemplate,
  };
}
