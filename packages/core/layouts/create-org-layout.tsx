import { loadMetadata, getCurrentDomain, requireAuthentication } from "@karrio/core/context/main";
import { Providers } from "@karrio/hooks/providers";
import { auth } from "@karrio/core/context/auth";
import { redirect } from "next/navigation";
import { Metadata } from "@karrio/types";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();
  await requireAuthentication(session);

  // Redirect to home if user already has an orgId in session
  // This prevents users from manually accessing create-organization when they already have an org
  if ((session as any)?.orgId) {
    redirect("/");
  }

  // Note: We rely on parent public-layout's metadata, but we get it from cache
  // This call will hit the cache populated by public-layout, so no extra API request
  const domain = await getCurrentDomain();
  const { metadata } = await loadMetadata(domain!);

  const pageProps = { metadata: metadata as Metadata, session };

  return <Providers {...pageProps}>{children}</Providers>;
}
