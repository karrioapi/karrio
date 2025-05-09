"use client";

import Link from "next/link";
import { Button } from "@karrio/ui/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@karrio/ui/components/ui/card";
import { DashboardHeader } from "@karrio/console/components/dashboard-header";
import { CardGrid } from "@karrio/console/components/card-grid";
import { PlusCircle, ChevronRight } from "lucide-react";
import { trpc } from "@karrio/console/trpc/client";

export default function OrganizationsPage() {
  const { data: organizations } = trpc.organizations.getAll.useQuery();

  return (
    <>
      <DashboardHeader
        title="Organizations"
        description="Manage your organizations"
      />
      <div className="flex flex-1 flex-col gap-4 p-4 bg-background">
        <div className="flex justify-between items-center mb-6">
          <Button asChild>
            <Link href="/orgs/create">
              <PlusCircle className="mr-2 h-4 w-4" />
              Create New Organization
            </Link>
          </Button>
        </div>

        <CardGrid>
          {organizations?.map((org: any) => (
            <Link key={org.id} href={`/orgs/${org.id}`}>
              <Card className="hover:bg-accent transition-colors cursor-pointer group">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>{org.name}</CardTitle>
                    <ChevronRight className="h-5 w-5 text-muted-foreground group-hover:text-foreground transition-colors" />
                  </div>
                </CardHeader>
                <CardContent className="text-sm text-muted-foreground">
                  Click to manage organization
                </CardContent>
              </Card>
            </Link>
          ))}
        </CardGrid>
      </div>
    </>
  );
}
