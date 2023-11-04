import { TokenObtainPair } from "karrio/rest";
import { isNoneOrEmpty, url$ } from "@/lib/helper";
import { NextApiRequest } from "next";
import logger from '@/lib/logger';
import axios from "axios";


export function computeTestMode(req: NextApiRequest): boolean {
  const cookieTestMode = (req.cookies['testMode'] || "").toLowerCase();
  const urlTestMode = (
    req.url?.includes("/test")
    || req.headers.referer?.includes("/test")
  ) as boolean;

  if (cookieTestMode === 'true' && urlTestMode) return true;
  if (cookieTestMode === 'false' && !urlTestMode) return false;

  return urlTestMode;
}

export function Auth(HOST: string) {
  return {
    async authenticate(credentials: TokenObtainPair) {
      logger.debug("authenticating...");

      const { data } = await axios({
        url: url$`${HOST || ''}/api/token`,
        method: 'POST',
        data: credentials
      });

      return data;
    },
    async refreshToken(refreshToken: string) {
      if (isNoneOrEmpty(refreshToken)) {
        return Promise.reject("Missing refresh token!")
      }

      logger.debug("Send refresh token request...");

      const { data: { refresh, access } } = await axios({
        url: url$`${HOST || ''}/api/token/refresh`,
        method: 'POST',
        data: { refresh: refreshToken }
      });
      return { access, refresh };
    },
    async getCurrentOrg(access: string, orgId?: string) {
      logger.debug("retrieving session org...");

      return (
        axios({
          url: url$`${HOST || ''}/graphql`,
          method: 'POST',
          data: { query: `{ organizations { id } }` },
          headers: { 'authorization': `Bearer ${access}` },
        })
          .then(({ data: { data } }) => {
            return (
              (data?.organizations || []).find(({ id }: any) => id === orgId)
              || (data?.organizations || [{ id: null }])[0]
            );
          })
          .catch(({ data }) => {
            logger.error(data)
            return { id: null };
          })
      );
    }
  }
}
