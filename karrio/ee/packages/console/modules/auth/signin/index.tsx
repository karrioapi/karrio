import { SignInClient } from "@karrio/console/modules/auth/signin-client";
import { auth } from "@karrio/console/apis/auth";
import { redirect } from "next/navigation";

export default async function SignInPage() {
  const session = await auth();
  if (session) redirect(`/orgs`);

  return <SignInClient />;
}
