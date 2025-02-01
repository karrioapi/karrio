"use client";

import { DashboardHeader } from "@karrio/console/components/dashboard-header";
import { trpc } from "@karrio/console/trpc/client";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@karrio/insiders/components/ui/card";
import {
  TENANT_API_DOMAIN,
  TENANT_DASHBOARD_DOMAIN,
} from "@karrio/console/shared/constants";
import { Alert, AlertDescription } from "@karrio/insiders/components/ui/alert";
import { Copy, Trash2, AlertCircle, PlusIcon, Globe } from "lucide-react";
import { Button } from "@karrio/insiders/components/ui/button";
import { Input } from "@karrio/insiders/components/ui/input";
import { useToast } from "@karrio/insiders/hooks/use-toast";
import { useState } from "react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@karrio/insiders/components/ui/alert-dialog";
import { useRouter } from "next/navigation";

const ProjectStatusBadge = ({ status }: { status: string }) => {
  const statusStyles = {
    PENDING: "bg-yellow-100 text-yellow-800",
    DEPLOYING: "bg-blue-100 text-blue-800",
    ACTIVE: "bg-green-100 text-green-800",
    FAILED: "bg-red-100 text-red-800",
    UNREACHABLE: "bg-orange-100 text-orange-800",
    DELETED: "bg-gray-100 text-gray-800",
  };

  return (
    <span
      className={`px-2 py-1 rounded-full text-xs font-medium ${statusStyles[status as keyof typeof statusStyles]
        }`}
    >
      {status}
    </span>
  );
};

export default function SettingsPage({
  params,
}: {
  params: { orgId: string; projectId: string };
}) {
  const { toast } = useToast();
  const router = useRouter();
  const utils = trpc.useUtils();
  const { data: currentProject } = trpc.projects.get.useQuery({
    id: params.projectId,
    orgId: params.orgId,
  });
  const { data: tenant } = trpc.projects.tenant.get.useQuery({
    projectId: params.projectId,
  });
  const updateProject = trpc.projects.update.useMutation<{
    id: string;
    name: string;
    orgId: string;
  }>({
    onSuccess: () => {
      utils.projects.get.invalidate();
      toast({
        title: "Success",
        description: "Project details updated successfully",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });
  const deleteProject = trpc.projects.delete.useMutation<{ id: string }>({
    onSuccess: () => {
      utils.projects.getAll.invalidate();
      toast({
        title: "Success",
        description: "Project deleted successfully",
      });
      router.push(`/orgs/${params.orgId}`);
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });
  const addApiDomain = trpc.projects.tenant.addApiDomain.useMutation({
    onSuccess: () => {
      utils.projects.tenant.get.invalidate();
      toast({
        title: "Success",
        description: "Domain added successfully",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });
  const removeApiDomain = trpc.projects.tenant.removeApiDomain.useMutation({
    onSuccess: () => {
      utils.projects.tenant.get.invalidate();
      toast({
        title: "Success",
        description: "Domain removed successfully",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });
  const updateDashboardDomains =
    trpc.projects.tenant.updateDashboardDomains.useMutation({
      onSuccess: () => {
        utils.projects.tenant.get.invalidate();
        toast({
          title: "Success",
          description: "Domains updated successfully",
        });
      },
      onError: (error) => {
        toast({
          title: "Error",
          description: error.message,
          variant: "destructive",
        });
      },
    });
  const checkTenantHealth = trpc.projects.checkTenantHealth.useMutation({
    onSuccess: () => {
      utils.projects.get.invalidate({
        id: params.projectId,
        orgId: params.orgId,
      });
      toast({
        title: "Success",
        description: "Tenant health check completed",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const [projectName, setProjectName] = useState(currentProject?.name || "");
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  const handleUpdateProject = async () => {
    try {
      await updateProject.mutateAsync({
        id: params.projectId,
        name: projectName,
        orgId: params.orgId,
      });
    } catch (error) {
      // Error is handled by the mutation callbacks
    }
  };

  const handleDeleteProject = async () => {
    try {
      await deleteProject.mutateAsync({
        id: params.projectId,
      });
    } catch (error) {
      // Error is handled by the mutation callbacks
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied",
      description: "Copied to clipboard",
    });
  };

  const formatDomainUrl = (domain: string) => {
    let url = domain;
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      url = "http://" + url;
    }
    return url;
  };

  const defaultApiDomain =
    tenant?.api_domains?.find((d: string) =>
      d.endsWith(TENANT_API_DOMAIN || ""),
    ) || "";
  const customApiDomains =
    tenant?.api_domains?.filter(
      (d: string) => !d.endsWith(TENANT_API_DOMAIN || ""),
    ) || [];
  const defaultAppDomain =
    tenant?.app_domains?.find((d: string) =>
      d.endsWith(TENANT_DASHBOARD_DOMAIN || ""),
    ) || "";
  const customAppDomains =
    tenant?.app_domains?.filter(
      (d: string) => !d.endsWith(TENANT_DASHBOARD_DOMAIN || ""),
    ) || [];

  return (
    <>
      <DashboardHeader
        title="Project Settings"
        description="Manage your project settings"
      />

      <div className="p-8 bg-background">
        <div className="max-w-7xl mx-auto space-y-16">
          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">
                  Project Information
                </h3>
                <p className="text-sm text-muted-foreground">
                  Basic information and deployment status
                </p>
              </div>

              <div className="flex-1 space-y-6">
                <Card>
                  <CardHeader>
                    <div className="flex justify-between items-center">
                      <CardTitle>Project Details</CardTitle>
                      <ProjectStatusBadge
                        status={currentProject?.status || "PENDING"}
                      />
                    </div>
                    <CardDescription>
                      {currentProject?.statusMessage ||
                        "Update your project's basic information"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="space-y-4">
                      <div className="grid gap-2">
                        <label className="text-sm font-medium">Name</label>
                        <div className="flex gap-4">
                          <Input
                            value={projectName}
                            onChange={(e) => setProjectName(e.target.value)}
                            placeholder={currentProject?.name || "Project name"}
                          />
                          <Button
                            onClick={handleUpdateProject}
                            disabled={
                              !projectName ||
                              projectName === currentProject?.name
                            }
                          >
                            Save
                          </Button>
                        </div>
                      </div>

                      <div className="grid gap-2">
                        <label className="text-sm font-medium">
                          Project ID
                        </label>
                        <div className="flex items-center gap-4">
                          <code className="relative rounded bg-muted px-[0.5rem] py-[0.4rem] font-mono text-sm">
                            {currentProject?.id}
                          </code>
                          <Button
                            variant="outline"
                            size="icon"
                            onClick={() =>
                              copyToClipboard(currentProject?.id || "")
                            }
                          >
                            <Copy className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>

                    {currentProject?.status === "FAILED" && (
                      <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertDescription>
                          Tenant deployment failed. Please check the logs or
                          contact support.
                        </AlertDescription>
                      </Alert>
                    )}

                    {currentProject?.status === "UNREACHABLE" && (
                      <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertDescription>
                          Tenant is currently unreachable. Last successful
                          connection:{" "}
                          {currentProject.lastPing
                            ? new Date(currentProject.lastPing).toLocaleString()
                            : "Never"}
                        </AlertDescription>
                      </Alert>
                    )}

                    {currentProject?.status === "ACTIVE" && (
                      <Button
                        onClick={() => {
                          checkTenantHealth.mutate({
                            projectId: currentProject.id,
                          });
                        }}
                        disabled={checkTenantHealth.status === "loading"}
                      >
                        Check Tenant Health
                      </Button>
                    )}
                  </CardContent>
                </Card>
              </div>
            </div>
          </section>

          <div className="border-t" />

          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">Custom Domains</h3>
                <p className="text-sm text-muted-foreground">
                  Configure custom domains for your project's API and dashboard
                  access
                </p>
              </div>

              <Card className="flex-1">
                <CardHeader>
                  <CardTitle>Domain Management</CardTitle>
                  <CardDescription>
                    Configure custom domains for your project
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-lg font-medium">API Domains</h3>
                      <p className="text-sm text-muted-foreground">
                        Manage the domains that can be used to access your API.
                      </p>
                    </div>

                    <div className="space-y-4">
                      <div className="flex items-center justify-between rounded-md border p-3">
                        <div className="flex items-center gap-2">
                          <Globe className="h-4 w-4 text-muted-foreground" />
                          <a
                            href={formatDomainUrl(defaultApiDomain)}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm hover:underline"
                          >
                            {defaultApiDomain}
                          </a>
                        </div>
                      </div>

                      <div className="space-y-2">
                        {customApiDomains.map((domain) => (
                          <div
                            key={domain}
                            className="flex items-center justify-between rounded-md border p-3"
                          >
                            <div className="flex items-center gap-2">
                              <Globe className="h-4 w-4 text-muted-foreground" />
                              <a
                                href={formatDomainUrl(domain)}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm hover:underline"
                              >
                                {domain}
                              </a>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="text-destructive"
                              onClick={async () => {
                                try {
                                  await removeApiDomain.mutateAsync({
                                    projectId: params.projectId,
                                    domain,
                                  });
                                } catch (error: any) {
                                  toast({
                                    title: "Error",
                                    description: error.message,
                                    variant: "destructive",
                                  });
                                }
                              }}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        ))}
                      </div>

                      <form
                        className="flex gap-2"
                        onSubmit={async (e) => {
                          e.preventDefault();
                          const form = e.target as HTMLFormElement;
                          const domain = (
                            form.elements.namedItem(
                              "domain",
                            ) as HTMLInputElement
                          ).value;
                          try {
                            await addApiDomain.mutateAsync({
                              projectId: params.projectId,
                              domain,
                            });
                            form.reset();
                          } catch (error: any) {
                            toast({
                              title: "Error",
                              description: error.message,
                              variant: "destructive",
                            });
                          }
                        }}
                      >
                        <Input
                          name="domain"
                          placeholder="Enter a custom domain"
                          className="flex-1"
                        />
                        <Button type="submit">
                          <PlusIcon className="h-4 w-4" />
                        </Button>
                      </form>
                    </div>

                    <div className="space-y-4">
                      <div>
                        <h3 className="text-lg font-medium">
                          Dashboard Domains
                        </h3>
                        <p className="text-sm text-muted-foreground">
                          Manage the domains that can be used to access your
                          dashboard.
                        </p>
                      </div>

                      <div className="flex items-center justify-between rounded-md border p-3">
                        <div className="flex items-center gap-2">
                          <Globe className="h-4 w-4 text-muted-foreground" />
                          <a
                            href={formatDomainUrl(defaultAppDomain)}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm hover:underline"
                          >
                            {defaultAppDomain}
                          </a>
                        </div>
                      </div>

                      <div className="space-y-2">
                        {customAppDomains.map((domain: string) => (
                          <div
                            key={domain}
                            className="flex items-center justify-between rounded-md border p-3"
                          >
                            <div className="flex items-center gap-2">
                              <Globe className="h-4 w-4 text-muted-foreground" />
                              <a
                                href={formatDomainUrl(domain)}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm hover:underline"
                              >
                                {domain}
                              </a>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="text-destructive"
                              onClick={async () => {
                                try {
                                  const currentDomains =
                                    tenant?.app_domains || [];
                                  await updateDashboardDomains.mutateAsync({
                                    projectId: params.projectId,
                                    domains: currentDomains.filter(
                                      (d: string) => d !== domain,
                                    ),
                                  });
                                } catch (error: any) {
                                  toast({
                                    title: "Error",
                                    description: error.message,
                                    variant: "destructive",
                                  });
                                }
                              }}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        ))}
                      </div>

                      <form
                        className="flex gap-2"
                        onSubmit={async (e) => {
                          e.preventDefault();
                          const form = e.target as HTMLFormElement;
                          const domain = (
                            form.elements.namedItem(
                              "domain",
                            ) as HTMLInputElement
                          ).value;
                          try {
                            const currentDomains = tenant?.app_domains || [];
                            await updateDashboardDomains.mutateAsync({
                              projectId: params.projectId,
                              domains: [...currentDomains, domain],
                            });
                            form.reset();
                          } catch (error: any) {
                            toast({
                              title: "Error",
                              description: error.message,
                              variant: "destructive",
                            });
                          }
                        }}
                      >
                        <Input
                          name="domain"
                          placeholder="Enter a custom domain"
                          className="flex-1"
                        />
                        <Button type="submit">
                          <PlusIcon className="h-4 w-4" />
                        </Button>
                      </form>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </section>

          <div className="border-t" />

          <section>
            <div className="flex flex-col md:flex-row gap-12">
              <div className="w-full md:w-2/5">
                <h3 className="text-lg font-medium mb-1">Danger Zone</h3>
                <p className="text-sm text-muted-foreground">
                  Irreversible and destructive actions
                </p>
              </div>

              <Card className="flex-1 border-destructive">
                <CardHeader>
                  <CardTitle className="text-destructive">
                    Danger Zone
                  </CardTitle>
                  <CardDescription>
                    These actions cannot be undone
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Alert variant="destructive" className="mb-4">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      Deleting a project will permanently remove all associated
                      data, including API keys, domains, and configurations.
                    </AlertDescription>
                  </Alert>
                  <Button
                    variant="destructive"
                    onClick={() => setShowDeleteDialog(true)}
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete Project
                  </Button>
                </CardContent>
              </Card>
            </div>
          </section>
        </div>
      </div>

      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent className="bg-background">
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Project</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete this project? This action cannot
              be undone and will permanently delete all associated data.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              onClick={handleDeleteProject}
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
