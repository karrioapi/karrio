import { z } from "zod";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { KarrioClient } from "../client.js";

export function registerLogTools(
  server: McpServer,
  client: KarrioClient,
): void {
  // Tool 1: list_api_logs
  server.tool(
    "list_api_logs",
    "List API request logs with optional filters. Use this to debug shipping API calls, investigate errors, find failed requests, or audit carrier API usage. Returns request path, method, status code, response time, and timestamps.",
    {
      api_endpoint: z
        .string()
        .optional()
        .describe("Filter by API endpoint path, e.g. '/v1/shipments'"),
      method: z
        .enum(["GET", "POST", "PUT", "PATCH", "DELETE"])
        .optional()
        .describe("HTTP method filter"),
      status_code: z
        .number()
        .optional()
        .describe("Filter by HTTP status code, e.g. 400 for errors"),
      status: z
        .enum(["succeeded", "failed"])
        .optional()
        .describe("Filter by request outcome"),
      date_after: z
        .string()
        .optional()
        .describe("Only logs after this ISO datetime"),
      date_before: z
        .string()
        .optional()
        .describe("Only logs before this ISO datetime"),
      entity_id: z
        .string()
        .optional()
        .describe("Filter logs related to a specific shipment/tracker ID"),
      request_id: z
        .string()
        .optional()
        .describe("Filter by specific request ID"),
      limit: z
        .number()
        .default(20)
        .describe("Maximum number of logs to return"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async (params) => {
      try {
        const filter: Record<string, unknown> = {};

        if (params.api_endpoint) filter.api_endpoint = params.api_endpoint;
        if (params.method) filter.method = [params.method];
        if (params.status_code) filter.status_code = [params.status_code];
        if (params.status) filter.status = params.status;
        if (params.date_after) filter.date_after = params.date_after;
        if (params.date_before) filter.date_before = params.date_before;
        if (params.entity_id) filter.entity_id = params.entity_id;
        if (params.request_id) filter.request_id = params.request_id;

        const data = await client.listLogs(
          Object.keys(filter).length > 0 ? filter : undefined,
        );

        const edges = data?.edges ?? [];
        const pageInfo = data?.page_info ?? { count: 0 };

        const logs = edges.slice(0, params.limit).map((edge: any) => {
          const node = edge.node;
          const log: Record<string, unknown> = {
            id: node.id,
            path: node.path,
            method: node.method,
            status_code: node.status_code,
            response_ms: node.response_ms,
            requested_at: node.requested_at,
            remote_addr: node.remote_addr,
            has_records: (node.records ?? []).length > 0,
          };

          // Include a response preview for error status codes
          if (node.status_code >= 400 && node.response) {
            const responseStr =
              typeof node.response === "string"
                ? node.response
                : JSON.stringify(node.response);
            log.response_preview = responseStr.slice(0, 200);
          }

          return log;
        });

        const result = {
          count: pageInfo.count,
          logs,
        };

        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error listing API logs: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );

  // Tool 2: get_api_log
  server.tool(
    "get_api_log",
    "Get full details of a specific API log entry by ID. Returns the complete request data, response body, and any tracing records (carrier API calls) associated with this request. Use this to debug a specific request.",
    {
      log_id: z.number().describe("The ID of the API log entry to retrieve"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async (params) => {
      try {
        const log = await client.getLog(params.log_id);

        if (!log) {
          return {
            content: [
              {
                type: "text",
                text: `No log found with ID ${params.log_id}`,
              },
            ],
            isError: true,
          };
        }

        const result = {
          id: log.id,
          path: log.path,
          host: log.host,
          method: log.method,
          status_code: log.status_code,
          response_ms: log.response_ms,
          requested_at: log.requested_at,
          remote_addr: log.remote_addr,
          query_params: log.query_params,
          data: log.data,
          response: log.response,
          records: (log.records ?? []).map((record: any) => ({
            id: record.id,
            key: record.key,
            timestamp: record.timestamp,
            test_mode: record.test_mode,
            created_at: record.created_at,
            meta: record.meta,
            record: record.record,
          })),
        };

        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error fetching API log: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );

  // Tool 3: list_tracing_records
  server.tool(
    "list_tracing_records",
    "List carrier API tracing records — the raw requests and responses sent to carrier APIs (FedEx, UPS, DHL, etc.). Use this to debug carrier-level errors, inspect what was sent to a carrier, or trace a shipment's carrier API journey.",
    {
      key: z
        .string()
        .optional()
        .describe(
          "Carrier or operation key, e.g. 'fedex' or 'fedex_create_shipment'",
        ),
      request_log_id: z
        .number()
        .optional()
        .describe("Link to a specific API log"),
      date_after: z
        .string()
        .optional()
        .describe("Only records after this ISO datetime"),
      date_before: z
        .string()
        .optional()
        .describe("Only records before this ISO datetime"),
      limit: z
        .number()
        .default(20)
        .describe("Maximum number of records to return"),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
    async (params) => {
      try {
        const filter: Record<string, unknown> = {};

        if (params.key) filter.key = params.key;
        if (params.request_log_id)
          filter.request_log_id = params.request_log_id;
        if (params.date_after) filter.date_after = params.date_after;
        if (params.date_before) filter.date_before = params.date_before;

        const data = await client.listTracingRecords(
          Object.keys(filter).length > 0 ? filter : undefined,
        );

        const edges = data?.edges ?? [];
        const pageInfo = data?.page_info ?? { count: 0 };

        const records = edges.slice(0, params.limit).map((edge: any) => {
          const node = edge.node;
          let recordContent = node.record;

          // Summarize large records
          if (recordContent) {
            const recordStr =
              typeof recordContent === "string"
                ? recordContent
                : JSON.stringify(recordContent);
            if (recordStr.length > 2000) {
              recordContent =
                recordStr.slice(0, 2000) + "... (truncated, use get_api_log for full details)";
            }
          }

          return {
            id: node.id,
            key: node.key,
            timestamp: node.timestamp,
            test_mode: node.test_mode,
            created_at: node.created_at,
            record: recordContent,
          };
        });

        const result = {
          count: pageInfo.count,
          records,
        };

        return {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
        };
      } catch (error: any) {
        return {
          content: [
            {
              type: "text",
              text: `Error listing tracing records: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    },
  );
}
