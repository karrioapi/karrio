import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import {
  GET_ACCOUNTS,
  CREATE_ORGANIZATION_ACCOUNT,
  UPDATE_ORGANIZATION_ACCOUNT,
  DISABLE_ORGANIZATION_ACCOUNT,
  DELETE_ORGANIZATION_ACCOUNT
} from "@karrio/types/graphql/admin/queries";
import {
  GetAccounts,
  GetAccountsVariables,
  CreateOrganizationAccount,
  CreateOrganizationAccountVariables,
  UpdateOrganizationAccount,
  UpdateOrganizationAccountVariables,
  DisableOrganizationAccount,
  DisableOrganizationAccountVariables,
  DeleteOrganizationAccount,
  DeleteOrganizationAccountVariables,
  AccountFilter,
} from "@karrio/types/graphql/admin";
import { useQueryClient } from "@tanstack/react-query";

// Types
export type OrganizationAccountType = GetAccounts['accounts']['edges'][0]['node'];

// -----------------------------------------------------------
// Organization Accounts List Hook
// -----------------------------------------------------------
export function useOrganizationAccounts(filter: AccountFilter = {}) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_organization_accounts', filter],
    queryFn: () => karrio.admin.request<GetAccounts>(gqlstr(GET_ACCOUNTS), { variables: { filter } }),
    staleTime: 5000,
  });

  return {
    query,
    accounts: query.data?.accounts,
  };
}

// -----------------------------------------------------------
// Organization Account Mutations Hook
// -----------------------------------------------------------
export function useOrganizationAccountMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateCache = () => {
    queryClient.invalidateQueries(['admin_organization_accounts']);
    queryClient.invalidateQueries(['admin_organization_account']);
  };

  const createOrganizationAccount = useAuthenticatedMutation({
    mutationFn: (data: CreateOrganizationAccountVariables["data"]) => karrio.admin.request<CreateOrganizationAccount>(
      gqlstr(CREATE_ORGANIZATION_ACCOUNT),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const updateOrganizationAccount = useAuthenticatedMutation({
    mutationFn: (data: UpdateOrganizationAccountVariables["data"]) => karrio.admin.request<UpdateOrganizationAccount>(
      gqlstr(UPDATE_ORGANIZATION_ACCOUNT),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const disableOrganizationAccount = useAuthenticatedMutation({
    mutationFn: (data: DisableOrganizationAccountVariables["data"]) => karrio.admin.request<DisableOrganizationAccount>(
      gqlstr(DISABLE_ORGANIZATION_ACCOUNT),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteOrganizationAccount = useAuthenticatedMutation({
    mutationFn: (data: DeleteOrganizationAccountVariables["data"]) => karrio.admin.request<DeleteOrganizationAccount>(
      gqlstr(DELETE_ORGANIZATION_ACCOUNT),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createOrganizationAccount,
    updateOrganizationAccount,
    disableOrganizationAccount,
    deleteOrganizationAccount,
  };
}
