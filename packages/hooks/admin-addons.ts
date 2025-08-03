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
  CreateAddon,
  CreateAddonVariables,
  UpdateAddon,
  UpdateAddonVariables,
  DeleteAddon,
  DeleteAddonVariables,
  AddonFilter,
} from "@karrio/types/graphql/admin";
import { useQueryClient } from "@tanstack/react-query";

// Types
export type AddonType = GetAddons['addons']['edges'][0]['node'];

// -----------------------------------------------------------
// Addons List Hook
// -----------------------------------------------------------
export function useAddons(filter: AddonFilter = {}) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_addons', filter],
    queryFn: () => karrio.admin.request<GetAddons>(gqlstr(GET_ADDONS), { variables: { filter } }),
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
export function useAddon(id: string) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_addon', id],
    queryFn: () => karrio.admin.request<GetAddon>(gqlstr(GET_ADDON), { variables: { id } }),
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
    mutationFn: (data: CreateAddonVariables["data"]) => karrio.admin.request<CreateAddon>(
      gqlstr(CREATE_ADDON),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const updateAddon = useAuthenticatedMutation({
    mutationFn: (data: UpdateAddonVariables["data"]) => karrio.admin.request<UpdateAddon>(
      gqlstr(UPDATE_ADDON),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteAddon = useAuthenticatedMutation({
    mutationFn: (data: DeleteAddonVariables["data"]) => karrio.admin.request<DeleteAddon>(
      gqlstr(DELETE_ADDON),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createAddon,
    updateAddon,
    deleteAddon,
  };
}
