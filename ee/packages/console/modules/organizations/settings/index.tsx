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
import { Alert, AlertDescription } from "@karrio/insiders/components/ui/alert";
import { Button } from "@karrio/insiders/components/ui/button";
import { UserPlus, Trash2, AlertCircle } from "lucide-react";
import { Input } from "@karrio/insiders/components/ui/input";
import { useToast } from "@karrio/insiders/hooks/use-toast";
import { useSession } from "next-auth/react";
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

export default async function SettingsPage({
  params,
}: {
  params: Promise<{ orgId: string }>;
}) {
  const { toast } = useToast();
  const router = useRouter();
  const utils = trpc.useContext();
  const { data: session } = useSession();
  const { orgId } = await params;
  const { data: organization } = trpc.organizations.get.useQuery({
    orgId,
  });
  const { data: members } = trpc.organizations.getMembers.useQuery({
    orgId,
  });


  const currentUser = members?.find(
    (member) => member.user.email === session?.user?.email,
  );
  const isOwner = currentUser?.role === "OWNER";

  const updateOrg = trpc.organizations.update.useMutation({
    onSuccess: () => {
      utils.organizations.get.invalidate();
      toast({
        title: "Success",
        description: "Organization details updated successfully",
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
  const inviteMember = trpc.organizations.inviteMember.useMutation({
    onSuccess: () => {
      utils.organizations.getMembers.invalidate();
      toast({
        title: "Success",
        description: "Invitation sent successfully",
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
  const removeMember = trpc.organizations.removeMember.useMutation({
    onSuccess: () => {
      utils.organizations.getMembers.invalidate();
      toast({
        title: "Success",
        description: "Member removed successfully",
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
  const deleteOrganization = trpc.billing.deleteOrganization.useMutation({
    onSuccess: () => {
      toast({
        title: "Success",
        description: "Organization deleted successfully",
      });
      router.push("/organizations");
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const [orgName, setOrgName] = useState(organization?.name || "");
  const [newMemberEmail, setNewMemberEmail] = useState("");
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  return (
    <>
      <DashboardHeader
        title="Settings"
        description="Manage your organization settings"
      />

      {organization && !isOwner && (
        <div className="p-4 bg-background">
          <Alert variant="destructive" className="max-w-2xl mx-auto">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              Only organization owners can modify settings. You have view-only
              access.
            </AlertDescription>
          </Alert>
        </div>
      )}

      <div className="p-8 bg-background">
        <div className="max-w-7xl mx-auto space-y-16">
          <div className="grid grid-cols-5 gap-8 items-start">
            <div className="col-span-2 space-y-12">
              <section>
                <h3 className="text-lg font-medium mb-1">
                  Organization Details
                </h3>
                <p className="text-sm text-muted-foreground">
                  Basic information about your organization.
                </p>
              </section>
            </div>
            <div className="col-span-3 space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Organization Details</CardTitle>
                  <CardDescription>
                    Update your organization's basic information
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid gap-2">
                      <label className="text-sm font-medium">Name</label>
                      <div className="flex gap-4">
                        <Input
                          value={orgName}
                          onChange={(e) => setOrgName(e.target.value)}
                          placeholder={
                            organization?.name || "Organization name"
                          }
                          disabled={!isOwner}
                        />
                        <Button
                          onClick={() =>
                            updateOrg.mutateAsync({ orgId, name: orgName })
                          }

                          disabled={
                            !isOwner ||
                            !orgName ||
                            orgName === organization?.name
                          }
                        >
                          Save
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          <hr className="border-t border-muted-foreground" />

          <div className="grid grid-cols-5 gap-8 items-start">
            <div className="col-span-2 space-y-12">
              <section>
                <h3 className="text-lg font-medium mb-1">Team Members</h3>
                <p className="text-sm text-muted-foreground">
                  Manage who has access to your organization.
                </p>
              </section>
            </div>
            <div className="col-span-3 space-y-6">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>Team Members</CardTitle>
                      <CardDescription>
                        People with access to this organization
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-4">
                    {members?.map((member) => (
                      <div
                        key={member.userId}
                        className="flex items-center justify-between py-2"
                      >
                        <div>
                          <div className="font-medium">{member.user.name}</div>
                          <div className="text-sm text-muted-foreground">
                            {member.user.email}
                          </div>
                        </div>
                        <div className="flex items-center gap-4">
                          <div className="text-sm text-muted-foreground">
                            {member.role}
                          </div>
                          {isOwner &&
                            members.length > 1 &&
                            member.role !== "OWNER" && (
                              <Button
                                variant="ghost"
                                size="icon"
                                onClick={() =>
                                  removeMember.mutateAsync({
                                    orgId,
                                    userId: member.userId,
                                  })
                                }

                              >
                                <Trash2 className="h-4 w-4 text-destructive" />
                              </Button>
                            )}
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="pt-4 border-t">
                    <div className="flex gap-4">
                      <Input
                        value={newMemberEmail}
                        onChange={(e) => setNewMemberEmail(e.target.value)}
                        placeholder="Email address"
                        type="email"
                        disabled={!isOwner}
                      />
                      <Button
                        onClick={() => {
                          inviteMember.mutateAsync({
                            orgId,
                            email: newMemberEmail,
                          });
                          setNewMemberEmail("");
                        }}

                        disabled={!isOwner || !newMemberEmail}
                        className="gap-2"
                      >
                        <UserPlus className="h-4 w-4" />
                        Invite
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          <hr className="border-t border-muted-foreground" />

          <div className="grid grid-cols-5 gap-8 items-start">
            <div className="col-span-2 space-y-12">
              <section>
                <h3 className="text-lg font-medium mb-1">Danger Zone</h3>
                <p className="text-sm text-muted-foreground">
                  Irreversible and destructive actions.
                </p>
              </section>
            </div>
            <div className="col-span-3 space-y-6">
              <Card className="border-destructive">
                <CardHeader>
                  <CardTitle className="text-destructive">
                    Danger Zone
                  </CardTitle>
                  <CardDescription>
                    These actions cannot be undone
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    variant="destructive"
                    disabled={!isOwner}
                    onClick={() => setShowDeleteDialog(true)}
                  >
                    Delete Organization
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>

      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent className="bg-background">
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Organization</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete this organization? This action
              cannot be undone and will permanently delete all associated data.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              onClick={() => {
                deleteOrganization.mutateAsync({ orgId });
                setShowDeleteDialog(false);
              }}

            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
