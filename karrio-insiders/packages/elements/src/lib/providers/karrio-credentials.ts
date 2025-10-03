import type { CredentialsConfig } from "next-auth/providers";
import { Auth, logger, KARRIO_API } from "@karrio/lib";
import { headers } from "next/headers";

/**
 * <div style={{display: "flex", justifyContent: "space-between", alignItems: "center", padding: 16}}>
 * <span>Karrio Credentials provider for username/password authentication with your Karrio instance</span>
 * </div>
 *
 * @module providers/karrio-credentials
 */

export interface KarrioCredentialsConfig {
  clientId?: string;
  apiUrl?: string;
}

/**
 * Credentials authentication for Karrio.
 *
 * @param config - The configuration options for the Karrio Credentials provider
 * @returns The configured Karrio Credentials provider
 *
 * @example
 * ```ts
 * import KarrioCredentials from "@karrio/elements/providers/karrio-credentials";
 *
 * export const { handlers, auth, signIn, signOut } = NextAuth({
 *   providers: [
 *     KarrioCredentials({
 *       apiUrl: process.env.NEXT_PUBLIC_KARRIO_API,
 *     }),
 *   ],
 * });
 * ```
 */
export default function KarrioCredentials(
  config?: KarrioCredentialsConfig,
): CredentialsConfig<{
  email: { label: string; type: string; placeholder: string };
  password: { label: string; type: string };
}> {
  const { clientId, apiUrl = KARRIO_API } = config || {};

  return {
    id: "karrio-credentials",
    name: "Karrio Credentials",
    type: "credentials",
    credentials: {
      email: { label: "Email", type: "email", placeholder: "email" },
      password: { label: "Password", type: "password" },
    },
    authorize: async (credentials, req) => {
      try {
        if (!credentials) {
          throw new Error("No credentials provided");
        }

        const email = credentials.email as string;
        const password = credentials.password as string;

        if (!email || !password) {
          throw new Error("Email and password are required");
        }

        const auth = Auth(apiUrl as string);
        const token = await auth.authenticate({ email, password });

        if (!token || !token.access) {
          throw new Error("Authentication failed");
        }

        // Get referer from headers - handle async headers API
        let testMode = false;
        try {
          const headersList = await headers();
          const referer = headersList.get('referer');
          testMode = referer?.includes('/test') || false;
        } catch (e) {
          logger.error('Error accessing headers:', e);
        }

        return {
          id: email,
          email,
          accessToken: token.access,
          refreshToken: token.refresh,
          testMode,
        };
      } catch (e) {
        logger.error("Karrio credentials authentication error:", e);
        return null;
      }
    },
  };
}
