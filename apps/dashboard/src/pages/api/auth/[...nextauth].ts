import CredentialProvider from "next-auth/providers/credentials";
import { loadAPIMetadata } from '@/lib/data-fetching';
import { NextApiRequest, NextApiResponse } from 'next';
import { isNoneOrEmpty, parseJwt } from '@/lib/helper';
import { computeTestMode, Auth } from '@/lib/auth';
import { JWT } from 'next-auth/jwt';
import getConfig from 'next/config';
import logger from '@/lib/logger';
import NextAuth from 'next-auth';
import moment from 'moment';

const { serverRuntimeConfig } = getConfig();
const secret = serverRuntimeConfig?.JWT_SECRET;


async function AuthAPI(req: NextApiRequest, res: NextApiResponse) {
  const { metadata } = await loadAPIMetadata({ req, res }).catch(_ => _);
  const auth = Auth(metadata?.HOST);

  return NextAuth({
    secret,
    pages: { signIn: '/login' },
    session: { strategy: 'jwt' },
    providers: [
      CredentialProvider({
        name: 'Credentials',
        credentials: {
          email: { label: "Email", type: "email", placeholder: "email" },
          password: { label: "Password", type: "password" }
        },
        async authorize({ orgId, ...credentials }: any, _) {
          try {
            const token = await auth.authenticate(credentials as any);
            const testMode = req.headers.referer?.includes("/test");
            const org = (metadata?.MULTI_ORGANIZATIONS
              ? await auth.getCurrentOrg(token.access, orgId)
              : { id: null }
            );

            return {
              accessToken: token.access,
              refreshToken: token.refresh,
              orgId: org?.id,
              testMode
            } as any;
          } catch (e) {
            logger.error(e);
          }

          // Return null if user data could not be retrieved
          return null;
        }
      })
    ],
    callbacks: {
      jwt: async ({ token, user }: any): Promise<JWT> => {
        if (user?.accessToken) {
          token.orgId = user.orgId;
          token.testMode = user.testMode;
          token.accessToken = user.accessToken;
          token.refreshToken = user.refreshToken;
          token.expiration = parseJwt(user.accessToken as string).exp;
        } else {
          token.testMode = computeTestMode(req);
        }

        // Check if organization updated
        const cookieOrgId = req.cookies['orgId'];
        if (!isNoneOrEmpty(cookieOrgId) && !isNoneOrEmpty((token as any).orgId) && cookieOrgId !== (token as any).orgId) {
          logger.debug(`Switching organization to ${cookieOrgId}...`);

          const org = await auth.getCurrentOrg((token as any).accessToken, cookieOrgId);
          token.orgId = org?.id;
        }

        // Return previous token if the access token has not expired yet
        if (moment().subtract(3, 'm').toDate().getTime() < (token.expiration as number) * 1000) {
          return token;
        }

        // Access token has expired, try to update it OR orgId has changed
        try {
          logger.info('Refreshing expired token...');
          const { access, refresh } = await auth.refreshToken(token.refreshToken as string);

          return {
            ...token,
            accessToken: access,
            refreshToken: refresh,
            expiration: parseJwt(access).exp
          };
        } catch (error) {
          logger.error(error);

          return {
            error: "RefreshAccessTokenError",
          }
        }
      },
      session: async ({ session, token }: any) => {
        session.accessToken = token.accessToken;
        session.expires = token.expiration;
        session.testMode = token.testMode;
        session.error = token.error;
        session.orgId = token.orgId;

        return session
      }
    }
  })(req, res);
}

export default AuthAPI;
