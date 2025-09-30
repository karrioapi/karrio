import { SignUpClient } from "@karrio/console/modules/auth/signup-client";
import { auth } from "@karrio/console/apis/auth";
import { redirect } from "next/navigation";

export default async function SignUpPage() {
  const session = await auth();
  if (session) redirect(`/orgs`);

  return <SignUpClient />;
}
