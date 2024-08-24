import { ExpandedSidebar } from "@karrio/ui/components/expanded-sidebar";
import { KARRIO_PUBLIC_URL, MULTI_TENANT } from "@karrio/lib";
import { Notifier } from "@karrio/ui/components/notifier";
import { Navbar } from "@karrio/ui/components/navbar";
import { Providers } from "@karrio/hooks/providers";
import { auth } from "@karrio/core/context/auth";
import { redirect } from "next/navigation";
import { Metadata } from "@karrio/types";
import {
  loadMetadata,
  loadOrgData,
  loadUserData,
} from "@karrio/core/context/main";
import { headers } from "next/headers";

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
        <div className="plex-wrapper is-flex is-flex-direction-column pb-0">
          <div className="wrapper-inner is-flex-grow-1 pb-0">
            <Notifier />
            <Navbar />

            <div
              className="dashboard-content is-relative pt-0 pb-4"
              style={{ minHeight: "93vh" }}
            >
              {children}
            </div>
          </div>
        </div>
      </Providers>
    </>
  );
}
