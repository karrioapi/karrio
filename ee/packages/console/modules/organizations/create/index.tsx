"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@karrio/insiders/components/ui/button";
import { Input } from "@karrio/insiders/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@karrio/insiders/components/ui/card";
import { trpc } from "@karrio/console/trpc/client";

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
      <div className="flex flex-1 flex-col items-center justify-center min-h-screen bg-background">
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
    </>
  );
}
