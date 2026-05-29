import { defineConfig } from "vite";
import { tanstackStart } from "@tanstack/react-start/plugin/vite";
import viteReact from "@vitejs/plugin-react";
import tsConfigPaths from "vite-tsconfig-paths";

// Karrio Studio — TanStack Start (SSR + server functions).
// Shipping data flows through @karrio/hooks → Karrio GraphQL/REST.
// Studio-native state (app config, agents, MCP) lives in the Drizzle DB.
export default defineConfig({
  server: { port: 3003 },
  plugins: [
    tsConfigPaths({ projects: ["./tsconfig.json"] }),
    tanstackStart(),
    viteReact(),
  ],
});
