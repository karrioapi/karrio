import {
  WorkflowFilter,
  GetWorkflows,
  GET_WORKFLOWS,
  GetWorkflow,
  GET_WORKFLOW,
  CreateWorkflow,
  UpdateWorkflow,
  UpdateWorkflowMutationInput,
  CreateWorkflowMutationInput,
  DELETE_WORKFLOW,
  UPDATE_WORKFLOW,
  CREATE_WORKFLOW,
  DeleteMutationInput,
  GetWorkflows_workflows_edges_node,
  CreateWorkflowTriggerMutationInput,
  CREATE_WORKFLOW_TRIGGER,
  CreateWorkflowTrigger,
  UpdateWorkflowTriggerMutationInput,
  UPDATE_WORKFLOW_TRIGGER,
  UpdateWorkflowTrigger,
  DELETE_WORKFLOW_TRIGGER,
  TRIGGER_SCHEDULED_WORKFLOW,
  VALIDATE_CRON_EXPRESSION,
  AutomationActionType,
  AutomationHTTPMethod,
  AutomationHTTPContentType,
  AutomationParametersType,
  PartialWorkflowActionMutationInput,
  PartialWorkflowTriggerMutationInput,
  ActionNodeInput,
  PartialWorkflowConnectionMutationInput,
  AutomationEventType,
  AutomationEventStatus,
  AutomationTriggerType,
} from "@karrio/types/graphql/ee";
import {
  WorkflowEventType,
  useWorkflowEventMutation,
  useWorkflowEvents,
} from "./workflow-events";
import { PREDEFINED_WORKFLOW_TEMPLATES } from "./workflow-templates";
import {
  gqlstr,
  insertUrlParam,
  isEqual,
  isNoneOrEmpty,
  onError,
  p,
} from "@karrio/lib";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useWorkflowConnectionMutation } from "./workflow-connections";
import { useWorkflowActionMutation } from "./workflow-actions";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useRouter } from "next/navigation";
import { NotificationType } from "@karrio/types";
import { useAppMode } from "./app-mode";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = WorkflowFilter & { setVariablesToURL?: boolean };

export type WorkflowType = GetWorkflows_workflows_edges_node;
export type WorkflowTriggerType = GetWorkflows_workflows_edges_node["trigger"];

export function useWorkflows({
  setVariablesToURL = false,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<WorkflowFilter>({
    ...PAGINATION,
    ...initialData,
  });
  const fetch = (variables: { filter: WorkflowFilter }) =>
    karrio.graphql.request<GetWorkflows>(gqlstr(GET_WORKFLOWS), { variables });

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["workflows", filter],
    queryFn: () => fetch({ filter }),
    keepPreviousData: true,
    staleTime: 5000,
    refetchInterval: 120000,
    onError,
  });

  function setFilter(options: WorkflowFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof WorkflowFilter])
        ? acc
        : {
          ...acc,
          [key]: ["offset", "first"].includes(key)
            ? parseInt((options as any)[key])
            : options[key as keyof WorkflowFilter],
        };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.workflows.page_info.has_next_page) {
      const _filter = { ...filter, offset: (filter.offset as number) + 20 };
      queryClient.prefetchQuery(["workflows", _filter], () =>
        fetch({ filter: _filter }),
      );
    }
  }, [query.data, filter.offset, queryClient]);

  return {
    query,
    get filter() {
      return filter;
    },
    setFilter,
  };
}

export function useScheduledWorkflows({
  setVariablesToURL = false,
  ...initialData
}: FilterType = {}) {
  return useWorkflows({
    setVariablesToURL,
    trigger_type: AutomationTriggerType.scheduled,
    ...initialData,
  });
}

export function useWorkflow({
  id,
  setVariablesToURL = false,
}: { id?: string; setVariablesToURL?: boolean } = {}) {
  const karrio = useKarrio();
  const [workflowId, _setWorkflowId] = React.useState<string>(id || "new");

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["workflows", id],
    queryFn: () => karrio.graphql.request<GetWorkflow>(gqlstr(GET_WORKFLOW), { variables: { id: workflowId } }),
    enabled: workflowId !== "new",
    onError,
  });

  function setWorkflowId(workflowId: string) {
    if (setVariablesToURL) insertUrlParam({ id: workflowId });
    _setWorkflowId(workflowId);
  }

  return {
    query,
    workflowId,
    setWorkflowId,
  };
}

export function useWorkflowMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ["workflows"] });
    queryClient.invalidateQueries({ queryKey: ["workflow_events"] });
    queryClient.invalidateQueries({ queryKey: ["workflow_connections"] });
    queryClient.invalidateQueries({ queryKey: ["workflow_actions"] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ["workflows"] });
  };

  // Mutations
  const createWorkflow = useMutation(
    (data: CreateWorkflowMutationInput) =>
      karrio.graphql.request<CreateWorkflow>(gqlstr(CREATE_WORKFLOW), { data }),
    { onSuccess: invalidateCache, onError },
  );
  const updateWorkflow = useMutation(
    (data: UpdateWorkflowMutationInput) =>
      karrio.graphql.request<UpdateWorkflow>(gqlstr(UPDATE_WORKFLOW), { data }),
    { onSuccess: invalidateCache, onError },
  );
  const deleteWorkflow = useMutation(
    (data: { id: string }) =>
      karrio.graphql.request<DeleteMutationInput>(gqlstr(DELETE_WORKFLOW), {
        data,
      }),
    { onSuccess: invalidateCache, onError },
  );
  const createWorkflowTrigger = useMutation(
    (data: CreateWorkflowTriggerMutationInput) =>
      karrio.graphql.request<CreateWorkflowTrigger>(
        gqlstr(CREATE_WORKFLOW_TRIGGER),
        { data },
      ),
    { onSuccess: invalidateCache, onError },
  );
  const updateWorkflowTrigger = useMutation(
    (data: UpdateWorkflowTriggerMutationInput) =>
      karrio.graphql.request<UpdateWorkflowTrigger>(
        gqlstr(UPDATE_WORKFLOW_TRIGGER),
        { data },
      ),
    { onSuccess: invalidateCache, onError },
  );
  const deleteWorkflowTrigger = useMutation(
    (data: { id: string }) =>
      karrio.graphql.request<DeleteMutationInput>(
        gqlstr(DELETE_WORKFLOW_TRIGGER),
        { data },
      ),
    { onSuccess: invalidateCache, onError },
  );
  const triggerScheduledWorkflow = useMutation(
    (trigger_id: string) =>
      karrio.graphql.request(gqlstr(TRIGGER_SCHEDULED_WORKFLOW), { trigger_id }),
    { onSuccess: invalidateCache, onError },
  );
  const validateCronExpression = useMutation(
    (input: { expression: string }) =>
      karrio.graphql.request(gqlstr(VALIDATE_CRON_EXPRESSION), { input }),
    { onError },
  );

  return {
    createWorkflow,
    updateWorkflow,
    deleteWorkflow,
    createWorkflowTrigger,
    updateWorkflowTrigger,
    deleteWorkflowTrigger,
    triggerScheduledWorkflow,
    validateCronExpression,
  };
}

type WorkflowDataType = (
  | CreateWorkflowMutationInput
  | UpdateWorkflowMutationInput
) & {
  id?: string;
  action_nodes: { order: number; slug?: string; index?: number }[];
  trigger: PartialWorkflowTriggerMutationInput & { id?: string };
  actions: (PartialWorkflowActionMutationInput & { id?: string })[];
};

const DEFAULT_STATE = {
  name: "",
  description: "",
  trigger: { trigger_type: AutomationTriggerType.manual },
  action_nodes: [{ order: 1, index: 0 }],
  actions: [
    {
      name: "",
      action_type: AutomationActionType.http_request,
      method: AutomationHTTPMethod.post,
      content_type: AutomationHTTPContentType.json,
      parameters_type: AutomationParametersType.data,
      parameters_template: `{
    "order_id": "{{ order_id }}",
}`,
      header_template: `{
    "Content-Type": "application/json",
}`,
    },
  ],
} as WorkflowDataType;
type ChangeType = {
  deleted?: boolean;
  created?: boolean;
  manuallyUpdated?: boolean;
  forcelocalUpdate?: boolean;
};

function reducer(
  state: Partial<WorkflowDataType>,
  { name, value }: { name: string; value: Partial<WorkflowDataType> },
): WorkflowDataType {
  switch (name) {
    case "full":
      return { ...(value as WorkflowDataType) };
    default:
      let newState = {
        ...state,
        ...(value as Partial<WorkflowDataType>),
      } as WorkflowDataType;
      Object.entries(value).forEach(([key, val]) => {
        if (val === undefined) delete newState[key as keyof WorkflowDataType];
      });
      return { ...state, ...(newState as WorkflowDataType) };
  }
}

export function useWorkflowForm({ id, templateSlug }: { id?: string; templateSlug?: string } = {}) {
  const loader = useLoader();
  const router = useRouter();
  const notifier = useNotifier();
  const { basePath } = useAppMode();
  const mutation = useWorkflowMutation();
  const eventMutation = useWorkflowEventMutation();
  const actionMutation = useWorkflowActionMutation();
  const connectionMutation = useWorkflowConnectionMutation();
  const [isNew, setIsNew] = React.useState<boolean>();
  const [debug_event, setDebugEvent] = React.useState<WorkflowEventType>();
  const [workflow, dispatch] = React.useReducer(
    reducer,
    DEFAULT_STATE,
    () => DEFAULT_STATE,
  );

  // Find template data (prioritize predefined templates)
  const selectedTemplate = React.useMemo(() => {
    if (!templateSlug) return null;

    // First check predefined templates
    const predefinedTemplate = PREDEFINED_WORKFLOW_TEMPLATES.find(t => t.slug === templateSlug);
    if (predefinedTemplate) return predefinedTemplate;

    // If not found in predefined, could extend to fetch from server
    return null;
  }, [templateSlug]);
  const {
    query: { data: { workflow: current } = {}, ...workflowQuery },
  } = useWorkflow({ id });
  const {
    query: { data: { workflow_events } = {}, ...eventsQuery },
    refetchInterval,
    setInterval,
  } = useWorkflowEvents({
    first: 1,
    ...(id !== "new" ? { keyword: id, parameters_key: ["debug"] } : {}),
  });

  // state checks
  const isLocalDraft = (id?: string) => isNoneOrEmpty(id) || id === "new";
  const zipActionWithNode = (
    actions: PartialWorkflowActionMutationInput[],
    action_nodes: ActionNodeInput[],
  ) => {
    const _tuple: [PartialWorkflowActionMutationInput, ActionNodeInput][] =
      Array.from(Array(actions.length).keys()).map((index) => {
        const action = actions[index];
        const node = action_nodes.find(
          (n) =>
            (!!n.slug && n.slug === action.slug) ||
            (!!n.index && n.index === index),
        ) || { order: index, slug: action.slug, index };

        return [action, node];
      });

    return _tuple.sort((a, b) => a[1].order - b[1].order);
  };

  // Queries
  const query = useQuery({
    queryKey: ["workflow-data", id],
    queryFn: () => (id === "new" ? { workflow } : current),
    enabled: !!id && (id === "new" || workflowQuery.isFetched),
  });

  // mutations
  const updateWorkflow = async (
    changes: Partial<WorkflowDataType>,
    change: ChangeType = { manuallyUpdated: false, forcelocalUpdate: false },
  ) => {
    const updateLocalState =
      change.forcelocalUpdate ||
      // always update local state if it is a new draft
      isLocalDraft(workflow.id) ||
      // only update local state first if it is not a draft and no new object is created or deleted.
      (!isLocalDraft(workflow.id) &&
        !change.created &&
        !change.deleted &&
        !change.manuallyUpdated);
    const uptateServerState = !isLocalDraft(workflow.id) && !!change.deleted;

    if (updateLocalState) {
      dispatch({ name: "partial", value: { ...workflow, ...changes } });
    }

    // if it is not a draft and hasn't been manually updated already
    if (uptateServerState) {
      try {
        let { ...data } = changes;
        if (Object.keys(data).length === 0) return; // abort if no data changes
        await mutation.updateWorkflow
          .mutateAsync({ id: workflow.id, ...data } as any)
          .then(({ update_workflow: { workflow } }) => {
            if (change.deleted && workflow) {
              dispatch({ name: "partial", value: changes });
            }
          });
      } catch (error: any) {
        notifier.notify({ type: NotificationType.error, message: error.data || error });
      }
    }
  };
  const addAction = async (data: PartialWorkflowActionMutationInput) => {
    const maxOrder = Math.max(...workflow.action_nodes.map((_) => _.order));
    const update = {
      actions: [...workflow.actions, data],
      action_nodes: [
        ...workflow.action_nodes,
        { order: maxOrder + 1, index: workflow.actions.length },
      ],
    };
    updateWorkflow(update as any);
  };
  const updateAction =
    (index: number, action_id?: string | null) =>
      async (data: PartialWorkflowActionMutationInput, change?: ChangeType) => {
        const update = {
          actions: workflow.actions.map(({ ...action }, idx) =>
            action.id === action_id || idx === index
              ? { ...action, ...data }
              : action,
          ),
        };
        updateWorkflow(update as any, change);
      };
  const deleteAction =
    (index: number, action_id?: string | null) => async () => {
      const action = workflow.actions.find((_, idx) => idx === index);
      const update = {
        actions: workflow.actions.filter((_, idx) => idx !== index),
        action_nodes: workflow.action_nodes.filter(
          (_, idx) =>
            _.index !== index && idx !== index && _.slug !== action?.slug,
        ),
      };

      if (!isLocalDraft(workflow.id) && !!action_id) {
        await actionMutation.deleteWorkflowAction.mutateAsync({
          id: action_id as string,
        });
      }

      updateWorkflow(update as any, { deleted: !!action_id });
    };
  const createActionConnection =
    (index: number, action_id?: string | null) =>
      async (
        data: PartialWorkflowConnectionMutationInput,
        change?: ChangeType,
      ) => {
        const action = workflow.actions.find(
          (_, idx) => idx === index || _.id === action_id,
        );
        updateAction(index, action_id)({ ...action, connection: data }, change);
      };
  const updateActionConnection =
    (index: number, action_id?: string | null) =>
      async (
        data: PartialWorkflowConnectionMutationInput,
        change?: ChangeType,
      ) => {
        const action = workflow.actions.find(
          (_, idx) => idx === index || _.id === action_id,
        );
        updateAction(index, action_id)(
          { ...action, connection: { ...(action?.connection || {}), ...data } },
          change,
        );
      };
  const deleteActionConnection =
    (index: number, action_id?: string | null, connection_id?: string | null) =>
      async () => {
        if (!isLocalDraft(workflow.id) && !!connection_id) {
          await connectionMutation.deleteWorkflowConnection.mutateAsync({
            id: connection_id as string,
          });
        }
        const action = workflow.actions.find(
          (_, idx) => idx === index || _.id === action_id,
        );
        updateAction(index, action_id)(
          { ...action, connection: null },
          { deleted: !!connection_id },
        );
      };

  // requests
  const save = async () => {
    const { id, ...data } = workflow;

    try {
      loader.setLoading(true);
      if (isLocalDraft(id)) {
        const {
          create_workflow: { workflow },
        } = await mutation.createWorkflow.mutateAsync(
          data as CreateWorkflowMutationInput,
        );
        notifier.notify({
          type: NotificationType.success,
          message: "Workflow saved!",
        });
        router.push(
          p`${basePath}/workflows/${workflow?.id}`.replace("//", "/"),
        );
      } else {
        await mutation.updateWorkflow.mutateAsync({
          id,
          ...data,
        } as UpdateWorkflowMutationInput);
        notifier.notify({
          type: NotificationType.success,
          message: "Workflow saved!",
        });
      }
    } catch (error: any) {
      notifier.notify({ type: NotificationType.error, message: error.data || error });
      loader.setLoading(false);
    }
  };
  const runWorkflow = async () => {
    try {
      if (!isEqual(workflow, current || DEFAULT_STATE)) {
        await save();
      }
      loader.setLoading(true);
      await eventMutation.createWorkflowEvent.mutateAsync({
        event_type: AutomationEventType.manual,
        workflow_id: workflow.id as string,
        parameters: { debug: true },
      });
      setInterval(4000);
    } catch (error: any) {
      notifier.notify({ type: NotificationType.error, message: error.data || error });
      loader.setLoading(false);
    }
  };

  React.useEffect(() => {
    setIsNew(id === "new");
  }, [id]);

  React.useEffect(() => {
    // Load template data when templateSlug is provided and it's a new workflow
    if (id === "new" && selectedTemplate) {
      const templateData = {
        name: selectedTemplate.name,
        description: selectedTemplate.description,
        // Remove slug from trigger as it's not accepted by the API mutation
        trigger: selectedTemplate.trigger ? {
          ...selectedTemplate.trigger,
          slug: undefined,
        } : undefined,
        // Remove id and slug from actions as they're not accepted by the API mutation
        actions: selectedTemplate.actions?.map((action: any, index: number) => ({
          ...action,
          id: undefined,
          slug: undefined,
        })) || [],
        action_nodes: selectedTemplate.actions?.map((_: any, index: number) => ({
          order: index + 1,
          index: index,
          slug: selectedTemplate.actions[index]?.slug,
        })) || [],
      };

      dispatch({ name: "full", value: templateData });
    }
  }, [id, selectedTemplate]);
  React.useEffect(() => {
    if (query.isFetched && id !== "new") {
      const _ordered = zipActionWithNode(
        current?.actions as any,
        current?.action_nodes as any,
      );
      dispatch({
        name: "full",
        value: {
          ...current,
          actions: _ordered.map((_) => _[0]),
          action_nodes: _ordered.map((_) => _[1]),
        } as any,
      });
    }
  }, [current, query.isFetched]);
  React.useEffect(() => {
    const event = workflow_events?.edges?.[0]?.node;
    const isRunning = [
      AutomationEventStatus.pending,
      AutomationEventStatus.running,
    ].includes(event?.status as any);
    if (isRunning && refetchInterval !== 4000) {
      setInterval(4000);
    }
    if (!isRunning && refetchInterval !== 120000) {
      setInterval(120000);
      eventsQuery.refetch();
    }
    setDebugEvent(event);
  }, [workflow_events, workflow_events?.edges]);

  return {
    debug_event,
    isNew,
    query,
    current,
    workflow,
    DEFAULT_STATE,
    save,
    addAction,
    updateAction,
    deleteAction,
    runWorkflow,
    updateWorkflow,
    createActionConnection,
    updateActionConnection,
    deleteActionConnection,
    zipActionWithNode,
  };
}
