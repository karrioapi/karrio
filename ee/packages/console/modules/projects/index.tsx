"use client";

import { DashboardHeader } from "@karrio/console/components/dashboard-header";
import { Button } from "@karrio/insiders/components/ui/button";
import { Input } from "@karrio/insiders/components/ui/input";
import { Card } from "@karrio/insiders/components/ui/card";
import { ChevronRight, Search, Plus } from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import { trpc } from "@karrio/console/trpc/client";


export default function Dashboard() {
  const params = useParams();
  const router = useRouter();
  const orgId = params.orgId as string;
  const { data, isLoading } = trpc.projects.getAll.useQuery({
    orgId: orgId,
  });
  const { projects, limit, count } = data || {
    projects: [],
    limit: 0,
    count: 0,
  };
  const canCreateProject = count < limit;

  return (
    <>
      <DashboardHeader title="Projects" description="Manage your projects" />
      <div className="flex flex-1 flex-col gap-4 p-4 bg-background">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <Button
              className="bg-[#5722cc] hover:bg-[#5722cc]/90"
              onClick={() => router.push(`/orgs/${orgId}/projects/create`)}
              disabled={!canCreateProject}
            >
              <Plus className="h-4 w-4 mr-2" />
              New project
            </Button>
            <span className="text-sm text-gray-400">
              {count} / {limit} projects
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
              <Input
                type="search"
                placeholder="Search for a project"
                className="pl-9 bg-[#2a2344] border-[#3a3354] text-white placeholder-gray-400 w-[300px] focus:border-[#79e5dd] focus:ring-[#79e5dd]"
              />
            </div>
          </div>
        </div>

        {!isLoading && projects?.length === 0 ? (
          <div className="flex flex-col items-center justify-center flex-1 min-h-[400px]">
            <h3 className="text-xl font-medium text-white mb-4">
              No projects found
            </h3>
            <p className="text-gray-400 mb-6">
              {canCreateProject
                ? "Create your first project to get started"
                : "Upgrade your plan to create more projects"}
            </p>
            <Button
              className="bg-[#5722cc] hover:bg-[#5722cc]/90"
              onClick={() =>
                canCreateProject
                  ? router.push(`/orgs/${orgId}/projects/create`)
                  : router.push(`/orgs/${orgId}/billing`)
              }
            >
              <Plus className="h-4 w-4 mr-2" />
              {canCreateProject ? "Create Project" : "Upgrade Plan"}
            </Button>
          </div>
        ) : (
          <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
            {(projects as any[])?.map((project, i) => (
              <Card
                key={i}
                className="bg-[#2a2344] border-[#3a3354] hover:border-[#79e5dd] transition-colors group"
              >
                <a
                  href={`/orgs/${orgId}/projects/${project.id}`}
                  className="block p-4"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-white font-medium mb-1 group-hover:text-[#79e5dd] transition-colors">
                        {project.name}
                      </h3>
                      <p className="text-sm text-gray-400">
                        Created{" "}
                        {new Date(project.createdAt).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <ChevronRight className="h-4 w-4 text-gray-400 group-hover:text-[#79e5dd] transition-colors" />
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 mt-4 text-sm text-gray-400">
                    <div className="flex items-center space-x-1">
                      <div className="h-2 w-2 rounded-full bg-[#79e5dd]" />
                      <span>Active</span>
                    </div>
                  </div>
                </a>
              </Card>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
