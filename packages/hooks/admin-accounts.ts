import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import {
  GET_ORGANIZATIONS as GET_ACCOUNTS,
  GET_ORGANIZATION_DETAILS,
  CREATE_ORGANIZATION_ACCOUNT,
  UPDATE_ORGANIZATION_ACCOUNT,
  DISABLE_ORGANIZATION_ACCOUNT,
  DELETE_ORGANIZATION_ACCOUNT
} from "@karrio/types/graphql/admin-ee/queries";
import {
  GetOrganizations,
  GetOrganizationDetails,
  CreateOrganizationAccount,
  CreateOrganizationAccountVariables,
  UpdateOrganizationAccount,
  UpdateOrganizationAccountVariables,
  DisableOrganizationAccount,
  DisableOrganizationAccountVariables,
  DeleteOrganizationAccount,
  DeleteOrganizationAccountVariables,
  AccountFilter,
} from "@karrio/types/graphql/admin-ee";
import { useQueryClient } from "@tanstack/react-query";
import { useMemo } from "react";

// Types
export type OrganizationAccountType = GetOrganizations['accounts']['edges'][0]['node'];

// -----------------------------------------------------------
// Organization Accounts List Hook
// -----------------------------------------------------------
export function useOrganizationAccounts(filter: AccountFilter = {}) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_organization_accounts', filter],
    queryFn: () => karrio.admin.request<GetOrganizations>(gqlstr(GET_ACCOUNTS), { variables: { filter } }),
    staleTime: 5000,
  });

  return {
    query,
    accounts: query.data?.accounts,
  };
}

// -----------------------------------------------------------
// System-wide Usage Statistics Hook (Simplified)
// -----------------------------------------------------------
export function useSystemUsageStats(usageFilter?: any) {
  const { query, accounts } = useOrganizationAccounts();

  // Since we can't use hooks in loops, we'll work with the basic account data
  // and aggregate the usage information that's already available
  const systemStats = useMemo(() => {
    if (query.isLoading || !accounts?.edges) return null;

    return accounts.edges.reduce((acc, { node }) => {
      const usage = node.usage || {};
      return {
        totalOrganizations: acc.totalOrganizations + 1,
        activeOrganizations: acc.activeOrganizations + (node.is_active ? 1 : 0),
        totalMembers: acc.totalMembers + (usage.members || 0),
        totalShipments: acc.totalShipments + (usage.total_shipments || 0),
        totalTrackers: acc.totalTrackers + (usage.total_trackers || 0),
        totalRequests: acc.totalRequests + (usage.total_requests || 0),
        totalSpend: acc.totalSpend + (usage.total_shipping_spend || 0),
        totalErrors: acc.totalErrors + (usage.total_errors || 0),
        orderVolume: acc.orderVolume + (usage.order_volume || 0),
        unfulfilled: acc.unfulfilled + (usage.unfulfilled_orders || 0),
        totalAddonsCharges: acc.totalAddonsCharges + (usage.total_addons_charges || 0),
        // Note: time series data would need to be fetched individually per org
        shippingSpendHistory: [],
        shipmentHistory: [],
        requestHistory: [],
        errorHistory: [],
        organizations: [...acc.organizations, {
          id: node.id,
          name: node.name,
          isActive: node.is_active,
          usage: usage
        }]
      };
    }, {
      totalOrganizations: 0,
      activeOrganizations: 0,
      totalMembers: 0,
      totalShipments: 0,
      totalTrackers: 0,
      totalRequests: 0,
      totalSpend: 0,
      totalErrors: 0,
      orderVolume: 0,
      unfulfilled: 0,
      totalAddonsCharges: 0,
      shippingSpendHistory: [] as any[],
      shipmentHistory: [] as any[],
      requestHistory: [] as any[],
      errorHistory: [] as any[],
      organizations: [] as any[]
    });
  }, [accounts, query.isLoading]);

  return {
    systemStats,
    isLoading: query.isLoading,
    hasError: !!query.error,
    refetch: query.refetch
  };
}

// -----------------------------------------------------------
// Organization Account Details Hook
// -----------------------------------------------------------
export function useOrganizationAccountDetails(id: string, usageFilter?: any) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_organization_account_details', id, usageFilter],
    queryFn: () => karrio.admin.request<GetOrganizationDetails>(
      gqlstr(GET_ORGANIZATION_DETAILS),
      { variables: { id, usageFilter } }
    ),
    enabled: !!id,
    staleTime: 5000,
  });

  return {
    query,
    account: query.data?.account,
  };
}

// -----------------------------------------------------------
// Organization Account Mutations Hook
// -----------------------------------------------------------
export function useOrganizationAccountMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ['admin_organization_accounts'] });
    queryClient.invalidateQueries({ queryKey: ['admin_organization_account'] });
    queryClient.invalidateQueries({ queryKey: ['admin_organization_account_details'] });
    queryClient.invalidateQueries({ queryKey: ['admin_system_usage'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['admin_organization_accounts'] });
  };

  const createOrganizationAccount = useAuthenticatedMutation({
    mutationFn: (input: CreateOrganizationAccountVariables["input"]) => karrio.admin.request<CreateOrganizationAccount>(
      gqlstr(CREATE_ORGANIZATION_ACCOUNT),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const updateOrganizationAccount = useAuthenticatedMutation({
    mutationFn: (input: UpdateOrganizationAccountVariables["input"]) => karrio.admin.request<UpdateOrganizationAccount>(
      gqlstr(UPDATE_ORGANIZATION_ACCOUNT),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const disableOrganizationAccount = useAuthenticatedMutation({
    mutationFn: (input: DisableOrganizationAccountVariables["input"]) => karrio.admin.request<DisableOrganizationAccount>(
      gqlstr(DISABLE_ORGANIZATION_ACCOUNT),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteOrganizationAccount = useAuthenticatedMutation({
    mutationFn: (input: DeleteOrganizationAccountVariables["input"]) => karrio.admin.request<DeleteOrganizationAccount>(
      gqlstr(DELETE_ORGANIZATION_ACCOUNT),
      { variables: { input } }
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
