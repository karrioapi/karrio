import {
  GET_TASK_EXECUTIONS,
  GET_WORKER_HEALTH,
  GetTaskExecutions,
  GetWorkerHealth,
  TaskExecutionFilter,
} from "@karrio/types/graphql/admin";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio, useAuthenticatedQuery } from "./karrio";

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
