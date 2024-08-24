import { ExpandedSidebar } from "@karrio/ui/components/expanded-sidebar";
import { KARRIO_PUBLIC_URL, MULTI_TENANT } from "@karrio/lib";
import { Providers } from "@karrio/hooks/providers";
import { auth } from "@karrio/core/context/auth";
import { redirect } from "next/navigation";
import { Metadata } from "@karrio/types";
import { headers } from "next/headers";
import {
  loadMetadata,
  loadOrgData,
  loadUserData,
} from "@karrio/core/context/main";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  if (!session || (session as any)?.error === "RefreshAccessTokenError") {
    const [pathname, search] = [
      headers().get("x-pathname") || "",
      headers().get("x-search") || "",
    ];
    const location = search.includes("next")
      ? search
      : `next=${pathname}${search}`;

    redirect(`/signin?next=${location}`);
  }

  const metadata = await loadMetadata();
  const user = await loadUserData(session, metadata.metadata as Metadata);
  const org = await loadOrgData(session, metadata.metadata as Metadata);
  const orgId = ((session as any)?.orgId as string) || null;

  const pageProps = {
    orgId,
    ...org,
    ...user,
    ...metadata,
    session,
    MULTI_TENANT,
    KARRIO_PUBLIC_URL,
  };

  return (
    <>
      <Providers {...pageProps}>
        <ExpandedSidebar />

        <div className="plex-wrapper is-relative p-0">{children}</div>
      </Providers>
    </>
  );
}
