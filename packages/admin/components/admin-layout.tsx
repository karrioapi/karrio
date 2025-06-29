import { AdminSidebar } from "@karrio/admin/components/admin-sidebar";
import { AdminHeader } from "@karrio/admin/components/admin-header";
import { KARRIO_PUBLIC_URL, MULTI_TENANT } from "@karrio/lib";
import { auth } from "@karrio/core/context/auth";
import React from "react";
import {
  loadMetadata,
  loadOrgData,
  loadUserData,
  getCurrentDomain,
  requireAuthentication,
} from "@karrio/core/context/main";
import { Metadata } from "@karrio/types";
import { redirect } from "next/navigation";
import { Providers } from "@karrio/hooks/providers";

interface AdminLayoutProps {
  children: React.ReactNode;
}

export default async function Layout({ children }: AdminLayoutProps) {
  const session = await auth();

  await requireAuthentication(session);

  const domain = await getCurrentDomain();
  const metadata = await loadMetadata(domain!);
  const user = await loadUserData(session, metadata.metadata as Metadata, domain!);
  const org = await loadOrgData(session, metadata.metadata as Metadata, domain!);
  const orgId = ((session as any)?.orgId as string) || null;

  if (
    user.user &&
    (user.user as any)?.is_staff === false &&
    metadata.metadata?.ADMIN_DASHBOARD == false
  ) {
    redirect(`/`);
  }

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
    <Providers {...pageProps}>
      <div className="min-h-screen bg-[#f6f6f7]">
        <AdminHeader />
        <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="pt-14 flex gap-x-8">
            <aside className="hidden lg:block w-[280px] shrink-0 py-4">
              <AdminSidebar />
            </aside>
            <main className="flex-1 py-4">
              {children}
            </main>
          </div>
        </div>
      </div>
    </Providers>
  );
}
