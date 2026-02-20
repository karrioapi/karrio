"use client";

import React from "react";
import {
  Server,
  Database,
  HardDrive,
  MemoryStick,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Cpu,
  ChevronDown,
  ChevronRight,
  Clock,
  Timer,
  RotateCcw,
} from "lucide-react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { cn } from "@karrio/ui/lib/utils";
import { url$ } from "@karrio/lib";
import { useWorkerHealth, useTaskExecutions, useWorkerActions } from "@karrio/hooks/admin-worker";

type HealthCheckStatus = Record<string, string>;

function useSystemHealth() {
  const { references } = useAPIMetadata();
  const [data, setData] = React.useState<HealthCheckStatus | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const fetchHealth = React.useCallback(async () => {
    if (!references?.HOST) return;
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch(url$`${references.HOST}/status/?format=json`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      setData(json);
    } catch (err: any) {
      setError(err.message || "Failed to fetch health status");
    } finally {
      setIsLoading(false);
    }
  }, [references?.HOST]);

  React.useEffect(() => {
    fetchHealth();
  }, [fetchHealth]);

  return { data, isLoading, error, refetch: fetchHealth };
}

// Map service names to icons
function getServiceIcon(name: string) {
  const lower = name.toLowerCase();
  if (lower.includes("database")) return <Database className="h-4 w-4 text-blue-400" />;
  if (lower.includes("cache")) return <Database className="h-4 w-4 text-purple-400" />;
  if (lower.includes("disk")) return <HardDrive className="h-4 w-4 text-yellow-400" />;
  if (lower.includes("memory")) return <MemoryStick className="h-4 w-4 text-green-400" />;
  return <Server className="h-4 w-4 text-muted-foreground" />;
}

// Simplify service display name
function formatServiceName(name: string) {
  if (name.toLowerCase().includes("database")) return "Database";
  if (name.toLowerCase().includes("cache")) return "Cache";
  if (name.toLowerCase().includes("disk")) return "Disk";
  if (name.toLowerCase().includes("memory")) return "Memory";
  return name;
}

export function SystemHealthView() {
  const { health, query: healthQuery } = useWorkerHealth();
  const { executions, query: executionsQuery } = useTaskExecutions({
    first: 1000,
  });
  const systemHealth = useSystemHealth();
  const {
    triggerTrackerUpdate,
    triggerDataArchiving,
    resetStuckTasks,
    cleanupTaskExecutions,
  } = useWorkerActions();

  const handleRefresh = () => {
    healthQuery.refetch();
    executionsQuery.refetch();
    systemHealth.refetch();
  };

  // Compute task stats from executions
  const stats = React.useMemo(() => {
    const edges = executions?.edges || [];
    const total = edges.length;
    const complete = edges.filter(
      ({ node }: any) => node.status === "complete",
    ).length;
    const errors = edges.filter(
      ({ node }: any) => node.status === "error",
    ).length;
    const executing = edges.filter(
      ({ node }: any) => node.status === "executing",
    ).length;
    const avgDuration =
      edges
        .filter(({ node }: any) => node.duration_ms)
        .reduce((sum: number, { node }: any) => sum + node.duration_ms, 0) /
        (edges.filter(({ node }: any) => node.duration_ms).length || 1) || 0;

    return { total, complete, errors, executing, avgDuration: Math.round(avgDuration) };
  }, [executions]);

  const isLoading = healthQuery.isLoading || executionsQuery.isLoading;

  // Determine overall system health status
  const allServicesOk = systemHealth.data
    ? Object.values(systemHealth.data).every((v) => v === "OK" || v === "working")
    : false;

  return (
    <div className="flex flex-col h-full p-4 pb-8 space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Server className="h-5 w-5 text-primary" />
          <h2 className="text-lg font-semibold text-foreground">
            Health
          </h2>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleRefresh}
          className="h-7 px-2 text-muted-foreground hover:text-foreground"
        >
          <RefreshCw
            className={cn(
              "h-3.5 w-3.5",
              (healthQuery.isFetching || executionsQuery.isFetching || systemHealth.isLoading) &&
                "animate-spin",
            )}
          />
        </Button>
      </div>

      {/* System Status (Django Health Check) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-muted-foreground">
            System Status
          </h3>
          {!systemHealth.isLoading && !systemHealth.error && (
            <Badge
              className={cn(
                "text-xs border-none",
                allServicesOk
                  ? "bg-green-500/20 text-green-400"
                  : "bg-red-500/20 text-red-400",
              )}
            >
              {allServicesOk ? "All systems operational" : "Issues detected"}
            </Badge>
          )}
        </div>

        {systemHealth.isLoading && (
          <div className="flex items-center justify-center h-20 text-muted-foreground text-sm">
            <Loader2 className="h-4 w-4 animate-spin mr-2" /> Checking services...
          </div>
        )}

        {systemHealth.error && (
          <div className="bg-red-900/20 border border-red-900/40 rounded-lg p-3 text-sm text-red-300">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4 text-red-400 flex-shrink-0" />
              Unable to reach health endpoint: {systemHealth.error}
            </div>
          </div>
        )}

        {systemHealth.data && (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {Object.entries(systemHealth.data).map(([service, status]) => (
              <div
                key={service}
                className="bg-card border border-border rounded-lg p-3"
              >
                <div className="flex items-center gap-2 mb-2">
                  {getServiceIcon(service)}
                  <span className="text-xs text-muted-foreground">
                    {formatServiceName(service)}
                  </span>
                </div>
                <div className="flex items-center gap-1.5">
                  {status === "OK" || status === "working" ? (
                    <CheckCircle2 className="h-4 w-4 text-green-400" />
                  ) : (
                    <AlertCircle className="h-4 w-4 text-red-400" />
                  )}
                  <span
                    className={cn(
                      "text-sm font-semibold",
                      status === "OK" || status === "working"
                        ? "text-green-400"
                        : "text-red-400",
                    )}
                  >
                    {status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-32 text-muted-foreground text-sm">
          <Loader2 className="h-4 w-4 animate-spin mr-2" /> Loading worker
          health...
        </div>
      ) : (
        <>
          {/* Worker Status */}
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-muted-foreground">
              Worker Status
            </h3>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
              <StatusCard
                label="Worker"
                value={health?.is_available ? "Online" : "Offline"}
                icon={
                  health?.is_available ? (
                    <CheckCircle2 className="h-4 w-4 text-green-400" />
                  ) : (
                    <AlertCircle className="h-4 w-4 text-red-400" />
                  )
                }
                variant={health?.is_available ? "success" : "error"}
              />
              <StatusCard
                label="Pending Tasks"
                value={String(health?.queue?.pending_count ?? 0)}
                icon={<Database className="h-4 w-4 text-blue-400" />}
              />
              <StatusCard
                label="Scheduled"
                value={String(health?.queue?.scheduled_count ?? 0)}
                icon={<Cpu className="h-4 w-4 text-purple-400" />}
              />
              <StatusCard
                label="Results"
                value={String(health?.queue?.result_count ?? 0)}
                icon={<Database className="h-4 w-4 text-muted-foreground" />}
              />
            </div>
          </div>

          {/* Task Statistics */}
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-muted-foreground">
              Task Statistics (Recent)
            </h3>
            <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
              <StatCard label="Total Recorded" value={stats.total} />
              <StatCard
                label="Completed"
                value={stats.complete}
                variant="success"
              />
              <StatCard label="Errors" value={stats.errors} variant="error" />
              <StatCard
                label="Executing"
                value={stats.executing}
                variant="info"
              />
              <StatCard
                label="Avg Duration"
                value={`${stats.avgDuration}ms`}
              />
            </div>
          </div>

          {/* Error Rate */}
          {stats.total > 0 && (
            <div className="space-y-3">
              <h3 className="text-sm font-medium text-muted-foreground">
                Error Rate
              </h3>
              <div className="bg-card border border-border rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-muted-foreground">
                    Success Rate
                  </span>
                  <span className="text-sm font-medium text-foreground">
                    {((stats.complete / stats.total) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full transition-all"
                    style={{
                      width: `${(stats.complete / stats.total) * 100}%`,
                    }}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Task Name Breakdown */}
          <TaskNameBreakdown executions={executions} />

          {/* Maintenance Actions */}
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-muted-foreground">
              Maintenance Actions
            </h3>
            <div className="bg-card border border-border rounded-lg p-4">
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  className="h-9 text-xs border-border text-foreground hover:bg-primary/10"
                  disabled={triggerTrackerUpdate.isLoading}
                  onClick={() => triggerTrackerUpdate.mutate({})}
                >
                  {triggerTrackerUpdate.isLoading ? (
                    <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                  ) : (
                    <RefreshCw className="h-3.5 w-3.5 mr-1.5" />
                  )}
                  Run Tracker Update
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="h-9 text-xs border-border text-foreground hover:bg-primary/10"
                  disabled={triggerDataArchiving.isLoading}
                  onClick={() => triggerDataArchiving.mutate()}
                >
                  {triggerDataArchiving.isLoading ? (
                    <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                  ) : (
                    <Database className="h-3.5 w-3.5 mr-1.5" />
                  )}
                  Run Data Archiving
                </Button>
                {stats.executing > 0 && (
                  <Button
                    variant="outline"
                    size="sm"
                    className="h-9 text-xs border-border text-yellow-400 hover:bg-yellow-500/10"
                    disabled={resetStuckTasks.isLoading}
                    onClick={() => resetStuckTasks.mutate({})}
                  >
                    {resetStuckTasks.isLoading ? (
                      <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                    ) : (
                      <AlertCircle className="h-3.5 w-3.5 mr-1.5" />
                    )}
                    Reset Stuck Tasks
                  </Button>
                )}
                <Button
                  variant="outline"
                  size="sm"
                  className="h-9 text-xs border-border text-foreground hover:bg-primary/10"
                  disabled={cleanupTaskExecutions.isLoading}
                  onClick={() => cleanupTaskExecutions.mutate({})}
                >
                  {cleanupTaskExecutions.isLoading ? (
                    <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                  ) : (
                    <HardDrive className="h-3.5 w-3.5 mr-1.5" />
                  )}
                  Cleanup Old Records
                </Button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function StatusCard({
  label,
  value,
  icon,
  variant,
}: {
  label: string;
  value: string;
  icon: React.ReactNode;
  variant?: "success" | "error" | "info";
}) {
  return (
    <div className="bg-card border border-border rounded-lg p-3">
      <div className="flex items-center gap-2 mb-1">
        {icon}
        <span className="text-xs text-muted-foreground">{label}</span>
      </div>
      <div
        className={cn(
          "text-lg font-semibold",
          variant === "success" && "text-green-400",
          variant === "error" && "text-red-400",
          variant === "info" && "text-blue-400",
          !variant && "text-foreground",
        )}
      >
        {value}
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  variant,
}: {
  label: string;
  value: number | string;
  variant?: "success" | "error" | "info";
}) {
  return (
    <div className="bg-card border border-border rounded-lg p-3 text-center">
      <div
        className={cn(
          "text-xl font-bold",
          variant === "success" && "text-green-400",
          variant === "error" && "text-red-400",
          variant === "info" && "text-blue-400",
          !variant && "text-foreground",
        )}
      >
        {value}
      </div>
      <div className="text-xs text-muted-foreground mt-1">{label}</div>
    </div>
  );
}

const STATUS_CONFIG: Record<string, { color: string; bg: string }> = {
  complete: { color: "text-green-400", bg: "bg-green-500/20" },
  error: { color: "text-red-400", bg: "bg-red-500/20" },
  executing: { color: "text-blue-400", bg: "bg-blue-500/20" },
  queued: { color: "text-yellow-400", bg: "bg-yellow-500/20" },
  retrying: { color: "text-orange-400", bg: "bg-orange-500/20" },
  revoked: { color: "text-muted-foreground", bg: "bg-muted/50" },
  expired: { color: "text-muted-foreground", bg: "bg-muted/50" },
};

function formatDuration(ms: number | null) {
  if (ms == null) return "-";
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${(ms / 60000).toFixed(1)}m`;
}

function formatTimestamp(ts: string | null) {
  if (!ts) return "-";
  const date = new Date(ts);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  let relative: string;
  if (diffMins < 1) relative = "just now";
  else if (diffMins < 60) relative = `${diffMins}m ago`;
  else if (diffHours < 24) relative = `${diffHours}h ago`;
  else relative = `${diffDays}d ago`;

  return relative;
}

function formatTimestampFull(ts: string | null) {
  if (!ts) return "";
  return new Date(ts).toLocaleString();
}

function TaskNameBreakdown({ executions }: { executions: any }) {
  const [expandedTask, setExpandedTask] = React.useState<string | null>(null);
  const [statusFilter, setStatusFilter] = React.useState<string | null>(null);

  const { breakdown, taskExecutions } = React.useMemo(() => {
    const edges = executions?.edges || [];
    const map = new Map<
      string,
      {
        total: number;
        complete: number;
        error: number;
        executing: number;
        queued: number;
        avgDuration: number;
        lastRun: string | null;
      }
    >();
    const byTask = new Map<string, any[]>();

    edges.forEach(({ node }: any) => {
      const entry = map.get(node.task_name) || {
        total: 0,
        complete: 0,
        error: 0,
        executing: 0,
        queued: 0,
        avgDuration: 0,
        lastRun: null,
      };
      entry.total++;
      if (node.status === "complete") entry.complete++;
      if (node.status === "error") entry.error++;
      if (node.status === "executing") entry.executing++;
      if (node.status === "queued") entry.queued++;

      const runTime = node.completed_at || node.started_at || node.queued_at;
      if (runTime && (!entry.lastRun || runTime > entry.lastRun)) {
        entry.lastRun = runTime;
      }

      map.set(node.task_name, entry);

      const list = byTask.get(node.task_name) || [];
      list.push(node);
      byTask.set(node.task_name, list);
    });

    // Compute avg durations
    map.forEach((entry, name) => {
      const tasks = byTask.get(name) || [];
      const withDuration = tasks.filter((t) => t.duration_ms != null);
      entry.avgDuration = withDuration.length
        ? Math.round(
            withDuration.reduce((s, t) => s + t.duration_ms, 0) /
              withDuration.length,
          )
        : 0;
    });

    return {
      breakdown: Array.from(map.entries())
        .sort((a, b) => b[1].total - a[1].total)
        .slice(0, 15),
      taskExecutions: byTask,
    };
  }, [executions]);

  if (breakdown.length === 0) return null;

  const filteredBreakdown = statusFilter
    ? breakdown.filter(([, stats]) => {
        if (statusFilter === "error") return stats.error > 0;
        if (statusFilter === "executing") return stats.executing > 0;
        if (statusFilter === "complete") return stats.complete > 0;
        return true;
      })
    : breakdown;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-muted-foreground">
          Task Breakdown
        </h3>
        <div className="flex items-center gap-1.5">
          {["all", "complete", "error", "executing"].map((filter) => (
            <button
              key={filter}
              onClick={() =>
                setStatusFilter(filter === "all" ? null : filter)
              }
              className={cn(
                "px-2 py-0.5 text-xs rounded-md transition-colors",
                (filter === "all" && !statusFilter) ||
                  statusFilter === filter
                  ? "bg-primary/20 text-primary"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted/50",
              )}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>
      <div className="bg-card border border-border rounded-lg divide-y divide-border">
        {filteredBreakdown.map(([name, stats]) => {
          const isExpanded = expandedTask === name;
          const tasks = taskExecutions.get(name) || [];
          const filteredTasks = statusFilter
            ? tasks.filter((t) => t.status === statusFilter)
            : tasks;

          return (
            <div key={name}>
              <button
                onClick={() =>
                  setExpandedTask(isExpanded ? null : name)
                }
                className="flex items-center justify-between w-full px-4 py-2.5 text-left hover:bg-muted/30 transition-colors"
              >
                <div className="flex items-center gap-2 min-w-0">
                  {isExpanded ? (
                    <ChevronDown className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                  ) : (
                    <ChevronRight className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                  )}
                  <span className="text-sm text-foreground truncate">
                    {name}
                  </span>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0 ml-3">
                  {stats.lastRun && (
                    <span
                      className="text-xs text-muted-foreground"
                      title={formatTimestampFull(stats.lastRun)}
                    >
                      {formatTimestamp(stats.lastRun)}
                    </span>
                  )}
                  {stats.avgDuration > 0 && (
                    <Badge className="bg-muted/50 text-muted-foreground border-none text-xs">
                      ~{formatDuration(stats.avgDuration)}
                    </Badge>
                  )}
                  <Badge className="bg-muted/50 text-muted-foreground border-none text-xs">
                    {stats.total}
                  </Badge>
                  {stats.complete > 0 && (
                    <Badge className="bg-green-500/20 text-green-400 border-none text-xs">
                      {stats.complete}
                    </Badge>
                  )}
                  {stats.error > 0 && (
                    <Badge className="bg-red-500/20 text-red-400 border-none text-xs">
                      {stats.error}
                    </Badge>
                  )}
                  {stats.executing > 0 && (
                    <Badge className="bg-blue-500/20 text-blue-400 border-none text-xs">
                      {stats.executing}
                    </Badge>
                  )}
                </div>
              </button>
              {isExpanded && (
                <div className="border-t border-border/50">
                  <div className="grid grid-cols-[1fr_80px_90px_90px_70px_60px] gap-2 px-4 py-1.5 text-xs text-muted-foreground border-b border-border/30 bg-muted/20">
                    <span>Task ID</span>
                    <span>Status</span>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" /> Queued
                    </span>
                    <span className="flex items-center gap-1">
                      <Timer className="h-3 w-3" /> Duration
                    </span>
                    <span className="flex items-center gap-1">
                      <RotateCcw className="h-3 w-3" /> Retries
                    </span>
                    <span></span>
                  </div>
                  <div className="max-h-[300px] overflow-y-auto">
                    {filteredTasks
                      .sort(
                        (a: any, b: any) =>
                          new Date(b.queued_at || 0).getTime() -
                          new Date(a.queued_at || 0).getTime(),
                      )
                      .slice(0, 50)
                      .map((task: any) => (
                        <TaskExecutionRow key={task.id} task={task} />
                      ))}
                    {filteredTasks.length > 50 && (
                      <div className="px-4 py-2 text-xs text-muted-foreground text-center">
                        Showing 50 of {filteredTasks.length} executions
                      </div>
                    )}
                    {filteredTasks.length === 0 && (
                      <div className="px-4 py-3 text-xs text-muted-foreground text-center">
                        No executions match the current filter
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function TaskExecutionRow({ task }: { task: any }) {
  const [showError, setShowError] = React.useState(false);
  const statusCfg = STATUS_CONFIG[task.status] || STATUS_CONFIG.queued;

  return (
    <>
      <div className="grid grid-cols-[1fr_80px_90px_90px_70px_60px] gap-2 px-4 py-1.5 text-xs hover:bg-muted/20 transition-colors items-center">
        <span
          className="text-muted-foreground truncate font-mono"
          title={task.task_id}
        >
          {task.task_id?.slice(0, 12)}...
        </span>
        <Badge
          className={cn(
            statusCfg.bg,
            statusCfg.color,
            "border-none text-xs px-1.5 py-0 h-5 justify-center",
          )}
        >
          {task.status}
        </Badge>
        <span
          className="text-muted-foreground"
          title={formatTimestampFull(task.queued_at)}
        >
          {formatTimestamp(task.queued_at)}
        </span>
        <span className="text-foreground">
          {formatDuration(task.duration_ms)}
        </span>
        <span className="text-muted-foreground">
          {task.retries > 0 ? task.retries : "-"}
        </span>
        <div>
          {task.error && (
            <button
              onClick={() => setShowError(!showError)}
              className="text-red-400 hover:text-red-300 text-xs underline"
            >
              {showError ? "hide" : "error"}
            </button>
          )}
        </div>
      </div>
      {showError && task.error && (
        <div className="mx-4 mb-2 p-2 bg-red-900/20 border border-red-900/40 rounded text-xs text-red-300 font-mono whitespace-pre-wrap break-all max-h-[120px] overflow-y-auto">
          {task.error}
        </div>
      )}
    </>
  );
}
