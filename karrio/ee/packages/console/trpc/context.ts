import { prisma } from "@karrio/console/prisma/client";
import { auth } from "@karrio/console/apis/auth";
import { Session } from "next-auth";
import { type inferAsyncReturnType } from "@trpc/server";

export const createContext = async () => {
  const session = await auth();

  return {
    session: session as Session | null,
    prisma,
    user: session?.user,
  };
};

export type Context = inferAsyncReturnType<typeof createContext>;
