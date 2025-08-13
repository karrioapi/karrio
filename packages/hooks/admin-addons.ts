import { useState, useMemo } from 'react';
import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import {
  GET_ADDONS,
  GET_ADDON,
  CREATE_ADDON,
  UPDATE_ADDON,
  DELETE_ADDON
} from "@karrio/types/graphql/admin/queries";
import {
  GetAddons,
  GetAddon,
  GetAddonsVariables,
  GetAddonVariables,
  CreateAddon,
  CreateAddonVariables,
  UpdateAddon,
  UpdateAddonVariables,
  DeleteAddon,
  DeleteAddonVariables,
  AddonFilter,
  CreateAddonMutationInput,
  SurchargeTypeEnum,
  UsageFilter,
} from "@karrio/types/graphql/admin";
import { useQueryClient } from "@tanstack/react-query";
import { useOrganizationAccounts } from "./admin-accounts";
import { useSystemConnections } from "./admin-system-connections";
import { useAPIMetadata } from "./api-metadata";

// Types
export type AddonType = GetAddons['addons']['edges'][0]['node'];

export interface AddonFormData {
  name: string;
  amount: string;
  surcharge_type: SurchargeTypeEnum;
  active: boolean;
  carriers: string[];
  services: string[];
  carrier_accounts: string[];
  organizations: string[];
}

// -----------------------------------------------------------
// Addons List Hook
// -----------------------------------------------------------
export function useAddons(
  filter: AddonFilter = {},
  usageFilter?: UsageFilter
) {
  const karrio = useKarrio();

  const variables: GetAddonsVariables = {
    filter,
    ...(usageFilter && { usageFilter }),
  };

  const query = useAuthenticatedQuery({
    queryKey: ['admin_addons', filter, usageFilter],
    queryFn: () => karrio.admin.request<GetAddons>(gqlstr(GET_ADDONS), { variables }),
    staleTime: 5000,
  });

  return {
    query,
    addons: query.data?.addons,
  };
}

// -----------------------------------------------------------
// Single Addon Hook
// -----------------------------------------------------------
export function useAddon(
  id: string,
  usageFilter?: UsageFilter
) {
  const karrio = useKarrio();

  const variables: GetAddonVariables = {
    id,
    ...(usageFilter && { usageFilter }),
  };

  const query = useAuthenticatedQuery({
    queryKey: ['admin_addon', id, usageFilter],
    queryFn: () => karrio.admin.request<GetAddon>(gqlstr(GET_ADDON), { variables }),
    staleTime: 5000,
    enabled: !!id,
  });

  return {
    query,
    addon: query.data?.addon,
  };
}

// -----------------------------------------------------------
// Addon Mutations Hook
// -----------------------------------------------------------
export function useAddonMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateCache = () => {
    queryClient.invalidateQueries(['admin_addons']);
    queryClient.invalidateQueries(['admin_addon']);
  };

  const createAddon = useAuthenticatedMutation({
    mutationFn: (input: CreateAddonVariables["input"]) => karrio.admin.request<CreateAddon>(
      gqlstr(CREATE_ADDON),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const updateAddon = useAuthenticatedMutation({
    mutationFn: (input: UpdateAddonVariables["input"]) => karrio.admin.request<UpdateAddon>(
      gqlstr(UPDATE_ADDON),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteAddon = useAuthenticatedMutation({
    mutationFn: (input: DeleteAddonVariables["input"]) => karrio.admin.request<DeleteAddon>(
      gqlstr(DELETE_ADDON),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createAddon,
    updateAddon,
    deleteAddon,
  };
}

// -----------------------------------------------------------
// Addon Form State Management Hook
// -----------------------------------------------------------
export function useAddonForm(initialData?: AddonType) {
  const [formData, setFormData] = useState<AddonFormData>({
    name: initialData?.name || '',
    amount: initialData?.amount?.toString() || '',
    surcharge_type: (initialData?.surcharge_type as SurchargeTypeEnum) || SurchargeTypeEnum.AMOUNT,
    active: initialData?.active ?? true,
    carriers: initialData?.carriers || [],
    services: initialData?.services || [],
    carrier_accounts: initialData?.carrier_accounts?.map(acc => acc.id) || [],
    organizations: [] // Not available in current GraphQL schema
  });

  const { references } = useAPIMetadata();
  const { query: organizationsQuery } = useOrganizationAccounts();
  const { query: systemConnectionsQuery } = useSystemConnections();

  const organizations = organizationsQuery.data?.accounts?.edges || [];
  const systemConnections = systemConnectionsQuery.data?.system_carrier_connections?.edges || [];

  // Get available carriers from references
  const availableCarriers = references?.carriers ? Object.keys(references.carriers) : [];

  // Get available services for selected carriers
  const availableServices = useMemo(() => {
    if (!references?.services || formData.carriers.length === 0) return [];

    const services: string[] = [];
    formData.carriers.forEach(carrier => {
      const carrierServices = references.services[carrier];
      if (carrierServices) {
        Object.keys(carrierServices).forEach(service => {
          if (!services.includes(service)) {
            services.push(service);
          }
        });
      }
    });
    return services;
  }, [references?.services, formData.carriers]);

  const updateFormData = (updates: Partial<AddonFormData>) => {
    setFormData(prev => ({ ...prev, ...updates }));
  };

  const handleCarrierChange = (carrier: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      carriers: checked
        ? [...prev.carriers, carrier]
        : prev.carriers.filter(c => c !== carrier),
      services: [] // Reset services when carriers change
    }));
  };

  const handleServiceChange = (service: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      services: checked
        ? [...prev.services, service]
        : prev.services.filter(s => s !== service)
    }));
  };

  const resetForm = () => {
    setFormData({
      name: '',
      amount: '',
      surcharge_type: SurchargeTypeEnum.AMOUNT,
      active: true,
      carriers: [],
      services: [],
      carrier_accounts: [],
      organizations: []
    });
  };

  const toMutationInput = (): CreateAddonMutationInput => ({
    name: formData.name,
    amount: parseFloat(formData.amount),
    surcharge_type: formData.surcharge_type,
    active: formData.active,
    carriers: formData.carriers.length > 0 ? formData.carriers : undefined,
    services: formData.services.length > 0 ? formData.services : undefined,
    carrier_accounts: formData.carrier_accounts.length > 0 ? formData.carrier_accounts : undefined,
  });

  return {
    formData,
    setFormData,
    updateFormData,
    handleCarrierChange,
    handleServiceChange,
    resetForm,
    toMutationInput,
    // Data for form fields
    organizations,
    systemConnections,
    availableCarriers,
    availableServices,
    // Loading states
    isLoadingOrganizations: organizationsQuery.isLoading,
    isLoadingConnections: systemConnectionsQuery.isLoading,
  };
}