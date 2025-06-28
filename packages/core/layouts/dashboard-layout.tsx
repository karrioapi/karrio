import { ModeIndicator } from "@karrio/ui/components/mode-indicator";
import { Notifier } from "@karrio/ui/core/components/notifier";
import { KARRIO_PUBLIC_URL, MULTI_TENANT } from "@karrio/lib";
import { AppSidebar } from "@karrio/ui/components/sidebar";
import { Navbar } from "@karrio/ui/components/navbar";
import { Providers } from "@karrio/hooks/providers";
import { auth } from "@karrio/core/context/auth";
import { Metadata } from "@karrio/types";
import {
  SidebarInset,
  SidebarProvider,
} from "@karrio/ui/components/ui/sidebar";
import {
  loadMetadata,
  loadOrgData,
  loadUserData,
  getCurrentDomain,
  requireAuthentication,
} from "@karrio/core/context/main";
import { DeveloperToolsProvider, DeveloperToolsDrawer } from "@karrio/developers";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  await requireAuthentication(session);

  const domain = await getCurrentDomain();
  const metadata = await loadMetadata(domain!);
  const user = await loadUserData(session, metadata.metadata as Metadata, domain!);
  const org = await loadOrgData(session, metadata.metadata as Metadata, domain!);
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
        <DeveloperToolsProvider>
          <ModeIndicator />
          <SidebarProvider>
            <AppSidebar />
            <SidebarInset className="flex flex-col h-screen overflow-hidden main-layout">
              <div className="flex-shrink-0">
                <Navbar />
              </div>
              <div className="flex-1 overflow-y-auto overflow-x-hidden scrollable-content">
                <div className="max-w-7xl mx-auto w-full px-4 2xl:px-0 py-4">
                  <Notifier />
                  {children}
                </div>
              </div>
            </SidebarInset>
          </SidebarProvider>
          <DeveloperToolsDrawer />
        </DeveloperToolsProvider>
      </Providers>
    </>
  );
}
