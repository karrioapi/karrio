"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@karrio/ui/components/ui/card";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useRouter, useParams } from "next/navigation";
import { trpc } from "@karrio/console/trpc/client";
import { useState } from "react";

export default function CreateProjectPage() {
  const router = useRouter();
  const params = useParams();
  const { toast } = useToast();
  const orgId = params.orgId as string;
  const [name, setName] = useState("");
  const createProject = trpc.projects.create.useMutation<{ id: string }>({
    onSuccess: (project) => {
      toast({
        title: "Success",
        description: "Project created successfully",
      });
      router.push(`/orgs/${orgId}/projects/${project.id}`);
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim()) {
      createProject.mutate({ name, orgId });
    }
  };

  return (
    <div className="flex flex-1 flex-col items-center justify-center min-h-screen bg-background">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <CardTitle>New Project</CardTitle>
          <CardDescription>
            Enter the details for your new project
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Input
                id="name"
                placeholder="Enter project name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <Button
              type="submit"
              className="w-full"
              disabled={createProject.status === "loading"}
            >
              {createProject.status === "loading" ? "Creating..." : "Create Project"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
