import { gqlstr } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import {
  GET_SYSTEM_CONNECTIONS,
  GET_SYSTEM_CONNECTION,
  CREATE_SYSTEM_CONNECTION,
  UPDATE_SYSTEM_CONNECTION,
  DELETE_SYSTEM_CONNECTION
} from "@karrio/types/graphql/admin/queries";
import {
  GetSystemConnections,
  GetSystemConnectionsVariables,
  GetSystemConnection,
  GetSystemConnectionVariables,
  CreateSystemConnection,
  CreateSystemConnectionVariables,
  UpdateSystemConnection,
  UpdateSystemConnectionVariables,
  DeleteSystemConnection,
  DeleteSystemConnectionVariables,
  CarrierFilter,
} from "@karrio/types/graphql/admin";
import { useQueryClient } from "@tanstack/react-query";

// Types
export type SystemConnectionType = GetSystemConnections['system_carrier_connections']['edges'][0]['node'];

// -----------------------------------------------------------
// System Connections List Hook
// -----------------------------------------------------------
export function useSystemConnections(filter: CarrierFilter = {}) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_system_connections', filter],
    queryFn: () => karrio.admin.request<GetSystemConnections>(gqlstr(GET_SYSTEM_CONNECTIONS), { variables: { filter } }),
    staleTime: 5000,
  });

  return {
    query,
    system_carrier_connections: query.data?.system_carrier_connections,
  };
}

// -----------------------------------------------------------
// Single System Connection Hook
// -----------------------------------------------------------
export function useSystemConnection(id: string) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['admin_system_connection', id],
    queryFn: () => karrio.admin.request<GetSystemConnection>(gqlstr(GET_SYSTEM_CONNECTION), { variables: { id } }),
    staleTime: 5000,
    enabled: !!id,
  });

  return {
    query,
    system_carrier_connection: query.data?.system_carrier_connection,
  };
}

// -----------------------------------------------------------
// System Connection Mutations Hook
// -----------------------------------------------------------
export function useSystemConnectionMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateCache = () => {
    queryClient.invalidateQueries(['admin_system_connections']);
    queryClient.invalidateQueries(['admin_system_connection']);
  };

  const createSystemConnection = useAuthenticatedMutation({
    mutationFn: (data: CreateSystemConnectionVariables["data"]) => karrio.admin.request<CreateSystemConnection>(
      gqlstr(CREATE_SYSTEM_CONNECTION),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const updateSystemConnection = useAuthenticatedMutation({
    mutationFn: (data: UpdateSystemConnectionVariables["data"]) => karrio.admin.request<UpdateSystemConnection>(
      gqlstr(UPDATE_SYSTEM_CONNECTION),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  const deleteSystemConnection = useAuthenticatedMutation({
    mutationFn: (data: DeleteSystemConnectionVariables["data"]) => karrio.admin.request<DeleteSystemConnection>(
      gqlstr(DELETE_SYSTEM_CONNECTION),
      { variables: { data } }
    ),
    onSuccess: invalidateCache,
  });

  return {
    createSystemConnection,
    updateSystemConnection,
    deleteSystemConnection,
  };
}
