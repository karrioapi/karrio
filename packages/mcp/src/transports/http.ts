import { createServer as createHTTPServer, type IncomingMessage, type ServerResponse } from "node:http";
import { randomUUID } from "node:crypto";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

export interface HttpTransportOptions {
  port: number;
  host?: string;
}

export async function startHttpTransport(
  server: McpServer,
  options: HttpTransportOptions,
): Promise<void> {
  const { port, host = "0.0.0.0" } = options;

  // Map of active session transports keyed by session ID
  const transports = new Map<string, StreamableHTTPServerTransport>();

  const httpServer = createHTTPServer(async (req: IncomingMessage, res: ServerResponse) => {
    const url = new URL(req.url || "/", `http://${req.headers.host}`);

    // Health check / MCP discovery endpoint
    if (url.pathname === "/.well-known/mcp" && req.method === "GET") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(
        JSON.stringify({
          name: "karrio",
          version: "1.0.0",
          description: "Karrio MCP Server — Multi-carrier shipping intelligence for AI agents",
          transport: "streamable-http",
          endpoint: "/mcp",
        }),
      );
      return;
    }

    // MCP endpoint — handle POST, GET, and DELETE
    if (url.pathname === "/mcp") {
      // Try to retrieve an existing session transport
      const sessionId = req.headers["mcp-session-id"] as string | undefined;

      if (sessionId && transports.has(sessionId)) {
        // Reuse existing transport for the session
        const transport = transports.get(sessionId)!;
        const body = req.method === "POST" ? await readBody(req) : undefined;
        await transport.handleRequest(req, res, body);
        return;
      }

      // For GET/DELETE without a valid session, reject
      if (req.method === "GET" || req.method === "DELETE") {
        if (!sessionId || !transports.has(sessionId)) {
          res.writeHead(400, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ error: "Invalid or missing session" }));
          return;
        }
      }

      // POST without existing session — initialize a new transport
      if (req.method === "POST") {
        const transport = new StreamableHTTPServerTransport({
          sessionIdGenerator: () => randomUUID(),
          onsessioninitialized: (newSessionId: string) => {
            transports.set(newSessionId, transport);
          },
        });

        transport.onclose = () => {
          if (transport.sessionId) {
            transports.delete(transport.sessionId);
          }
        };

        await server.connect(transport);

        const body = await readBody(req);
        await transport.handleRequest(req, res, body);
        return;
      }

      // Unsupported method
      res.writeHead(405, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Method not allowed" }));
      return;
    }

    // 404 for everything else
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "Not found" }));
  });

  return new Promise<void>((resolve) => {
    httpServer.listen(port, host, () => {
      console.error(`Karrio MCP server listening on http://${host}:${port}/mcp`);
      resolve();
    });
  });
}

/**
 * Read the request body as a parsed JSON object.
 */
function readBody(req: IncomingMessage): Promise<unknown> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    req.on("data", (chunk: Buffer) => chunks.push(chunk));
    req.on("end", () => {
      try {
        const raw = Buffer.concat(chunks).toString("utf-8");
        resolve(raw ? JSON.parse(raw) : undefined);
      } catch (err) {
        reject(err);
      }
    });
    req.on("error", reject);
  });
}
