// db/index.ts — Drizzle client for Studio-native state. Server-only.
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "~/db/schema";

const connectionString = process.env.DATABASE_URL;

// Lazily create the client so the app can boot (and tests can run UI-only)
// without a database configured. Server functions that need the DB call db().
let _client: ReturnType<typeof drizzle<typeof schema>> | null = null;

export function db() {
  if (!connectionString) {
    throw new Error("DATABASE_URL is not set — Studio-native DB unavailable.");
  }
  if (!_client) {
    const sql = postgres(connectionString, { max: 5 });
    _client = drizzle(sql, { schema });
  }
  return _client;
}

export { schema };
