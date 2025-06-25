import { TokenObtainPair } from "@karrio/types/rest/api";
import { isNoneOrEmpty, url$ } from "./helper";
import { logger } from "./logger";
import axios from "axios";

export function computeTestMode(cookies: any, headers: any): boolean {
  const cookieTestMode = (
    (cookies.get("testMode")?.value as string) || ""
  ).toLowerCase();
  const urlTestMode = headers.get("referer")?.includes("/test") as boolean;

  if (cookieTestMode === "true" && urlTestMode) return true;
  if (cookieTestMode === "false" && !urlTestMode) return false;

  return urlTestMode;
}

export function Auth(HOST: string) {
  return {
    async authenticate(credentials: TokenObtainPair) {
      logger.debug("authenticating...");

      const { data } = await axios({
        url: url$`${HOST || ""}/api/token`,
        method: "POST",
        data: credentials,
      });

      return data;
    },
    async refreshToken(refreshToken: string) {
      if (isNoneOrEmpty(refreshToken)) {
        return Promise.reject("Missing refresh token!");
      }

      logger.debug("Send refresh token request...");

      const {
        data: { refresh, access },
      } = await axios({
        url: url$`${HOST || ""}/api/token/refresh`,
        method: "POST",
        data: { refresh: refreshToken },
      });
      return { access, refresh };
    },
    async getCurrentOrg({
      accessToken,
      orgId,
      testMode,
      currentOrgId,
    }: {
      accessToken: string;
      testMode: boolean;
      orgId?: string;
      currentOrgId?: string;
    }) {
      logger.debug({
        msg: "retrieving session org...",
        orgId,
        testMode,
      });

      return axios({
        url: url$`${HOST || ""}/graphql`,
        method: "POST",
        data: { query: `{ organizations { id } }` },
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "x-test-mode": testMode,
        },
      })
        .then(({ data }) => {
          console.log("orgs data", data);
          const organizations = data?.data?.organizations || [];
          // First try to find the specified org
          const selectedOrg = organizations.find(({ id }: any) => id === orgId);
          if (selectedOrg) return selectedOrg;

          // If no org matches orgId, use currentOrgId if provided
          if (currentOrgId) {
            const currentOrg = organizations.find(({ id }: any) => id === currentOrgId);
            if (currentOrg) return currentOrg;
          }

          // Finally, fall back to first org or null
          return organizations[0] || { id: null };
        })
        .catch(({ data }) => {
          logger.error(data);
          return { id: null };
        });
    },
  };
}
