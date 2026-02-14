"use client";

import React from "react";
import {
  Server,
  Database,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Cpu,
} from "lucide-react";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { cn } from "@karrio/ui/lib/utils";
import { useWorkerHealth, useTaskExecutions } from "@karrio/hooks/admin-worker";

export function SystemHealthView() {
  const { health, query: healthQuery } = useWorkerHealth();
  const { executions, query: executionsQuery } = useTaskExecutions({
    first: 100,
  });

  const handleRefresh = () => {
    healthQuery.refetch();
    executionsQuery.refetch();
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

  return (
    <div className="flex flex-col h-full p-4 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Server className="h-5 w-5 text-primary" />
          <h2 className="text-lg font-semibold text-foreground">
            System Health
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
              (healthQuery.isFetching || executionsQuery.isFetching) &&
                "animate-spin",
            )}
          />
        </Button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-32 text-muted-foreground text-sm">
          <Loader2 className="h-4 w-4 animate-spin mr-2" /> Loading system
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

function TaskNameBreakdown({ executions }: { executions: any }) {
  const breakdown = React.useMemo(() => {
    const edges = executions?.edges || [];
    const map = new Map<
      string,
      { total: number; complete: number; error: number }
    >();
    edges.forEach(({ node }: any) => {
      const entry = map.get(node.task_name) || {
        total: 0,
        complete: 0,
        error: 0,
      };
      entry.total++;
      if (node.status === "complete") entry.complete++;
      if (node.status === "error") entry.error++;
      map.set(node.task_name, entry);
    });
    return Array.from(map.entries())
      .sort((a, b) => b[1].total - a[1].total)
      .slice(0, 10);
  }, [executions]);

  if (breakdown.length === 0) return null;

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium text-muted-foreground">
        Task Breakdown
      </h3>
      <div className="bg-card border border-border rounded-lg divide-y divide-border">
        {breakdown.map(([name, stats]) => (
          <div
            key={name}
            className="flex items-center justify-between px-4 py-2.5"
          >
            <span className="text-sm text-foreground truncate max-w-[200px]">
              {name}
            </span>
            <div className="flex items-center gap-3">
              <Badge className="bg-muted/50 text-muted-foreground border-none text-xs">
                {stats.total} total
              </Badge>
              {stats.complete > 0 && (
                <Badge className="bg-green-500/20 text-green-400 border-none text-xs">
                  {stats.complete} ok
                </Badge>
              )}
              {stats.error > 0 && (
                <Badge className="bg-red-500/20 text-red-400 border-none text-xs">
                  {stats.error} err
                </Badge>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
