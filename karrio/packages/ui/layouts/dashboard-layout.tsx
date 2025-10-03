import { KARRIO_PUBLIC_URL, MULTI_TENANT } from "@karrio/lib";
import { Sidebar } from "@karrio/ui/components/sidebar";
import { Navbar } from "@karrio/ui/components/navbar";
import { Providers } from "@karrio/hooks/providers";
// import { getCurrentDomain } from "@karrio/core/context/main";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  // const session = await auth();

  // await requireAuthentication(session);

  // const domain = await getCurrentDomain();
  // const metadata = await loadMetadata(domain!);
  // const user = await loadUserData(session, metadata.metadata as Metadata, domain!);
  // const org = await loadOrgData(session, metadata.metadata as Metadata, domain!);
  // const orgId = ((session as any)?.orgId as string) || null;

  const pageProps = {
    // orgId,
    // ...org,
    // ...user,
    // ...metadata,
    // session,
    // MULTI_TENANT,
    // KARRIO_PUBLIC_URL,
  };

  return (
    <>
      <Providers {...pageProps}>
        <div className="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[220px_1fr]">
          <Sidebar />

          <div className="flex flex-col">
            <Navbar />

            {children}
          </div>
        </div>
      </Providers>
    </>
  );
}
