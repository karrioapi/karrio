"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@karrio/ui/components/ui/card";
import { trpc } from "@karrio/console/trpc/client";
import { signOut } from "next-auth/react";
import { LogOut } from "lucide-react";
import { KarrioLogo } from "@karrio/console/components/karrio-logo";

export default function CreateOrganizationPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const createOrg = trpc.organizations.create.useMutation({
    onSuccess: (org) => {
      router.push(`/orgs/${org.id}`);
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      createOrg.mutate({ name });
    }
  };

  return (
    <>
      <div className="flex flex-col min-h-screen bg-background">
        <header className="border-b">
          <div className="container flex h-16 items-center justify-between px-4">
            <div className="flex items-center gap-4">
              <KarrioLogo />
              <div className="h-6 w-px bg-border"></div>
              <h3 className="text-lg font-semibold">Create Organization</h3>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => signOut()}
              className="flex items-center gap-2"
            >
              <LogOut className="h-4 w-4" />
              Sign Out
            </Button>
          </div>
        </header>

        <div className="flex flex-1 flex-col items-center justify-center p-4">
          <Card className="w-full max-w-lg">
            <CardHeader>
              <CardTitle>New Organization</CardTitle>
              <CardDescription>
                Enter the details for your new organization
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Input
                    id="name"
                    placeholder="Enter organization name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
                <Button
                  type="submit"
                  className="w-full"
                  disabled={createOrg.status === "loading"}
                >
                  {createOrg.status === "loading"
                    ? "Creating..."
                    : "Create Organization"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
}
