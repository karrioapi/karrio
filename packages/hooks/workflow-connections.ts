import { WorkflowConnectionFilter, GetWorkflowConnections, GET_WORKFLOW_CONNECTIONS, GetWorkflowConnection, GET_WORKFLOW_CONNECTION, CreateWorkflowConnection, UpdateWorkflowConnection, UpdateWorkflowConnectionMutationInput, CreateWorkflowConnectionMutationInput, DELETE_WORKFLOW_CONNECTION, UPDATE_WORKFLOW_CONNECTION, CREATE_WORKFLOW_CONNECTION, DeleteMutationInput } from "@karrio/types/graphql/ee";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = WorkflowConnectionFilter & { setVariablesToURL?: boolean };

export function useWorkflowConnections({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<WorkflowConnectionFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: WorkflowConnectionFilter }) => karrio.graphql.request<GetWorkflowConnections>(
    gqlstr(GET_WORKFLOW_CONNECTIONS), { variables }
  );

  // Queries
  const query = useQuery(
    ['workflow-connections', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, refetchInterval: 120000, onError },
  );

  function setFilter(options: WorkflowConnectionFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof WorkflowConnectionFilter]) ? acc : {
        ...acc,
        [key]: (["offset", "first"].includes(key)
          ? parseInt((options as any)[key])
          : options[key as keyof WorkflowConnectionFilter]
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.workflow_connections.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['workflow-connections', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])

  return {
    query,
    get filter() { return filter; },
    setFilter,
  };
}


type Args = { id?: string, setVariablesToURL?: boolean };

export function useWorkflowConnection({ id, setVariablesToURL = false }: Args = {}) {
  const karrio = useKarrio();
  const [workflowActionId, _setWorkflowConnectionId] = React.useState<string>(id || 'new');

  // Queries
  const query = useQuery(['workflow-connections', id], {
    queryFn: () => karrio.graphql.request<GetWorkflowConnection>(gqlstr(GET_WORKFLOW_CONNECTION), { variables: { id: workflowActionId } }),
    enabled: (workflowActionId !== 'new'),
    onError,
  });

  function setWorkflowConnectionId(workflowActionId: string) {
    if (setVariablesToURL) insertUrlParam({ id: workflowActionId });
    _setWorkflowConnectionId(workflowActionId);
  }

  return {
    query,
    workflowActionId,
    setWorkflowConnectionId,
  };
}


export function useWorkflowConnectionMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => { queryClient.invalidateQueries(['workflow-connections']) };

  // Mutations
  const createWorkflowConnection = useMutation(
    (data: CreateWorkflowConnectionMutationInput) => karrio.graphql.request<CreateWorkflowConnection>(
      gqlstr(CREATE_WORKFLOW_CONNECTION), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateWorkflowConnection = useMutation(
    (data: UpdateWorkflowConnectionMutationInput) => karrio.graphql.request<UpdateWorkflowConnection>(
      gqlstr(UPDATE_WORKFLOW_CONNECTION), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteWorkflowConnection = useMutation(
    (data: { id: string }) => karrio.graphql.request<DeleteMutationInput>(
      gqlstr(DELETE_WORKFLOW_CONNECTION), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createWorkflowConnection,
    updateWorkflowConnection,
    deleteWorkflowConnection,
  };
}
