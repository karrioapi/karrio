"use client";

import React, { useState } from "react";
import { Clock, Filter, RefreshCw, Copy, Check, AlertCircle, CheckCircle2, Loader2, RotateCw } from "lucide-react";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { formatDateTimeLong, failsafe, jsonify } from "@karrio/lib";
import { cn } from "@karrio/ui/lib/utils";
import CodeMirror from "@uiw/react-codemirror";
import { json } from "@codemirror/lang-json";
import { useWorkerHealth, useTaskExecutions } from "@karrio/hooks/admin-worker";

// Convert Python repr strings (single quotes, tuples, None, True/False) to valid JSON
function pythonToJson(value: string): string {
  try {
    // First try direct JSON parse
    return JSON.stringify(JSON.parse(value), null, 2);
  } catch {
    // Convert Python syntax to JSON-compatible syntax
    let converted = value
      .replace(/'/g, '"')           // single quotes → double quotes
      .replace(/\bNone\b/g, 'null')
      .replace(/\bTrue\b/g, 'true')
      .replace(/\bFalse\b/g, 'false');

    // Handle Python tuples: (a, b) → [a, b]
    converted = converted.replace(/^\(/, '[').replace(/\)$/, ']');

    try {
      return JSON.stringify(JSON.parse(converted), null, 2);
    } catch {
      return value;
    }
  }
}

const getStatusColor = (status: string | null) => {
  switch (status) {
    case "complete": return "bg-green-500/20 text-green-400";
    case "error": return "bg-red-500/20 text-red-400";
    case "executing": return "bg-blue-500/20 text-blue-400";
    case "retrying": return "bg-yellow-500/20 text-yellow-400";
    case "revoked": return "bg-gray-500/20 text-gray-400";
    case "expired": return "bg-orange-500/20 text-orange-400";
    case "queued": return "bg-purple-500/20 text-purple-400";
    default: return "bg-gray-500/20 text-gray-400";
  }
};

const getStatusIcon = (status: string | null) => {
  switch (status) {
    case "complete": return <CheckCircle2 className="h-3 w-3" />;
    case "error": return <AlertCircle className="h-3 w-3" />;
    case "executing": return <Loader2 className="h-3 w-3 animate-spin" />;
    case "retrying": return <RotateCw className="h-3 w-3" />;
    default: return <Clock className="h-3 w-3" />;
  }
};

const TaskExecutionListItem = ({
  execution,
  isSelected,
  onClick,
}: {
  execution: any;
  isSelected: boolean;
  onClick: () => void;
}) => {
  return (
    <div
      className={cn(
        "p-3 border-b border-border cursor-pointer transition-colors",
        isSelected
          ? "bg-primary/10 border-l-2 border-l-primary"
          : "hover:bg-muted/30"
      )}
      onClick={onClick}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <Badge className={`${getStatusColor(execution.status)} border-none text-xs`}>
              {getStatusIcon(execution.status)}
              <span className="ml-1">{execution.status}</span>
            </Badge>
            {execution.duration_ms && (
              <span className="text-xs text-muted-foreground">{execution.duration_ms}ms</span>
            )}
          </div>
          <div className="text-xs font-medium text-foreground truncate">
            {execution.task_name}
          </div>
          <div className="text-xs text-neutral-400 truncate mt-0.5">
            ID: {execution.task_id}
          </div>
        </div>
        <div className="text-[10px] text-neutral-500 whitespace-nowrap flex-shrink-0 pt-0.5">
          {failsafe(() => formatDateTimeLong(execution.started_at || execution.queued_at))}
        </div>
      </div>
    </div>
  );
};

const TaskExecutionDetailViewer = ({ execution }: { execution: any | null }) => {
  const [copiedFull, setCopiedFull] = useState(false);

  const copyFullExecution = () => {
    const full = JSON.stringify(execution, null, 2);
    navigator.clipboard.writeText(full);
    setCopiedFull(true);
    setTimeout(() => setCopiedFull(false), 2000);
  };

  if (!execution) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
        Select a task execution to view details
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="border-b border-border px-4 py-3 flex-shrink-0">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Badge className={`${getStatusColor(execution.status)} border-none`}>
              {getStatusIcon(execution.status)}
              <span className="ml-1">{execution.status}</span>
            </Badge>
            {execution.duration_ms && (
              <Badge className="bg-muted/50 text-muted-foreground border-none text-xs">
                {execution.duration_ms}ms
              </Badge>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={copyFullExecution}
              className="h-7 px-2 border-border text-muted-foreground hover:bg-primary/20"
              title="Copy full execution as JSON">
              {copiedFull ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
              <span className="ml-1 text-xs">{copiedFull ? "Copied" : "Copy"}</span>
            </Button>
          </div>
        </div>
        <div className="text-xs text-muted-foreground space-y-1">
          <div className="text-sm font-medium text-foreground">{execution.task_name}</div>
          <div>Task ID: {execution.task_id}</div>
          {execution.queued_at && <div>Queued: {formatDateTimeLong(execution.queued_at)}</div>}
          {execution.started_at && <div>Started: {formatDateTimeLong(execution.started_at)}</div>}
          {execution.completed_at && <div>Completed: {formatDateTimeLong(execution.completed_at)}</div>}
          {execution.retries > 0 && <div>Retries: {execution.retries}</div>}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {execution.error && (
          <div>
            <div className="text-xs font-medium text-red-400 mb-2">Error</div>
            <CodeMirror
              value={execution.error}
              theme="dark"
              readOnly
              basicSetup={{ lineNumbers: true, foldGutter: false }}
              className="text-xs border border-border rounded overflow-hidden [&_.cm-editor]:!bg-card [&_.cm-gutters]:!bg-card"
              maxHeight="300px"
            />
          </div>
        )}
        {execution.args_summary && (
          <div>
            <div className="text-xs font-medium text-muted-foreground mb-2">Arguments</div>
            <CodeMirror
              value={pythonToJson(execution.args_summary)}
              theme="dark"
              extensions={[json()]}
              readOnly
              basicSetup={{ lineNumbers: true, foldGutter: false }}
              className="text-xs border border-border rounded overflow-hidden [&_.cm-editor]:!bg-card [&_.cm-gutters]:!bg-card"
              maxHeight="300px"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export function WorkersView() {
  const [selectedExecution, setSelectedExecution] = useState<any | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [taskNameFilter, setTaskNameFilter] = useState<string>("all");

  const { health, query: healthQuery } = useWorkerHealth();
  const { executions, query: executionsQuery } = useTaskExecutions({
    ...(statusFilter !== "all" ? { status: statusFilter } : {}),
    ...(taskNameFilter !== "all" ? { task_name: taskNameFilter } : {}),
    first: 50,
  });

  const edges = executions?.edges || [];
  const taskNames = React.useMemo(() => {
    const names = new Set<string>();
    edges.forEach(({ node }: any) => names.add(node.task_name));
    return Array.from(names).sort();
  }, [edges]);

  const handleRefresh = () => {
    healthQuery.refetch();
    executionsQuery.refetch();
  };

  return (
    <div className="flex flex-col h-full">
      {/* Queue Overview */}
      {health && (
        <div className="border-b border-border px-4 py-2 flex items-center gap-4 text-xs flex-shrink-0">
          <span className="text-muted-foreground">Queue:</span>
          <span className="text-foreground">{health.queue?.pending_count ?? 0} pending</span>
          <span className="text-foreground">{health.queue?.scheduled_count ?? 0} scheduled</span>
          <span className="text-foreground">{health.queue?.result_count ?? 0} results</span>
        </div>
      )}

      {/* Toolbar */}
      <div className="border-b border-border px-4 py-2 flex items-center gap-2 flex-shrink-0">
        <Filter className="h-3.5 w-3.5 text-muted-foreground" />
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="h-7 w-[120px] text-xs bg-card border-border">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent className="dark">
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="complete">Complete</SelectItem>
            <SelectItem value="error">Error</SelectItem>
            <SelectItem value="executing">Executing</SelectItem>
            <SelectItem value="retrying">Retrying</SelectItem>
          </SelectContent>
        </Select>
        <Select value={taskNameFilter} onValueChange={setTaskNameFilter}>
          <SelectTrigger className="h-7 w-[160px] text-xs bg-card border-border">
            <SelectValue placeholder="Task" />
          </SelectTrigger>
          <SelectContent className="dark">
            <SelectItem value="all">All Tasks</SelectItem>
            {taskNames.map(name => (
              <SelectItem key={name} value={name}>{name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <div className="flex-1" />
        <Button variant="ghost" size="sm" onClick={handleRefresh} className="h-7 px-2 text-muted-foreground hover:text-foreground">
          <RefreshCw className={cn("h-3.5 w-3.5", (healthQuery.isFetching || executionsQuery.isFetching) && "animate-spin")} />
        </Button>
      </div>

      {/* Split Panel */}
      <div className="flex flex-1 min-h-0">
        {/* Left: List */}
        <div className="w-[380px] border-r border-border overflow-y-auto flex-shrink-0">
          {executionsQuery.isLoading ? (
            <div className="flex items-center justify-center h-32 text-muted-foreground text-sm">
              <Loader2 className="h-4 w-4 animate-spin mr-2" /> Loading...
            </div>
          ) : edges.length === 0 ? (
            <div className="flex items-center justify-center h-32 text-muted-foreground text-sm">
              No task executions found
            </div>
          ) : (
            edges.map(({ node }: any) => (
              <TaskExecutionListItem
                key={node.id}
                execution={node}
                isSelected={selectedExecution?.id === node.id}
                onClick={() => setSelectedExecution(node)}
              />
            ))
          )}
        </div>

        {/* Right: Detail */}
        <div className="flex-1 overflow-hidden">
          <TaskExecutionDetailViewer execution={selectedExecution} />
        </div>
      </div>
    </div>
  );
}
