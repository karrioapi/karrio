import GitHubProvider from "next-auth/providers/github";
import { resend } from "@karrio/console/shared/resend";
import { prisma } from "@karrio/console/prisma/client";
import { PrismaAdapter } from "@auth/prisma-adapter";
import Resend from "next-auth/providers/resend";
import { Session } from "next-auth";
import { JWT } from "next-auth/jwt";
import NextAuth from "next-auth";

export const { auth, handlers, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
    Resend({
      from: process.env.EMAIL_FROM || "no-reply@karrio.io",
      apiKey: process.env.RESEND_API_KEY,
      async sendVerificationRequest({ identifier: email, url }) {
        await resend.emails.send({
          from: process.env.EMAIL_FROM || "no-reply@karrio.io",
          to: email,
          subject: "Sign in to Karrio",
          html: `
            <h1>Welcome to Karrio</h1>
            <p>Click the link below to sign in:</p>
            <a href="${url}">Sign in to Karrio</a>
          `,
        });
      },
    }),
  ],
  session: { strategy: "jwt" },
  secret: process.env.NEXTAUTH_SECRET!,
  callbacks: {
    async session({ session, token }: { session: Session; token: JWT }) {
      return {
        ...session,
        user: {
          ...session.user,
          id: token.sub!,
        },
      };
    },
    async jwt({ token, user }) {
      if (user) {
        token.sub = user.id;
      }
      return token;
    },
    async signIn({ user, account }) {
      if (!account || !user.email) return false;

      await prisma.user.upsert({
        where: { email: user.email },
        create: {
          email: user.email,
          name: user.name,
          image: user.image,
          accounts: {
            create: {
              type: account.type,
              provider: account.provider,
              providerAccountId: account.providerAccountId,
              access_token: account.access_token,
              token_type: account.token_type,
              scope: account.scope,
            },
          },
        },
        update: {},
      });

      return true;
    },
  },
  pages: {
    signIn: "/signin",
    newUser: "/orgs/create",
    verifyRequest: "/auth/verify-request",
  },
});
