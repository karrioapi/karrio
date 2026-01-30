import { AddressFilter, CreateAddressInput, create_address, CREATE_ADDRESS, delete_address, DELETE_ADDRESS, get_addresses, GET_ADDRESSES, UpdateAddressInput, update_address, UPDATE_ADDRESS } from "@karrio/types";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import { gqlstr, insertUrlParam, isNoneOrEmpty } from "@karrio/lib";
import { useQueryClient } from "@tanstack/react-query";
import React from "react";

const PAGE_SIZE = 25;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = AddressFilter & { setVariablesToURL?: boolean, isDisabled?: boolean; preloadNextPage?: boolean; };

export function useAddresses({ setVariablesToURL = false, isDisabled = false, preloadNextPage = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<AddressFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: AddressFilter }) => karrio.graphql.request<get_addresses>(
    gqlstr(GET_ADDRESSES), { variables }
  );

  const query = useAuthenticatedQuery({
    queryKey: ['addresses', filter],
    queryFn: () => fetch({ filter }),
    enabled: !isDisabled,
    keepPreviousData: true,
    staleTime: 5000,
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
    if (query.data?.addresses.page_info.has_next_page) {
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

export function useAddressMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ['addresses'] });
    queryClient.invalidateQueries({ queryKey: ['default_templates'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['addresses'] });
  };

  const createAddress = useAuthenticatedMutation({
    mutationFn: (data: CreateAddressInput) => karrio.graphql.request<create_address>(
      gqlstr(CREATE_ADDRESS), { data }
    ),
    onSuccess: invalidateCache,
  });

  const updateAddress = useAuthenticatedMutation({
    mutationFn: (data: UpdateAddressInput) => karrio.graphql.request<update_address>(
      gqlstr(UPDATE_ADDRESS), { data }
    ),
    onSuccess: invalidateCache,
  });

  const deleteAddress = useAuthenticatedMutation({
    mutationFn: (data: { id: string }) => karrio.graphql.request<delete_address>(gqlstr(DELETE_ADDRESS), { data }),
    onSuccess: invalidateCache,
  });

  return {
    createAddress,
    updateAddress,
    deleteAddress,
  };
}
