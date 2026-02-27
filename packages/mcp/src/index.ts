import { parseArgs } from "node:util";
import { createServer } from "./server.js";
import { validateApiKey } from "./auth.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

async function main() {
  const { values } = parseArgs({
    options: {
      "api-url": { type: "string", default: process.env.KARRIO_API_URL || "http://localhost:5002" },
      "api-key": { type: "string", default: process.env.KARRIO_API_KEY || "" },
      "http": { type: "boolean", default: false },
      "port": { type: "string", default: process.env.PORT || "3100" },
    },
  });

  const apiUrl = values["api-url"]!;
  const apiKey = validateApiKey(values["api-key"]);

  const server = createServer({ apiUrl, apiKey });

  if (values.http) {
    const { startHttpTransport } = await import("./transports/http.js");
    await startHttpTransport(server, { port: parseInt(values.port!, 10) });
  } else {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error(`Karrio MCP server running on stdio (API: ${apiUrl})`);
  }
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
