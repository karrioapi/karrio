import { useState, useMemo } from 'react';
import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import {
  GET_MARKUPS,
  GET_MARKUP,
  CREATE_MARKUP,
  UPDATE_MARKUP,
  DELETE_MARKUP
} from "@karrio/types/graphql/admin/queries";
import {
  GetMarkups,
  GetMarkup,
  GetMarkupsVariables,
  GetMarkupVariables,
  CreateMarkup,
  CreateMarkupVariables,
  UpdateMarkup,
  UpdateMarkupVariables,
  DeleteMarkup,
  DeleteMarkupVariables,
  MarkupFilter,
  CreateMarkupMutationInput,
  MarkupTypeEnum,
  UsageFilter,
} from "@karrio/types/graphql/admin";
import { useQueryClient } from "@tanstack/react-query";
import { useOrganizationAccounts } from "./admin-accounts";
import { useSystemConnections } from "./admin-system-connections";
import { useAPIMetadata } from "./api-metadata";

// Types
export type MarkupType = GetMarkups['markups']['edges'][0]['node'];

export interface MarkupFormData {
  name: string;
  amount: string;
  markup_type: MarkupTypeEnum;
  active: boolean;
  is_visible: boolean;
  carrier_codes: string[];
  service_codes: string[];
  connection_ids: string[];
  organization_ids: string[];
  metadata: Record<string, any>;
}

// -----------------------------------------------------------
// Markups List Hook
// -----------------------------------------------------------
export function useMarkups(
  filter: MarkupFilter = {},
  usageFilter?: UsageFilter
) {
  const karrio = useKarrio();

  const variables: GetMarkupsVariables = {
    filter,
    ...(usageFilter && { usageFilter }),
  };

  const query = useAuthenticatedQuery({
    queryKey: ['admin_markups', filter, usageFilter],
    queryFn: () => karrio.admin.request<GetMarkups>(gqlstr(GET_MARKUPS), { variables }),
    staleTime: 5000,
  });

  return {
    query,
    markups: query.data?.markups,
  };
}

// -----------------------------------------------------------
// Single Markup Hook
// -----------------------------------------------------------
export function useMarkup(
  id: string,
  usageFilter?: UsageFilter
) {
  const karrio = useKarrio();

  const variables: GetMarkupVariables = {
    id,
    ...(usageFilter && { usageFilter }),
  };

  const query = useAuthenticatedQuery({
    queryKey: ['admin_markup', id, usageFilter],
    queryFn: () => karrio.admin.request<GetMarkup>(gqlstr(GET_MARKUP), { variables }),
    staleTime: 5000,
    enabled: !!id,
  });

  return {
    query,
    markup: query.data?.markup,
  };
}

// -----------------------------------------------------------
// Markup Mutations Hook
// -----------------------------------------------------------
export function useMarkupMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ['admin_markups'] });
    queryClient.invalidateQueries({ queryKey: ['admin_markup'] });
    queryClient.invalidateQueries({ queryKey: ['admin_system_usage'] });
    queryClient.invalidateQueries({ queryKey: ['admin_organization_accounts'] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ['admin_markups'] });
    queryClient.refetchQueries({ queryKey: ['admin_system_usage'] });
  };

  const createMarkup = useAuthenticatedMutation({
    mutationFn: (input: CreateMarkupVariables["input"]) => karrio.admin.request<CreateMarkup>(
      gqlstr(CREATE_MARKUP),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const updateMarkup = useAuthenticatedMutation({
    mutationFn: (input: UpdateMarkupVariables["input"]) => karrio.admin.request<UpdateMarkup>(
      gqlstr(UPDATE_MARKUP),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteMarkup = useAuthenticatedMutation({
    mutationFn: (input: DeleteMarkupVariables["input"]) => karrio.admin.request<DeleteMarkup>(
      gqlstr(DELETE_MARKUP),
      { variables: { input } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createMarkup,
    updateMarkup,
    deleteMarkup,
  };
}

// -----------------------------------------------------------
// Markup Form State Management Hook
// -----------------------------------------------------------
export function useMarkupForm(initialData?: MarkupType) {
  const [formData, setFormData] = useState<MarkupFormData>({
    name: initialData?.name || '',
    amount: initialData?.amount?.toString() || '',
    markup_type: (initialData?.markup_type as MarkupTypeEnum) || MarkupTypeEnum.AMOUNT,
    active: initialData?.active ?? true,
    is_visible: initialData?.is_visible ?? true,
    carrier_codes: initialData?.carrier_codes || [],
    service_codes: initialData?.service_codes || [],
    connection_ids: initialData?.connection_ids || [],
    organization_ids: initialData?.organization_ids || [],
    metadata: initialData?.metadata || {},
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
    if (!references?.services || formData.carrier_codes.length === 0) return [];

    const services: string[] = [];
    formData.carrier_codes.forEach(carrier => {
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
  }, [references?.services, formData.carrier_codes]);

  const updateFormData = (updates: Partial<MarkupFormData>) => {
    setFormData(prev => ({ ...prev, ...updates }));
  };

  const handleCarrierChange = (carrier: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      carrier_codes: checked
        ? [...prev.carrier_codes, carrier]
        : prev.carrier_codes.filter(c => c !== carrier),
      service_codes: [] // Reset services when carriers change
    }));
  };

  const handleServiceChange = (service: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      service_codes: checked
        ? [...prev.service_codes, service]
        : prev.service_codes.filter(s => s !== service)
    }));
  };

  const handleConnectionChange = (connectionId: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      connection_ids: checked
        ? [...prev.connection_ids, connectionId]
        : prev.connection_ids.filter(id => id !== connectionId)
    }));
  };

  const handleOrganizationChange = (orgId: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      organization_ids: checked
        ? [...prev.organization_ids, orgId]
        : prev.organization_ids.filter(id => id !== orgId)
    }));
  };

  const resetForm = () => {
    setFormData({
      name: '',
      amount: '',
      markup_type: MarkupTypeEnum.AMOUNT,
      active: true,
      is_visible: true,
      carrier_codes: [],
      service_codes: [],
      connection_ids: [],
      organization_ids: [],
      metadata: {},
    });
  };

  const toMutationInput = (): CreateMarkupMutationInput => ({
    name: formData.name,
    amount: parseFloat(formData.amount),
    markup_type: formData.markup_type,
    active: formData.active,
    is_visible: formData.is_visible,
    carrier_codes: formData.carrier_codes.length > 0 ? formData.carrier_codes : undefined,
    service_codes: formData.service_codes.length > 0 ? formData.service_codes : undefined,
    connection_ids: formData.connection_ids.length > 0 ? formData.connection_ids : undefined,
    organizations: formData.organization_ids.length > 0 ? formData.organization_ids : undefined,
    metadata: Object.keys(formData.metadata).length > 0 ? formData.metadata : undefined,
  });

  return {
    formData,
    setFormData,
    updateFormData,
    handleCarrierChange,
    handleServiceChange,
    handleConnectionChange,
    handleOrganizationChange,
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
