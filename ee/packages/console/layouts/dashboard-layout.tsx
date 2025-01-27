import { DashboardSidebar } from "@karrio/console/components/dashboard-sidebar";
import { auth } from "@karrio/console/apis/auth";
import { redirect } from "next/navigation";
import { ReactNode } from "react";
import {
  SidebarInset,
  SidebarProvider,
} from "@karrio/insiders/components/ui/sidebar";
import { prisma } from "@karrio/console/prisma/client";

export default async function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  const session = await auth();

  if (!session) {
    redirect("/signin");
  }

  // Add this check
  const organizations = await prisma.organization.findMany({
    where: {
      members: {
        some: {
          userId: session.user.id,
        },
      },
    },
  });
  if (organizations?.length === 0) {
    redirect("/orgs/create");
  }

  return (
    <SidebarProvider>
      <DashboardSidebar />
      <SidebarInset className="bg-background">{children}</SidebarInset>
    </SidebarProvider>
  );
}
