import {
  GET_TASK_EXECUTIONS,
  GET_WORKER_HEALTH,
  TRIGGER_TRACKER_UPDATE,
  RETRY_WEBHOOK,
  REVOKE_TASK,
  CLEANUP_TASK_EXECUTIONS,
  RESET_STUCK_TASKS,
  TRIGGER_DATA_ARCHIVING,
  GetTaskExecutions,
  GetWorkerHealth,
  TriggerTrackerUpdate,
  RetryWebhook,
  RevokeTask,
  CleanupTaskExecutions,
  ResetStuckTasks,
  TriggerDataArchiving,
  TaskExecutionFilter,
} from "@karrio/types/graphql/admin";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import { useQueryClient } from "@tanstack/react-query";

export function useWorkerHealth() {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ["admin_worker_health"],
    queryFn: () =>
      karrio.admin.request<GetWorkerHealth>(gqlstr(GET_WORKER_HEALTH)),
    staleTime: 10000,
    onError,
  });

  return {
    query,
    health: query.data?.worker_health,
  };
}

export function useTaskExecutions(filter?: TaskExecutionFilter) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ["admin_task_executions", filter],
    queryFn: () =>
      karrio.admin.request<GetTaskExecutions>(gqlstr(GET_TASK_EXECUTIONS), {
        variables: { filter },
      }),
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  return {
    query,
    executions: query.data?.task_executions,
  };
}

export function useWorkerActions() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();

  const invalidateWorkerData = () => {
    queryClient.invalidateQueries({ queryKey: ["admin_task_executions"] });
    queryClient.invalidateQueries({ queryKey: ["admin_worker_health"] });
  };

  const triggerTrackerUpdate = useAuthenticatedMutation({
    mutationFn: (input: { tracker_ids?: string[] }) =>
      karrio.admin.request<TriggerTrackerUpdate>(
        gqlstr(TRIGGER_TRACKER_UPDATE),
        { variables: { input } },
      ),
    onSuccess: invalidateWorkerData,
  });

  const retryWebhook = useAuthenticatedMutation({
    mutationFn: (input: { event_id: string }) =>
      karrio.admin.request<RetryWebhook>(
        gqlstr(RETRY_WEBHOOK),
        { variables: { input } },
      ),
    onSuccess: invalidateWorkerData,
  });

  const revokeTask = useAuthenticatedMutation({
    mutationFn: (input: { task_id: string }) =>
      karrio.admin.request<RevokeTask>(
        gqlstr(REVOKE_TASK),
        { variables: { input } },
      ),
    onSuccess: invalidateWorkerData,
  });

  const cleanupTaskExecutions = useAuthenticatedMutation({
    mutationFn: (input: { retention_days?: number; statuses?: string[] }) =>
      karrio.admin.request<CleanupTaskExecutions>(
        gqlstr(CLEANUP_TASK_EXECUTIONS),
        { variables: { input } },
      ),
    onSuccess: invalidateWorkerData,
  });

  const resetStuckTasks = useAuthenticatedMutation({
    mutationFn: (input: { threshold_minutes?: number; statuses?: string[] }) =>
      karrio.admin.request<ResetStuckTasks>(
        gqlstr(RESET_STUCK_TASKS),
        { variables: { input } },
      ),
    onSuccess: invalidateWorkerData,
  });

  const triggerDataArchiving = useAuthenticatedMutation({
    mutationFn: () =>
      karrio.admin.request<TriggerDataArchiving>(
        gqlstr(TRIGGER_DATA_ARCHIVING),
      ),
    onSuccess: invalidateWorkerData,
  });

  return {
    triggerTrackerUpdate,
    retryWebhook,
    revokeTask,
    cleanupTaskExecutions,
    resetStuckTasks,
    triggerDataArchiving,
  };
}
