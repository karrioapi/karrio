import { WorkflowEventFilter, GetWorkflowEvents, GET_WORKFLOW_EVENTS, GetWorkflowEvent, GET_WORKFLOW_EVENT, CreateWorkflowEvent, CreateWorkflowEventMutationInput, CREATE_WORKFLOW_EVENT, DeleteMutationInput, CancelWorkflowEvent, CancelWorkflowEventMutationInput, CANCEL_WORKFLOW_EVENT } from "@karrio/types/graphql/ee";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = WorkflowEventFilter & { setVariablesToURL?: boolean };

export function useWorkflowEvents({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<WorkflowEventFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: WorkflowEventFilter }) => karrio.graphql.request<GetWorkflowEvents>(
    gqlstr(GET_WORKFLOW_EVENTS), { variables }
  );

  // Queries
  const query = useQuery(
    ['workflow-events', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, refetchInterval: 120000, onError },
  );

  function setFilter(options: WorkflowEventFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof WorkflowEventFilter]) ? acc : {
        ...acc,
        [key]: (["offset", "first"].includes(key)
          ? parseInt((options as any)[key])
          : options[key as keyof WorkflowEventFilter]
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.workflow_events.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['workflow_events', _filter],
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

export function useWorkflowEvent(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(['workflow-events', id], {
    queryFn: () => karrio.graphql.request<GetWorkflowEvent>(gqlstr(GET_WORKFLOW_EVENT), { variables: { id } }),
    enabled: !!id,
    onError,
  });

  return {
    query,
  };
}


export function useWorkflowEventMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => { queryClient.invalidateQueries(['workflow-events']) };

  // Mutations
  const createWorkflowEvent = useMutation(
    (data: CreateWorkflowEventMutationInput) => karrio.graphql.request<CreateWorkflowEvent>(
      gqlstr(CREATE_WORKFLOW_EVENT), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const cancelWorkflowEvent = useMutation(
    (data: CancelWorkflowEventMutationInput) => karrio.graphql.request<CancelWorkflowEvent>(
      gqlstr(CANCEL_WORKFLOW_EVENT), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createWorkflowEvent,
    cancelWorkflowEvent,
  };
}
