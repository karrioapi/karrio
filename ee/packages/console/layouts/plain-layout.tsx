import { auth } from "@karrio/console/apis/auth";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

export default async function Layout({ children }: { children: ReactNode }) {
  const session = await auth();

  if (!session) {
    redirect("/signin");
  }

  return <>{children}</>;
}
