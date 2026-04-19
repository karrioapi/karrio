/**
 * Seed a minimal dataset for the e2e smoke suite.
 *
 * Creates (idempotently, best-effort):
 *   - a shipping address
 *   - a parcel template
 *
 * Uses only the public REST API — never touches the DB directly.
 *
 * Run:
 *   node -r ts-node/register packages/e2e/scripts/seed.ts
 * or (compiled):
 *   tsx packages/e2e/scripts/seed.ts
 */
import { KarrioApi } from "../helpers/api";
import { waitForStack } from "../helpers/wait-for-stack";

async function main() {
  await waitForStack(180_000);
  const api = new KarrioApi();
  await api.login();

  const addr = await api.createAddress({ person_name: "E2E Seed" }).catch((e) => {
    console.warn(`[seed] address create skipped: ${e?.message ?? e}`);
    return null;
  });
  if (addr) console.log(`[seed] address created id=${addr.id}`);

  const parcel = await api.createParcel().catch((e) => {
    console.warn(`[seed] parcel create skipped: ${e?.message ?? e}`);
    return null;
  });
  if (parcel) console.log(`[seed] parcel created id=${parcel.id}`);

  await api.dispose();
  console.log("[seed] done");
}

main().catch((err) => {
  console.error("[seed] failed:", err);
  process.exit(1);
});
