import { WorkflowActionFilter, GetWorkflowActions, GET_WORKFLOW_ACTIONS, GetWorkflowAction, GET_WORKFLOW_ACTION, CreateWorkflowAction, UpdateWorkflowAction, UpdateWorkflowActionMutationInput, CreateWorkflowActionMutationInput, DELETE_WORKFLOW_ACTION, UPDATE_WORKFLOW_ACTION, CREATE_WORKFLOW_ACTION, DeleteMutationInput, GetWorkflowActions_workflow_actions_edges_node } from "@karrio/types/graphql/ee";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = WorkflowActionFilter & { setVariablesToURL?: boolean };

export type WorkflowActionType = GetWorkflowActions_workflow_actions_edges_node;

export function useWorkflowActions({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
    const karrio = useKarrio();
    const queryClient = useQueryClient();
    const [filter, _setFilter] = React.useState<WorkflowActionFilter>({ ...PAGINATION, ...initialData });
    const fetch = (variables: { filter: WorkflowActionFilter }) => karrio.graphql.request<GetWorkflowActions>(
        gqlstr(GET_WORKFLOW_ACTIONS), { variables }
    );

    // Queries
    const query = useQuery(
        ['workflow-actions', filter],
        () => fetch({ filter }),
        { keepPreviousData: true, staleTime: 5000, refetchInterval: 120000, onError },
    );

    function setFilter(options: WorkflowActionFilter) {
        const params = Object.keys(options).reduce((acc, key) => {
            if (["modal"].includes(key)) return acc;
            return isNoneOrEmpty(options[key as keyof WorkflowActionFilter]) ? acc : {
                ...acc,
                [key]: (["offset", "first"].includes(key)
                    ? parseInt((options as any)[key])
                    : options[key as keyof WorkflowActionFilter]
                )
            };
        }, PAGINATION);

        if (setVariablesToURL) insertUrlParam(params);
        _setFilter(params);

        return params;
    }

    React.useEffect(() => {
        if (query.data?.workflow_actions.page_info.has_next_page) {
            const _filter = { ...filter, offset: filter.offset as number + 20 };
            queryClient.prefetchQuery(
                ['workflow-actions', _filter],
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

export function useWorkflowAction({ id, setVariablesToURL = false }: Args = {}) {
    const karrio = useKarrio();
    const [workflowActionId, _setWorkflowActionId] = React.useState<string>(id || 'new');

    // Queries
    const query = useQuery(['workflow-actions', id], {
        queryFn: () => karrio.graphql.request<GetWorkflowAction>(gqlstr(GET_WORKFLOW_ACTION), { variables: { id: workflowActionId } }),
        enabled: (workflowActionId !== 'new'),
        onError,
    });

    function setWorkflowActionId(workflowActionId: string) {
        if (setVariablesToURL) insertUrlParam({ id: workflowActionId });
        _setWorkflowActionId(workflowActionId);
    }

    return {
        query,
        workflowActionId,
        setWorkflowActionId,
    };
}


export function useWorkflowActionMutation() {
    const queryClient = useQueryClient();
    const karrio = useKarrio();
    const invalidateCache = () => { queryClient.invalidateQueries(['workflow-actions']) };

    // Mutations
    const createWorkflowAction = useMutation(
        (data: CreateWorkflowActionMutationInput) => karrio.graphql.request<CreateWorkflowAction>(
            gqlstr(CREATE_WORKFLOW_ACTION), { data }
        ),
        { onSuccess: invalidateCache, onError }
    );
    const updateWorkflowAction = useMutation(
        (data: UpdateWorkflowActionMutationInput) => karrio.graphql.request<UpdateWorkflowAction>(
            gqlstr(UPDATE_WORKFLOW_ACTION), { data }
        ),
        { onSuccess: invalidateCache, onError }
    );
    const deleteWorkflowAction = useMutation(
        (data: { id: string }) => karrio.graphql.request<DeleteMutationInput>(
            gqlstr(DELETE_WORKFLOW_ACTION), { data }
        ),
        { onSuccess: invalidateCache, onError }
    );

    return {
        createWorkflowAction,
        updateWorkflowAction,
        deleteWorkflowAction,
    };
}