import { ExpandedSidebar } from "@karrio/ui/core/components/expanded-sidebar";
import { KARRIO_PUBLIC_URL, MULTI_TENANT } from "@karrio/lib";
import { Providers } from "@karrio/hooks/providers";
import { auth } from "@karrio/core/context/auth";
import { Metadata } from "@karrio/types";
import {
  loadMetadata,
  loadOrgData,
  loadUserData,
  requireAuthentication,
} from "@karrio/core/context/main";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  await requireAuthentication(session);

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
