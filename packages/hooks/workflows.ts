import { WorkflowFilter, GetWorkflows, GET_WORKFLOWS, GetWorkflow, GET_WORKFLOW, CreateWorkflow, UpdateWorkflow, UpdateWorkflowMutationInput, CreateWorkflowMutationInput, DELETE_WORKFLOW, UPDATE_WORKFLOW, CREATE_WORKFLOW, DeleteMutationInput, GetWorkflows_workflows_edges_node } from "@karrio/types/graphql/ee";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = WorkflowFilter & { setVariablesToURL?: boolean };

export type WorkflowType = GetWorkflows_workflows_edges_node;

export function useWorkflows({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<WorkflowFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: WorkflowFilter }) => karrio.graphql.request<GetWorkflows>(
    gqlstr(GET_WORKFLOWS), { variables }
  );

  // Queries
  const query = useQuery(
    ['workflows', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, refetchInterval: 120000, onError },
  );

  function setFilter(options: WorkflowFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof WorkflowFilter]) ? acc : {
        ...acc,
        [key]: (["offset", "first"].includes(key)
          ? parseInt((options as any)[key])
          : options[key as keyof WorkflowFilter]
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.workflows.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['workflows', _filter],
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

export function useWorkflow(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(['workflows', id], {
    queryFn: () => karrio.graphql.request<GetWorkflow>(gqlstr(GET_WORKFLOW), { data: { id } }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}


export function useWorkflowMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => { queryClient.invalidateQueries(['workflows']) };

  // Mutations
  const createWorkflow = useMutation(
    (data: CreateWorkflowMutationInput) => karrio.graphql.request<CreateWorkflow>(
      gqlstr(CREATE_WORKFLOW), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateWorkflow = useMutation(
    (data: UpdateWorkflowMutationInput) => karrio.graphql.request<UpdateWorkflow>(
      gqlstr(UPDATE_WORKFLOW), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteWorkflow = useMutation(
    (data: { id: string }) => karrio.graphql.request<DeleteMutationInput>(
      gqlstr(DELETE_WORKFLOW), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createWorkflow,
    updateWorkflow,
    deleteWorkflow,
  };
}
