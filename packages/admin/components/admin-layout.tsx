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
import { Providers } from "@karrio/admin/hooks/providers";

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
    !(user.user as any)?.is_staff || !metadata.metadata?.ADMIN_DASHBOARD
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
    <>
      <Providers {...pageProps}>
        <AdminHeader />

        <div className="min-h-screen bg-[#f6f6f7] pt-14">
          <div className="p-4">
            <div className="relative mx-auto max-w-[1200px]">
              <div className="flex gap-5">
                <div className="w-[280px] shrink-0">
                  <AdminSidebar />
                </div>

                <main className="flex-1 space-y-6">{children}</main>
              </div>
            </div>
          </div>
        </div>
      </Providers>
    </>
  );
}
