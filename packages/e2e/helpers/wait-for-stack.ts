import { env } from "./env";

/**
 * Poll the API + dashboard until both are responsive, or throw after `timeoutMs`.
 * Used as a pre-flight in CI before Playwright attempts its first navigation.
 *
 * Invoke from a Node script (e.g. `node -e "require('./helpers/wait-for-stack').waitForStack()"`)
 * or from the global-setup hook.
 */
export async function waitForStack(timeoutMs = 120_000): Promise<void> {
  const deadline = Date.now() + timeoutMs;
  const apiHealth = `${env.apiUrl}/`;
  const dashboardHealth = `${env.dashboardUrl}/signin`;

  const probe = async (url: string): Promise<boolean> => {
    try {
      const res = await fetch(url, { method: "GET" });
      return res.status < 500;
    } catch {
      return false;
    }
  };

  while (Date.now() < deadline) {
    const [api, dash] = await Promise.all([probe(apiHealth), probe(dashboardHealth)]);
    if (api && dash) return;
    await new Promise((r) => setTimeout(r, 2_000));
  }
  throw new Error(
    `waitForStack timed out after ${timeoutMs}ms — api=${apiHealth} dashboard=${dashboardHealth}`,
  );
}

if (require.main === module) {
  waitForStack().then(
    () => {
      // eslint-disable-next-line no-console
      console.log("karrio stack is healthy");
      process.exit(0);
    },
    (err) => {
      // eslint-disable-next-line no-console
      console.error(err.message);
      process.exit(1);
    },
  );
}
