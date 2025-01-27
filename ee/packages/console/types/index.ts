export * from "@karrio/console/types/api";

export interface Project {
  id: string;
  name: string;
  organizationId: string;
  tenantId: string | null;
  tenantApiKey: string | null;
  status:
    | "PENDING"
    | "DEPLOYING"
    | "ACTIVE"
    | "FAILED"
    | "UNREACHABLE"
    | "DELETED";
  statusMessage: string | null;
  metadata: {
    deployment_started_at: string;
    deployment_completed_at?: string;
    deployment_failed_at?: string;
    [key: string]: any;
  } | null;
  lastPing: string | null;
  createdAt: string;
  updatedAt: string;
}
