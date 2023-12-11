import { AccountFilter, GET_ACCOUNTS, GetAccounts, UPDATE_ORGANIZATION_ACCOUNT, UpdateOrganizationAccount, UpdateOrganizationAccountMutationInput } from "@karrio/types/graphql/admin";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "../karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = AccountFilter & { setVariablesToURL?: boolean };

export function useAccounts({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<AccountFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: AccountFilter }) => karrio.admin.request<GetAccounts>(
    gqlstr(GET_ACCOUNTS), { variables }
  );

  // Queries
  const query = useQuery(
    ['accounts', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  function setFilter(options: AccountFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof AccountFilter]) ? acc : {
        ...acc,
        [key]: (["status", "option_key"].includes(key)
          ? ([].concat(options[key as keyof AccountFilter] as any).reduce(
            (acc, item: string) => (
              typeof item == 'string'
                ? [].concat(acc, item.split(',') as any)
                : [].concat(acc, item)
            ), []
          ))
          : (["offset", "first"].includes(key)
            ? parseInt(options[key as keyof AccountFilter] as any)
            : options[key as keyof AccountFilter]
          )
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.accounts.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['accounts', _filter],
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

export function useAccountMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['accounts']);
  };

  // Mutations
  const updateAccount = useMutation(
    (data: UpdateOrganizationAccountMutationInput) => karrio.graphql.request<UpdateOrganizationAccount>(
      gqlstr(UPDATE_ORGANIZATION_ACCOUNT), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    updateAccount,
  };
}
