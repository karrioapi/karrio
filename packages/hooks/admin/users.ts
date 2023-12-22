import { CREATE_USER, CreateUser, CreateUserMutationInput, DeleteUserMutationInput, GET_USERS, GetUsers, REMOVE_USER, RemoveUser, UPDATE_USER, UpdateUser, UpdateUserMutationInput, UserFilter } from "@karrio/types/graphql/admin";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "../karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = UserFilter & { setVariablesToURL?: boolean };
export type StaffUserType = GetUsers['users']['edges'][0]['node'];

export function useUsers({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<UserFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: UserFilter }) => karrio.admin.request<GetUsers>(
    gqlstr(GET_USERS), { variables }
  );

  // Queries
  const query = useQuery(
    ['users', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  function setFilter(options: UserFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof UserFilter]) ? acc : {
        ...acc,
        [key]: (["status", "option_key"].includes(key)
          ? ([].concat(options[key as keyof UserFilter] as any).reduce(
            (acc, item: string) => (
              typeof item == 'string'
                ? [].concat(acc, item.split(',') as any)
                : [].concat(acc, item)
            ), []
          ))
          : (["offset", "first"].includes(key)
            ? parseInt(options[key as keyof UserFilter] as any)
            : options[key as keyof UserFilter]
          )
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.users.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['users', _filter],
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

export function useUserMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['users']);
  };

  // Mutations
  const createUser = useMutation(
    (data: CreateUserMutationInput) => karrio.admin.request<CreateUser>(
      gqlstr(CREATE_USER), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateUser = useMutation(
    (data: UpdateUserMutationInput) => karrio.admin.request<UpdateUser>(
      gqlstr(UPDATE_USER), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteUser = useMutation(
    (data: DeleteUserMutationInput) => karrio.admin.request<RemoveUser>(gqlstr(REMOVE_USER), { data }),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createUser,
    updateUser,
    deleteUser,
  };
}
