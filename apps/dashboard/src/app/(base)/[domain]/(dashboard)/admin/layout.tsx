import { auth } from "@karrio/core/context/auth";
import {
  loadMetadata,
  loadUserData,
  getCurrentDomain,
  requireAuthentication,
} from "@karrio/core/context/main";
import { Metadata } from "@karrio/types";
import { redirect } from "next/navigation";

interface AdminLayoutProps {
  children: React.ReactNode;
}

export default async function AdminLayout({ children }: AdminLayoutProps) {
  const session = await auth();
  await requireAuthentication(session);

  const domain = await getCurrentDomain();
  const metadata = await loadMetadata(domain!);
  const user = await loadUserData(session, metadata.metadata as Metadata, domain!);

  // Permission check: redirect if not staff or admin dashboard not enabled
  if (!(user.user as any)?.is_staff || !metadata.metadata?.ADMIN_DASHBOARD) {
    redirect("/");
  }

  return <>{children}</>;
}
