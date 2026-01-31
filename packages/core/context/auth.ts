import {
  Auth,
  logger,
  parseJwt,
  KARRIO_API,
  computeTestMode,
} from "@karrio/lib";
import { cookies, headers } from "next/headers";
import { getCurrentDomain, loadMetadata } from "@karrio/core/context/main";
import Credentials from "next-auth/providers/credentials";
import NextAuth from "next-auth";
import moment from "moment";

export const { handlers, signIn, signOut, auth } = NextAuth({
  secret: process.env.NEXTAUTH_SECRET,
  pages: { signIn: "/signin" },
  session: { strategy: "jwt" },
  providers: [
    Credentials({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email", placeholder: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize({ orgId, ...credentials }: any, req: any) {
        try {
          const headersList = await headers();
          const domain = await getCurrentDomain();
          const { metadata } = await loadMetadata(domain!);
          const auth = Auth(metadata?.HOST || (KARRIO_API as string));
          const token = await auth.authenticate(credentials as any);
          const testMode = Boolean(headersList.get("referer")?.includes("/test"));
          const org = metadata?.MULTI_ORGANIZATIONS
            ? await auth.getCurrentOrg({
              accessToken: token.access,
              testMode,
              orgId,
            })
            : { id: null };

          return {
            email: credentials.email,
            accessToken: token.access,
            refreshToken: token.refresh,
            orgId: org?.id,
            testMode,
          } as any;
        } catch (e) {
          logger.error(e);
        }

        // Return null if user data could not be retrieved
        return null;
      },
    }),
  ],
  callbacks: {
    redirect: async ({ url, baseUrl, trigger }: any) => {
      // Handle signout redirects to current site host with fallback
      if (trigger === "signOut") {
        try {
          const currentDomain = await getCurrentDomain();
          if (currentDomain) {
            // Use the current domain as the redirect target
            const protocol = currentDomain.startsWith("localhost") ? "http" : "https";
            return `${protocol}://${currentDomain}`;
          }
        } catch (error) {
          logger.error("Failed to get current domain for signout redirect:", error);
        }

        // Fallback to NEXTAUTH_URL if current domain is unavailable
        return process.env.NEXTAUTH_URL || baseUrl;
      }

      // For other redirects (signin, error), use default behavior
      // Allows relative callback URLs
      if (url.startsWith("/")) return `${baseUrl}${url}`;
      // Allows callback URLs on the same origin
      else if (new URL(url).origin === baseUrl) return url;
      return baseUrl;
    },
    jwt: async ({ token, user, trigger, session }: any): Promise<any> => {
      const headersList = await headers();
      const domain = await getCurrentDomain();
      const host = domain || (KARRIO_API as string);
      const { metadata } = await loadMetadata(host);
      const auth = Auth(metadata?.HOST || host);

      if (user?.accessToken) {
        token.orgId = user.orgId;
        token.testMode = user.testMode;
        token.accessToken = user.accessToken;
        token.refreshToken = user.refreshToken;
        token.expiration = parseJwt(user.accessToken as string).exp;
      } else if (headersList.get("referer")) {
        token.testMode = computeTestMode(await cookies(), await headers());
      }

      if (trigger === "update" && session?.orgId) {
        // Note, that `session` can be any arbitrary object, remember to validate it!
        const org = await auth.getCurrentOrg({
          accessToken: (token as any).accessToken,
          testMode: token.testMode,
          orgId: session.orgId,
        });
        token.orgId = org?.id || token.orgId;
      }

      // Return previous token if the access token has not expired yet
      if (
        moment().subtract(3, "m").toDate().getTime() <
        (token.expiration as number) * 1000
      ) {
        return token;
      }

      // Access token has expired, try to update it
      try {
        logger.info("Refreshing expired token...");
        const { access, refresh } = await auth.refreshToken(
          token.refreshToken as string,
        );
        return {
          ...token,
          accessToken: access,
          refreshToken: refresh,
          expiration: parseJwt(access).exp,
        };
      } catch (error) {
        logger.error(error);
        return {
          error: "RefreshAccessTokenError",
        };
      }
    },
    session: async ({ session, token, user }: any) => {
      session.accessToken = token.accessToken;
      session.expires = token.expiration;
      session.testMode = token.testMode;
      session.error = token.error;
      session.orgId = token.orgId;
      session.user = {
        ...(user || session.user || {}),
        accessToken: token.accessToken,
        testMode: token.testMode,
        orgId: token.orgId,
      };

      return session;
    },
  },
});
